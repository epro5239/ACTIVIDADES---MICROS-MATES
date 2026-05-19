import numpy as np
import matplotlib.pyplot as plt

def ejercicio28():
    print("=" * 70)
    print("EJERCICIO 28: Trayectoria de proyectil")
    print("=" * 70)
    
    g = 9.81  # m/s²
    
    print(f"\nDatos:")
    print(f"  g = {g} m/s²")
    print(f"  Condición: impacto con ángulo de 45° (pendiente -1)")
    
    # Resolver ángulo de la ecuación tan θ = 3
    theta = np.arctan(3)
    theta_grados = np.degrees(theta)
    
    print(f"\n📌 Ángulo de lanzamiento:")
    print(f"   θ = {theta_grados:.6f}°")
    print(f"   θ = {theta:.6f} rad")
    
    # Relación entre v y T
    sinth = np.sin(theta)
    costh = np.cos(theta)
    suma_sc = sinth + costh
    
    print(f"\n📊 Relación v-T:")
    print(f"   T = v × ({suma_sc:.6f}) / {g} = v × {suma_sc/g:.6f}")
    
    # Elegir una velocidad para graficar
    v = 100  # m/s
    T = suma_sc * v / g
    
    print(f"\n🔍 Para v = {v} m/s:")
    print(f"   T = {T:.4f} s")
    
    # Generar trayectoria
    t = np.linspace(0, T, 100)
    x = v * costh * t
    y = -0.5 * g * t**2 + v * sinth * t
    
    # Punto de impacto
    x_impacto = x[-1]
    y_impacto = y[-1]
    
    print(f"   Alcance: {x_impacto:.2f} m")
    print(f"   Altura máxima: {np.max(y):.2f} m")
    
    # Verificar condiciones
    pendiente = (-g*T + v*sinth) / (v*costh)
    print(f"\n✅ Verificación:")
    print(f"   y_impacto/x_impacto = {y_impacto/x_impacto:.4f} (debe ser 1)")
    print(f"   Pendiente en impacto = {pendiente:.4f} (debe ser -1)")
    
    # ============================================================
    # GRÁFICA
    # ============================================================
    plt.figure(figsize=(12, 8))
    
    # Trayectoria
    plt.plot(x, y, 'b-', linewidth=2, label='Trayectoria')
    
    # Punto de lanzamiento
    plt.plot(0, 0, 'ro', markersize=8, label='Lanzamiento')
    
    # Punto de impacto
    plt.plot(x_impacto, y_impacto, 'g*', markersize=15, label='Impacto')
    
    # Línea a 45°
    x_linea = np.linspace(0, x_impacto, 100)
    y_linea = x_linea
    plt.plot(x_linea, y_linea, 'r--', alpha=0.5, label='Línea y = x')
    
    # Marcar altura máxima
    idx_max = np.argmax(y)
    plt.plot(x[idx_max], y[idx_max], 'mo', markersize=8, label='Altura máxima')
    
    # Anotaciones
    plt.annotate(f'θ = {theta_grados:.1f}°', (10, 200), fontsize=12)
    plt.annotate(f'v = {v} m/s', (10, 150), fontsize=12)
    plt.annotate(f'T = {T:.2f} s', (10, 100), fontsize=12)
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Ejercicio 28: Trayectoria de proyectil con impacto a 45°')
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    return theta, v, T

# Ejecutar
if __name__ == "__main__":
    theta, v, T = ejercicio28()