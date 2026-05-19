import numpy as np
import matplotlib.pyplot as plt

def ejercicio27():
    print("=" * 70)
    print("EJERCICIO 27: Órbita de satélite")
    print("=" * 70)
    print("Ecuación: R = C/(1 + e·sin(θ + α))")
    
    # Datos observados
    theta_grados = np.array([-30, 0, 30])
    R_obs = np.array([6870, 6728, 6615])
    
    print("\nDatos observados:")
    for th, r in zip(theta_grados, R_obs):
        print(f"  θ = {th:3d}° → R = {r} km")
    
    # Convertir a radianes
    theta = np.radians(theta_grados)
    
    # Sistema linealizado: 1/R = u + p·sinθ + q·cosθ
    invR = 1/R_obs
    A = np.column_stack([np.ones(3), np.sin(theta), np.cos(theta)])
    
    # Resolver
    u, p, q = np.linalg.solve(A, invR)
    
    # Recuperar parámetros
    C = 1/u
    v = np.sqrt(p**2 + q**2)
    e = v * C
    alpha = np.arctan2(q, p)
    
    print(f"\n📌 Parámetros de la órbita:")
    print(f"   C = {C:.2f} km")
    print(f"   e = {e:.6f}")
    print(f"   α = {np.degrees(alpha):.4f}°")
    
    # Calcular R mínimo
    R_min = C / (1 + e)
    R_max = C / (1 - e)
    
    print(f"\n📊 Análisis de la órbita:")
    print(f"   R mínimo = {R_min:.2f} km (punto más cercano)")
    print(f"   R máximo = {R_max:.2f} km (punto más lejano)")
    
    # Ángulo para R mínimo
    theta_min = np.pi/2 - alpha
    theta_min_grados = np.degrees(theta_min)
    print(f"   θ para R mínimo = {theta_min_grados:.2f}°")
    
    # ============================================================
    # GRÁFICA
    # ============================================================
    plt.figure(figsize=(10, 8))
    
    # Generar órbita completa
    theta_orbita = np.linspace(-np.pi, np.pi, 360)
    R_orbita = C / (1 + e * np.sin(theta_orbita + alpha))
    
    # Convertir a coordenadas cartesianas
    x = R_orbita * np.cos(theta_orbita)
    y = R_orbita * np.sin(theta_orbita)
    
    # Graficar órbita
    plt.plot(x, y, 'b-', linewidth=2, label='Órbita del satélite')
    
    # Puntos observados
    x_obs = R_obs * np.cos(theta)
    y_obs = R_obs * np.sin(theta)
    plt.plot(x_obs, y_obs, 'ro', markersize=8, label='Observaciones')
    
    # Punto de R mínimo
    x_min = R_min * np.cos(theta_min)
    y_min = R_min * np.sin(theta_min)
    plt.plot(x_min, y_min, 'g*', markersize=15, label=f'R mínimo: {R_min:.0f} km')
    
    # Tierra en el origen
    plt.plot(0, 0, 'yo', markersize=20, label='Tierra')
    
    # Configuración
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    plt.axis('equal')
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title('Ejercicio 27: Órbita del satélite')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return C, e, alpha, R_min, theta_min_grados

# Ejecutar
if __name__ == "__main__":
    C, e, alpha, R_min, theta_min = ejercicio27()