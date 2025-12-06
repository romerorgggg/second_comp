#include "ChemicalState.h"
#include <iostream>
#include <random>

ChemicalState::ChemicalState(double omega12, double omega21)
    : omega12_(omega12), omega21_(omega21), current_state_(1) {
    
    std::random_device rd;
    generador_.seed(rd());
    distribucion_ = std::uniform_real_distribution<>(0.0, 1.0);
}

void ChemicalState::updateState(double dt) {
    double r = distribucion_(generador_);
    
    if (current_state_ == 1) {
        // Transición 1 -> 2
        double prob_12 = 1.0 - std::exp(-omega12_ * dt);
        if (r < prob_12) {
            current_state_ = 2;
        }
    } else {
        // Transición 2 -> 1
        double prob_21 = 1.0 - std::exp(-omega21_ * dt);
        if (r < prob_21) {
            current_state_ = 1;
        }
    }
}