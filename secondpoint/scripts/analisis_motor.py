#!/usr/bin/env python3
"""
Análisis y Visualización de resultados del Motor Molecular (Problema 2)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Ajusta el nombre del archivo de entrada según la salida de tu main.cpp
ARCHIVO_DATOS = 'results/motor_cargo_run.dat'

def analizar_motor():
    """Carga los datos y genera las gráficas clave para el motor molecular."""
    try:
        data = np.loadtxt(ARCHIVO_DATOS, skiprows=1)
    except FileNotFoundError:
        print(f"Error: El archivo '{ARCHIVO_DATOS}' no se encontró. ¿Ejecutaste 'make run'?")
        return

    t = data[:, 0]  # Tiempo
    x = data[:, 1]  # Posición
    s = data[:, 3]  # Estado Químico (1: Activo, 2: Inactivo)

    # ====================================================================
    # GRÁFICA 1: Trayectoria y Desplazamiento Dirigido
    # ====================================================================
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    # Análisis de regresión lineal para calcular la velocidad promedio
    slope, intercept, r_value, p_value, std_err = linregress(t, x)
    
    x_ajuste = intercept + slope * t
    ax1.plot(t, x, label='Posición $x(t)$', color='blue', alpha=0.7)
    ax1.plot(t, x_ajuste, label=f'Ajuste Lineal ($\langle v \\rangle \\approx {slope:.4f}$)', 
             color='red', linestyle='--', linewidth=2)
             
    ax1.set_xlabel('Tiempo $t$ (u.r.)')
    ax1.set_ylabel('Posición $x$ (u.r.)')
    ax1.set_title('Trayectoria $x(t)$ y Transporte Dirigido')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    fig1.savefig('results/trayectoria_motor.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 1 guardada: results/trayectoria_motor.png")
    print(f"Velocidad de transporte calculada: {slope:.4f}")

    # ====================================================================
    # GRÁFICA 2: Rectificación y Estados Químicos
    # ====================================================================
    fig2, (axA, axB) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Subplot A: Estado Químico vs Tiempo
    axA.plot(t, s, color='darkgreen', linewidth=1.5, drawstyle='steps-post')
    axA.set_yticks([1, 2])
    axA.set_yticklabels(['Estado 1 (Activo)', 'Estado 2 (Inactivo)'])
    axA.set_title('Conmutación del Estado Químico $s(t)$')
    axA.grid(True, axis='y', alpha=0.3)
    
    # Subplot B: Posición vs Tiempo (con colores por estado)
    colores_estado = np.where(s == 1, 'red', 'gray')
    axB.scatter(t, x, c=colores_estado, s=2, alpha=0.5)
    
    axB.set_xlabel('Tiempo $t$ (u.r.)')
    axB.set_ylabel('Posición $x$ (u.r.)')
    axB.set_title('Trayectoria $x(t)$ segmentada por Estado Químico')
    
    fig2.suptitle('Análisis de Rectificación (Estado Químico vs Posición)', fontsize=14)
    fig2.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig2.savefig('results/rectificacion_motor.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 2 guardada: results/rectificacion_motor.png")
    
    plt.close('all')


if __name__ == "__main__":
    analizar_motor()
    print("\nAnálisis del Motor Molecular Finalizado.")
