
# ==============================================================================
# EJERCICIO 3: Integrar y' = sin(y)
# ==============================================================================
def ejercicio3():
    titulo("EJERCICIO 3: Integrar y' = sin(y) con Taylor de 2° orden")
    print("Ecuación: y' = sin(y)")
    print("Condición inicial: y(0) = 1")
    print("Rango: x de 0 a 0.5, h = 0.1")
    
    h = 0.1
    x = 0.0
    y = 1.0
    
    print(f"\nPaso 0: x = {x:.1f}, y = {y:.6f}")
    
    for i in range(1, 6):
        yp = np.sin(y)
        ypp = np.cos(y) * yp  # derivada de sin(y) es cos(y)*y'
        
        y_new = y + h*yp + (h**2/2)*ypp
        x_new = x + h
        
        print(f"Paso {i}:")
        print(f"  y'({x:.1f}) = {yp:.6f}")
        print(f"  y''({x:.1f}) = {ypp:.6f}")
        print(f"  y({x_new:.1f}) = {y_new:.6f}")
        
        x, y = x_new, y_new
    
    print("\nCONCLUSIÓN: La solución aproximada en x=0.5 es y = {:.6f}".format(y))
