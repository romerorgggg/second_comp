# Motor Molecular (Molecular Ratchet - Problema 2)

## Descripción

Este proyecto implementa una simulación de dinámica de Langevin para un modelo de **Motor Molecular de Trinquete de Dos Estados (Two-State Ratchet)**. El objetivo es demostrar la existencia de transporte dirigido (rectificación) en un sistema operando fuera del equilibrio termodinámico, impulsado por un ciclo químico asimétrico.

## Estructura del Repositorio
. ├── include/ # Cabeceras (.h) de las clases (Particle, MotorModel, Potential, ChemicalState) ├── src/ # Archivos fuente (.cpp) ├── scripts/ # Scripts de análisis en Python (analisis_motor.py) ├── results/ # Archivos de datos (.dat) y figuras (.png) generadas ├── documents/ # Documento del informe en LaTeX y PDF final ├── Makefile # Script de construcción y ejecución └── README.md # Este archivo
## Construcción y Ejecución

La compilación y ejecución se gestionan mediante el `Makefile`.

1.  **Compilar el proyecto:**
    ```bash
    make
    ```
2.  **Ejecutar la simulación:**
    ```bash
    make run
    ```
3.  **Ejecutar el análisis y generar gráficas:**
    * *Asegúrate de tener un entorno virtual activo (venv) con numpy, matplotlib y scipy.*
    ```bash
    make analyze
    ```
4.  **Generar documentación Doxygen:**
    ```bash
    make doc
    ```

## Dependencias de Software

* C++ Compiler (g++ con soporte C++14 o superior)
* GNU Make
* Python 3.x con librerías: `numpy`, `matplotlib`, `scipy`
* Doxygen (para generar la documentación del código)
# Doxyfile for Molecular Motor Project

# --- Project identification ---
PROJECT_NAME           = "Motor Molecular (Trinquete)"
PROJECT_BRIEF          = "Simulación de Motor Molecular fuera del equilibrio"
PROJECT_LOGO           =

# --- Directory configuration ---
INPUT                  = include src
FILE_PATTERNS          = *.h *.cpp
RECURSIVE              = YES
EXCLUDE_PATTERNS       =
OUTPUTDIRECTORY        = doc
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES

# --- Output settings ---
GENERATE_HTML          = YES
GENERATE_LATEX         = NO
HTML_OUTPUT            = html
# HTML_FILE_EXTENSION    = .html
# HTML_HEADER            = 
# HTML_FOOTER            = 

# --- Source code browsing ---
SOURCE_BROWSER         = YES
INLINE_SOURCES         = YES
STRIP_CODE_LT          = YES

# --- Documentation generation ---
QUIET                  = NO
WARNINGS               = YES
WARN_IF_UNDOCUMENTED   = YES
WARN_IF_DEPRECATED     = YES

# --- Dot configuration (Graphs) ---
HAVE_DOT               = YES
CLASS_DIAGRAMS         = YES
UML_LOOK               = YES
# CALL_GRAPH             = YES
# CALLER_GRAPH           = YES
