#ifndef CHEMICALSTATE_H
#define CHEMICALSTATE_H

#include <random>

class ChemicalState {
private:
    double omega12_;    ///< Tasa de transición 1 -> 2
    double omega21_;    ///< Tasa de transición 2 -> 1
    int current_state_; ///< Estado actual (1 o 2)
    std::mt19937 generador_;
    std::uniform_real_distribution<> distribucion_;

public:
    ChemicalState(double omega12, double omega21);
    
    void updateState(double dt);
    
    int GetState() const { return current_state_; }
};

#endif // CHEMICALSTATE_H