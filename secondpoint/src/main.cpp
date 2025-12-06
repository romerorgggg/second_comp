#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <iomanip>
#include "MotorModel.h"

// Parámetros de la simulación
const double T_FINAL = 5000.0; // Tiempo total de simulación
const double DT = 0.001;       // Paso temporal (debe ser muy pequeño)
const double DT_SALIDA = 5.0;  // Frecuencia de guardado para el análisis

// Parámetros del Motor Molecular
const double M = 1.0;            // Masa
const double GAMMA = 1.0;        // Fricción
const double T_TEMP = 1.0;       // Temperatura (k_B=1)
const double U0 = 10.0;          // Altura del potencial
const double L = 10.0;           // Período del trinquete
// Desequilibrio: w12 > w21 -> Transporte dirigido (Rectificación)
const double W12 = 0.01;         // Tasa de transición 1 -> 2 (motor activo)
const double W21 = 0.005;        // Tasa de transición 2 -> 1 (motor inactivo)

void guardar_estado(std::ofstream& archivo, double t, const MotorModel& motor) {
    archivo << std::fixed << std::setprecision(6) 
            << t << "\t"
            << motor.GetX() << "\t"
            << motor.GetV() << "\t"
            << motor.GetState() << "\n";
}

int main() {
    std::cout << "=== Simulación de Motor Molecular (Problema 2) ===" << std::endl;
    
    // 1. Creación del objeto MotorModel
    MotorModel motor(M, GAMMA, T_TEMP, U0, L, W12, W21);
    
    // 2. Inicialización del archivo de salida
    const std::string NOMBRE_ARCHIVO = "results/motor_cargo_run.dat";
    std::ofstream archivo_salida(NOMBRE_ARCHIVO);
    // ... (manejo de errores de archivo omitido por brevedad)
    
    archivo_salida << "# t\t x\t v\t s (state)\n";
    
    double tiempo = 0.0;
    double proximo_tiempo_guardado = 0.0;
    
    guardar_estado(archivo_salida, tiempo, motor);
    
    // 3. Bucle principal de la simulación
    while (tiempo < T_FINAL) {
        
        motor.evolve(DT);
        tiempo += DT;
        
        if (tiempo >= proximo_tiempo_guardado) {
            guardar_estado(archivo_salida, tiempo, motor);
            proximo_tiempo_guardado += DT_SALIDA;
        }
    }
    
    archivo_salida.close();
    std::cout << "\nSimulación finalizada." << std::endl;
    std::cout << "Desplazamiento Neto Final (x): " << motor.GetX() << std::endl;
    
    return 0;
}