#!/usr/bin/env python3
"""
Análisis de distribución de velocidades y comparación con Maxwell-Boltzmann
Física Computacional 2 - 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import maxwell # Asumimos que SciPy ya está instalado

def cargar_datos(archivo):
    """Carga los datos de la simulación"""
    try:
        # Usamos usecols para leer solo las columnas necesarias para mayor robustez
        datos = np.loadtxt(archivo)
        return datos
    except Exception as e:
        print(f"Error al cargar {archivo}: {e}")
        return None

def extraer_velocidades(datos, num_particulas):
    """Extrae las velocidades vx, vy de todas las partículas (después del 20% inicial)"""
    vx = []
    vy = []
    
    # Se toman los últimos frames (estado estable) para el histograma
    # Ignoramos el transitorio inicial (primer 20% de los datos)
    start_frame = int(len(datos) * 0.2)
    datos_estables = datos[start_frame:]
    
    # Iteramos sobre las partículas
    for i in range(num_particulas):
        col_vx = 3 + 4*i
        col_vy = 4 + 4*i
        
        # Asegurarse de que las columnas existan
        if col_vy >= datos_estables.shape[1]:
            print(f"Error: La columna de velocidad y (índice {col_vy}) está fuera de los límites del archivo de datos.")
            return np.array([]), np.array([])

        vx.append(datos_estables[:, col_vx])
        vy.append(datos_estables[:, col_vy])
    
    return np.array(vx).flatten(), np.array(vy).flatten()

def maxwell_boltzmann_2d(v, temperatura, masa=1.0):
    """
    Distribución de Maxwell-Boltzmann en 2D
    P(v) = (m / (k*T)) * v * exp(-m*v^2 / (2*k*T))
    Asumimos k_B = 1 para unidades reducidas
    """
    if temperatura <= 0:
        return np.zeros_like(v)
    return (masa * v / temperatura) * np.exp(-masa * v**2 / (2 * temperatura))

def analizar_distribucion(archivo, titulo="Distribución de Velocidades"):
    """Analiza la distribución de velocidades y compara con Maxwell-Boltzmann"""
    datos = cargar_datos(archivo)
    if datos is None or datos.size == 0:
        return None
    
    # El archivo tiene: t, (x, y, vx, vy)xN, E_pot
    num_cols = datos.shape[1]
    num_particulas = (num_cols - 2) // 4
    
    if num_particulas <= 0:
        print("Error: No se detectaron partículas o el formato es incorrecto.")
        return None
    
    print(f"\n=== {titulo} ===")
    print(f"Número de partículas: {num_particulas}")
    print(f"Total de frames analizados: {len(datos)}")
    
    # Extraer velocidades
    vx, vy = extraer_velocidades(datos, num_particulas)
    if vx.size == 0:
        return None

    rapideces = np.sqrt(vx**2 + vy**2)
    
    # Estimar temperatura efectiva del sistema
    temperatura = 0.5 * np.mean(rapideces**2)
    
    print(f"Velocidad media: {np.mean(rapideces):.4f}")
    print(f"Temperatura efectiva (k_B=1): {temperatura:.4f}")
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 1. Histograma de la simulación
    ax.hist(rapideces, bins=60, density=True, 
            alpha=0.6, color='skyblue', edgecolor='black', 
            label='Datos Simulación')
    
    # 2. Curva Teórica Maxwell-Boltzmann 2D usando la T calculada
    v_teorico = np.linspace(0, np.max(rapideces) * 1.1, 200)
    pdf_teorica = maxwell_boltzmann_2d(v_teorico, temperatura)
    
    ax.plot(v_teorico, pdf_teorica, 'r-', linewidth=2.5, 
            label=f'Maxwell-Boltzmann 2D\n(T={temperatura:.3f})')
    
    ax.set_xlabel('Rapidez $v = \sqrt{v_x^2 + v_y^2}$')
    ax.set_ylabel('Densidad de Probabilidad $P(v)$')
    ax.set_title(f'Distribución de Velocidades - Gas Lennard-Jones\n(Validación Estadística)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    archivo = "results/gas_lj_verlet.dat"
    print("Generando análisis de velocidades...")
    
    try:
        fig = analizar_distribucion(archivo)
        if fig:
            plt.savefig("results/distribucion_velocidades_lj.png", dpi=300, bbox_inches='tight')
            print("✓ Gráfica guardada en: results/distribucion_velocidades_lj.png")
            plt.close(fig) # Usar fig para asegurar que se cierra la correcta
        else:
            print("✖ No se pudo generar la figura de Distribución de Velocidades. Revisar datos.")
    except Exception as e:
        print(f"Error CRÍTICO durante el análisis de velocidades: {e}")
