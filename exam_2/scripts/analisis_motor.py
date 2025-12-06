#!/usr/bin/env python3
"""
Análisis y Visualización de resultados del Motor Molecular (Problema 2)
Física Computacional 2 - 2025
"""

import numpy as np
import matplotlib.pyplot as plt

def analizar_motor():
    """Carga los datos y genera las gráficas clave para el motor molecular."""
    try:
        data = np.loadtxt('results/motor_cargo_run.dat', skiprows=1)
    except FileNotFoundError:
        print("Error: El archivo 'results/motor_cargo_run.dat' no se encontró. ¿Ejecutaste 'make run'?")
        return

    t = data[:, 0]  # Tiempo
    x = data[:, 1]  # Posición
    v = data[:, 2]  # Velocidad
    s = data[:, 3]  # Estado Químico (1: Activo, 2: Inactivo)

    # ====================================================================
    # GRÁFICA 1: Trayectoria y Desplazamiento Dirigido
    # ====================================================================
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    # Suavizar el desplazamiento con una media móvil para mejor visualización
    # window_size = 50 
    # x_smooth = np.convolve(x, np.ones(window_size)/window_size, mode='valid')
    # t_smooth = t[window_size - 1:]

    ax1.plot(t, x, label='Posición $x(t)$', color='blue', alpha=0.7)
    
    # Calcular velocidad promedio y trazar ajuste lineal
    vx_promedio = (x[-1] - x[0]) / (t[-1] - t[0])
    x_ajuste = x[0] + vx_promedio * t
    ax1.plot(t, x_ajuste, label=f'Ajuste Lineal (v={vx_promedio:.4f})', 
             color='red', linestyle='--', linewidth=2)
             
    ax1.set_xlabel('Tiempo $t$ (u.r.)')
    ax1.set_ylabel('Posición $x$ (u.r.)')
    ax1.set_title('Trayectoria $x(t)$ y Transporte Dirigido')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    fig1.savefig('results/trayectoria_motor.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 1 guardada: results/trayectoria_motor.png")

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
    # Colorear la trayectoria según el estado
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
    print("\nAnálisis del Problema 2 Finalizado.")
