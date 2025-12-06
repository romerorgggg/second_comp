#include "Bola.h"

Bola::Bola()
    : x_(0.0), y_(0.0), vx_(0.0), vy_(0.0), masa_(1.0), radio_(0.1), 
      ax_(0.0), ay_(0.0), ax_prev_(0.0) {}

Bola::Bola(double x, double y, double vx, double vy, double masa, double radio)
    : x_(x), y_(y), vx_(vx), vy_(vy), masa_(masa), radio_(radio),
      ax_(0.0), ay_(0.0), ax_prev_(0.0) {}

void Bola::Iniciar(double x, double y, double vx, double vy, double masa, double radio) {
  x_ = x;
  y_ = y;
  vx_ = vx;
  vy_ = vy;
  masa_ = masa;
  radio_ = radio;
  ax_ = 0.0;
  ay_ = 0.0;
  ax_prev_ = 0.0;
}

void Bola::MoverseVerlet_Paso1(double dt) {
  x_ += vx_ * dt + 0.5 * ax_ * dt * dt;
  y_ += vy_ * dt + 0.5 * ay_ * dt * dt;
  
  vx_ += 0.5 * ax_ * dt;
  vy_ += 0.5 * ay_ * dt;

  ax_prev_ = ax_;
  ax_ = 0.0; 
  ay_ = 0.0; 
}

void Bola::MoverseVerlet_Paso2(double dt) {
  vx_ += 0.5 * ax_ * dt;
  vy_ += 0.5 * ay_ * dt;
}

void Bola::RebotePared(double W, double H) {
  // Rebote en x
  if (x_ - radio_ < 0.0) {
    x_ = radio_;
    vx_ *= -1.0;
  } else if (x_ + radio_ > W) {
    x_ = W - radio_;
    vx_ *= -1.0;
  }

  // Rebote en y
  if (y_ - radio_ < 0.0) {
    y_ = radio_;
    vy_ *= -1.0;
  } else if (y_ + radio_ > H) {
    y_ = H - radio_;
    vy_ *= -1.0;
  }
}

double Bola::EnergiaCinetica() const {
  return 0.5 * masa_ * (vx_ * vx_ + vy_ * vy_);
}

double Bola::Rapidez() const {
  return std::sqrt(vx_ * vx_ + vy_ * vy_);
}