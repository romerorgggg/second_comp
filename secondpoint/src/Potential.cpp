#include "Potential.h"
#include <iostream>

Potential::Potential(double U0, double L) 
    : U0_(U0), L_(L) {}

double Potential::getForce(double x, int state) const {
    double k = 2.0 * M_PI / L_;
    
    // 1. Fuerza base F(x) = -dU/dx (trinquete asimétrico)
    double F_base = k * U0_ * (std::cos(k * x) + std::cos(2.0 * k * x));
    
    // 2. Modulación por el estado químico (s): Rectificación
    if (state == 1) {
        // Estado 1 ('Bound', potencial activo): Fuerza total del trinquete
        return F_base;
    } else {
        // Estado 2 ('Unbound', potencial casi inactivo): 
        // Se reduce drásticamente la interacción con el trinquete.
        return 0.1 * F_base; 
    }
}
