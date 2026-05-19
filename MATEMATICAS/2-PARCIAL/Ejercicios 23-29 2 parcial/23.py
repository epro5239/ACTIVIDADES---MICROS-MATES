import numpy as np
import matplotlib.pyplot as plt  # 👈 PASO 1

# ============================================================
# PASO 2: Función modificada que guarda historial
# ============================================================
def newton_raphson_con_historial(f, jacobian, x_inicial, tol=1e-4, max_iter=100):
    x = np.array(x_inicial, dtype=float)
    historial = [x.copy()]  # 👈 Guardar primera iteración
    
    print("Iteración |      x1       |      x2       |    ||Δx||    |    ||f||")
    print("-" * 65)
    
    for i in range(max_iter):
        F = f(x[0], x[1])
        J = jacobian(x[0], x[1])
        delta = np.linalg.solve(J, -F)
        x_nuevo = x + delta
        historial.append(x_nuevo.copy())  # 👈 Guardar cada iteración
        
        norm_delta = np.linalg.norm(delta)
        norm_f = np.linalg.norm(F)
        
        print(f"{i+1:9d} | {x_nuevo[0]:.6f} | {x_nuevo[1]:.6f} | {norm_delta:.2e} | {norm_f:.2e}")
        
        if norm_delta < tol:
            print(f"\n✅ Convergencia en {i+1} iteraciones")
            return x_nuevo, historial  # 👈 Retornar también historial
        
        x = x_nuevo
    
    return x, historial


# ============================================================
# PASO 3: Función para graficar
# ============================================================
def graficar_convergencia(historial):
    plt.figure(figsize=(10, 8))
    
    # Dibujar círculos
    theta = np.linspace(0, 2*np.pi, 100)
    plt.plot(2 + 2*np.cos(theta), 2*np.sin(theta), 'b-', alpha=0.5, label='(x-2)² + y² = 4')
    plt.plot(2*np.cos(theta), 3 + 2*np.sin(theta), 'r-', alpha=0.5, label='x² + (y-3)² = 4')
    
    # Convertir historial a array
    h = np.array(historial)
    
    # Dibujar camino
    plt.plot(h[:, 0], h[:, 1], 'g--', linewidth=2, label='Camino')
    
    # Puntos
    plt.plot(h[0, 0], h[0, 1], 'ro', markersize=10, label=f'Inicio: ({h[0,0]:.3f}, {h[0,1]:.3f})')
    plt.plot(h[-1, 0], h[-1, 1], 'g*', markersize=15, label=f'Final: ({h[-1,0]:.3f}, {h[-1,1]:.3f})')
    
    # Puntos intermedios
    for i, (x, y) in enumerate(h[1:-1], 1):
        plt.plot(x, y, 'ko', markersize=5)
        plt.annotate(str(i), (x, y), xytext=(3, 3), textcoords='offset points')
    
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.xlim(-1, 4)
    plt.ylim(-1, 5)
    plt.title('Convergencia de Newton-Raphson - Ejercicio 23')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


# ============================================================
# PASO 4: Tu ejercicio modificado
# ============================================================
def ejercicio23():
    print("=" * 70)
    print("EJERCICIO 23: Intersección de círculos")
    print("=" * 70)
    
    def f(x, y):
        return np.array([(x-2)**2 + y**2 - 4, x**2 + (y-3)**2 - 4])
    
    def jacobian(x, y):
        return np.array([[2*(x-2), 2*y], [2*x, 2*(y-3)]])
    
    # Primer punto
    x0_1 = [0.5, 1.5]
    print("\n🔍 Primer punto...")
    sol1, hist1 = newton_raphson_con_historial(f, jacobian, x0_1)
    print(f"\n📌 Solución 1: ({sol1[0]:.6f}, {sol1[1]:.6f})")
    graficar_convergencia(hist1)  # 👈 Mostrar gráfica
    
    # Segundo punto
    x0_2 = [2.5, 1.5]
    print("\n🔍 Segundo punto...")
    sol2, hist2 = newton_raphson_con_historial(f, jacobian, x0_2)
    print(f"\n📌 Solución 2: ({sol2[0]:.6f}, {sol2[1]:.6f})")
    graficar_convergencia(hist2)  # 👈 Mostrar gráfica
    
    return sol1, sol2


# Ejecutar
if __name__ == "__main__":
    ejercicio23()