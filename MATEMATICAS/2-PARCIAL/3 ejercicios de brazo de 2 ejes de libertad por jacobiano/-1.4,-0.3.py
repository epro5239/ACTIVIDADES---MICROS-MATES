import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d
import matplotlib.patches as patches

# ============================================================
# CONFIGURACIÓN DE ESTILO PROFESIONAL
# ============================================================
plt.style.use('dark_background')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10


# ============================================================
# CLASE PARA EL BRAZO ROBÓTICO
# ============================================================
class BrazoRobotico:
    def __init__(self, z1=1, z2=1):
        self.z1 = z1  # Longitud brazo 1
        self.z2 = z2  # Longitud brazo 2
        self.historial_angulos = []  # Para guardar trayectorias
        
    def cinematica_directa(self, theta1, theta2):
        """Calcula posición del efector dados los ángulos"""
        x = self.z1 * np.cos(theta1) + self.z2 * np.cos(theta1 + theta2)
        y = self.z1 * np.sin(theta1) + self.z2 * np.sin(theta1 + theta2)
        return x, y
    
    def cinematica_inversa(self, x_obj, y_obj, configuracion='arriba', tol=1e-4):
        """
        Resuelve cinemática inversa con Newton-Raphson
        configuracion: 'arriba' (θ₂ positivo) o 'abajo' (θ₂ negativo)
        """
        # Verificar alcanzabilidad
        r = np.sqrt(x_obj**2 + y_obj**2)
        if r > self.z1 + self.z2:
            print(f"⚠️  Punto ({x_obj}, {y_obj}) fuera de alcance (r={r:.2f} > {self.z1+self.z2})")
            return None, None
        
        # Ley de cosenos para estimar θ₂
        cos_theta2 = (r**2 - self.z1**2 - self.z2**2) / (2 * self.z1 * self.z2)
        cos_theta2 = np.clip(cos_theta2, -1, 1)
        
        # Elegir signo según configuración
        if configuracion == 'arriba':
            theta2_est = np.arccos(cos_theta2)
        else:
            theta2_est = -np.arccos(cos_theta2)
        
        # Estimar θ₁
        phi = np.arctan2(y_obj, x_obj)
        if r > 0:
            alpha = np.arccos((self.z1**2 + r**2 - self.z2**2) / (2 * self.z1 * r))
            if configuracion == 'arriba':
                theta1_est = phi - alpha
            else:
                theta1_est = phi + alpha
        else:
            theta1_est = 0
        
        # Funciones para Newton-Raphson
        def f(theta1, theta2):
            f1 = self.z1*np.cos(theta1) + self.z2*np.cos(theta1 + theta2) - x_obj
            f2 = self.z1*np.sin(theta1) + self.z2*np.sin(theta1 + theta2) - y_obj
            return np.array([f1, f2])
        
        def jacobian(theta1, theta2):
            J = np.array([[-self.z1*np.sin(theta1) - self.z2*np.sin(theta1 + theta2), 
                           -self.z2*np.sin(theta1 + theta2)],
                          [self.z1*np.cos(theta1) + self.z2*np.cos(theta1 + theta2), 
                           self.z2*np.cos(theta1 + theta2)]])
            return J
        
        # Newton-Raphson
        x = np.array([theta1_est, theta2_est])
        historial = [x.copy()]
        
        for i in range(50):
            F = f(x[0], x[1])
            J = jacobian(x[0], x[1])
            
            try:
                delta = np.linalg.solve(J, -F)
            except:
                break
            
            x = x + delta
            historial.append(x.copy())
            
            if np.linalg.norm(delta) < tol:
                return x, historial
        
        return x, historial
    
    def generar_trayectoria_suave(self, theta_inicial, theta_final, num_frames=200):
        """
        Genera una trayectoria suave entre dos configuraciones
        usando interpolación lineal (CORREGIDO)
        """
        t = np.linspace(0, 1, num_frames)
        
        # INTERPOLACIÓN LINEAL - Siempre funciona
        theta1_tray = theta_inicial[0] + (theta_final[0] - theta_inicial[0]) * t
        theta2_tray = theta_inicial[1] + (theta_final[1] - theta_inicial[1]) * t
        
        return np.column_stack([theta1_tray, theta2_tray])


