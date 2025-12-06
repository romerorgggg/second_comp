#!/usr/bin/env python3
"""
Análisis de conservación de energía
Física Computacional 2 - 2025
MODIFICADO para incluir Energía Potencial de Lennard-Jones.
"""

import numpy as np
import matplotlib.pyplot as plt

def cargar_datos(archivo):
    """Carga los datos de la simulación"""
    try:
        datos = np.loadtxt(archivo)
        return datos
    except Exception as e:
        print(f"Error al cargar {archivo}: {e}")
        return None

def calcular_energia_total(datos, masa=1.0):
    """
    Calcula la Energía Total (Cinética + Potencial)
    
    El formato de datos esperado es:
    t, x1, y1, vx1, vy1, ..., xN, yN, vxN, vyN, EpotencialTotal (4N+2 columnas)
    """
    num_cols = datos.shape[1]
    
    # El número de partículas N se calcula restando 2 (t y Epot) y dividiendo por 4 (x,y,vx,vy)
    num_particulas = (num_cols - 2) // 4 
    
    if num_particulas <= 0:
        print("Error: El número de columnas no corresponde al formato esperado (4N+2).")
        return None
        
    t = datos[:, 0]
    
    # Energía Potencial Total (última columna)
    energia_potencial = datos[:, -1]
    
    # Cálculo de Energía Cinética Total
    energia_cinetica = np.zeros(len(t))
    
    for i in range(num_particulas):
        col_vx = 3 + 4*i
        col_vy = 4 + 4*i
        vx = datos[:, col_vx]
        vy = datos[:, col_vy]
        
        energia_cinetica += 0.5 * masa * (vx**2 + vy**2)
    
    # Energía Total = Cinética + Potencial
    energia_total = energia_cinetica + energia_potencial
    
    return t, energia_total, energia_cinetica, energia_potencial

def analizar_conservacion(archivo, titulo="Conservación de Energía Total"):
    """Analiza la conservación de energía en la simulación"""
    datos = cargar_datos(archivo)
    if datos is None:
        return None
    
    resultado_e = calcular_energia_total(datos)
    if resultado_e is None:
        return None
        
    t, energia_total, energia_cinetica, energia_potencial = resultado_e
    
    E0 = energia_total[0]
    E_final = energia_total[-1]
    E_media = np.mean(energia_total)
    E_std = np.std(energia_total)
    
    # El error relativo debe ser pequeño si el integrador es bueno
    error_relativo = abs(E_final - E0) / abs(E0) * 100
    fluctuacion = E_std / E_media * 100
    
    print(f"\n=== {titulo} ===")
    print(f"Número de partículas: {(datos.shape[1] - 2) // 4}")
    print(f"Energía Total inicial: {E0:.6f}")
    print(f"Energía Total final: {E_final:.6f}")
    print(f"Energía Total media: {E_media:.6f}")
    print(f"Desv. estándar (Total): {E_std:.6f}")
    print(f"Error relativo (Total): {error_relativo:.4f}%")
    print(f"Fluctuación (Total): {fluctuacion:.4f}%")
    
    return t, energia_total, energia_cinetica, energia_potencial, E0, error_relativo

def graficar_energia(archivo, titulo="Conservación de Energía Total"):
    """Grafica la evolución temporal de la energía"""
    resultado = analizar_conservacion(archivo, titulo)
    if resultado is None:
        return None
    
    t, energia_total, energia_cinetica, energia_potencial, E0, error = resultado
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Energía vs tiempo
    ax1.plot(t, energia_total, 'b-', linewidth=1, alpha=0.7, label='Energía Total')
    ax1.plot(t, energia_cinetica, 'r--', linewidth=1, alpha=0.7, label='Energía Cinética')
    ax1.plot(t, energia_potencial, 'g:', linewidth=1, alpha=0.7, label='Energía Potencial')
    
    ax1.axhline(y=E0, color='k', linestyle='-', linewidth=2, label=f'E_Total 0 = {E0:.3f}')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Energía')
    ax1.set_title(f'{titulo} (Velocity-Verlet)\nError relativo total: {error:.4f}%')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Error relativo vs tiempo
    error_rel = (energia_total - E0) / E0 * 100
    ax2.plot(t, error_rel, 'r-', linewidth=1)
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=1)
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Error relativo (%)')
    ax2.set_title('Error en la conservación de Energía Total')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    archivo_lj = "results/gas_lj_verlet.dat"
    
    print("Verificando conservación de energía para el Gas de Lennard-Jones...")
    
    # Intenta generar y guardar la gráfica
    try:
        fig_lj = graficar_energia(archivo_lj, "Conservación de Energía - Gas Lennard-Jones")
        if fig_lj:
            plt.savefig("results/conservacion_energia_lj.png", dpi=150, bbox_inches='tight')
            print("\nGráfica de conservación de energía guardada en results/conservacion_energia_lj.png")
            plt.close(fig_lj)
    except Exception as e:
        print(f"\nNo se pudo generar la gráfica. Asegúrese de correr la simulación C++ primero. Error: {e}")
