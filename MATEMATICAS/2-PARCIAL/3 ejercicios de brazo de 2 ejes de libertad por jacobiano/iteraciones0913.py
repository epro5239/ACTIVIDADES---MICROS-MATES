import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D

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
        self.z1 = z1
        self.z2 = z2
        
    def cinematica_directa(self, theta1, theta2):
        x = self.z1 * np.cos(theta1) + self.z2 * np.cos(theta1 + theta2)
        y = self.z1 * np.sin(theta1) + self.z2 * np.sin(theta1 + theta2)
        return x, y
    
    def cinematica_inversa(self, x_obj, y_obj, configuracion='arriba', tol=1e-4):
        # Verificar alcanzabilidad
        r = np.sqrt(x_obj**2 + y_obj**2)
        if r > self.z1 + self.z2:
            print(f"⚠️  Punto ({x_obj}, {y_obj}) fuera de alcance")
            return None, None
        
        # ÁNGULOS INICIALES - EVITANDO SINGULARIDAD
        theta1_est = 0.1  # ~5.73 grados
        theta2_est = 0.1  # ~5.73 grados
        
        if configuracion == 'abajo':
            theta2_est = -0.1
        
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
        
        x = np.array([theta1_est, theta2_est])
        historial = [x.copy()]
        
        print(f"\n🔍 {configuracion.upper()} - Iteraciones:")
        print("-" * 70)
        print("Iter |     θ₁°     |     θ₂°     |    ||Δθ||    |    ||f||")
        print("-" * 70)
        
        for i in range(50):
            F = f(x[0], x[1])
            J = jacobian(x[0], x[1])
            
            det = np.linalg.det(J)
            if abs(det) < 1e-10:
                x = x + np.array([0.01, 0.01])
                continue
            
            try:
                delta = np.linalg.solve(J, -F)
            except:
                x = x + np.array([0.05, 0.05])
                continue
            
            x_nuevo = x + delta
            historial.append(x_nuevo.copy())
            
            norm_delta = np.linalg.norm(delta)
            norm_f = np.linalg.norm(F)
            
            print(f"{i+1:4d} | {np.degrees(x_nuevo[0]):9.4f} | {np.degrees(x_nuevo[1]):9.4f} | {norm_delta:.2e} | {norm_f:.2e}")
            
            if norm_delta < tol:
                print("-" * 70)
                print(f"✅ Convergencia en {i+1} iteraciones")
                return x_nuevo, historial
            
            x = x_nuevo
        
        return x, historial
    
    def generar_trayectoria_suave(self, historial, num_frames=100):
        """Genera una trayectoria suave entre las iteraciones del historial"""
        if len(historial) < 2:
            return np.array(historial)
        
        t_orig = np.linspace(0, 1, len(historial))
        t_suave = np.linspace(0, 1, num_frames)
        
        theta1_suave = np.interp(t_suave, t_orig, [h[0] for h in historial])
        theta2_suave = np.interp(t_suave, t_orig, [h[1] for h in historial])
        
        return np.column_stack([theta1_suave, theta2_suave])