# ============================================================
# VISUALIZACIÓN 2D CON ANIMACIÓN FLUIDA
# ============================================================
class Visualizador2D:
    def __init__(self, brazo):
        self.brazo = brazo
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#1a1a1a')
        
        # Variables para la animación
        self.trayectoria = None
        self.anim = None
        self.punto_objetivo = (-1, -0.5)
        self.config_actual = 'arriba'
        
    def configurar_escena(self):
        """Configura los elementos estáticos de la escena"""
        self.ax.clear()
        
        # Límites
        self.ax.set_xlim(-2.2, 2.2)
        self.ax.set_ylim(-2.2, 2.2)
        self.ax.set_aspect('equal')
        
        # Cuadrícula
        self.ax.grid(True, alpha=0.2, linestyle='--')
        self.ax.axhline(y=0, color='#666666', linewidth=0.5)
        self.ax.axvline(x=0, color='#666666', linewidth=0.5)
        
        # Círculo de alcance máximo
        theta = np.linspace(0, 2*np.pi, 100)
        self.ax.plot(2*np.cos(theta), 2*np.sin(theta), '--', 
                    color='#444444', linewidth=1.5, alpha=0.5)
        
        # Punto objetivo
        x_obj, y_obj = self.punto_objetivo
        self.ax.scatter([x_obj], [y_obj], c='red', s=300, 
                       marker='X', edgecolors='white', linewidth=2,
                       zorder=10, label='Objetivo')
        
        # Elementos que se actualizarán
        self.brazo1_line, = self.ax.plot([], [], 'c-', linewidth=6, 
                                         solid_capstyle='round', label='Brazo 1')
        self.brazo2_line, = self.ax.plot([], [], 'm-', linewidth=6,
                                         solid_capstyle='round', label='Brazo 2')
        
        # Articulaciones
        self.base_point = self.ax.scatter([0], [0], c='white', s=200,
                                         edgecolors='cyan', linewidth=2, zorder=10)
        self.articulacion_point = self.ax.scatter([], [], c='yellow', s=150,
                                                 edgecolors='orange', linewidth=2, zorder=10)
        self.efector_point = self.ax.scatter([], [], c='lime', s=250,
                                            edgecolors='white', linewidth=2, 
                                            marker='*', zorder=10)
        
        # Estela del movimiento
        self.estela_scatter = self.ax.scatter([], [], c=[], cmap='viridis',
                                             s=30, alpha=0.6, zorder=5)
        
        # Texto informativo
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                      color='white', fontsize=10, verticalalignment='top',
                                      bbox=dict(boxstyle="round,pad=0.3", 
                                               facecolor='#333333', alpha=0.8))
        
        self.ax.legend(loc='upper right', facecolor='#333333', edgecolor='white')
        
    def animar_movimiento(self, theta_inicial, theta_final, num_frames=200):
        """
        Anima el movimiento desde theta_inicial hasta theta_final
        con interpolación suave
        """
        self.configurar_escena()
        
        # Generar trayectoria suave
        trayectoria = self.brazo.generar_trayectoria_suave(theta_inicial, theta_final, num_frames)
        self.trayectoria = trayectoria
        
        # Pre-calcular posiciones para la estela
        posiciones_efector = []
        for th1, th2 in trayectoria:
            x, y = self.brazo.cinematica_directa(th1, th2)
            posiciones_efector.append([x, y])
        self.posiciones_efector = np.array(posiciones_efector)
        
        def update(frame):
            # Ángulos actuales
            theta1, theta2 = trayectoria[frame]
            
            # Posiciones
            x1 = self.brazo.z1 * np.cos(theta1)
            y1 = self.brazo.z1 * np.sin(theta1)
            x2, y2 = self.brazo.cinematica_directa(theta1, theta2)
            
            # Actualizar brazos
            self.brazo1_line.set_data([0, x1], [0, y1])
            self.brazo2_line.set_data([x1, x2], [y1, y2])
            
            # Actualizar articulaciones
            self.articulacion_point.set_offsets([[x1, y1]])
            self.efector_point.set_offsets([[x2, y2]])
            
            # Actualizar estela (últimos 50 puntos)
            inicio = max(0, frame - 50)
            estela_x = self.posiciones_efector[inicio:frame+1, 0]
            estela_y = self.posiciones_efector[inicio:frame+1, 1]
            if len(estela_x) > 0:
                self.estela_scatter.set_offsets(np.column_stack([estela_x, estela_y]))
                # Colores por tiempo
                colors = np.linspace(0, 1, len(estela_x))
                self.estela_scatter.set_array(colors)
            
            # Actualizar texto
            x_obj, y_obj = self.punto_objetivo
            error = np.sqrt((x2 - x_obj)**2 + (y2 - y_obj)**2)
            self.info_text.set_text(
                f'Frame: {frame}/{len(trayectoria)-1}\n'
                f'θ₁ = {np.degrees(theta1):.2f}°\n'
                f'θ₂ = {np.degrees(theta2):.2f}°\n'
                f'Error = {error:.2e}'
            )
            
            return (self.brazo1_line, self.brazo2_line, self.articulacion_point,
                    self.efector_point, self.estela_scatter, self.info_text)
        
        self.anim = FuncAnimation(self.fig, update, frames=len(trayectoria),
                                 interval=20, blit=True, repeat=True)
        plt.show()
        
        return self.anim


