#include "Caja.h"
#include <cmath>
#include <iostream>
#include <numeric>

Caja::Caja(double ancho, double alto, double epsilon, double sigma, double r_cut)
    : ancho_(ancho), alto_(alto), epsilon_(epsilon), sigma_(sigma), r_cut_(r_cut) {
  
  std::random_device rd;
  generador_.seed(rd());
  
  // Pre-cálculo de la corrección de energía (E_shift)
  double r6_cut = std::pow(r_cut_, -6.0); 
  double r12_cut = r6_cut * r6_cut;      
  e_shift_ = 4.0 * epsilon_ * (r12_cut - r6_cut);
}

void Caja::InicializarRejilla(int N, double masa, double radio, double v_max, double densidad_deseada) {
    bolas_.clear();
    
    // Calcular el espaciado para una rejilla
    double area_total = ancho_ * alto_;
    double area_por_particula = area_total / N;
    double lado_unidad = std::sqrt(area_por_particula);
    
    // Determinar cuántas columnas y filas caben
    int num_cols = std::floor(ancho_ / lado_unidad);
    int num_filas = std::ceil((double)N / num_cols);
    
    double dx = ancho_ / num_cols;
    double dy = alto_ / num_filas;
    
    std::uniform_real_distribution<> dist_pos(0.0, 1.0); // para pequeña perturbación
    std::uniform_real_distribution<> dist_vel(-v_max, v_max);
    
    double vx_cm = 0.0;
    double vy_cm = 0.0;
    
    int count = 0;
    for (int i = 0; i < num_filas; ++i) {
        for (int j = 0; j < num_cols; ++j) {
            if (count < N) {
                // Posición inicial en rejilla, centrada
                double x_base = j * dx + dx / 2.0;
                double y_base = i * dy + dy / 2.0;
                
                // Perturbación de la posición
                double x = x_base + dist_pos(generador_) * 0.1 * dx;
                double y = y_base + dist_pos(generador_) * 0.1 * dy;

                // Asegurar que la bola esté dentro de los límites
                x = std::fmax(radio, std::fmin(ancho_ - radio, x));
                y = std::fmax(radio, std::fmin(alto_ - radio, y));
                
                double vx = dist_vel(generador_);
                double vy = dist_vel(generador_);
                
                bolas_.emplace_back(x, y, vx, vy, masa, radio);
                vx_cm += vx;
                vy_cm += vy;
                count++;
            }
        }
    }
    
    // Ajustar la velocidad del centro de masa a cero
    if (N > 0) {
        vx_cm /= N;
        vy_cm /= N;
        for (auto& bola : bolas_) {
            bola.SetVx(bola.GetVx() - vx_cm);
            bola.SetVy(bola.GetVy() - vy_cm);
        }
    }

    // Primer cálculo de aceleraciones (necesario para el primer paso de Verlet)
    CalcularFuerzasLJ(); 
}

// Método clave: Calcula las fuerzas LJ en un paso de tiempo y devuelve la energía potencial total
double Caja::CalcularFuerzasLJ() {
    double energia_potencial = 0.0;
    int N = bolas_.size();
    
    // 1. Resetear aceleraciones (fuerzas)
    for (auto& bola : bolas_) {
        bola.SetAx(0.0); 
        bola.SetAy(0.0);
    }

    // 2. Iterar sobre todos los pares (i, j) con i < j
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            Bola& bola_i = bolas_[i];
            Bola& bola_j = bolas_[j];
            
            // Distancia vectorial
            double rx = bola_i.GetX() - bola_j.GetX();
            double ry = bola_i.GetY() - bola_j.GetY();
            
            double r2 = rx * rx + ry * ry;
            
            // Verificar si está dentro del radio de corte (r_cut^2)
            if (r2 < r_cut_ * r_cut_) {
                double r = std::sqrt(r2);
                
                double s_r = sigma_ / r;
                double s_r6 = s_r * s_r * s_r * s_r * s_r * s_r; 
                double s_r12 = s_r6 * s_r6;                       

                // 2.1. Cálculo de Energía Potencial (con corrección)
                double U = 4.0 * epsilon_ * (s_r12 - s_r6) - e_shift_;
                energia_potencial += U;

                // 2.2. Cálculo de Fuerza radial: F_r = -dU/dr
                double dUdr = 4.0 * epsilon_ * ((-12.0 * s_r12 / r) + (6.0 * s_r6 / r));
                double F_r = -dUdr; 

                // 2.3. Descomposición de la fuerza y aplicación de a=F/m
                double Fx_ij = F_r * (rx / r);
                double Fy_ij = F_r * (ry / r);

                double m_i = bola_i.GetMasa();
                double m_j = bola_j.GetMasa();

                // F_ji sobre i
                bola_i.SetAx(bola_i.GetAx() + Fx_ij / m_i);
                bola_i.SetAy(bola_i.GetAy() + Fy_ij / m_i);
                
                // F_ij sobre j
                bola_j.SetAx(bola_j.GetAx() - Fx_ij / m_j);
                bola_j.SetAy(bola_j.GetAy() - Fy_ij / m_j);
            }
        }
    }
    
    return energia_potencial;
}