# ============================================================
# VISUALIZACIÓN 2D CON ANIMACIÓN DE ITERACIONES
# ============================================================
class Visualizador2D:
    def __init__(self, brazo):
        self.brazo = brazo
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#1a1a1a')
        
        self.anim = None
        self.punto_objetivo = (-1, -0.5)
        self.historial = None
        self.trayectoria_suave = None
        
    def configurar_escena(self):
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
                    color='#444444', linewidth=1.5, alpha=0.5, label='Alcance máximo')
        
        # Punto objetivo
        x_obj, y_obj = self.punto_objetivo
        self.ax.scatter([x_obj], [y_obj], c='red', s=300, 
                       marker='X', edgecolors='white', linewidth=2,
                       zorder=10, label='Objetivo')
        
        # Elementos animados
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
        
        # Estela de todas las iteraciones
        self.estela_scatter = self.ax.scatter([], [], c=[], cmap='viridis',
                                             s=50, alpha=0.7, zorder=5,
                                             label='Iteraciones')
        
        # Texto informativo
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                      color='white', fontsize=10, verticalalignment='top',
                                      bbox=dict(boxstyle="round,pad=0.3", 
                                               facecolor='#333333', alpha=0.8))
        
        self.ax.legend(loc='upper right', facecolor='#333333', edgecolor='white')
        
    def animar_iteraciones(self, historial, config_nombre):
        """Anima el brazo siguiendo las iteraciones del historial"""
        self.historial = historial
        self.configurar_escena()
        
        # Generar trayectoria suave para animación fluida
        self.trayectoria_suave = self.brazo.generar_trayectoria_suave(historial, num_frames=200)
        
        # Pre-calcular posiciones del efector para cada frame
        n_frames = len(self.trayectoria_suave)
        posiciones_efector = []
        posiciones_articulacion = []
        
        for th1, th2 in self.trayectoria_suave:
            x1 = self.brazo.z1 * np.cos(th1)
            y1 = self.brazo.z1 * np.sin(th1)
            x2, y2 = self.brazo.cinematica_directa(th1, th2)
            posiciones_articulacion.append([x1, y1])
            posiciones_efector.append([x2, y2])
        
        self.posiciones_articulacion = np.array(posiciones_articulacion)
        self.posiciones_efector = np.array(posiciones_efector)
        
        # Pre-calcular posiciones de las iteraciones reales para la estela
        self.estela_posiciones = []
        for th1, th2 in historial:
            x2, y2 = self.brazo.cinematica_directa(th1, th2)
            self.estela_posiciones.append([x2, y2])
        self.estela_posiciones = np.array(self.estela_posiciones)
        
        def update(frame):
            # Ángulos actuales del frame suave
            theta1, theta2 = self.trayectoria_suave[frame]
            
            # Posiciones actuales
            x1 = self.brazo.z1 * np.cos(theta1)
            y1 = self.brazo.z1 * np.sin(theta1)
            x2, y2 = self.brazo.cinematica_directa(theta1, theta2)
            
            # Actualizar brazos
            self.brazo1_line.set_data([0, x1], [0, y1])
            self.brazo2_line.set_data([x1, x2], [y1, y2])
            
            # Actualizar articulaciones
            self.articulacion_point.set_offsets([[x1, y1]])
            self.efector_point.set_offsets([[x2, y2]])
            
            # Actualizar estela (todas las iteraciones hasta ahora)
            progreso = frame / len(self.trayectoria_suave)
            num_iteraciones_mostrar = int(progreso * len(self.estela_posiciones))
            
            if num_iteraciones_mostrar > 0:
                estela_x = self.estela_posiciones[:num_iteraciones_mostrar, 0]
                estela_y = self.estela_posiciones[:num_iteraciones_mostrar, 1]
                self.estela_scatter.set_offsets(np.column_stack([estela_x, estela_y]))
                
                # Colorear por orden de iteración
                colors = np.linspace(0, 1, num_iteraciones_mostrar)
                self.estela_scatter.set_array(colors)
            
            # Actualizar texto
            x_obj, y_obj = self.punto_objetivo
            error = np.sqrt((x2 - x_obj)**2 + (y2 - y_obj)**2)
            self.info_text.set_text(
                f'Config: {config_nombre}\n'
                f'Frame: {frame}/{len(self.trayectoria_suave)-1}\n'
                f'θ₁ = {np.degrees(theta1):.2f}°\n'
                f'θ₂ = {np.degrees(theta2):.2f}°\n'
                f'Error = {error:.2e}'
            )
            
            return (self.brazo1_line, self.brazo2_line, self.articulacion_point,
                    self.efector_point, self.estela_scatter, self.info_text)
        
        self.anim = FuncAnimation(self.fig, update, frames=len(self.trayectoria_suave),
                                 interval=50, blit=True, repeat=True)
        plt.show()
        
        return self.anim


