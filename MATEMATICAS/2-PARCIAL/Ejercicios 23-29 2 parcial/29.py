import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# FUNCIÓN DE NEWTON-RAPHSON PARA 2 VARIABLES
# ============================================================
def newton_raphson_2d(f, jacobian, x0, nombre="", tol=1e-4, max_iter=100):
    """
    Newton-Raphson para 2 variables (θ₁, θ₂)
    """
    x = np.array(x0, dtype=float)
    historial = [x.copy()]
    
    print(f"\n{nombre}")
    print("="*55)
    print("Iter |     θ₁      |     θ₂      |    ||Δx||    |    ||f||")
    print("-" * 55)
    
    for i in range(max_iter):
        F = f(x[0], x[1])
        J = jacobian(x[0], x[1])
        
        # Verificar si Jacobiano es singular
        det = np.linalg.det(J)
        if abs(det) < 1e-10:
            print(f"⚠️  Jacobiano casi singular (det = {det:.2e})")
            print(f"   Prueba con otra estimación inicial")
            return None, historial
        
        try:
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            print("❌ Error: Jacobiano exactamente singular")
            return None, historial
        
        x_nuevo = x + delta
        historial.append(x_nuevo.copy())
        
        norm_delta = np.linalg.norm(delta)
        norm_f = np.linalg.norm(F)
        
        print(f"{i+1:3d}   | {np.degrees(x_nuevo[0]):8.4f} | {np.degrees(x_nuevo[1]):8.4f} | {norm_delta:.2e} | {norm_f:.2e}")
        
        if norm_delta < tol:
            print("-" * 55)
            print(f"✅ CONVERGENCIA en {i+1} iteraciones")
            return x_nuevo, historial
        
        x = x_nuevo
    
    return x, historial


