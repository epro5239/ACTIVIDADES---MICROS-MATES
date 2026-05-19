
# ==============================================================================
# EJERCICIO 11: Péndulo con soporte oscilante
# ==============================================================================
def ejercicio11():
    titulo("EJERCICIO 11: Péndulo con soporte oscilante")
    print("Ecuación: θ'' = -(g/L)sin(θ) + (ω²/L)Ycos(θ)sin(ωt)")
    print("Datos: g=9.80665, L=1.0, Y=0.25, ω=2.5 rad/s")
    print("Condiciones iniciales: θ(0)=0, θ'(0)=0\n")
    
    g = 9.80665
    L = 1.0
    Y = 0.25
    omega = 2.5
    
    def sistema(y, t):
        theta, dtheta = y
        d2theta = -(g/L)*np.sin(theta) + (omega**2/L)*Y*np.cos(theta)*np.sin(omega*t)
        return [dtheta, d2theta]
    
    t = np.linspace(0, 10, 1000)
    y0 = [0, 0]
    sol = odeint(sistema, y0, t)
    
    theta = sol[:,0]
    max_theta = np.max(np.abs(theta))
    
    print("Se muestran algunos valores de θ vs tiempo:")
    for i in range(0, 1000, 100):
        print(f"  t = {t[i]:.2f}s, θ = {theta[i]:.6f} rad")
    
    print(f"\nMáximo ángulo alcanzado: {max_theta:.6f} rad ({np.degrees(max_theta):.2f}°)")
    
    plt.figure()
    plt.plot(t, theta)
    plt.title('Ejercicio 11: Péndulo con soporte oscilante')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo θ (rad)')
    plt.grid(True)
    plt.show()
    
    print("\nCONCLUSIÓN: El péndulo responde a la oscilación del soporte generando un movimiento")
    print("que crece hasta alcanzar un máximo de {:.2f}° antes de estabilizarse.".format(np.degrees(max_theta)))