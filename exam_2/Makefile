# =========================================================
# Makefile para el Problema 1: Gas de Lennard-Jones
# Archivos: main_lj.cpp, Bola.cpp, Caja.cpp
# =========================================================

BUILD_DIR = build
BIN_DIR = bin
SRC_DIR = src
INCLUDE_DIR = include
RESULTS_DIR = results

CXX = g++
CXXFLAGS = -std=c++14 -Wall -O3 -I$(INCLUDE_DIR) -lm
LDFLAGS = -lm

# 🔴 Archivos fuente con el nuevo nombre
SRCS = $(SRC_DIR)/main_lj.cpp \
       $(SRC_DIR)/Bola.cpp \
       $(SRC_DIR)/Caja.cpp

OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))

TARGET = $(BIN_DIR)/simulacion_lj

.PHONY: all clean run setup

all: setup $(TARGET)

setup:
	@mkdir -p $(BUILD_DIR) $(BIN_DIR) $(RESULTS_DIR)

# Regla de compilación genérica para .cpp -> .o
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	@echo "Compilando $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regla de enlazado (LJ)
$(TARGET): $(OBJS) | $(BIN_DIR)
	@echo "Enlazando $(TARGET)"
	$(CXX) $^ -o $@ $(LDFLAGS)

run: $(TARGET)
	@echo "Ejecutando simulación LJ..."
	./$(TARGET)

clean:
	@echo "Limpiando archivos objeto y ejecutables..."
	rm -rf $(BUILD_DIR) $(BIN_DIR)/simulacion_lj
