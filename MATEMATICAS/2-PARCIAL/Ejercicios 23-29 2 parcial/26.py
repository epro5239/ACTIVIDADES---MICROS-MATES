import numpy as np
import matplotlib.pyplot as plt

def ejercicio26():
    print("=" * 70)
    print("EJERCICIO 26: Círculo por 3 puntos")
    print("=" * 70)
    
    # Puntos dados
    puntos = [(8.21, 0.00), (0.34, 6.62), (5.96, -1.12)]
    
    print("\nPuntos dados:")
    for i, (x, y) in enumerate(puntos, 1):
        print(f"  P{i}: ({x:.2f}, {y:.2f})")
    
    # Construir sistema lineal
    A = []
    B = []
    
    for i in range(3):
        for j in range(i+1, 3):
            xi, yi = puntos[i]
            xj, yj = puntos[j]
            A.append([2*(xj - xi), 2*(yj - yi)])
            B.append(xj**2 + yj**2 - xi**2 - yi**2)
    
    A = np.array(A)
    B = np.array(B)
    
    # Resolver para a, b (centro)
    a, b = np.linalg.lstsq(A, B, rcond=None)[0]
    
    # Calcular radio
    R2 = (puntos[0][0] - a)**2 + (puntos[0][1] - b)**2
    R = np.sqrt(R2)
    
    print(f"\n📌 Resultados:")
    print(f"   Centro: a = {a:.6f}, b = {b:.6f}")
    print(f"   Radio: R = {R:.6f}")
    
    # Verificación
    print(f"\n✅ Verificación (todos deben dar R² ≈ {R2:.4f}):")
    for i, (x, y) in enumerate(puntos, 1):
        dist2 = (x - a)**2 + (y - b)**2
        print(f"   P{i}: {dist2:.6f} (diferencia: {dist2 - R2:.2e})")
    
    # ============================================================
    # GRÁFICA
    # ============================================================
    plt.figure(figsize=(10, 8))
    
    # Dibujar círculo
    theta = np.linspace(0, 2*np.pi, 100)
    x_circulo = a + R * np.cos(theta)
    y_circulo = b + R * np.sin(theta)
    plt.plot(x_circulo, y_circulo, 'b-', linewidth=2, label=f'Círculo solución')
    
    # Dibujar puntos dados
    puntos_x = [p[0] for p in puntos]
    puntos_y = [p[1] for p in puntos]
    plt.plot(puntos_x, puntos_y, 'ro', markersize=10, label='Puntos dados')
    
    # Marcar centro
    plt.plot(a, b, 'g*', markersize=15, label=f'Centro ({a:.2f}, {b:.2f})')
    
    # Anotaciones
    for i, (x, y) in enumerate(puntos, 1):
        plt.annotate(f'P{i}', (x, y), xytext=(5, 5), 
                    textcoords='offset points', fontsize=10)
    
    # Líneas desde el centro a los puntos
    for x, y in puntos:
        plt.plot([a, x], [b, y], 'k--', alpha=0.3)
    
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Ejercicio 26: Círculo que pasa por 3 puntos')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return a, b, R

# Ejecutar
if __name__ == "__main__":
    a, b, R = ejercicio26()