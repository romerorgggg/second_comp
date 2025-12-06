# =========================================================
# Makefile para el Problema 2: Motor Molecular (Motor-Cargo)
# Ubicación: Raíz del Proyecto Motor Molecular
# =========================================================

BUILD_DIR = build
BIN_DIR = bin
SRC_DIR = src
INCLUDE_DIR = include
RESULTS_DIR = results
SCRIPTS_DIR = scripts 

CXX = g++
CXXFLAGS = -std=c++14 -Wall -O3 -I$(INCLUDE_DIR) -lm
LDFLAGS = -lm

# Archivos fuente específicos del Problema 2
SRCS = $(SRC_DIR)/main.cpp \
       $(SRC_DIR)/Particle.cpp \
       $(SRC_DIR)/Potential.cpp \
       $(SRC_DIR)/ChemicalState.cpp \
       $(SRC_DIR)/MotorModel.cpp

OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))

TARGET = $(BIN_DIR)/motor_cargo

.PHONY: all clean run setup analyze

all: setup $(TARGET)

setup:
	@mkdir -p $(BUILD_DIR) $(BIN_DIR) $(RESULTS_DIR) $(SCRIPTS_DIR)

# Regla de compilación genérica para .cpp -> .o
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	@echo "Compilando $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regla de enlazado (Motor)
$(TARGET): $(OBJS) | $(BIN_DIR)
	@echo "Enlazando $(TARGET)"
	$(CXX) $^ -o $@ $(LDFLAGS)

run: $(TARGET)
	@echo "Ejecutando simulación de Motor Molecular..."
	./$(TARGET)

analyze: 
	@echo "Generando gráficas de análisis del Motor Molecular..."
	python3 scripts/analisis_motor.py #

clean:
	@echo "Limpiando archivos objeto y ejecutables..."
	rm -rf $(BUILD_DIR) 
	rm -f $(BIN_DIR)/motor_cargo
doc: 
	@echo "Generando documentación con Doxygen..."
	doxygen Doxyfile
    
# Añade 'doc' al .PHONY
.PHONY: all clean run setup analyze doc
