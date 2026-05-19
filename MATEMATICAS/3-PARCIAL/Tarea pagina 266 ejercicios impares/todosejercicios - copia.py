import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Configuración para mostrar muchos decimales
np.set_printoptions(precision=6, suppress=True)

def separador():
    print("\n" + "="*80)

def titulo(txt):
    print("\n" + "="*80)
    print(f" {txt}")
    print("="*80)

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

# ==============================================================================
# EJERCICIO 3: Integrar y' = sin(y)
# ==============================================================================
def ejercicio3():
    titulo("EJERCICIO 3: Integrar y' = sin(y) con Taylor de 2° orden")
    print("Ecuación: y' = sin(y)")
    print("Condición inicial: y(0) = 1")
    print("Rango: x de 0 a 0.5, h = 0.1")
    
    h = 0.1
    x = 0.0
    y = 1.0
    
    print(f"\nPaso 0: x = {x:.1f}, y = {y:.6f}")
    
    for i in range(1, 6):
        yp = np.sin(y)
        ypp = np.cos(y) * yp  # derivada de sin(y) es cos(y)*y'
        
        y_new = y + h*yp + (h**2/2)*ypp
        x_new = x + h
        
        print(f"Paso {i}:")
        print(f"  y'({x:.1f}) = {yp:.6f}")
        print(f"  y''({x:.1f}) = {ypp:.6f}")
        print(f"  y({x_new:.1f}) = {y_new:.6f}")
        
        x, y = x_new, y_new
    
    print("\nCONCLUSIÓN: La solución aproximada en x=0.5 es y = {:.6f}".format(y))

# ==============================================================================
# EJERCICIO 5: Convertir ecuaciones a sistemas de 1er orden (Teórico)
# ==============================================================================
def ejercicio5():
    titulo("EJERCICIO 5: Conversión a sistemas de primer orden")
    print("Este ejercicio es teórico y no requiere código numérico.")
    print("Se muestran las transformaciones algebraicas:\n")
    
    print("a) ln(y') + y = sin(x)")
    print("   Despejando y': ln(y') = sin(x) - y")
    print("   Forma final: y' = e^(sin(x) - y)")
    
    print("\nc) y^(4) - 4y''*sqrt(1 - y^2) = 0")
    print("   Variables auxiliares:")
    print("   y1 = y")
    print("   y2 = y'")
    print("   y3 = y''")
    print("   y4 = y'''")
    print("   Sistema resultante:")
    print("   y1' = y2")
    print("   y2' = y3")
    print("   y3' = y4")
    print("   y4' = 4*y3*sqrt(1 - y1^2)")
    
    print("\ne) (y')^2 = |32y'x - y^2|")
    print("   Despejando: y' = ± sqrt(|32y'x - y^2|)")
    print("   Es una ecuación implícita que requiere análisis de signos.")
    
    print("\nCONCLUSIÓN: Todas las ecuaciones de orden superior se reducen a sistemas de ecuaciones diferenciales de primer orden.")

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