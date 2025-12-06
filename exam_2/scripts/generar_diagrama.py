#!/usr/bin/env python3
"""
Genera el diagrama de clases para el Problema 1 (Caja y Bola)
Física Computacional 2 - 2025
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as patches

def crear_diagrama_clases():
    """Crea el diagrama de clases para Caja y Bola."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # --- Definición de clases ---
    
    def dibujar_clase(ax, x, y, ancho, alto, nombre):
        """Dibuja la caja base de una clase UML-lite."""
        # Caja principal
        rect = patches.Rectangle((x, y), ancho, alto, linewidth=1.5, edgecolor='black', facecolor='white')
        ax.add_patch(rect)
        # Línea divisoria entre nombre y atributos
        ax.plot([x, x + ancho], [y + alto - 0.7, y + alto - 0.7], 'k-', linewidth=1.5)
        # Nombre de la clase
        ax.text(x + ancho/2, y + alto - 0.35, nombre, ha='center', va='center', 
                fontsize=12, weight='bold', color='darkblue')
        return x, y
    
    # --- Clase Bola ---
    bola_x, bola_y = dibujar_clase(ax, 1.0, 1.0, 3.5, 4.5, "Bola")
    
    # Atributos (Privados: -)
    attrs_bola = [
        "- x, y, vx, vy, masa, radio",
        "- ax, ay, ax_prev"
    ]
    for i, attr in enumerate(attrs_bola):
        ax.text(bola_x + 0.1, bola_y + 3.4 - i*0.3, attr, fontsize=9, family='monospace')
    
    # Métodos (Públicos: +)
    metodos_bola = [
        "+ Iniciar()",
        "+ MoverseVerlet_Paso1()",
        "+ MoverseVerlet_Paso2()",
        "+ RebotePared()",
        "+ EnergiaCinetica()",
        "+ Getters/Setters"
    ]
    for i, met in enumerate(metodos_bola):
        ax.text(bola_x + 0.1, bola_y + 2.0 - i*0.3, met, fontsize=9, family='monospace', color='darkgreen')


    # --- Clase Caja ---
    caja_x, caja_y = dibujar_clase(ax, 5.5, 1.0, 3.5, 4.5, "Caja")

    # Atributos (Privados: -)
    attrs_caja = [
        "- ancho, alto, generador",
        "- epsilon, sigma, r_cut, e_shift",
        "- bolas_: vector<Bola>" # La clave de la composición
    ]
    for i, attr in enumerate(attrs_caja):
        ax.text(caja_x + 0.1, caja_y + 3.4 - i*0.3, attr, fontsize=9, family='monospace')

    # Métodos (Públicos: +)
    metodos_caja = [
        "+ InicializarRejilla()",
        "+ CalcularFuerzasLJ()",
        "+ EvolucionarVerlet(dt)",
        "+ SimularCompleto()",
        "+ EnergiaCineticaTotal()"
    ]
    for i, met in enumerate(metodos_caja):
        ax.text(caja_x + 0.1, caja_y + 2.0 - i*0.3, met, fontsize=9, family='monospace', color='darkgreen')
    
    # --- Relación de Composición (Caja contiene Bola) ---
    # Flecha desde Caja hacia Bola
    
    # Diamante relleno (Composición)
    ax.plot(caja_x, 3.2, 'D', color='black', markersize=8)
    
    # Línea de conexión desde el diamante al borde de Bola
    arrow = FancyArrowPatch((caja_x, 3.2), (bola_x + 3.5, 3.2),
                           arrowstyle='-', mutation_scale=10,
                           linewidth=1.5, color='black')
    ax.add_patch(arrow)
    
    # Multiplicidad (1..N)
    ax.text(caja_x - 0.1, 3.4, '1', ha='right', fontsize=10, weight='bold')
    ax.text(bola_x + 3.5 + 0.1, 3.4, '0..N', ha='left', fontsize=10, weight='bold')
    
    ax.set_title("Diagrama de Clases del Problema 1 (C++), Relación de Composición", fontsize=14)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    print("Generando diagrama de clases...")
    try:
        fig = crear_diagrama_clases()
        fig.savefig('results/diagrama_clases.png', dpi=300)
        print("✓ Diagrama guardado en: results/diagrama_clases.png")
        plt.close(fig)
    except ImportError:
        print("Error: Necesitas instalar matplotlib. Usa 'pip install matplotlib'.")
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")
