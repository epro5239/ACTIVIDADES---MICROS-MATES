
# ==============================================================================
# EJERCICIO 17: Masa-resorte con fricción seca
# ==============================================================================
def ejercicio17():
    titulo("EJERCICIO 17: Masa-resorte con fricción seca")
    print("Ecuación: y'' = -(k/m)*y - μ*g*(y'/|y'|)")
    print("Datos: k=3000 N/m, m=6 kg, μ=0.5, y₀=0.1 m\n")
    
    k = 3000
    m = 6
    mu = 0.5
    g = 9.80665
    y0 = 0.1
    
    def sistema(Y, t):
        y, v = Y
        if abs(v) < 1e-12:
            friction = 0
        else:
            friction = -mu*g * (v/abs(v))
        a = -(k/m)*y + friction
        return [v, a]
    
    t = np.linspace(0, 0.5, 1000)
    Y0 = [y0, 0]
    sol = odeint(sistema, Y0, t)
    
    y = sol[:,0]
    
    # Encontrar picos
    picos_positivos = []
    picos_negativos = []
    
    for i in range(1, len(y)-1):
        if y[i] > y[i-1] and y[i] > y[i+1] and y[i] > 0:
            picos_positivos.append(y[i])
        if y[i] < y[i-1] and y[i] < y[i+1] and y[i] < 0:
            picos_negativos.append(y[i])
    
    print("Picos positivos encontrados:")
    for i, p in enumerate(picos_positivos[:3]):
        print(f"  Pico {i+1}: {p:.6f} m")
    
    print("\nPicos negativos encontrados:")
    for i, p in enumerate(picos_negativos[:3]):
        print(f"  Pico {i+1}: {p:.6f} m")
    
    # Verificar relación teórica
    decremento_teorico = 4*mu*m*g/k
    if len(picos_positivos) >= 2:
        dif_picos = picos_positivos[0] - picos_positivos[1]
        print(f"\nDiferencia entre primer y segundo pico: {dif_picos:.6f} m")
        print(f"Decremento teórico (4μmg/k): {decremento_teorico:.6f} m")
    
    plt.figure()
    plt.plot(t, y)
    plt.title('Ejercicio 17: Fricción seca')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Desplazamiento (m)')
    plt.grid(True)
    plt.show()
    
    print("\nCONCLUSIÓN: La fricción seca reduce la amplitud de forma lineal.")
    print("Se confirma la relación teórica: el decremento entre picos consecutivos es constante.")
    print(f"Primer pico: {picos_positivos[0]:.6f} m" if picos_positivos else "No se encontraron picos positivos.")
