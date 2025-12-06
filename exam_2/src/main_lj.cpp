#include <iostream>
#include <cstdlib> 
#include "Caja.h"

// Definiciones de parámetros del problema
const double W = 10.0;      // Ancho de la caja
const double H = 10.0;      // Alto de la caja
const int N = 100;          // Número de partículas
const double MASA = 1.0;    // Masa (unidades reducidas)
const double RADIO = 0.5;   // Radio 

// Parámetros de Lennard-Jones (unidades reducidas LJ)
const double EPSILON = 1.0; 
const double SIGMA = 1.0;   
const double R_CUT = 2.5 * SIGMA; 

// Parámetros de simulación - ¡Validados para estabilidad!
const double T_FINAL = 5.0;       // Tiempo total de simulación
const double DT = 0.00005;        // Paso de tiempo (VALIDADO: 0.00005)
const double DT_SALIDA = 0.05;    // Frecuencia de guardado
const double V_MAX_INICIAL = 1.0; 

const double DENSIDAD_INICIAL = (double)N / (W * H); 

int main() {
    // Crear el directorio de resultados
    system("mkdir -p results"); 
    
    // 1. Crear el objeto Caja con los parámetros LJ
    Caja caja(W, H, EPSILON, SIGMA, R_CUT);
    
    // 2. Inicializar partículas en rejilla y ajustar V_cm = 0
    caja.InicializarRejilla(N, MASA, RADIO, V_MAX_INICIAL, DENSIDAD_INICIAL); 
    
    // 3. Ejecutar la simulación con Velocity-Verlet
    std::string nombre_archivo = "results/gas_lj_verlet.dat";
    std::cout << "Iniciando simulación de Gas Lennard-Jones con Velocity-Verlet..." << std::endl;
    std::cout << "Usando DT = " << DT << " para estabilidad..." << std::endl;
    
    caja.SimularCompleto(T_FINAL, DT, DT_SALIDA, nombre_archivo);
    
    std::cout << "Simulación finalizada." << std::endl;

    return 0;
}
