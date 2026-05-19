
# ==============================================================================
# EJERCICIO 1: Taylor de 2° orden
# ==============================================================================
def ejercicio1():
    titulo("EJERCICIO 1: Método de Taylor de segundo orden")
    print("Ecuación diferencial: y' + 4y = x^2")
    print("Condición inicial: y(0) = 1")
    print("Objetivo: Calcular y(0.1) usando 2 pasos (h = 0.05)")
    print("\nMétodo: y_{n+1} = y_n + h*y'_n + (h^2/2)*y''_n")
    
    h = 0.05
    x = 0.0
    y = 1.0
    
    print(f"\nPaso 0: x = {x:.2f}, y = {y:.6f}")
    
    for i in range(1, 3):
        # Calcular derivadas en el punto actual
        yp = x**2 - 4*y               # y' = x^2 - 4y
        ypp = 2*x - 4*yp              # y'' = 2x - 4y'
        
        y_new = y + h*yp + (h**2/2)*ypp
        x_new = x + h
        
        print(f"Paso {i}:")
        print(f"  y'({x:.2f}) = {yp:.6f}")
        print(f"  y''({x:.2f}) = {ypp:.6f}")
        print(f"  y({x_new:.2f}) = {y_new:.6f}")
        
        x, y = x_new, y_new
    
    print("\nCONCLUSIÓN: El valor aproximado de y(0.1) es {:.6f}".format(y))
    print("Este método es más preciso que Euler porque incluye el término de segundo orden.")
