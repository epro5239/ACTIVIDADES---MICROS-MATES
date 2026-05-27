"""
interfaz_motor_final.py
Practica 13 - Control de motor DC
Version optimizada con respuesta inmediata
"""

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time

COLORS = {
    'bg': '#1a1a2e',
    'card': '#16213e',
    'accent': '#e94560',
    'fwd': '#00ff88',
    'rev': '#ff4444',
    'stop': '#ffaa00',
    'text': '#ffffff',
    'text_sec': '#94a3b8'
}

class MotorApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Practica 13 - Control de Motor DC")
        self.geometry("450x600")
        self.resizable(False, False)
        self.configure(bg=COLORS['bg'])
        
        self.serial = None
        self.connected = False
        self.direction = "F"
        self.current_speed = 0
        self._send_timer = None  # Para debounce
        
        self._build_ui()
        self._refresh_ports()
    
    def _build_ui(self):
        # Titulo
        tk.Label(self, text="CONTROL DE MOTOR DC",
                font=("Arial", 18, "bold"),
                bg=COLORS['bg'], fg=COLORS['accent']).pack(pady=15)
        
        tk.Label(self, text="Raspberry Pi Pico W | Puente H TIP122",
                font=("Arial", 9),
                bg=COLORS['bg'], fg=COLORS['text_sec']).pack()
        
        # Conexion
        conn_frame = tk.Frame(self, bg=COLORS['card'])
        conn_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(conn_frame, text="Puerto:", bg=COLORS['card'], 
                fg=COLORS['text']).pack(side="left", padx=5)
        self.port_combo = ttk.Combobox(conn_frame, width=12, state="readonly")
        self.port_combo.pack(side="left", padx=5)
        
        tk.Label(conn_frame, text="Baud:", bg=COLORS['card'],
                fg=COLORS['text']).pack(side="left", padx=5)
        self.baud_combo = ttk.Combobox(conn_frame, width=8, state="readonly",
                                       values=["115200"])
        self.baud_combo.set("115200")
        self.baud_combo.pack(side="left", padx=5)
        
        self.btn_connect = tk.Button(conn_frame, text="Conectar", width=10,
                                    bg=COLORS['fwd'], fg="black",
                                    font=("Arial", 9, "bold"),
                                    command=self._toggle_connect)
        self.btn_connect.pack(side="left", padx=5)
        
        self.btn_refresh = tk.Button(conn_frame, text="🔄", width=3,
                                    bg=COLORS['accent'], fg=COLORS['text'],
                                    command=self._refresh_ports)
        self.btn_refresh.pack(side="left", padx=5)
        
        self.lbl_status = tk.Label(self, text="⚫ Desconectado",
                                   bg=COLORS['bg'], fg=COLORS['text_sec'])
        self.lbl_status.pack(pady=5)
        
        tk.Frame(self, height=2, bg=COLORS['accent']).pack(fill="x", padx=15, pady=10)
        
        # Velocidad
        tk.Label(self, text="VELOCIDAD", font=("Arial", 12, "bold"),
                bg=COLORS['bg'], fg=COLORS['text']).pack()
        
        self.speed_var = tk.IntVar(value=0)
        self.speed_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL,
                                     length=300, variable=self.speed_var,
                                     bg=COLORS['card'], fg=COLORS['text'],
                                     highlightthickness=0,
                                     command=self._on_speed_change)
        self.speed_slider.pack(pady=10)
        
        self.lbl_speed = tk.Label(self, text="0%", font=("Arial", 24, "bold"),
                                  bg=COLORS['bg'], fg=COLORS['accent'])
        self.lbl_speed.pack()
        
        # Botones presets
        preset_frame = tk.Frame(self, bg=COLORS['bg'])
        preset_frame.pack(pady=10)
        for pct in [0, 15, 30, 50, 75, 100]:
            btn = tk.Button(preset_frame, text=f"{pct}%", width=4,
                          bg=COLORS['card'], fg=COLORS['text'],
                          command=lambda v=pct: self._set_preset(v))
            btn.pack(side="left", padx=2)
        
        # Direccion
        tk.Label(self, text="DIRECCION", font=("Arial", 12, "bold"),
                bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(15, 5))
        
        self.lbl_direction = tk.Label(self, text="▶  ADELANTE",
                                     font=("Arial", 16, "bold"),
                                     bg=COLORS['bg'], fg=COLORS['fwd'])
        self.lbl_direction.pack()
        
        self.btn_invert = tk.Button(self, text="⇄  INVERTIR GIRO", width=20,
                                   bg=COLORS['accent'], fg=COLORS['text'],
                                   font=("Arial", 10, "bold"),
                                   command=self._invert_direction)
        self.btn_invert.pack(pady=10)
        
        # Stop
        self.btn_stop = tk.Button(self, text="■  STOP  ■", width=20,
                                 bg=COLORS['stop'], fg="black",
                                 font=("Arial", 12, "bold"),
                                 command=self._stop_motor)
        self.btn_stop.pack(pady=10)
        
        # Log
        log_frame = tk.LabelFrame(self, text=" Comunicacion ",
                                  bg=COLORS['card'], fg=COLORS['text'])
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.log_text = tk.Text(log_frame, height=6,
                                bg=COLORS['bg'], fg=COLORS['text'],
                                font=("Consolas", 8),
                                wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Button(log_frame, text="Limpiar", width=8,
                 bg=COLORS['accent'], fg=COLORS['text'],
                 command=self._clear_log).pack(pady=5)
    
    def _log(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
    
    def _refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
    
    def _toggle_connect(self):
        if self.connected:
            self._disconnect()
        else:
            self._connect()
    
    def _connect(self):
        port = self.port_combo.get()
        if not port:
            messagebox.showerror("Error", "Selecciona un puerto")
            return
        
        try:
            self.serial = serial.Serial(port, 115200, timeout=0.1)
            time.sleep(2)
            self.connected = True
            self.btn_connect.config(text="Desconectar", bg=COLORS['rev'])
            self.lbl_status.config(text=f"🟢 Conectado a {port}", fg=COLORS['fwd'])
            self._log(f"Conectado a {port}")
            
            # Leer bienvenida
            time.sleep(0.3)
            while self.serial.in_waiting:
                self._log(f"← {self.serial.readline().decode().strip()}")
            
            self._send_command()
            
            # Iniciar lector
            self.reader_thread = threading.Thread(target=self._reader, daemon=True)
            self.reader_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _reader(self):
        while self.connected and self.serial:
            try:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode().strip()
                    if line:
                        self.after(0, self._log, f"← {line}")
            except:
                break
            time.sleep(0.01)
    
    def _disconnect(self):
        self.connected = False
        if self.serial:
            self.serial.close()
        self.btn_connect.config(text="Conectar", bg=COLORS['fwd'])
        self.lbl_status.config(text="⚫ Desconectado", fg=COLORS['text_sec'])
        self._log("Desconectado")
    
    def _send_command(self):
        if not self.connected or not self.serial:
            return
        cmd = f"{self.direction}{self.current_speed}\n"
        try:
            self.serial.write(cmd.encode())
            self._log(f"→ {cmd.strip()}")
        except:
            self._disconnect()
    
    def _on_speed_change(self, value):
        self.current_speed = int(value)
        self.lbl_speed.config(text=f"{self.current_speed}%")
        # Envio inmediato sin delay
        self._send_command()
    
    def _set_preset(self, value):
        self.speed_slider.set(value)
        self.current_speed = value
        self.lbl_speed.config(text=f"{value}%")
        self._send_command()
    
    def _invert_direction(self):
        if self.direction == "F":
            self.direction = "B"
            self.lbl_direction.config(text="◀  ATRAS", fg=COLORS['rev'])
        else:
            self.direction = "F"
            self.lbl_direction.config(text="▶  ADELANTE", fg=COLORS['fwd'])
        self._send_command()
        self._log(f"Direccion: {'ADELANTE' if self.direction == 'F' else 'ATRAS'}")
    
    def _stop_motor(self):
        if not self.connected:
            return
        try:
            self.serial.write(b"S\n")
            self._log("→ STOP")
            self.speed_slider.set(0)
            self.current_speed = 0
            self.lbl_speed.config(text="0%")
        except:
            pass

if __name__ == "__main__":
    app = MotorApp()
    app.mainloop()