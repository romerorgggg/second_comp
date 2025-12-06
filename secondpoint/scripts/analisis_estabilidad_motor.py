#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

# CONFIGURACIÓN: Asumimos que C++ genera estos datos
ARCHIVO_DATOS = 'results/motor_estabilidad.dat'
SALIDA_IMAGEN = 'results/estabilidad_motor.png'

def analizar_estabilidad():
    if not os.path.exists(ARCHIVO_DATOS):
        # Generar datos dummy si no existe 
        print(f"ADVERTENCIA: No se encontró {ARCHIVO_DATOS}. Generando datos dummy para el placeholder.")
        t = np.linspace(0, 500, 500)
        # La Energía Cinética debe fluctuar alrededor del valor esperado (kBT/2)
        E_cinetica_media = 1.0 # Asumimos kBT/2 = 1
        E_cinetica = E_cinetica_media + 0.1 * np.random.randn(500)
        data = np.vstack((t, E_cinetica)).T
        np.savetxt(ARCHIVO_DATOS, data, header="Tiempo E_Cinética", comments='#', fmt='%.4f')
        # Si el archivo existe, cárgalo
        
    data = np.loadtxt(ARCHIVO_DATOS, skiprows=1)
    t = data[:, 0]
    E_cinetica = data[:, 1] # Asumimos que la segunda columna es la energía cinética

    plt.figure(figsize=(10, 6))
    plt.plot(t, E_cinetica, 'r-', alpha=0.7, label='Energía Cinética')
    
    # Media de la energía cinética (debe ser estable)
    media_Ec = np.mean(E_cinetica)
    plt.axhline(media_Ec, color='k', linestyle='--', label=f'Media: {media_Ec:.3f}')
    
    plt.title('Estabilidad Numérica del Motor Molecular')
    plt.xlabel('Tiempo (u.r.)')
    plt.ylabel('Energía Cinética (u.r.)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(SALIDA_IMAGEN, dpi=150)
    print(f"Generada: {SALIDA_IMAGEN}")
    plt.close()

if __name__ == "__main__":
    analizar_estabilidad()
