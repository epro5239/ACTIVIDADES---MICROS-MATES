import math

def punto_fijo(g, p0, tol, max_iter, nombre):
    print("\n" + "="*60)
    print(f"Resolviendo: {nombre}")
    print("="*60)
    
    print(f"{'Iter':<6}{'p_n':<20}{'Error':<20}")
    print("-"*60)
    
    for i in range(1, max_iter + 1):
        p = g(p0)
        error = abs(p - p0)
        
        print(f"{i:<6}{p:<20.10f}{error:<20.10f}")
        
        if error < tol:
            print("\nConvergencia alcanzada.")
            print(f"Solución aproximada: {p:.10f}")
            return p
        
        p0 = p
    
    print("\nSe alcanzó el máximo de iteraciones.")
    return p


# =========================
# EJERCICIO 5
# =========================
def ejercicio5():
    g = lambda x: ((3*x**2 + 3)/4)**(1/3)
    return punto_fijo(g, p0=1, tol=1e-4, max_iter=100, 
                      nombre="Ejercicio 5: 4x^3 - 3x^2 - 3 = 0")


# =========================
# EJERCICIO 6
# =========================
def ejercicio6():
    g = lambda x: (x + 1)**(1/3)
    return punto_fijo(g, p0=1, tol=1e-2, max_iter=100, 
                      nombre="Ejercicio 6: x^3 - x - 1 = 0")


# =========================
# EJERCICIO 9
# =========================
def ejercicio9():
    g = lambda x: 0.5*(x + 3/x)
    return punto_fijo(g, p0=1, tol=1e-4, max_iter=100, 
                      nombre="Ejercicio 9: Aproximación de sqrt(3)")


# =========================
# EJERCICIO 20
# =========================
def ejercicio20(A):
    g = lambda x: 0.5*x + A/(2*x)
    return punto_fijo(g, p0=1, tol=1e-6, max_iter=100, 
                      nombre=f"Ejercicio 20: Aproximación de sqrt({A})")


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    
    ejercicio5()
    ejercicio6()
    ejercicio9()
    ejercicio20(5) 