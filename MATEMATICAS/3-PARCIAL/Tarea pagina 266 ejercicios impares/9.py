
# ==============================================================================
# EJERCICIO 9: Masa-resorte con P(t) variable
# ==============================================================================
def ejercicio9():
    titulo("EJERCICIO 9: Masa-resorte con fuerza variable")
    print("Ecuación: y'' = P(t)/m - (k/m)y")
    print("Datos: m = 2.5 kg, k = 75 N/m, y(0) = 0, y'(0) = 0")
    print("Fuerza P(t): 10t para t < 2s, 20N para t ≥ 2s\n")
    
    m = 2.5
    k = 75
    
    def P(t):
        if t < 2:
            return 10*t
        else:
            return 20
    
    def sistema(y, t):
        pos, vel = y
        dpos = vel
        dvel = P(t)/m - (k/m)*pos
        return [dpos, dvel]
    
    t = np.linspace(0, 5, 1000)
    y0 = [0, 0]
    sol = odeint(sistema, y0, t)
    
    despl = sol[:,0]
    max_despl = np.max(despl)
    
    print(f"Evaluación de P(t) en algunos puntos:")
    for t_test in [0, 1, 1.5, 2, 3]:
        print(f"  P({t_test}) = {P(t_test)} N")
    
    print(f"\nDesplazamiento máximo encontrado: {max_despl:.6f} m")
    
    plt.figure()
    plt.plot(t, despl)
    plt.axhline(y=max_despl, color='r', linestyle='--', label=f'Máx = {max_despl:.4f}')
    plt.axvline(x=2, color='g', linestyle='--', label='P(t) cambia en t=2')
    plt.title('Ejercicio 9: Masa-resorte con fuerza variable')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Desplazamiento (m)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print("\nCONCLUSIÓN: La masa alcanza un desplazamiento máximo de {:.6f} m".format(max_despl))
    print("El cambio brusco de P(t) en t=2 genera una respuesta dinámica visible.")