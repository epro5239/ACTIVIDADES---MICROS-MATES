
# ==============================================================================
# EJERCICIO 15: Masa con cuerda elástica
# ==============================================================================
def ejercicio15():
    titulo("EJERCICIO 15: Masa con cuerda elástica")
    print("Ecuaciones en coordenadas polares:")
    print("  r'' = r*(θ')² + g*cos(θ) - (k/m)*(r-L)")
    print("  θ'' = (-2*r'*θ' - g*sin(θ)) / r")
    print("Datos: m=0.25kg, k=40N/m, L=0.5m, θ₀=60°, r₀=L\n")
    
    g = 9.80665
    k = 40
    L = 0.5
    m = 0.25
    
    def sistema(Y, t):
        r, dr, theta, dtheta = Y
        d2r = r*dtheta**2 + g*np.cos(theta) - (k/m)*(r-L)
        d2theta = (-2*dr*dtheta - g*np.sin(theta)) / r
        return [dr, d2r, dtheta, d2theta]
    
    t = np.linspace(0, 3, 1000)
    Y0 = [L, 0.0, np.radians(60), 0.0]
    sol = odeint(sistema, Y0, t)
    
    r = sol[:,0]
    theta = sol[:,2]
    
    # Encontrar cuando θ=0 por primera vez
    cruces_theta = np.where(np.diff(np.sign(theta)))[0]
    if len(cruces_theta) > 0:
        i = cruces_theta[0]
        t_llegada = t[i]
        r_llegada = r[i]
        
        print("Iteración de búsqueda de θ=0:")
        for j in range(i-2, i+3):
            if 0 <= j < len(t):
                print(f"  t={t[j]:.4f}s, θ={np.degrees(theta[j]):.4f}°, r={r[j]:.4f}m")
        
        print(f"\nResultado final:")
        print(f"  Tiempo para θ=0: {t_llegada:.4f} s")
        print(f"  Longitud r en ese instante: {r_llegada:.4f} m")
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(t, r)
    plt.title('Evolución de r')
    plt.grid(True)
    
    plt.subplot(2,1,2)
    plt.plot(t, np.degrees(theta))
    plt.title('Evolución de θ (grados)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    print("\nCONCLUSIÓN: La masa oscila extendiendo y contrayendo la cuerda elástica,")
    print("alcanzando la vertical (θ=0) en {:.4f} s con una longitud de {:.4f} m.".format(t_llegada, r_llegada))