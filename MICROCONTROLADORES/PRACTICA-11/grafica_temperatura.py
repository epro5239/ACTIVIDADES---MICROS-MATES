"""
Versión con tkinter para mejor control
"""

import tkinter as tk
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import threading
import time
import re
from datetime import datetime

class MonitorTemperatura:
    def __init__(self, puerto='COM3', baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        self.serial_activo = False
        self.ser = None
        
        # Datos
        self.tiempos = []
        self.temperaturas = []
        self.max_puntos = 200
        self.tiempo_inicio = None
        
        # Patrón
        self.patron = re.compile(r'T:([0-9.]+),')
        
        # Ventana
        self.root = tk.Tk()
        self.root.title("Monitor Temperatura Tiempo Real")
        self.root.geometry("1000x600")
        
        self.crear_interfaz()
        self.configurar_grafica()
        
    def crear_interfaz(self):
        # Frame controles
        frame_controles = ttk.Frame(self.root, padding=10)
        frame_controles.pack(fill=tk.X)
        
        ttk.Label(frame_controles, text="Puerto:").pack(side=tk.LEFT, padx=5)
        self.entry_puerto = ttk.Entry(frame_controles, width=10)
        self.entry_puerto.pack(side=tk.LEFT, padx=5)
        self.entry_puerto.insert(0, self.puerto)
        
        self.btn_conectar = ttk.Button(frame_controles, text="Conectar", 
                                       command=self.conectar)
        self.btn_conectar.pack(side=tk.LEFT, padx=5)
        
        self.btn_desconectar = ttk.Button(frame_controles, text="Desconectar", 
                                          command=self.desconectar, state='disabled')
        self.btn_desconectar.pack(side=tk.LEFT, padx=5)
        
        self.label_estado = ttk.Label(frame_controles, text="Desconectado", 
                                      foreground='red')
        self.label_estado.pack(side=tk.LEFT, padx=20)
        
        # Frame temperatura actual
        frame_temp = ttk.Frame(self.root, padding=10)
        frame_temp.pack(fill=tk.X)
        
        self.label_temp = ttk.Label(frame_temp, text="-- °C", 
                                    font=('Arial', 24, 'bold'))
        self.label_temp.pack(side=tk.LEFT, padx=20)
        
        self.label_stats = ttk.Label(frame_temp, text="Muestras: 0 | Min: -- | Max: --")
        self.label_stats.pack(side=tk.LEFT, padx=20)
        
        # Frame gráfica
        frame_grafica = ttk.Frame(self.root)
        frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Temperatura (°C)')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=45, color='r', linestyle='--', label='Umbral 45°C')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.legend()
        self.linea, = self.ax.plot([], [], 'b-', linewidth=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafica)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def configurar_grafica(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.actualizar_grafica,
            interval=200, cache_frame_data=False, blit=False
        )
        
    def conectar(self):
        try:
            self.puerto = self.entry_puerto.get()
            self.ser = serial.Serial(self.puerto, self.baudrate, timeout=0.1)
            self.serial_activo = True
            self.tiempo_inicio = time.time()
            
            # Limpiar datos
            self.tiempos = []
            self.temperaturas = []
            
            self.label_estado.config(text="Conectado", foreground='green')
            self.btn_conectar.config(state='disabled')
            self.btn_desconectar.config(state='normal')
            
            # Iniciar hilo de lectura
            self.hilo = threading.Thread(target=self.leer_datos, daemon=True)
            self.hilo.start()
            
            print("✅ Conectado")
            
        except Exception as e:
            self.label_estado.config(text=f"Error: {e}", foreground='red')
            
    def desconectar(self):
        self.serial_activo = False
        if self.ser:
            self.ser.close()
        self.label_estado.config(text="Desconectado", foreground='red')
        self.btn_conectar.config(state='normal')
        self.btn_desconectar.config(state='disabled')
        print("🔌 Desconectado")
        
    def leer_datos(self):
        while self.serial_activo:
            try:
                if self.ser and self.ser.in_waiting:
                    linea = self.ser.readline().decode('utf-8').strip()
                    
                    match = self.patron.search(linea)
                    if match:
                        temp = float(match.group(1))
                        t = time.time() - self.tiempo_inicio
                        
                        # Actualizar desde el hilo principal
                        self.root.after(0, self.agregar_dato, t, temp)
                        
            except Exception as e:
                print(f"Error lectura: {e}")
            time.sleep(0.01)
            
    def agregar_dato(self, t, temp):
        # Agregar datos
        self.tiempos.append(t)
        self.temperaturas.append(temp)
        
        # Mantener límite
        if len(self.tiempos) > self.max_puntos:
            self.tiempos.pop(0)
            self.temperaturas.pop(0)
        
        # Actualizar etiquetas
        self.label_temp.config(
            text=f"{temp:.2f} °C",
            foreground='red' if temp > 45 else 'black'
        )
        
        if self.temperaturas:
            muestras = len(self.temperaturas)
            min_temp = min(self.temperaturas)
            max_temp = max(self.temperaturas)
            self.label_stats.config(
                text=f"Muestras: {muestras} | Min: {min_temp:.2f}°C | Max: {max_temp:.2f}°C"
            )
        
    def actualizar_grafica(self, frame):
        if self.tiempos and self.temperaturas:
            self.linea.set_data(self.tiempos, self.temperaturas)
            
            # Ajustar ejes
            if self.tiempos:
                t_max = max(self.tiempos)
                self.ax.set_xlim(max(0, t_max-60), t_max+1)
            
            if self.temperaturas:
                y_min = max(0, min(self.temperaturas)-5)
                y_max = min(100, max(self.temperaturas)+5)
                self.ax.set_ylim(y_min, y_max)
            
            self.canvas.draw_idle()
        
        return self.linea,
    
    def iniciar(self):
        self.root.mainloop()

# Ejecutar
if __name__ == "__main__":
    # Detectar puerto automáticamente
    import serial.tools.list_ports
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    
    if puertos:
        print(f"Puertos disponibles: {puertos}")
        puerto = puertos[0]
    else:
        puerto = 'COM9'
        print("No se detectaron puertos, usando COM3")
    
    app = MonitorTemperatura(puerto=puerto)
    app.iniciar()