# ============================================================
# FUNCIÓN PARA GRAFICAR EL MECANISMO
# ============================================================
def graficar_mecanismo(theta1, theta2, theta3, titulo):
    plt.figure(figsize=(10, 8))
    
    # Longitudes
    L1 = 150
    L2 = 180
    L3 = 200
    L4 = 200
    
    # Coordenadas
    x0, y0 = 0, 0
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta2)
    y2 = y1 + L2 * np.sin(theta2)
    x3 = L4
    y3 = 0
    
    # Verificar si cierra
    error_cierre = np.sqrt((x2 - x3)**2 + (y2 - y3)**2)
    
    # Dibujar barras
    plt.plot([x0, x1], [y0, y1], 'b-', linewidth=4, label=f'Barra 1: {L1}')
    plt.plot([x1, x2], [y1, y2], 'r-', linewidth=4, label=f'Barra 2: {L2}')
    plt.plot([x2, x3], [y2, y3], 'g-', linewidth=4, label=f'Barra 3: {L3}')
    plt.plot([x0, x3], [y0, y3], 'k-', linewidth=2, label=f'Barra fija: {L4}')
    
    # Dibujar articulaciones
    plt.plot([x0, x1, x2, x3], [y0, y1, y2, y3], 'ko', markersize=10)
    
    # Anotaciones
    plt.annotate('O', (x0, y0), xytext=(-15, -15), fontsize=12, weight='bold')
    plt.annotate('A', (x1, y1), xytext=(5, 5), fontsize=12, weight='bold')
    plt.annotate('B', (x2, y2), xytext=(5, 5), fontsize=12, weight='bold')
    plt.annotate('C', (x3, y3), xytext=(5, -15), fontsize=12, weight='bold')
    
    # Ángulos
    plt.annotate(f'θ₁ = {np.degrees(theta1):.1f}°', 
                (x1/2, y1/2), fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    plt.annotate(f'θ₂ = {np.degrees(theta2):.1f}°', 
                (x1 + L2/2*np.cos(theta2), y1 + L2/2*np.sin(theta2)), 
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
    plt.annotate(f'θ₃ = 75°', 
                ((x2+x3)/2, (y2+y3)/2), 
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    
    plt.title(f'{titulo}\nError de cierre: {error_cierre:.2e}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    plt.axis('equal')
    plt.xlim(-50, 350)
    plt.ylim(-150, 250)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return error_cierre


# ============================================================
# EJERCICIO 29 - CON θ₃ = 75° Y DOS SOLUCIONES
# ============================================================
def ejercicio29():
    print("=" * 70)
    print("EJERCICIO 29: Mecanismo de 4 barras con θ₃ = 75°")
    print("=" * 70)
    
    print("\nEcuaciones del mecanismo:")
    print("  150·cos θ₁ + 180·cos θ₂ - 200·cos(75°) = 200")
    print("  150·sin θ₁ + 180·sin θ₂ - 200·sin(75°) = 0")
    print("\n📌 NOTA: Se buscan DOS soluciones (configuraciones abierta y cruzada)")
    
    # Fijar θ₃ = 75°
    theta3_fijo = np.radians(75)
    print(f"\n🔍 θ₃ fijo = 75° ({theta3_fijo:.4f} rad)")
    
    # Función para resolver (solo θ₁, θ₂)
    def f(theta1, theta2):
        f1 = 150*np.cos(theta1) + 180*np.cos(theta2) - 200*np.cos(theta3_fijo) - 200
        f2 = 150*np.sin(theta1) + 180*np.sin(theta2) - 200*np.sin(theta3_fijo)
        return np.array([f1, f2])
    
    def jacobian(theta1, theta2):
        J = np.array([[-150*np.sin(theta1), -180*np.sin(theta2)],
                      [150*np.cos(theta1), 180*np.cos(theta2)]])
        return J
    
    # ========================================================
    # SOLUCIÓN 1: Configuración "abierta" 
    # (MEJOR ESTIMACIÓN INICIAL: 20°, 10°)
    # ========================================================
    print("\n" + "="*50)
    print("🔍 BUSCANDO SOLUCIÓN 1 (configuración abierta)")
    print("="*50)
    
    # Estimación inicial mejorada: θ₁ ≈ 20°, θ₂ ≈ 10°
    x0_1 = [np.radians(20), np.radians(10)]
    print(f"\nEstimación inicial: θ₁ = 20°, θ₂ = 10°")
    
    sol1, hist1 = newton_raphson_2d(f, jacobian, x0_1, nombre="SOLUCIÓN 1")
    
    if sol1 is not None:
        print(f"\n📌 SOLUCIÓN 1 encontrada:")
        print(f"   θ₁ = {np.degrees(sol1[0]):.6f}°")
        print(f"   θ₂ = {np.degrees(sol1[1]):.6f}°")
        print(f"   θ₃ = 75° (fijo)")
        
        # Verificar
        f1, f2 = f(sol1[0], sol1[1])
        print(f"\n✅ Verificación:")
        print(f"   f1 = {f1:.2e} (debe ser 0)")
        print(f"   f2 = {f2:.2e} (debe ser 0)")
        
        # Graficar solución 1
        print("\n🎨 Generando gráfica de la Solución 1...")
        error1 = graficar_mecanismo(sol1[0], sol1[1], theta3_fijo, 
                                    "Solución 1: Configuración Abierta")
    else:
        print("\n❌ No se pudo encontrar la Solución 1")
        error1 = float('inf')
        sol1 = None
    
    # ========================================================
    # SOLUCIÓN 2: Configuración "cruzada"
    # (MEJOR ESTIMACIÓN INICIAL: 50°, -40°)
    # ========================================================
    print("\n" + "="*50)
    print("🔍 BUSCANDO SOLUCIÓN 2 (configuración cruzada)")
    print("="*50)
    
    # Estimación inicial mejorada: θ₁ ≈ 50°, θ₂ ≈ -40°
    x0_2 = [np.radians(50), np.radians(-40)]
    print(f"\nEstimación inicial: θ₁ = 50°, θ₂ = -40°")
    
    sol2, hist2 = newton_raphson_2d(f, jacobian, x0_2, nombre="SOLUCIÓN 2")
    
    if sol2 is not None:
        print(f"\n📌 SOLUCIÓN 2 encontrada:")
        print(f"   θ₁ = {np.degrees(sol2[0]):.6f}°")
        print(f"   θ₂ = {np.degrees(sol2[1]):.6f}°")
        print(f"   θ₃ = 75° (fijo)")
        
        # Verificar
        f1, f2 = f(sol2[0], sol2[1])
        print(f"\n✅ Verificación:")
        print(f"   f1 = {f1:.2e} (debe ser 0)")
        print(f"   f2 = {f2:.2e} (debe ser 0)")
        
        # Graficar solución 2
        print("\n🎨 Generando gráfica de la Solución 2...")
        error2 = graficar_mecanismo(sol2[0], sol2[1], theta3_fijo, 
                                    "Solución 2: Configuración Cruzada")
    else:
        print("\n❌ No se pudo encontrar la Solución 2")
        error2 = float('inf')
        sol2 = None
    
    # ========================================================
    # COMPARACIÓN DE SOLUCIONES
    # ========================================================
    print("\n" + "="*50)
    print("📊 COMPARACIÓN DE LAS DOS SOLUCIONES")
    print("="*50)
    
    if sol1 is not None:
        print(f"\n✅ Solución 1 (abierta):")
        print(f"   θ₁ = {np.degrees(sol1[0]):.4f}°")
        print(f"   θ₂ = {np.degrees(sol1[1]):.4f}°")
        print(f"   Error de cierre: {error1:.2e}")
    else:
        print("\n❌ Solución 1: No encontrada")
    
    if sol2 is not None:
        print(f"\n✅ Solución 2 (cruzada):")
        print(f"   θ₁ = {np.degrees(sol2[0]):.4f}°")
        print(f"   θ₂ = {np.degrees(sol2[1]):.4f}°")
        print(f"   Error de cierre: {error2:.2e}")
    else:
        print("\n❌ Solución 2: No encontrada")
    
    # Explicación física
    print("\n" + "="*50)
    print("🔬 EXPLICACIÓN FÍSICA")
    print("="*50)
    print("""
    En un mecanismo de 4 barras, para una misma posición de la barra 3 (θ₃ = 75°),
    existen DOS formas de ensamblar el mecanismo:
    
    1. CONFIGURACIÓN ABIERTA:
       - La barra 2 apunta hacia arriba (θ₂ positivo)
       - El mecanismo se abre hacia arriba
    
    2. CONFIGURACIÓN CRUZADA:
       - La barra 2 apunta hacia abajo (θ₂ negativo)
       - El mecanismo se cruza sobre sí mismo
       
    IMPORTANTE: La estimación inicial (30°, 30°) daba Jacobiano singular 
    porque está cerca de un punto donde las barras se alinean.
    Las nuevas estimaciones (20°,10°) y (50°,-40°) funcionan correctamente.
    """)
    
    return (sol1, sol2), (error1, error2)


# ============================================================
# EJECUTAR
# ============================================================
if __name__ == "__main__":
    soluciones, errores = ejercicio29()