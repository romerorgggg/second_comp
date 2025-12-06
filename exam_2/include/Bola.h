#ifndef BOLA_H
#define BOLA_H

#include <cmath>

class Bola {
 private:
  double x_;       ///< Posición en x
  double y_;       ///< Posición en y
  double vx_;      ///< Velocidad en x
  double vy_;      ///< Velocidad en y
  double masa_;    ///< Masa de la partícula
  double radio_;   
  
  double ax_;      ///< Aceleración actual en x
  double ay_;      ///< Aceleración actual en y
  double ax_prev_; ///< Aceleración anterior en x (para el Paso 2 de Verlet)

 public:
  Bola();
  Bola(double x, double y, double vx, double vy, double masa, double radio);
  void Iniciar(double x, double y, double vx, double vy, double masa, double radio);
  
  // Métodos de movimiento (Versión Verlet)
  void MoverseVerlet_Paso1(double dt); // r(t+dt) y v(t+dt/2)
  void MoverseVerlet_Paso2(double dt); // v(t+dt)

  void RebotePared(double W, double H);
  
  // Propiedades
  double EnergiaCinetica() const;
  double Rapidez() const;

  // Getters
  double GetX() const { return x_; }
  double GetY() const { return y_; }
  double GetVx() const { return vx_; }
  double GetVy() const { return vy_; }
  double GetMasa() const { return masa_; }
  
  // Setters y Getters de aceleración
  void SetVx(double vx) { vx_ = vx; }
  void SetVy(double vy) { vy_ = vy; }
  void SetAx(double ax) { ax_ = ax; }
  void SetAy(double ay) { ay_ = ay; }
  double GetAx() const { return ax_; }
  double GetAy() const { return ay_; }
};

#endif // BOLA_H