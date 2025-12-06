#ifndef POTENTIAL_H
#define POTENTIAL_H

#include <cmath>

class Potential {
private:
    double U0_;         ///< Altura del potencial
    double L_;          ///< Período del trinquete
    
public:
    Potential(double U0 = 10.0, double L = 1.0);
    
    double getForce(double x, int state) const;
};

#endif // POTENTIAL_H