// Implementación del integrador Velocity-Verlet
void Caja::EvolucionarVerlet(double dt) {
    // 1. Actualizar posiciones y velocidades a t+dt/2 (Paso 1)
    for (auto& bola : bolas_) {
        bola.MoverseVerlet_Paso1(dt);
    }
    
    // 2. Aplicar rebote en paredes
    for (auto& bola : bolas_) {
        bola.RebotePared(ancho_, alto_);
    }
    
    // 3. Calcular la nueva fuerza F(t+dt)
    CalcularFuerzasLJ();
    
    // 4. Actualizar velocidad a t+dt (Paso 2)
    for (auto& bola : bolas_) {
        bola.MoverseVerlet_Paso2(dt);
    }
}

double Caja::EnergiaCineticaTotal() const {
    double ecin_total = 0.0;
    for (const auto& bola : bolas_) {
        ecin_total += bola.EnergiaCinetica();
    }
    return ecin_total;
}

void Caja::GuardarEstado(std::ofstream& archivo, double tiempo, double epot) const {
    archivo << tiempo;
    for (const auto& bola : bolas_) {
        archivo << "\t" << bola.GetX() << "\t" << bola.GetY()
                << "\t" << bola.GetVx() << "\t" << bola.GetVy();
    }
    // La energía potencial total (última columna)
    archivo << "\t" << epot; 
    archivo << "\n";
}

void Caja::SimularCompleto(double t_final, double dt, double dt_salida,
                       const std::string& nombre_archivo) {
    std::ofstream archivo_salida(nombre_archivo);
    if (!archivo_salida.is_open()) {
        std::cerr << "Error: No se pudo abrir el archivo de salida: " << nombre_archivo << std::endl;
        return;
    }

    double tiempo = 0.0;
    double proximo_tiempo_guardado = 0.0;
    
    // Calcular energía inicial y guardar
    double epot_inicial = CalcularFuerzasLJ(); 
    double ecin_inicial = EnergiaCineticaTotal();
    double etotal_inicial = ecin_inicial + epot_inicial;
    
    // Imprimir encabezado
    std::cout << "t=0: E_cinetica=" << ecin_inicial
              << ", E_potencial=" << epot_inicial
              << ", E_total=" << etotal_inicial << std::endl;
    
    // Bucle principal de la simulación
    while (tiempo < t_final) {
        
        // 1. Integración
        EvolucionarVerlet(dt); 
        
        // 2. Cálculo de Energías para logging (solo si es tiempo de guardar)
        if (tiempo >= proximo_tiempo_guardado) {
            double ecin = EnergiaCineticaTotal();
            // Recalcular fuerzas (y Epot) para obtener el valor al tiempo t+dt
            double epot = CalcularFuerzasLJ();
            double etotal = ecin + epot;
            
            // 3. Guardar estado y Energía
            GuardarEstado(archivo_salida, tiempo, epot);
            
            // 4. Imprimir a consola
            std::cout << "t=" << tiempo << ": E_cinetica=" << ecin
                      << ", E_potencial=" << epot
                      << ", E_total=" << etotal << std::endl;
            
            proximo_tiempo_guardado += dt_salida;
        }
        
        tiempo += dt;
        
        // Manejar errores de redondeo
        if (tiempo >= proximo_tiempo_guardado + dt) {
             proximo_tiempo_guardado = tiempo; // Forzar el próximo guardado si se perdió
        }
    }
    
    archivo_salida.close();
}