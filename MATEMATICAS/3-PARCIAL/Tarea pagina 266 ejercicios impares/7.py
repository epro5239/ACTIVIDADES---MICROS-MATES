
# ==============================================================================
# EJERCICIO 7: Péndulo simple
# ==============================================================================
def ejercicio7():
    titulo("EJERCICIO 7: Péndulo simple")
    print("Ecuación transformada: d²θ/dτ² = -sin(θ)")
    print("Condiciones: θ₀ = 1 rad, velocidad inicial = 0")
    print("Método: Integración numérica con odeint (RK45)\n")
    
    def pendulo(y, t):
        theta, omega = y
        dtheta = omega
        domega = -np.sin(theta)
        return [dtheta, domega]
    
    t = np.linspace(0, 15, 1000)
    y0 = [1.0, 0.0]
    sol = odeint(pendulo, y0, t)
    
    theta = sol[:,0]
    
    # Buscar cruces por cero para calcular período
    cruces = np.where(np.diff(np.sign(theta)))[0]
    if len(cruces) >= 2:
        t1 = t[cruces[0]]
        t2 = t[cruces[1]]
        periodo = 2 * (t2 - t1)
        periodo_pequeno = 2*np.pi
        print(f"Detalle del cálculo:")
        print(f"  Primer cruce por θ=0 en τ = {t1:.4f}")
        print(f"  Segundo cruce por θ=0 en τ = {t2:.4f}")
        print(f"  Período medido = {periodo:.4f}")
        print(f"  Período para pequeñas oscilaciones (teórico) = {periodo_pequeno:.4f}")
    
    print("\nCONCLUSIÓN: El período para una amplitud de 1 rad es mayor que el período de pequeñas oscilaciones.")
    print("Esto se debe a que la aproximación sin(θ) ≈ θ deja de ser exacta para ángulos grandes.")
