#include "Particle.h"

Particle::Particle(double m, double gamma, double x0, double v0)
    : x_(x0), v_(v0), m_(m), gamma_(gamma), a_(0.0), a_prev_(0.0) {}

void Particle::SetA(double a) {
    a_prev_ = a_; 
    a_ = a;       
}

// Paso 1 de Velocity-Verlet: Posición y velocidad a t+dt/2
void Particle::MoveVerlet_Step1(double dt) {
    double dt2_2 = 0.5 * dt * dt;
    double dt_2 = 0.5 * dt;

    x_ += v_ * dt + a_ * dt2_2;
    v_ += a_ * dt_2;
}

// Paso 2 de Velocity-Verlet: Velocidad final a t+dt
void Particle::MoveVerlet_Step2(double dt, double new_a) {
    double dt_2 = 0.5 * dt;
    v_ += new_a * dt_2;
}