# ============================================================
# VISUALIZACIÓN 3D CON ANIMACIÓN DE ITERACIONES
# ============================================================
class Visualizador3D:
    def __init__(self, brazo):
        self.brazo = brazo
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#1a1a1a')
        
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('#333333')
        self.ax.yaxis.pane.set_edgecolor('#333333')
        self.ax.zaxis.pane.set_edgecolor('#333333')
        
        self.ax.xaxis.pane.set_alpha(0.3)
        self.ax.yaxis.pane.set_alpha(0.3)
        self.ax.zaxis.pane.set_alpha(0.3)
        
        self.punto_objetivo = (-1, -0.5)
        self.anim = None
        
    def configurar_escena(self):
        self.ax.clear()
        
        self.ax.set_xlim(-2.5, 2.5)
        self.ax.set_ylim(-2.5, 2.5)
        self.ax.set_zlim(-0.5, 2.5)
        
        self.ax.set_xlabel('X', color='white', fontsize=12, labelpad=10)
        self.ax.set_ylabel('Y', color='white', fontsize=12, labelpad=10)
        self.ax.set_zlabel('Z', color='white', fontsize=12, labelpad=10)
        self.ax.tick_params(colors='white', labelsize=8)
        
        # Plano de referencia
        xx, yy = np.meshgrid(np.linspace(-2.5, 2.5, 20), 
                            np.linspace(-2.5, 2.5, 20))
        zz = np.zeros_like(xx)
        self.ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray', edgecolor='none')
        
        # Círculo de alcance
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = 2 * np.cos(theta)
        y_circle = 2 * np.sin(theta)
        z_circle = np.zeros_like(theta)
        self.ax.plot(x_circle, y_circle, z_circle, '--',
                    color='#444444', linewidth=1.5, alpha=0.5, label='Alcance máximo')
        
        # Punto objetivo
        x_obj, y_obj = self.punto_objetivo
        self.ax.scatter([x_obj], [y_obj], [0], c='red', s=300,
                       marker='X', edgecolors='white', linewidth=2, 
                       label='Objetivo', alpha=0.9, zorder=20)
        
        # Elementos animados
        self.brazo1_line, = self.ax.plot([], [], [], 'c-', linewidth=8, 
                                         solid_capstyle='round', label='Brazo 1')
        self.brazo2_line, = self.ax.plot([], [], [], 'm-', linewidth=8,
                                         solid_capstyle='round', label='Brazo 2')
        
        self.base_point = self.ax.scatter([0], [0], [0], c='white', s=300,
                                         edgecolors='cyan', linewidth=2, zorder=15)
        self.articulacion_point = self.ax.scatter([], [], [], c='yellow', s=250,
                                                 edgecolors='orange', linewidth=2, zorder=15)
        self.efector_point = self.ax.scatter([], [], [], c='lime', s=350,
                                            edgecolors='white', linewidth=2, 
                                            marker='*', zorder=15)
        
        self.estela_scatter = self.ax.scatter([], [], [], c=[], cmap='viridis',
                                             s=50, alpha=0.7, zorder=5)
        
        self.info_text = self.ax.text2D(0.02, 0.95, '', transform=self.ax.transAxes,
                                        color='white', fontsize=10, 
                                        verticalalignment='top',
                                        bbox=dict(boxstyle="round,pad=0.3", 
                                                 facecolor='#333333', alpha=0.9))
        
        self.ax.view_init(elev=25, azim=-60)
        
    def animar_iteraciones(self, historial, config_nombre):
        """Anima el brazo en 3D siguiendo las iteraciones"""
        self.configurar_escena()
        
        # Generar trayectoria suave
        trayectoria_suave = self.brazo.generar_trayectoria_suave(historial, num_frames=200)
        
        # Pre-calcular posiciones
        n_frames = len(trayectoria_suave)
        posiciones = np.zeros((n_frames, 4))
        
        for i, (th1, th2) in enumerate(trayectoria_suave):
            x1 = self.brazo.z1 * np.cos(th1)
            y1 = self.brazo.z1 * np.sin(th1)
            x2, y2 = self.brazo.cinematica_directa(th1, th2)
            posiciones[i] = [x1, y1, x2, y2]
        
        # Posiciones reales de las iteraciones para la estela
        estela_posiciones = []
        for th1, th2 in historial:
            x2, y2 = self.brazo.cinematica_directa(th1, th2)
            estela_posiciones.append([x2, y2])
        estela_posiciones = np.array(estela_posiciones)
        
        def update(frame):
            x1, y1, x2, y2 = posiciones[frame]
            
            # Actualizar brazos
            self.brazo1_line.set_data([0, x1], [0, y1])
            self.brazo1_line.set_3d_properties([0, 0])
            self.brazo2_line.set_data([x1, x2], [y1, y2])
            self.brazo2_line.set_3d_properties([0, 0])
            
            # Actualizar articulaciones
            self.articulacion_point._offsets3d = ([x1], [y1], [0])
            self.efector_point._offsets3d = ([x2], [y2], [0])
            
            # Actualizar estela
            progreso = frame / n_frames
            num_iter_mostrar = int(progreso * len(estela_posiciones))
            
            if num_iter_mostrar > 0:
                estela_x = estela_posiciones[:num_iter_mostrar, 0]
                estela_y = estela_posiciones[:num_iter_mostrar, 1]
                estela_z = [0] * len(estela_x)
                self.estela_scatter._offsets3d = (estela_x, estela_y, estela_z)
                colors = np.linspace(0, 1, num_iter_mostrar)
                self.estela_scatter.set_array(colors)
            
            # Error actual
            x_obj, y_obj = self.punto_objetivo
            error = np.sqrt((x2 - x_obj)**2 + (y2 - y_obj)**2)
            
            # Ángulos actuales
            th1, th2 = trayectoria_suave[frame]
            self.info_text.set_text(
                f'Config: {config_nombre}\n'
                f'Frame: {frame}/{n_frames-1}\n'
                f'θ₁ = {np.degrees(th1):.2f}°\n'
                f'θ₂ = {np.degrees(th2):.2f}°\n'
                f'Error = {error:.2e}'
            )
            
            # Rotar vista
            if frame % 2 == 0:
                azim_actual = -60 + (frame / n_frames) * 30
                self.ax.view_init(elev=25, azim=azim_actual)
            
            self.fig.canvas.draw_idle()
            
            return (self.brazo1_line, self.brazo2_line, 
                    self.articulacion_point, self.efector_point,
                    self.estela_scatter, self.info_text)
        
        self.anim = FuncAnimation(self.fig, update, frames=n_frames,
                                 interval=50, blit=False, repeat=True)
        
        plt.tight_layout()
        plt.show()
        
        return self.anim


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================
def main():
    print("=" * 70)
    print("🤖 BRAZO ROBÓTICO DE 2 ESLABONES - CON GRÁFICAS DE ITERACIONES")
    print("=" * 70)
    
    brazo = BrazoRobotico(z1=1, z2=1)
    
    # PUNTO (-1, -0.5)
    x_obj, y_obj = -0.9, 1.3
    print(f"\n🎯 Punto objetivo: ({x_obj}, {y_obj})")
    
    print("\n🔍 Resolviendo cinemática inversa...")
    
    # Resolver ambas configuraciones
    sol_arriba, hist_arriba = brazo.cinematica_inversa(x_obj, y_obj, 'arriba')
    sol_abajo, hist_abajo = brazo.cinematica_inversa(x_obj, y_obj, 'abajo')
    
    # Mostrar resultados
    if sol_arriba is not None:
        print(f"\n✅ Configuración CODO ARRIBA:")
        print(f"   θ₁ = {np.degrees(sol_arriba[0]):.6f}°")
        print(f"   θ₂ = {np.degrees(sol_arriba[1]):.6f}°")
        x_final, y_final = brazo.cinematica_directa(sol_arriba[0], sol_arriba[1])
        print(f"   Posición final: ({x_final:.6f}, {y_final:.6f})")
    
    if sol_abajo is not None:
        print(f"\n✅ Configuración CODO ABAJO:")
        print(f"   θ₁ = {np.degrees(sol_abajo[0]):.6f}°")
        print(f"   θ₂ = {np.degrees(sol_abajo[1]):.6f}°")
        x_final, y_final = brazo.cinematica_directa(sol_abajo[0], sol_abajo[1])
        print(f"   Posición final: ({x_final:.6f}, {y_final:.6f})")
    
    # ============================================================
    # ANIMACIONES 2D
    # ============================================================
    print("\n" + "="*70)
    print("🎬 INICIANDO ANIMACIONES 2D")
    print("="*70)
    
    if sol_arriba is not None:
        print("\n🖥️  Animación 2D - Codo ARRIBA")
        visor2d = Visualizador2D(brazo)
        visor2d.punto_objetivo = (x_obj, y_obj)
        visor2d.animar_iteraciones(hist_arriba, "CODO ARRIBA")
    
    if sol_abajo is not None:
        print("\n🖥️  Animación 2D - Codo ABAJO")
        visor2d = Visualizador2D(brazo)
        visor2d.punto_objetivo = (x_obj, y_obj)
        visor2d.animar_iteraciones(hist_abajo, "CODO ABAJO")
    
    # ============================================================
    # ANIMACIONES 3D
    # ============================================================
    print("\n" + "="*70)
    print("🎬 INICIANDO ANIMACIONES 3D")
    print("="*70)
    
    if sol_arriba is not None:
        print("\n🖥️  Animación 3D - Codo ARRIBA")
        visor3d = Visualizador3D(brazo)
        visor3d.punto_objetivo = (x_obj, y_obj)
        visor3d.animar_iteraciones(hist_arriba, "CODO ARRIBA")
    
    if sol_abajo is not None:
        print("\n🖥️  Animación 3D - Codo ABAJO")
        visor3d = Visualizador3D(brazo)
        visor3d.punto_objetivo = (x_obj, y_obj)
        visor3d.animar_iteraciones(hist_abajo, "CODO ABAJO")


if __name__ == "__main__":
    main()