# ============================================================
# VISUALIZACIÓN 3D CON ANIMACIÓN FLUIDA
# ============================================================
class Visualizador3D:
    def __init__(self, brazo):
        self.brazo = brazo
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#1a1a1a')
        
        # Configuración 3D
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('#333333')
        self.ax.yaxis.pane.set_edgecolor('#333333')
        self.ax.zaxis.pane.set_edgecolor('#333333')
        
        # Mejorar la visualización 3D
        self.ax.xaxis.pane.set_alpha(0.3)
        self.ax.yaxis.pane.set_alpha(0.3)
        self.ax.zaxis.pane.set_alpha(0.3)
        
        self.punto_objetivo = (-1, -0.5)
        self.anim = None
        
    def configurar_escena(self):
        """Configura elementos estáticos 3D"""
        self.ax.clear()
        
        # Límites con un poco de espacio extra
        self.ax.set_xlim(-2.5, 2.5)
        self.ax.set_ylim(-2.5, 2.5)
        self.ax.set_zlim(-0.5, 2.5)
        
        # Etiquetas con colores claros
        self.ax.set_xlabel('X', color='white', fontsize=12, labelpad=10)
        self.ax.set_ylabel('Y', color='white', fontsize=12, labelpad=10)
        self.ax.set_zlabel('Z', color='white', fontsize=12, labelpad=10)
        
        # Configurar ticks con color blanco
        self.ax.tick_params(colors='white', labelsize=8)
        
        # Plano de referencia (semi-transparente)
        xx, yy = np.meshgrid(np.linspace(-2.5, 2.5, 20), 
                            np.linspace(-2.5, 2.5, 20))
        zz = np.zeros_like(xx)
        self.ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray', edgecolor='none')
        
        # Círculo de alcance en 3D
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = 2 * np.cos(theta)
        y_circle = 2 * np.sin(theta)
        z_circle = np.zeros_like(theta)
        self.ax.plot(x_circle, y_circle, z_circle, '--',
                    color='#444444', linewidth=1.5, alpha=0.5, label='Alcance máximo')
        
        # Líneas de los ejes
        self.ax.plot([-2.5, 2.5], [0, 0], [0, 0], 'w-', alpha=0.2, linewidth=0.5)
        self.ax.plot([0, 0], [-2.5, 2.5], [0, 0], 'w-', alpha=0.2, linewidth=0.5)
        
        # Punto objetivo (estático)
        x_obj, y_obj = self.punto_objetivo
        self.ax.scatter([x_obj], [y_obj], [0], c='red', s=300,
                       marker='X', edgecolors='white', linewidth=2, 
                       label='Objetivo', alpha=0.9, zorder=20)
        
        # Elementos animados (inicialmente vacíos)
        self.brazo1_line, = self.ax.plot([], [], [], 'c-', linewidth=8, 
                                         solid_capstyle='round', label='Brazo 1')
        self.brazo2_line, = self.ax.plot([], [], [], 'm-', linewidth=8,
                                         solid_capstyle='round', label='Brazo 2')
        
        # Puntos de las articulaciones
        self.base_point = self.ax.scatter([0], [0], [0], c='white', s=300,
                                         edgecolors='cyan', linewidth=2, 
                                         label='Base', zorder=15)
        
        self.articulacion_point = self.ax.scatter([], [], [], c='yellow', s=250,
                                                 edgecolors='orange', linewidth=2,
                                                 label='Articulación', zorder=15)
        
        self.efector_point = self.ax.scatter([], [], [], c='lime', s=350,
                                            edgecolors='white', linewidth=2, 
                                            marker='*', label='Efector', zorder=15)
        
        # Estela (puntos del camino recorrido)
        self.estela_scatter = self.ax.scatter([], [], [], c=[], cmap='viridis',
                                             s=50, alpha=0.6, zorder=5)
        
        # Texto informativo en 3D (posicionado en el espacio 3D)
        self.info_text = self.ax.text2D(0.02, 0.95, '', transform=self.ax.transAxes,
                                        color='white', fontsize=10, 
                                        verticalalignment='top',
                                        bbox=dict(boxstyle="round,pad=0.3", 
                                                 facecolor='#333333', alpha=0.9,
                                                 edgecolor='white'))
        
        # Leyenda
        self.ax.legend(loc='upper right', facecolor='#333333', 
                      edgecolor='white', labelcolor='white')
        
        # Ángulo de vista inicial
        self.ax.view_init(elev=25, azim=-60)
        
    def animar_movimiento(self, theta_inicial, theta_final, num_frames=200):
        """Animación 3D suave - CORREGIDA"""
        self.configurar_escena()
        
        # Generar trayectoria
        trayectoria = self.brazo.generar_trayectoria_suave(theta_inicial, theta_final, num_frames)
        
        # Pre-calcular todas las posiciones para eficiencia
        n_frames = len(trayectoria)
        posiciones = np.zeros((n_frames, 4))  # x1, y1, x2, y2
        
        for i, (th1, th2) in enumerate(trayectoria):
            x1 = self.brazo.z1 * np.cos(th1)
            y1 = self.brazo.z1 * np.sin(th1)
            x2, y2 = self.brazo.cinematica_directa(th1, th2)
            posiciones[i] = [x1, y1, x2, y2]
        
        def update(frame):
            # Obtener posición actual
            x1, y1, x2, y2 = posiciones[frame]
            
            # Actualizar brazos (necesita 3 coordenadas)
            self.brazo1_line.set_data([0, x1], [0, y1])
            self.brazo1_line.set_3d_properties([0, 0])
            
            self.brazo2_line.set_data([x1, x2], [y1, y2])
            self.brazo2_line.set_3d_properties([0, 0])
            
            # Actualizar articulaciones
            self.articulacion_point._offsets3d = ([x1], [y1], [0])
            self.efector_point._offsets3d = ([x2], [y2], [0])
            
            # Actualizar estela (últimos 30 puntos para no saturar)
            inicio = max(0, frame - 30)
            estela_x = posiciones[inicio:frame+1, 2]  # x del efector
            estela_y = posiciones[inicio:frame+1, 3]  # y del efector
            estela_z = [0] * len(estela_x)
            
            if len(estela_x) > 0:
                self.estela_scatter._offsets3d = (estela_x, estela_y, estela_z)
                # Colores basados en el progreso
                colors = np.linspace(0, 1, len(estela_x))
                self.estela_scatter.set_array(colors)
            
            # Calcular error actual
            x_obj, y_obj = self.punto_objetivo
            error = np.sqrt((x2 - x_obj)**2 + (y2 - y_obj)**2)
            
            # Actualizar texto
            th1, th2 = trayectoria[frame]
            self.info_text.set_text(
                f'Frame: {frame}/{n_frames-1}\n'
                f'θ₁ = {np.degrees(th1):.2f}°\n'
                f'θ₂ = {np.degrees(th2):.2f}°\n'
                f'Error = {error:.2e}'
            )
            
            # Rotar la vista lentamente para mejor efecto
            if frame % 2 == 0:  # Cada 2 frames
                azim_actual = -60 + (frame / n_frames) * 30  # Gira 30°
                self.ax.view_init(elev=25, azim=azim_actual)
            
            # Forzar actualización de la figura
            self.fig.canvas.draw_idle()
            
            return (self.brazo1_line, self.brazo2_line, 
                    self.articulacion_point, self.efector_point,
                    self.estela_scatter, self.info_text)
        
        # Crear animación con blit=False para 3D (importante)
        self.anim = FuncAnimation(self.fig, update, frames=len(trayectoria),
                                 interval=30, blit=False, repeat=True)
        
        plt.tight_layout()
        plt.show()
        
        return self.anim
