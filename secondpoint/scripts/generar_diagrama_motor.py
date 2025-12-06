#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Asegura que la carpeta results exista
if not os.path.exists('results'):
    os.makedirs('results')

def crear_diagrama_motor():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    def caja(x, y, w, h, titulo, metodos):
        rect = patches.Rectangle((x,y), w, h, fc='white', ec='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h-0.3, titulo, ha='center', weight='bold')
        ax.plot([x, x+w], [y+h-0.6, y+h-0.6], 'k-')
        ax.text(x+0.1, y+h-1.0, metodos, va='top', fontsize=9, family='monospace')

    # Clases
    caja(0.5, 3.5, 2.5, 2.0, "Particle", "+ MoveVerlet()\n+ getX(), getV()")
    caja(3.5, 3.5, 3.0, 2.0, "MotorModel", "+ evolve(dt)\n+ calcForce()")
    caja(7.0, 3.5, 2.5, 2.0, "Potential", "+ getForce(x,s)")
    caja(3.5, 0.5, 3.0, 1.5, "ChemicalState", "+ updateState(dt)")

    # Conexiones (Composición)
    ax.plot([3.0, 3.5], [4.5, 4.5], 'k-') 
    ax.plot([6.5, 7.0], [4.5, 4.5], 'k-') 
    ax.plot([5.0, 5.0], [2.0, 3.5], 'k-') 

    ax.text(5, 5.8, "Diagrama de Clases: Motor Molecular", ha='center', fontsize=14)
    plt.savefig('results/diagrama_clases_motor.png', bbox_inches='tight', dpi=150)
    print("Diagrama generado: results/diagrama_clases_motor.png")

if __name__ == "__main__":
    crear_diagrama_motor()
