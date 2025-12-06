#ifndef MOTORMODEL_H
#define MOTORMODEL_H

#include "Particle.h"
#include "Potential.h"
#include "ChemicalState.h"
#include <random>

class MotorModel {
private:
    Particle particle_;
    Potential potential_;
    ChemicalState chemical_state_;
    
    double T_; ///< Temperatura
    double k_B_; ///< Constante de Boltzmann (k_B=1)
    
    std::mt19937 generador_;
    std::normal_distribution<> ruido_dist_;
    
public:
    MotorModel(double m, double gamma, double T, double U0, double L, double w12, double w21);
    
    double calculateAcceleration(double dt);
    void evolve(double dt);
    
    // Getters para logging
    double GetX() const { return particle_.GetX(); }
    double GetV() const { return particle_.GetV(); }
    int GetState() const { return chemical_state_.GetState(); }
};

#endif // MOTORMODEL_H