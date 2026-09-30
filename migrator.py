import os
import shutil
import string
import threading
import customtkinter as ctk
from tkinter import messagebox

# Set modern dark appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Critical system items to NEVER touch
SYSTEM_PROTECTED_ITEMS = {
    "windows",
    "program files",
    "program files (x86)",
    "programdata",
    "system volume information",
    "$recycle.bin",
    "recovery",
    "boot",
    "msocache",
    "pagefile.sys",
    "hiberfil.sys",
    "swapfile.sys",
}


class OneClickMigratorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("1-Click Smart File Migrator")
        self.geometry("600x600")

        # Detect drives automatically
        self.target_drive = self.find_secondary_drive()

        # UI Header
        self.title_label = ctk.CTkLabel(
            self,
            text="1-Click PC Storage Saver",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Automatically moves non-essential personal files off your C: drive.",
            text_color="gray",
        )
        self.subtitle_label.pack(pady=(0, 15))

        # Drive Status Information
        drive_status_text = (
            f" Target Destination Drive: {self.target_drive}"
            if self.target_drive
            else " No secondary drive (D:, E:) detected!"
        )
        self.drive_label = ctk.CTkLabel(
            self,
            text=drive_status_text,
            font=ctk.CTkFont(weight="bold"),
            text_color="#2B7A78" if self.target_drive else "#D9534F",
        )
        self.drive_label.pack(pady=10)

        # BIG 1-CLICK BUTTON
        self.migrate_btn = ctk.CTkButton(
            self,
            text="🚀 MIGRATE NOW (ONE CLICK)",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=300,
            fg_color="#D9534F" if self.target_drive else "gray",
            hover_color="#C9302C",
            command=self.start_one_click_migration,
            state="normal" if self.target_drive else "disabled",
        )
        self.migrate_btn.pack(pady=15)

        # Visual Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)  # Starts at 0%
        self.progress_bar.pack(pady=10)

        # Output Results Box
        self.textbox = ctk.CTkTextbox(self, width=520, height=220)
        self.textbox.pack(pady=15)

        self.textbox.insert(
            "end", "System ready.\nClick 'MIGRATE NOW' to automatically:\n"
        )
        self.textbox.insert(
            "end",
            "• Scan user folders (Downloads, Desktop, Videos, Documents, Pictures)\n",
        )
        self.textbox.insert(
            "end", "• Ignore all critical Windows system files\n"
        )

        target_text = self.target_drive if self.target_drive else "D:"
        self.textbox.insert(
            "end",
            f"• Transfer non-essential files to {target_text}\\C_Drive_Backup\n\n",
        )

    @staticmethod
    def find_secondary_drive():
        """Scans the computer to find the first available drive that is NOT C:"""
        available_drives = [
            f"{d}:"
            for d in string.ascii_uppercase
            if os.path.exists(f"{d}:") and d != "C"
        ]
        return available_drives[0] if available_drives else None

    @staticmethod
    def get_user_folders():
        """Finds standard user folders like Downloads, Desktop, Documents, Videos, Pictures"""
        user_profile = os.environ.get("USERPROFILE", r"C:\Users\Default")
        folders_to_clean = [
            os.path.join(user_profile, "Downloads"),
            os.path.join(user_profile, "Desktop"),
            os.path.join(user_profile, "Documents"),
            os.path.join(user_profile, "Videos"),
            os.path.join(user_profile, "Pictures"),
        ]
        return [f for f in folders_to_clean if os.path.exists(f)]

    @staticmethod
    def is_safe_to_move(item_name):
        """Security filter to protect Windows"""
        name_lower = item_name.lower()

        if name_lower in SYSTEM_PROTECTED_ITEMS:
            return False
        if name_lower.endswith((".sys", ".dll", ".dat", ".bat", ".ini")):
            return False

        return True

    def start_one_click_migration(self):
        """Initiates migration process on a background thread to keep GUI responsive."""
        if not self.target_drive:
            self.textbox.insert("end", "\n Error: No destination drive found!")
            return

        self.migrate_btn.configure(
            state="disabled", text="Migrating... Please wait"
        )
        self.progress_bar.set(0)
        self.textbox.delete("0.0", "end")
        self.textbox.insert("end", " Starting 1-Click Smart Migration...\n\n")

        # Execute heavy tasks on a daemon thread
        threading.Thread(target=self._run_migration_thread, daemon=True).start()

    def _run_migration_thread(self):
        """Background worker thread handling file operations."""
        if not self.target_drive:
            return

        destination_base = os.path.join(self.target_drive, "C_Drive_Backup")
        os.makedirs(destination_base, exist_ok=True)

        user_folders = self.get_user_folders()

        # Step 1: Collect all safe items to move
        items_to_move = []
        for folder in user_folders:
            folder_name = os.path.basename(folder)
            dest_folder = os.path.join(destination_base, folder_name)

            try:
                for item_name in os.listdir(folder):
                    full_path = os.path.join(folder, item_name)
                    if self.is_safe_to_move(item_name):
                        items_to_move.append((full_path, dest_folder, item_name))
            except (PermissionError, OSError):
                continue

        total_items = len(items_to_move)

        if total_items == 0:
            self.textbox.insert(
                "end", " No files or folders found to migrate."
            )
            self.migrate_btn.configure(
                state="normal", text="🚀 MIGRATE NOW (ONE CLICK)"
            )
            return

        # Step 2: Move items and update progress
        moved_count = 0
        for full_path, dest_folder, item_name in items_to_move:
            os.makedirs(dest_folder, exist_ok=True)
            try:
                shutil.move(full_path, dest_folder)
                self.textbox.insert("end", f"  Moved: {item_name}\n")
                moved_count += 1
            except (PermissionError, OSError, shutil.Error):
                self.textbox.insert(
                    "end", f"  Skipped ({item_name}): File in use or access denied\n"
                )

            # Update progress ratio
            progress_ratio = moved_count / total_items
            self.progress_bar.set(progress_ratio)

        # Final completion output
        self.progress_bar.set(1.0)
        self.textbox.insert(
            "end",
            f"\n Migration Finished! Successfully moved {moved_count} item(s) to {destination_base}.",
        )
        self.migrate_btn.configure(
            state="normal", text="🚀 MIGRATE NOW (ONE CLICK)"
        )

        # Friendly popup dialog box
        messagebox.showinfo(
            "Migration Complete",
            f"Successfully moved {moved_count} item(s) to your {self.target_drive} drive!",
        )


if __name__ == "__main__":
    app = OneClickMigratorApp()
    app.mainloop()