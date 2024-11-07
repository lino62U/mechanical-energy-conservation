import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QLineEdit, QPushButton, QGridLayout, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Funciones para calcular las energías
def energia_cinetica(m, v):
    return 0.5 * m * v**2

def energia_potencial(m, h, g):
    return m * g * h

def energia_mecanica(m, v, h, g):
    return energia_cinetica(m, v) + energia_potencial(m, h, g)

class EnergyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.setWindowTitle("Conservación de la Energía Mecánica")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crear el widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Diseño general en una cuadrícula
        main_layout = QGridLayout()
        
        # Sección de entrada de datos
        input_layout = QVBoxLayout()
        
        # Etiquetas y campos de entrada
        input_layout.addWidget(QLabel("Masa (kg):"))
        self.mass_input = QLineEdit()
        input_layout.addWidget(self.mass_input)
        
        input_layout.addWidget(QLabel("Velocidad inicial (m/s):"))
        self.velocity_input = QLineEdit()
        input_layout.addWidget(self.velocity_input)
        
        input_layout.addWidget(QLabel("Altura inicial (m):"))
        self.height_input = QLineEdit()
        input_layout.addWidget(self.height_input)
        
        input_layout.addWidget(QLabel("Tiempo total (s):"))
        self.time_input = QLineEdit()
        input_layout.addWidget(self.time_input)
        
        input_layout.addWidget(QLabel("Gravedad (m/s²):"))
        self.gravity_input = QLineEdit("9.8")  # Valor por defecto de la gravedad
        input_layout.addWidget(self.gravity_input)
        
        # Botón para generar los gráficos
        self.calc_button = QPushButton("Calcular y Graficar")
        self.calc_button.clicked.connect(self.plot_energies)
        input_layout.addWidget(self.calc_button)
        
        # Etiqueta para mostrar la energía mecánica calculada
        self.energy_label = QLabel("Energía Mecánica Total: -")
        input_layout.addWidget(self.energy_label)
        
        # Agregar la sección de entrada al layout principal (izquierda)
        main_layout.addLayout(input_layout, 0, 0)
        
        # Crear contenedor para los gráficos
        graph_layout = QVBoxLayout()
        
        # Crear canvas para el gráfico principal (Energía vs Tiempo)
        self.canvas_main = FigureCanvas(Figure(figsize=(8, 5)))
        graph_layout.addWidget(self.canvas_main)
        
        # Crear una sección horizontal para los gráficos de energía cinética y potencial
        sub_graph_layout = QHBoxLayout()
        
        # Crear canvas para el gráfico de Energía Cinética vs Velocidad (más pequeño)
        self.canvas_kinetic = FigureCanvas(Figure(figsize=(4, 2.5)))
        sub_graph_layout.addWidget(self.canvas_kinetic)
        
        # Crear canvas para el gráfico de Energía Potencial vs Altura (más pequeño)
        self.canvas_potential = FigureCanvas(Figure(figsize=(4, 2.5)))
        sub_graph_layout.addWidget(self.canvas_potential)
        
        # Agregar la sección de gráficos secundarios (inferior) al layout de gráficos
        graph_layout.addLayout(sub_graph_layout)
        
        # Agregar la sección de gráficos al layout principal (derecha)
        main_layout.addLayout(graph_layout, 0, 1)
        
        # Configuración del diseño principal
        main_widget.setLayout(main_layout)
    
    def plot_energies(self):
        # Validar y obtener datos de entrada
        try:
            m = float(self.mass_input.text())
            v_inicial = float(self.velocity_input.text())
            h_inicial = float(self.height_input.text())
            tiempo_total = float(self.time_input.text())
            g = float(self.gravity_input.text())
            if m <= 0 or h_inicial < 0 or tiempo_total <= 0 or g <= 0:
                raise ValueError("Los valores deben ser positivos.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        
        # Configuración de la simulación
        num_puntos = 100
        tiempos = np.linspace(0, tiempo_total, num_puntos)
        alturas = h_inicial - 0.5 * g * tiempos**2
        velocidades = np.sqrt(v_inicial**2 + 2 * g * (h_inicial - alturas))
        
        # Clipping para que no haya alturas negativas
        alturas = np.clip(alturas, 0, h_inicial)
        
        # Cálculo de energías
        energias_cineticas = [energia_cinetica(m, v) for v in velocidades]
        energias_potenciales = [energia_potencial(m, h, g) for h in alturas]
        energias_mecanicas = [energia_mecanica(m, v, h, g) for v, h in zip(velocidades, alturas)]
        
        # Mostrar energía mecánica total (último valor)
        self.energy_label.setText(f"Energía Mecánica Total: {energias_mecanicas[-1]:.2f} J")
        
        # Limpiar figuras anteriores
        self.canvas_main.figure.clf()
        self.canvas_kinetic.figure.clf()
        self.canvas_potential.figure.clf()
        
        # Gráfico de Energías en función del tiempo
        ax_main = self.canvas_main.figure.add_subplot(111)
        ax_main.plot(tiempos, energias_cineticas, label="Energía Cinética (EK)", color="blue")
        ax_main.plot(tiempos, energias_potenciales, label="Energía Potencial (EP)", color="green")
        ax_main.plot(tiempos, energias_mecanicas, label="Energía Mecánica Total (Em)", color="red", linestyle="--")
        ax_main.set_title("Energías Cinética, Potencial y Mecánica Total vs Tiempo")
        ax_main.set_xlabel("Tiempo (s)")
        ax_main.set_ylabel("Energía (J)")
        ax_main.legend()
        ax_main.grid(True)
        
        # Gráfico de Energía Cinética vs Velocidad
        ax_kinetic = self.canvas_kinetic.figure.add_subplot(111)
        ax_kinetic.plot(velocidades, energias_cineticas, color="blue")
        ax_kinetic.set_title("Energía Cinética vs Velocidad")
        ax_kinetic.set_xlabel("Velocidad (m/s)")
        ax_kinetic.set_ylabel("Energía Cinética (J)")
        ax_kinetic.grid(True)
        
        # Gráfico de Energía Potencial vs Altura
        ax_potential = self.canvas_potential.figure.add_subplot(111)
        ax_potential.plot(alturas, energias_potenciales, color="green")
        ax_potential.set_title("Energía Potencial vs Altura")
        ax_potential.set_xlabel("Altura (m)")
        ax_potential.set_ylabel("Energía Potencial (J)")
        ax_potential.grid(True)
        
        # Mostrar gráficos actualizados
        self.canvas_main.draw()
        self.canvas_kinetic.draw()
        self.canvas_potential.draw()

# Inicializar la aplicación de PyQt
app = QApplication(sys.argv)
window = EnergyApp()
window.show()
sys.exit(app.exec_())
