#ifndef CAJA_H
#define CAJA_H

#include <vector>
#include <fstream>
#include <string>
#include <random>
#include "Bola.h"

/**
 * @class Caja
 * @brief Gestiona un sistema de N partículas con interacción Lennard-Jones
 */
class Caja {
 private:
  double ancho_;
  double alto_;
  std::vector<Bola> bolas_;
  
  // Parámetros de Lennard-Jones
  double epsilon_;
  double sigma_;
  double r_cut_;
  double e_shift_; // Corrección de energía en r_cut
  
  std::mt19937 generador_;

  // Método clave: calcula la fuerza LJ en todas las partículas y devuelve la Epot
  double CalcularFuerzasLJ(); 

 public:
  Caja(double ancho, double alto, double epsilon, double sigma, double r_cut);
  
  void InicializarRejilla(int N, double masa, double radio, double v_max, double densidad_deseada);
  
  void EvolucionarVerlet(double dt);
  
  // Métodos de Energía
  double EnergiaCineticaTotal() const;
  
  void GuardarEstado(std::ofstream& archivo, double tiempo, double epot) const;
  void SimularCompleto(double t_final, double dt, double dt_salida,
                       const std::string& nombre_archivo);
  
  int GetNumBolas() const { return bolas_.size(); }
};

#endif // CAJA_H