"""
Práctica 12: Visualización gráfica del control RGB
Muestra los valores de los potenciómetros en tiempo real
"""

import tkinter as tk
from tkinter import ttk
import serial
import threading
import time
import re
from datetime import datetime

class ControlRGB:
    def __init__(self, puerto='COM3', baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        self.serial_activo = False
        self.ser = None
        
        # Valores actuales
        self.r_val = 0
        self.g_val = 0
        self.b_val = 0
        
        # Patrón para detectar datos
        self.patron = re.compile(r'R:(\d+)% \| G:(\d+)% \| B:(\d+)%')
        
        # Crear interfaz
        self.root = tk.Tk()
        self.root.title("Control RGB - Práctica 12")
        self.root.geometry("800x500")
        self.root.configure(bg='#2b2b2b')
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Control de LED RGB", 
                         font=('Arial', 24, 'bold'),
                         bg='#2b2b2b', fg='white')
        titulo.pack(pady=20)
        
        # Frame de conexión
        frame_conexion = tk.Frame(self.root, bg='#2b2b2b')
        frame_conexion.pack(pady=10)
        
        tk.Label(frame_conexion, text="Puerto:", bg='#2b2b2b', fg='white').pack(side=tk.LEFT, padx=5)
        self.entry_puerto = tk.Entry(frame_conexion, width=10)
        self.entry_puerto.pack(side=tk.LEFT, padx=5)
        self.entry_puerto.insert(0, self.puerto)
        
        self.btn_conectar = tk.Button(frame_conexion, text="Conectar", 
                                      command=self.conectar,
                                      bg='#4CAF50', fg='white')
        self.btn_conectar.pack(side=tk.LEFT, padx=5)
        
        self.btn_desconectar = tk.Button(frame_conexion, text="Desconectar", 
                                         command=self.desconectar,
                                         bg='#f44336', fg='white',
                                         state='disabled')
        self.btn_desconectar.pack(side=tk.LEFT, padx=5)
        
        self.label_estado = tk.Label(frame_conexion, text="Desconectado", 
                                     bg='#2b2b2b', fg='red')
        self.label_estado.pack(side=tk.LEFT, padx=20)
        
        # Frame para mostrar colores
        frame_colores = tk.Frame(self.root, bg='#2b2b2b')
        frame_colores.pack(pady=30)
        
        # Rojo
        frame_r = tk.Frame(frame_colores, bg='#2b2b2b')
        frame_r.pack(side=tk.LEFT, padx=20)
        
        self.label_r = tk.Label(frame_r, text="ROJO", font=('Arial', 14, 'bold'),
                               bg='#2b2b2b', fg='#ff4444')
        self.label_r.pack()
        
        self.canvas_r = tk.Canvas(frame_r, width=100, height=100, bg='#1a1a1a')
        self.canvas_r.pack()
        self.rect_r = self.canvas_r.create_rectangle(0, 0, 100, 100, fill='#000000')
        
        self.valor_r = tk.Label(frame_r, text="0%", font=('Arial', 16, 'bold'),
                               bg='#2b2b2b', fg='white')
        self.valor_r.pack()
        
        # Verde
        frame_g = tk.Frame(frame_colores, bg='#2b2b2b')
        frame_g.pack(side=tk.LEFT, padx=20)
        
        self.label_g = tk.Label(frame_g, text="VERDE", font=('Arial', 14, 'bold'),
                               bg='#2b2b2b', fg='#44ff44')
        self.label_g.pack()
        
        self.canvas_g = tk.Canvas(frame_g, width=100, height=100, bg='#1a1a1a')
        self.canvas_g.pack()
        self.rect_g = self.canvas_g.create_rectangle(0, 0, 100, 100, fill='#000000')
        
        self.valor_g = tk.Label(frame_g, text="0%", font=('Arial', 16, 'bold'),
                               bg='#2b2b2b', fg='white')
        self.valor_g.pack()
        
        # Azul
        frame_b = tk.Frame(frame_colores, bg='#2b2b2b')
        frame_b.pack(side=tk.LEFT, padx=20)
        
        self.label_b = tk.Label(frame_b, text="AZUL", font=('Arial', 14, 'bold'),
                               bg='#2b2b2b', fg='#4444ff')
        self.label_b.pack()
        
        self.canvas_b = tk.Canvas(frame_b, width=100, height=100, bg='#1a1a1a')
        self.canvas_b.pack()
        self.rect_b = self.canvas_b.create_rectangle(0, 0, 100, 100, fill='#000000')
        
        self.valor_b = tk.Label(frame_b, text="0%", font=('Arial', 16, 'bold'),
                               bg='#2b2b2b', fg='white')
        self.valor_b.pack()
        
        # Color resultante
        frame_resultado = tk.Frame(self.root, bg='#2b2b2b')
        frame_resultado.pack(pady=30)
        
        tk.Label(frame_resultado, text="Color resultante:", 
                font=('Arial', 12), bg='#2b2b2b', fg='white').pack()
        
        self.canvas_resultado = tk.Canvas(frame_resultado, width=200, height=50, 
                                         bg='#000000', highlightthickness=2,
                                         highlightbackground='white')
        self.canvas_resultado.pack()
        
    def conectar(self):
        try:
            self.puerto = self.entry_puerto.get()
            self.ser = serial.Serial(self.puerto, self.baudrate, timeout=0.1)
            self.serial_activo = True
            
            self.label_estado.config(text="Conectado", fg='green')
            self.btn_conectar.config(state='disabled')
            self.btn_desconectar.config(state='normal')
            
            # Iniciar hilo de lectura
            self.hilo = threading.Thread(target=self.leer_datos, daemon=True)
            self.hilo.start()
            
            print(f"✅ Conectado a {self.puerto}")
            
        except Exception as e:
            self.label_estado.config(text=f"Error: {e}", fg='red')
            
    def desconectar(self):
        self.serial_activo = False
        if self.ser:
            self.ser.close()
        self.label_estado.config(text="Desconectado", fg='red')
        self.btn_conectar.config(state='normal')
        self.btn_desconectar.config(state='disabled')
        print("🔌 Desconectado")
        
    def leer_datos(self):
        while self.serial_activo:
            try:
                if self.ser and self.ser.in_waiting:
                    linea = self.ser.readline().decode('utf-8').strip()
                    
                    # Buscar patrón R:XX% | G:XX% | B:XX%
                    match = self.patron.search(linea)
                    if match:
                        r = int(match.group(1))
                        g = int(match.group(2))
                        b = int(match.group(3))
                        
                        # Actualizar desde el hilo principal
                        self.root.after(0, self.actualizar_valores, r, g, b)
                        
            except Exception as e:
                print(f"Error lectura: {e}")
            time.sleep(0.05)
            
    def actualizar_valores(self, r, g, b):
        # Guardar valores
        self.r_val = r
        self.g_val = g
        self.b_val = b
        
        # Actualizar etiquetas
        self.valor_r.config(text=f"{r}%")
        self.valor_g.config(text=f"{g}%")
        self.valor_b.config(text=f"{b}%")
        
        # Actualizar colores de los cuadros
        r_hex = int(r * 2.55)  # Convertir % a 0-255
        g_hex = int(g * 2.55)
        b_hex = int(b * 2.55)
        
        color_r = f'#{r_hex:02x}0000'
        color_g = f'#00{g_hex:02x}00'
        color_b = f'#0000{b_hex:02x}'
        color_rgb = f'#{r_hex:02x}{g_hex:02x}{b_hex:02x}'
        
        self.canvas_r.itemconfig(self.rect_r, fill=color_r)
        self.canvas_g.itemconfig(self.rect_g, fill=color_g)
        self.canvas_b.itemconfig(self.rect_b, fill=color_b)
        self.canvas_resultado.configure(bg=color_rgb)
        
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Detectar puerto
    import serial.tools.list_ports
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    
    if puertos:
        print(f"Puertos disponibles: {puertos}")
        puerto = puertos[0]
    else:
        puerto = 'COM3'
        print("Usando COM3 por defecto")
    
    app = ControlRGB(puerto=puerto)
    app.iniciar()