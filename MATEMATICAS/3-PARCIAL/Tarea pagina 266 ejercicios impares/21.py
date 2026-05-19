
# ==============================================================================
# EJERCICIO 21: Circuito eléctrico
# ==============================================================================
def ejercicio21():
    titulo("EJERCICIO 21: Circuito eléctrico")
    print("ATENCIÓN: El enunciado no proporciona todos los valores numéricos para C y L2.")
    print("Se usarán valores hipotéticos para demostrar el método:\n")
    print("  E(t) = 240*sin(120πt) V")
    print("  R = 1.0 Ω")
    print("  L = 0.2e-3 H")
    print("  C = 3.5e-3 F")
    print("  L2 = 0.2e-3 H (asumido igual a L)\n")
    
    # Parámetros
    R = 1.0
    L1 = 0.2e-3
    L2 = 0.2e-3  # Asumido
    C = 3.5e-3
    
    def E(t):
        return 240 * np.sin(120*np.pi*t)
    
    # Sistema de ecuaciones:
    # L1*di1/dt + R*i1 + 2R(i1+i2) = E
    # L2*di2/dt + R*i2 + 2R(i1+i2) + q2/C = E
    # dq2/dt = i2
    
    def circuito(Y, t):
        i1, i2, q2 = Y
        # Resolver sistema lineal para di1/dt y di2/dt
        # L1*di1/dt + 3R*i1 + 2R*i2 = E
        # L2*di2/dt + 2R*i1 + 3R*i2 + q2/C = E
        
        A = np.array([[L1, 0], [0, L2]])
        b = np.array([E(t) - 3*R*i1 - 2*R*i2, 
                      E(t) - 2*R*i1 - 3*R*i2 - q2/C])
        
        sol = np.linalg.solve(A, b)
        di1 = sol[0]
        di2 = sol[1]
        
        return [di1, di2, i2]
    
    t = np.linspace(0, 0.05, 500)
    Y0 = [0, 0, 0]
    sol = odeint(circuito, Y0, t)
    
    i1 = sol[:,0]
    i2 = sol[:,1]
    
    print("Valores de corrientes en diferentes tiempos:")
    for i in range(0, len(t), 50):
        print(f"  t={t[i]:.4f}s: i1={i1[i]:.4f}A, i2={i2[i]:.4f}A")
    
    plt.figure()
    plt.plot(t, i1, label='i1(t)')
    plt.plot(t, i2, label='i2(t)')
    plt.title('Ejercicio 21: Corrientes en el circuito')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Corriente (A)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print("\nCONCLUSIÓN: Las corrientes i1 e i2 muestran un comportamiento transitorio")
    print("que tiende a estabilizarse en una oscilación forzada por E(t).")
    print("Se observa que i1 e i2 tienen amplitudes y fases diferentes debido a la")
    print("presencia del capacitor en la segunda rama.")

# ==============================================================================
# MAIN: Ejecutar todos los ejercicios
# ==============================================================================

print("INICIANDO RESOLUCIÓN DE EJERCICIOS IMPARES")
print("="*80)

ejercicio1()
ejercicio3()
ejercicio5()
ejercicio7()
ejercicio9()
ejercicio11()
ejercicio13()
ejercicio15()
ejercicio17()
ejercicio19()
ejercicio21()

print("\n" + "="*80)
print(" TODOS LOS EJERCICIOS HAN SIDO PROCESADOS ")
print("="*80)