# ============================================================
# INTERFAZ INTERACTIVA CON SLIDER
# ============================================================
class SimuladorInteractivo:
    def __init__(self):
        self.brazo = BrazoRobotico()
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Punto objetivo inicial
        self.x_obj, self.y_obj = -1, -0.5
        self.configuracion = 'arriba'
        
        # Resolver configuración inicial
        self.solucion_actual, _ = self.brazo.cinematica_inversa(
            self.x_obj, self.y_obj, self.configuracion)
        
        self.setup_ui()
        self.anim = None
        
    def setup_ui(self):
        """Configura la interfaz con sliders"""
        plt.subplots_adjust(bottom=0.25)
        
        # Slider para X
        ax_x = plt.axes([0.2, 0.15, 0.6, 0.03])
        self.slider_x = Slider(ax_x, 'X objetivo', -2, 2, 
                               valinit=self.x_obj, valstep=0.01,
                               color='cyan')
        
        # Slider para Y
        ax_y = plt.axes([0.2, 0.1, 0.6, 0.03])
        self.slider_y = Slider(ax_y, 'Y objetivo', -2, 2,
                               valinit=self.y_obj, valstep=0.01,
                               color='magenta')
        
        # Botones de configuración
        ax_arriba = plt.axes([0.2, 0.05, 0.2, 0.04])
        self.boton_arriba = Button(ax_arriba, 'Codo Arriba', color='#333333')
        self.boton_arriba.on_clicked(lambda x: self.cambiar_config('arriba'))
        
        ax_abajo = plt.axes([0.6, 0.05, 0.2, 0.04])
        self.boton_abajo = Button(ax_abajo, 'Codo Abajo', color='#333333')
        self.boton_abajo.on_clicked(lambda x: self.cambiar_config('abajo'))
        
        # Conectar sliders
        self.slider_x.on_changed(self.actualizar_punto)
        self.slider_y.on_changed(self.actualizar_punto)
        
        # Dibujar estado inicial
        self.dibujar_brazo()
        
    def dibujar_brazo(self):
        """Dibuja el brazo en su configuración actual"""
        self.ax.clear()
        
        if self.solucion_actual is None:
            self.ax.text(0, 0, 'Punto inalcanzable', color='red', 
                        ha='center', va='center', fontsize=16)
        else:
            theta1, theta2 = self.solucion_actual
            x1 = self.brazo.z1 * np.cos(theta1)
            y1 = self.brazo.z1 * np.sin(theta1)
            x2, y2 = self.brazo.cinematica_directa(theta1, theta2)
            
            # Dibujar brazos
            self.ax.plot([0, x1], [0, y1], 'c-', linewidth=6, label='Brazo 1')
            self.ax.plot([x1, x2], [y1, y2], 'm-', linewidth=6, label='Brazo 2')
            
            # Articulaciones
            self.ax.scatter([0], [0], c='white', s=200, edgecolors='cyan')
            self.ax.scatter([x1], [y1], c='yellow', s=150, edgecolors='orange')
            self.ax.scatter([x2], [y2], c='lime', s=250, edgecolors='white', marker='*')
            
            # Texto de ángulos
            self.ax.text(x1/2, y1/2, f'θ₁={np.degrees(theta1):.1f}°',
                        bbox=dict(boxstyle="round", facecolor='#333333', alpha=0.8))
            self.ax.text(x1 + (x2-x1)/2, y1 + (y2-y1)/2, f'θ₂={np.degrees(theta2):.1f}°',
                        bbox=dict(boxstyle="round", facecolor='#333333', alpha=0.8))
        
        # Punto objetivo
        self.ax.scatter([self.x_obj], [self.y_obj], c='red', s=300,
                       marker='X', edgecolors='white', linewidth=2)
        
        # Configuración de escena
        self.ax.set_xlim(-2.2, 2.2)
        self.ax.set_ylim(-2.2, 2.2)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2)
        self.ax.axhline(0, color='#666666', linewidth=0.5)
        self.ax.axvline(0, color='#666666', linewidth=0.5)
        
        # Círculo de alcance
        theta = np.linspace(0, 2*np.pi, 100)
        self.ax.plot(2*np.cos(theta), 2*np.sin(theta), '--', 
                    color='#444444', alpha=0.5)
        
        self.ax.set_title(f'Configuración: {self.configuracion}', color='white')
        self.ax.legend()
        self.fig.canvas.draw()
        
    def actualizar_punto(self, val):
        """Actualiza cuando cambia el punto objetivo"""
        self.x_obj = self.slider_x.val
        self.y_obj = self.slider_y.val
        
        self.solucion_actual, _ = self.brazo.cinematica_inversa(
            self.x_obj, self.y_obj, self.configuracion)
        
        self.dibujar_brazo()
        
    def cambiar_config(self, config):
        """Cambia entre codo arriba/abajo"""
        self.configuracion = config
        self.solucion_actual, _ = self.brazo.cinematica_inversa(
            self.x_obj, self.y_obj, self.configuracion)
        self.dibujar_brazo()


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================
def main():
    print("=" * 70)
    print("🤖 SIMULADOR DE BRAZO ROBÓTICO DE 2 ESLABONES")
    print("=" * 70)
    
    # Crear brazo
    brazo = BrazoRobotico(z1=1, z2=1)
    
    # Punto objetivo
    x_obj, y_obj = -1.4, -0.3
    print(f"\n🎯 Punto objetivo: ({x_obj}, {y_obj})")
    
    # Resolver para ambas configuraciones
    print("\n🔍 Resolviendo cinemática inversa...")
    
    sol_arriba, hist_arriba = brazo.cinematica_inversa(x_obj, y_obj, 'arriba')
    sol_abajo, hist_abajo = brazo.cinematica_inversa(x_obj, y_obj, 'abajo')
    
    if sol_arriba is not None:
        print(f"\n✅ Configuración CODO ARRIBA:")
        print(f"   θ₁ = {np.degrees(sol_arriba[0]):.4f}°")
        print(f"   θ₂ = {np.degrees(sol_arriba[1]):.4f}°")
    
    if sol_abajo is not None:
        print(f"\n✅ Configuración CODO ABAJO:")
        print(f"   θ₁ = {np.degrees(sol_abajo[0]):.4f}°")
        print(f"   θ₂ = {np.degrees(sol_abajo[1]):.4f}°")
    
    # Ángulos iniciales (0°, 0°)
    theta_inicial = [0, 0]
    
    print("\n" + "="*70)
    print("🎬 INICIANDO ANIMACIONES 2D Y 3D")
    print("="*70)
    print("\n📌 Las animaciones mostrarán:")
    print("   • Brazo partiendo de 0°, 0°")
    print("   • Movimiento SUAVE y FLUIDO (200 frames)")
    print("   • Estela del movimiento")
    print("   • Información en tiempo real")
    
    # ANIMACIÓN 2D - Configuración arriba
    if sol_arriba is not None:
        print("\n🖥️  Mostrando animación 2D (Codo arriba)...")
        visor2d = Visualizador2D(brazo)
        visor2d.punto_objetivo = (x_obj, y_obj)
        visor2d.animar_movimiento(theta_inicial, sol_arriba, num_frames=200)
    
    # ANIMACIÓN 3D - Configuración arriba
    if sol_arriba is not None:
        print("\n🖥️  Mostrando animación 3D (Codo arriba)...")
        visor3d = Visualizador3D(brazo)
        visor3d.punto_objetivo = (x_obj, y_obj)
        visor3d.animar_movimiento(theta_inicial, sol_arriba, num_frames=200)
    
    # ANIMACIÓN 2D - Configuración abajo
    if sol_abajo is not None:
        print("\n🖥️  Mostrando animación 2D (Codo abajo)...")
        visor2d = Visualizador2D(brazo)
        visor2d.punto_objetivo = (x_obj, y_obj)
        visor2d.configuracion = 'abajo'
        visor2d.animar_movimiento(theta_inicial, sol_abajo, num_frames=200)
    
    # ANIMACIÓN 3D - Configuración abajo
    if sol_abajo is not None:
        print("\n🖥️  Mostrando animación 3D (Codo abajo)...")
        visor3d = Visualizador3D(brazo)
        visor3d.punto_objetivo = (x_obj, y_obj)
        visor3d.animar_movimiento(theta_inicial, sol_abajo, num_frames=200)
    
    # SIMULADOR INTERACTIVO
    print("\n" + "="*70)
    print("🎮 INICIANDO SIMULADOR INTERACTIVO")
    print("="*70)
    print("\n📌 Usa los sliders para cambiar el punto objetivo")
    print("   • Slider X: mover punto en horizontal")
    print("   • Slider Y: mover punto en vertical")
    print("   • Botones: cambiar entre codo arriba/abajo")
    
    simulador = SimuladorInteractivo()
    plt.show()


# ============================================================
# RESPUESTA A LA PREGUNTA
# ============================================================
"""
📝 RESPUESTA: ¿Se puede cambiar el punto objetivo?

¡SÍ! Hay DOS formas de cambiar el punto objetivo:

1️⃣ EN EL CÓDIGO (estático):
   - Modifica las variables x_obj, y_obj en la función main()
   - Ejemplo: x_obj, y_obj = 1.5, 1.0

2️⃣ INTERACTIVO (en tiempo real):
   - Ejecuta el SimuladorInteractivo() al final
   - Usa los sliders para cambiar X e Y
   - El brazo se actualiza instantáneamente
   - Prueba diferentes configuraciones

⚠️ NOTA: El punto debe estar dentro del círculo de radio 2
   para ser alcanzable. El simulador te avisará si no lo es.
"""

if __name__ == "__main__":
    main()