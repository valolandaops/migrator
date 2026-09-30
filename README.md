# 1-Click Smart File Migrator 🚀

**1-Click Smart File Migrator** es una aplicación de escritorio liviana y automatizada diseñada para liberar espacio crítico en la unidad principal (`C:`) de sistemas Windows. Transfiere de forma segura carpetas personales y archivos no esenciales hacia una unidad secundaria (`D:`, `E:`, etc.), manteniendo protegidos en todo momento los componentes del sistema operativo.

---

## 🎯 Finalidad del Proyecto

* **Optimización Automática de Almacenamiento:** Detecta la presencia de unidades secundarias y mueve archivos pesados del usuario con un solo clic.
* **Seguridad Operativa:** Evita la alteración o corrupción de archivos críticos de Windows durante el proceso de transferencia.
* **Experiencia de Usuario Fluida:** Ofrece una interfaz gráfica moderna, con actualización del progreso en tiempo real e hilos de ejecución secundarios para no congelar la ventana durante transferencias pesadas.

---

## 🛡️ Restricciones y Protección de Archivos

Para garantizar la estabilidad del sistema operativo, el migrador cuenta con un filtro estricto de seguridad (`is_safe_to_move`):

### 1. Elementos y Directorios Protegidos (Jamás se mueven):
* `Windows`
* `Program Files` y `Program Files (x86)`
* `ProgramData`
* `System Volume Information`
* `$Recycle.Bin`
* `Recovery`, `Boot`, `MSOCache`
* Archivos de sistema: `pagefile.sys`, `hiberfil.sys`, `swapfile.sys`

### 2. Extensiones Excluidas:
* Archivos de sistema, librerías y scripts de ejecución: `.sys`, `.dll`, `.dat`, `.bat`, `.ini`.

---

## 💻 Software y Tecnologías Utilizadas

* **Lenguaje:** Python 3.14+
* **Interfaz Gráfica (GUI):** `CustomTkinter` (Tema Dark/Blue)
* **Gestión de Entorno y Compilación:** PyCharm IDE, PyInstaller
* **Control de Versiones:** Git / GitHub

---

## 🔬 Ciencias y Principios Aplicados

* **Sistemas Operativos:** Gestión de File System (módulos `os` y `shutil`), variables de entorno (`USERPROFILE`) y manejo de rutas de disco en Windows.
* **Programación Concurrente (Multithreading):** Uso de hilos secundarios (`threading.Thread` en modo daemon) para aislar las operaciones pesadas de I/O de la interfaz de usuario, garantizando responsividad en todo momento.
* **Manejo Seguro de Excepciones:** Control explícito de errores (`PermissionError`, `OSError`, `shutil.Error`) para gestionar archivos bloqueados o sin permisos sin interrumpir el flujo del programa.
* **Arquitectura de Software Clean & Static:** Declaración de funciones auxiliares sin estado como `@staticmethod` para optimización de memoria y cumplimiento de estándares PEP 8.

---

## 📋 Requerimientos del Sistema

### Para Ejecutar la Aplicación (`.exe`):
* Sistema Operativo: Windows 10 o Windows 11 (64-bit).
* Al menos una unidad de disco secundaria instalada (`D:`, `E:`, etc.).

### Para Desarrollo y Compilación desde Código Fuente:
```text
customtkinter>=5.2.0
pyinstaller>=6.0.0

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
