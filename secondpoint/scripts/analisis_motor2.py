#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

# CONFIGURACIÓN: Rutas conectadas con tu C++
ARCHIVO_DATOS = 'results/motor_cargo_run.dat'
SALIDA_TRAYECTORIA = 'results/trayectoria_motor.png'
SALIDA_RECTIFICACION = 'results/rectificacion_motor.png'

def analizar_motor():
    # 1. Verificar que existan los datos del C++
    if not os.path.exists(ARCHIVO_DATOS):
        print(f"ERROR: No se encontró {ARCHIVO_DATOS}")
        print("¿Ejecutaste 'make run' primero?")
        return

    print(f"Leyendo datos de {ARCHIVO_DATOS}...")
    try:
        data = np.loadtxt(ARCHIVO_DATOS, skiprows=1) # Saltar encabezado
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return

    t = data[:, 0]  # Tiempo
    x = data[:, 1]  # Posición
    v = data[:, 2]  # Velocidad
    s = data[:, 3]  # Estado (1 o 2)

    # --- GRÁFICA 1: Trayectoria y Transporte ---
    plt.figure(figsize=(10, 6))
    
    # Regresión lineal para ver la velocidad de deriva
    slope, intercept, _, _, _ = linregress(t, x)
    
    plt.plot(t, x, label='Trayectoria $x(t)$', color='blue', alpha=0.6, linewidth=0.8)
    plt.plot(t, intercept + slope*t, 'r--', label=f'Tendencia (v={slope:.4f})', linewidth=2)
    
    plt.title(f'Transporte Dirigido (Velocidad neta: {slope:.4f})')
    plt.xlabel('Tiempo')
    plt.ylabel('Posición')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(SALIDA_TRAYECTORIA, dpi=150)
    print(f"Generada: {SALIDA_TRAYECTORIA}")
    plt.close()

    # --- GRÁFICA 2: Rectificación (Color por estado) ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [1, 3]})
    
    # Subplot superior: Estados
    ax1.plot(t, s, 'g-', drawstyle='steps-post', linewidth=1)
    ax1.set_ylabel('Estado Químico')
    ax1.set_yticks([1, 2])
    ax1.set_yticklabels(['Activo (1)', 'Inactivo (2)'])
    ax1.set_title('Mecanismo de Rectificación')
    ax1.grid(True, alpha=0.3)

    # Subplot inferior: Trayectoria coloreada
    # Rojo = Activo (Fuerza), Gris = Inactivo (Difusión)
    colors = np.where(s == 1, 'red', 'gray')
    ax2.scatter(t, x, c=colors, s=1, alpha=0.5, label='Partícula')
    
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('Posición')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(SALIDA_RECTIFICACION, dpi=150)
    print(f"Generada: {SALIDA_RECTIFICACION}")
    plt.close()

if __name__ == "__main__":
    analizar_motor()
