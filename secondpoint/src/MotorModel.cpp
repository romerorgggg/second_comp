#include "MotorModel.h" // CRÍTICO: Incluye la definición de la clase MotorModel
#include <cmath>
#include <iostream>
#include <random>

MotorModel::MotorModel(double m, double gamma, double T, double U0, double L, double w12, double w21)
    // Inicialización del constructor (los miembros privados se ven porque MotorModel.h está incluido)
    : particle_(m, gamma), potential_(U0, L), chemical_state_(w12, w21), T_(T), k_B_(1.0) {
    
    // Inicializar generador de ruido Gaussiano
    std::random_device rd;
    generador_.seed(rd());
    ruido_dist_ = std::normal_distribution<>(0.0, 1.0);
}

double MotorModel::calculateAcceleration(double dt) {
    // 1. Fuerza del Potencial (dependiente del estado químico s)
    int state = chemical_state_.GetState();
    double F_pot = potential_.getForce(particle_.GetX(), state);
    
    // 2. Fuerza de Fricción (Stokes)
    double gamma = particle_.GetGamma();
    double F_fric = -gamma * particle_.GetV();
    
    // 3. Fuerza de Ruido (Langevin, término estocástico)
    double ruido_std = std::sqrt(2.0 * gamma * k_B_ * T_ / dt);
    double xi = ruido_dist_(generador_);
    double F_ruido = ruido_std * xi;
    
    // 4. Fuerza Total y Aceleración
    double F_total = F_pot + F_fric + F_ruido;
    double a = F_total / particle_.GetM();
    
    return a;
}

void MotorModel::evolve(double dt) {
    // 1. Paso 1 de Verlet (actualiza x y v a mitad de paso)
    particle_.MoveVerlet_Step1(dt);
    
    // 2. Conmutación de Estado Químico (s(t) -> s(t+dt))
    chemical_state_.updateState(dt);
    
    // 3. Calcular la nueva aceleración a(t+dt)
    double a_new = calculateAcceleration(dt);
    
    // 4. Paso 2 de Verlet (actualiza v final)
    particle_.MoveVerlet_Step2(dt, a_new);
    
    // 5. Actualizar la aceleración guardada en la partícula
    particle_.SetA(a_new);
}