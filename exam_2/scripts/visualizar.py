#!/usr/bin/env python3
"""
Visualización de trayectorias de partículas
Física Computacional 2 - 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def graficar_trayectorias(archivo, num_mostrar=10):
    """Grafica las trayectorias de algunas partículas seleccionadas"""
    try:
        datos = np.loadtxt(archivo)
    except Exception as e:
        print(f"Error al cargar {archivo}: {e}")
        return None

    if datos.size == 0:
        return None
        
    num_cols = datos.shape[1]
    num_particulas = (num_cols - 2) // 4
    
    # MEJORA 1: Seleccionar partículas distribuidas uniformemente en la lista
    # (por ejemplo: la 0, la 10, la 20...) en lugar de las primeras 10 seguidas.
    indices = np.linspace(0, num_particulas-1, num_mostrar, dtype=int)
    
    print(f"Graficando trayectorias de partículas índices: {indices}")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    W, H = 10.0, 10.0
    ax.add_patch(Rectangle((0, 0), W, H, fill=False, edgecolor='black', linewidth=2))
    
    colores = plt.cm.jet(np.linspace(0, 1, num_mostrar))
    
    for k, i in enumerate(indices):
        col_x = 1 + 4*i
        col_y = 2 + 4*i
        
        x = datos[:, col_x]
        y = datos[:, col_y]
        
        # MEJORA 2: Líneas más visibles y marcadores más pequeños
        ax.plot(x, y, '-', color=colores[k], alpha=0.8, linewidth=1.5)
        
        # Inicio (punto pequeño)
        ax.plot(x[0], y[0], 'o', color=colores[k], markersize=4, alpha=0.6)
        # Fin (cuadrado pequeño)
        ax.plot(x[-1], y[-1], 's', color=colores[k], markersize=4, alpha=0.9)

    ax.set_xlim(-0.5, W + 0.5)
    ax.set_ylim(-0.5, H + 0.5)
    ax.set_xlabel('Posición X')
    ax.set_ylabel('Posición Y')
    ax.set_title(f'Trayectorias en Gas Denso (Lennard-Jones)\nEfecto de "Jaula" y Difusión')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    archivo = "results/gas_lj_verlet.dat"
    try:
        fig = graficar_trayectorias(archivo, num_mostrar=12) # Mostramos 12 para ver más
        if fig:
            plt.savefig("results/trayectorias_lj.png", dpi=300, bbox_inches='tight')
            print("✓ Gráfica mejorada guardada en: results/trayectorias_lj.png")
            plt.close(fig)
    except Exception as e:
        print(f"Error: {e}")
