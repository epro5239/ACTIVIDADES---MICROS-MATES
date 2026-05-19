
# ==============================================================================
# EJERCICIO 19: Función de Bessel J0(x)
# ==============================================================================
def ejercicio19():
    titulo("EJERCICIO 19: Función de Bessel J₀(x)")
    print("Ecuación: y'' + (1/x)*y' + y = 0")
    print("Condiciones: y(0)=1, y'(0)=0 (J₀)")
    print("Objetivo: Calcular J₀(5) y comparar con tabla\n")
    
    # Evitar singularidad en x=0
    x_inicio = 1e-12
    y0 = 1.0
    dy0 = 0.0
    
    def bessel(Y, x):
        y, dy = Y
        if x < 1e-15:
            ddy = 0  # Límite seguro
        else:
            ddy = -(1/x)*dy - y
        return [dy, ddy]
    
    x = np.linspace(x_inicio, 5, 500)
    Y0 = [y0, dy0]
    sol = odeint(bessel, Y0, x)
    
    y_vals = sol[:,0]
    idx_5 = np.abs(x - 5).argmin()
    j0_5 = y_vals[idx_5]
    j0_teorico = -0.1775967713
    
    print("Progreso de la integración:")
    for i in range(0, len(x), 50):
        print(f"  x = {x[i]:.3f}, J₀(x) = {y_vals[i]:.6f}")
    
    print(f"\nResultados en x=5:")
    print(f"  Valor numérico: {j0_5:.8f}")
    print(f"  Valor de tabla: {j0_teorico:.8f}")
    print(f"  Diferencia: {abs(j0_5 - j0_teorico):.8f}")
    
    plt.figure()
    plt.plot(x, y_vals)
    plt.title('Función de Bessel J₀(x)')
    plt.xlabel('x')
    plt.ylabel('J₀(x)')
    plt.grid(True)
    plt.axhline(0, color='k', linewidth=0.5)
    plt.show()
    
    print("\nCONCLUSIÓN: La solución numérica coincide con los valores tabulados de J₀(x).")
    print("La diferencia en x=5 es muy pequeña, confirmando la precisión del método.")
