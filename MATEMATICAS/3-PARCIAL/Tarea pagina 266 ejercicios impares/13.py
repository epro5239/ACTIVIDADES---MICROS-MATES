
# ==============================================================================
# EJERCICIO 13: Proyectil con arrastre aerodinámico
# ==============================================================================
def ejercicio13():
    titulo("EJERCICIO 13: Proyectil con arrastre")
    print("Ecuaciones:")
    print("  x'' = -(CD/m)*v^(1/2)*x'")
    print("  y'' = -(CD/m)*v^(1/2)*y' - g")
    print("Datos: m=0.25kg, CD=0.03, v0=50m/s, ángulo=30°, g=9.80665\n")
    
    m = 0.25
    CD = 0.03
    g = 9.80665
    v0 = 50
    angulo = np.radians(30)
    
    vx0 = v0 * np.cos(angulo)
    vy0 = v0 * np.sin(angulo)
    
    print("Condiciones iniciales:")
    print(f"  vx0 = {vx0:.4f} m/s")
    print(f"  vy0 = {vy0:.4f} m/s")
    
    def sistema(Y, t):
        x, y, vx, vy = Y
        v = np.sqrt(vx**2 + vy**2)
        ax = -(CD/m)*np.sqrt(v)*vx
        ay = -(CD/m)*np.sqrt(v)*vy - g
        return [vx, vy, ax, ay]
    
    t = np.linspace(0, 5, 1000)
    Y0 = [0, 0, vx0, vy0]
    sol = odeint(sistema, Y0, t)
    
    x = sol[:,0]
    y = sol[:,1]
    
    # Encontrar impacto
    idx_impacto = np.where(y < 0)[0]
    if len(idx_impacto) > 0:
        i = idx_impacto[0]
        t_vuelo = t[i]
        alcance = x[i]
        altura_max = np.max(y)
        
        print(f"\nResultados de la trayectoria:")
        print(f"  Tiempo de vuelo: {t_vuelo:.4f} s")
        print(f"  Alcance R: {alcance:.4f} m")
        print(f"  Altura máxima: {altura_max:.4f} m")
        
        # Mostrar algunos puntos intermedios
        print("\nPuntos intermedios de la trayectoria:")
        for j in range(0, len(t), 100):
            if j < len(t):
                print(f"  t={t[j]:.3f}s, x={x[j]:.3f}m, y={y[j]:.3f}m")
    
    plt.figure()
    plt.plot(x, y)
    plt.title('Ejercicio 13: Proyectil con arrastre')
    plt.xlabel('Alcance x (m)')
    plt.ylabel('Altura y (m)')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    
    print("\nCONCLUSIÓN: El arrastre reduce significativamente el alcance y la altura máxima")
    print("en comparación con el caso ideal sin fricción. Con los datos dados,")
    print("el proyectil impacta a {:.2f} m de distancia después de {:.2f} s.".format(alcance, t_vuelo))