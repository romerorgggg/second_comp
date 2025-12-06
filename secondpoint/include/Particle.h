#ifndef PARTICLE_H
#define PARTICLE_H

class Particle {
private:
    double x_;          ///< Posición
    double v_;          ///< Velocidad
    double m_;          ///< Masa
    double gamma_;      ///< Coeficiente de fricción (gamma)
    double a_;          ///< Aceleración actual
    double a_prev_;     ///< Aceleración en t-dt (necesaria para Velocity-Verlet)

public:
    Particle(double m = 1.0, double gamma = 1.0, double x0 = 0.0, double v0 = 0.0);
    
    // Métodos del integrador (Position/Velocity-Verlet)
    void MoveVerlet_Step1(double dt);
    void MoveVerlet_Step2(double dt, double new_a);
    
    // Getters y Setters
    double GetX() const { return x_; }
    double GetV() const { return v_; }
    double GetM() const { return m_; }
    double GetGamma() const { return gamma_; }
    
    void SetA(double a);
};

#endif // PARTICLE_H