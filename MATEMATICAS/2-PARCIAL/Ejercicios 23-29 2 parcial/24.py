import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# FUNCIÓN DE NEWTON-RAPHSON CON HISTORIAL (IGUAL)
# ============================================================
def newton_raphson_con_historial(f, jacobian, x_inicial, tol=1e-4, max_iter=100):
    x = np.array(x_inicial, dtype=float)
    historial = [x.copy()]
    
    print("\n" + "="*60)
    print("PROCESO DE ITERACIONES:")
    print("="*60)
    print("Iter |      x      |      y      |    ||Δx||    |    ||f||")
    print("-" * 60)
    
    for i in range(max_iter):
        F = f(x[0], x[1])
        J = jacobian(x[0], x[1])
        
        try:
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            print("¡Error! Jacobiano singular")
            return None, historial
        
        x_nuevo = x + delta
        historial.append(x_nuevo.copy())
        
        norm_delta = np.linalg.norm(delta)
        norm_f = np.linalg.norm(F)
        
        print(f"{i+1:3d}   | {x_nuevo[0]:.6f} | {x_nuevo[1]:.6f} | {norm_delta:.2e} | {norm_f:.2e}")
        
        if norm_delta < tol:
            print("-" * 60)
            print(f"✅ CONVERGENCIA en {i+1} iteraciones")
            return x_nuevo, historial
        
        x = x_nuevo
    
    return x, historial


# ============================================================
# FUNCIÓN PARA GRAFICAR CONVERGENCIA (CORREGIDA)
# ============================================================
def graficar_convergencia(historial, titulo, x_range, y_range, curvas_func=None):
    plt.figure(figsize=(12, 8))
    
    historial = np.array(historial)
    
    # Dibujar curvas de las funciones si se proporcionan
    if curvas_func:
        curvas_func()
    
    # Dibujar camino de convergencia
    plt.plot(historial[:, 0], historial[:, 1], 'g--', linewidth=2, 
             alpha=0.7, label='Camino de convergencia')
    
    # Dibujar puntos de iteración
    colores = plt.cm.rainbow(np.linspace(0, 1, len(historial)))
    
    for i, (x, y) in enumerate(historial):
        if i == 0:
            plt.plot(x, y, 'ro', markersize=12, label=f'Inicio (Iter 0)')
            plt.annotate(f'INICIO', (x, y), xytext=(10, 10), 
                        textcoords='offset points', fontsize=10, weight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="red", alpha=0.7))
        elif i == len(historial) - 1:
            plt.plot(x, y, 'g*', markersize=18, label=f'Solución (Iter {i})')
            plt.annotate(f'FIN', (x, y), xytext=(10, -15), 
                        textcoords='offset points', fontsize=10, weight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="green", alpha=0.7))
        else:
            plt.plot(x, y, 'o', color=colores[i], markersize=8)
            plt.annotate(f'{i}', (x, y), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8)
    
    plt.grid(True, alpha=0.3)
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.title(f'{titulo}\nConvergencia de Newton-Raphson', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='best')
    
    # ===== CORRECCIÓN AQUÍ =====
    # Crear la barra de color correctamente
    sm = plt.cm.ScalarMappable(cmap='rainbow', norm=plt.Normalize(0, len(historial)-1))
    sm.set_array([])  # Esto evita el error
    
    # Añadir la barra de color al eje actual
    cbar = plt.colorbar(sm, ax=plt.gca())
    cbar.set_label('Número de iteración', fontsize=10)
    # ============================
    
    plt.tight_layout()
    plt.show()


# ============================================================
# EJERCICIO 24 (IGUAL, solo asegurar que dibujar_curvas está definida)
# ============================================================
def ejercicio24():
    print("=" * 70)
    print("EJERCICIO 24: Sistema trigonométrico")
    print("=" * 70)
    print("Ecuaciones:")
    print("  f1: sin x + 3 cos x - 2 = 0")
    print("  f2: cos x - sin y + 0.2 = 0")
    
    def f(x, y):
        f1 = np.sin(x) + 3*np.cos(x) - 2
        f2 = np.cos(x) - np.sin(y) + 0.2
        return np.array([f1, f2])
    
    def jacobian(x, y):
        J = np.array([[np.cos(x) - 3*np.sin(x), 0],
                      [-np.sin(x), -np.cos(y)]])
        return J
    
    # Punto inicial (cerca de 1,1 como indica el problema)
    x0 = [1.0, 1.0]
    print(f"\n🔍 Punto inicial: ({x0[0]}, {x0[1]})")
    
    # Ejecutar Newton-Raphson
    solucion, historial = newton_raphson_con_historial(f, jacobian, x0)
    
    print(f"\n📌 Solución encontrada: ({solucion[0]:.6f}, {solucion[1]:.6f})")
    
    # Verificación
    f1, f2 = f(solucion[0], solucion[1])
    print(f"\n✅ Verificación:")
    print(f"   f1 = {f1:.2e} (debe ser 0)")
    print(f"   f2 = {f2:.2e} (debe ser 0)")
    
    # Función para dibujar las curvas
    def dibujar_curvas():
        x = np.linspace(0.8, 1.4, 100)
        y = np.linspace(0.3, 1.1, 100)
        X, Y = np.meshgrid(x, y)
        
        # Curva f1 = 0
        plt.contour(X, Y, np.sin(X) + 3*np.cos(X) - 2, levels=[0], 
                   colors='blue', linewidths=2, alpha=0.5)
        
        # Curva f2 = 0
        plt.contour(X, Y, np.cos(X) - np.sin(Y) + 0.2, levels=[0], 
                   colors='red', linewidths=2, alpha=0.5)
        
        # Etiquetas
        plt.text(1.2, 0.5, 'f1 = 0', color='blue', fontsize=12)
        plt.text(1.0, 0.8, 'f2 = 0', color='red', fontsize=12)
    
    # Graficar convergencia
    graficar_convergencia(historial,
                         titulo="Ejercicio 24: Sistema trigonométrico",
                         x_range=(0.8, 1.4),
                         y_range=(0.3, 1.1),
                         curvas_func=dibujar_curvas)
    
    return solucion, historial

# Ejecutar
if __name__ == "__main__":
    sol24, hist24 = ejercicio24()