import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# FUNCIÓN DE NEWTON-RAPHSON CON HISTORIAL
# ============================================================
def newton_raphson_con_historial(f, jacobian, x_inicial, tol=1e-4, max_iter=100):
    """
    Versión que guarda TODAS las iteraciones para graficar después
    """
    x = np.array(x_inicial, dtype=float)
    historial = [x.copy()]  # Aquí guardamos cada iteración
    
    print("\n" + "="*60)
    print("PROCESO DE ITERACIONES:")
    print("="*60)
    print("Iter |      x      |      y      |    ||Δx||    |    ||f||")
    print("-" * 60)
    
    for i in range(max_iter):
        # PASO 1: Evaluar f(x)
        F = f(x[0], x[1])
        
        # PASO 2: Calcular Jacobiano
        J = jacobian(x[0], x[1])
        
        # PASO 3: Resolver J·Δx = -f(x)
        try:
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            print("¡Error! Jacobiano singular")
            return None, historial
        
        # PASO 4: Actualizar x
        x_nuevo = x + delta
        historial.append(x_nuevo.copy())  # GUARDAR para la gráfica
        
        # Calcular normas
        norm_delta = np.linalg.norm(delta)
        norm_f = np.linalg.norm(F)
        
        # Mostrar iteración
        print(f"{i+1:3d}   | {x_nuevo[0]:.6f} | {x_nuevo[1]:.6f} | {norm_delta:.2e} | {norm_f:.2e}")
        
        # PASO 5: Verificar convergencia
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
    
    # Barra de color CORREGIDA
    sm = plt.cm.ScalarMappable(cmap='rainbow', norm=plt.Normalize(0, len(historial)-1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca())
    cbar.set_label('Número de iteración', fontsize=10)
    
    plt.tight_layout()
    plt.show()


# ============================================================
# EJERCICIO 25
# ============================================================
def ejercicio25():
    print("=" * 70)
    print("EJERCICIO 25: Sistema con tangente")
    print("=" * 70)
    print("Ecuaciones:")
    print("  f1: tan x - y = 1")
    print("  f2: cos x - 3 sin y = 0")
    print(f"  Buscar en 0 < x < 1.5")
    
    def f(x, y):
        f1 = np.tan(x) - y - 1
        f2 = np.cos(x) - 3*np.sin(y)
        return np.array([f1, f2])
    
    def jacobian(x, y):
        J = np.array([[1/(np.cos(x)**2), -1],
                      [-np.sin(x), -3*np.cos(y)]])
        return J
    
    # Estimar punto inicial
    x_est = 0.9
    y_est = np.tan(x_est) - 1
    x0 = [x_est, y_est]
    print(f"\n🔍 Estimación inicial: ({x0[0]:.4f}, {x0[1]:.4f})")
    
    # Ejecutar Newton-Raphson
    solucion, historial = newton_raphson_con_historial(f, jacobian, x0)
    
    print(f"\n📌 Solución encontrada: ({solucion[0]:.6f}, {solucion[1]:.6f})")
    
    # Verificar que está en el intervalo
    if 0 < solucion[0] < 1.5:
        print(f"✅ x = {solucion[0]:.6f} está en (0, 1.5)")
    else:
        print(f"⚠️  x = {solucion[0]:.6f} NO está en el intervalo requerido")
    
    # Verificación
    f1, f2 = f(solucion[0], solucion[1])
    print(f"\n✅ Verificación:")
    print(f"   f1 = {f1:.2e} (debe ser 0)")
    print(f"   f2 = {f2:.2e} (debe ser 0)")
    
    # Función para dibujar las curvas
    def dibujar_curvas():
        x = np.linspace(0.7, 1.1, 100)
        
        # Curva de f1: y = tan x - 1
        y1 = np.tan(x) - 1
        plt.plot(x, y1, 'b-', linewidth=2, alpha=0.5, label='tan x - y = 1')
        
        # Curva de f2: cos x - 3 sin y = 0
        y_malla = np.linspace(0.1, 0.5, 100)
        X, Y = np.meshgrid(x, y_malla)
        plt.contour(X, Y, np.cos(X) - 3*np.sin(Y), levels=[0], 
                   colors='red', linewidths=2, alpha=0.5)
        
        # Marcar el intervalo
        plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=1.5, color='k', linestyle='--', alpha=0.3, label='Intervalo (0, 1.5)')
        
        # Etiquetas
        plt.text(1.0, 0.35, 'f1 = 0', color='blue', fontsize=12)
        plt.text(0.85, 0.25, 'f2 = 0', color='red', fontsize=12)
    
    # Graficar convergencia
    graficar_convergencia(historial,
                         titulo="Ejercicio 25: tan x - y = 1  y  cos x - 3 sin y = 0",
                         x_range=(0.7, 1.1),
                         y_range=(0.1, 0.5),
                         curvas_func=dibujar_curvas)
    
    return solucion, historial


# ============================================================
# EJECUTAR
# ============================================================
if __name__ == "__main__":
    sol25, hist25 = ejercicio25()