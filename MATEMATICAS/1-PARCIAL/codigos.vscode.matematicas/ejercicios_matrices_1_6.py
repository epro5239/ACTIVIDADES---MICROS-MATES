import numpy as np

np.set_printoptions(precision=3, suppress=True)

print("="*60)
print("EJERCICIO 1 - CREACIÓN DE MATRICES")
print("="*60)

A = np.array([[1, -2, 3],
              [2, 1, 4],
              [3, -1, -2]])

B = np.array([[0, 4, 2],
              [3, -1, -3]])

C = np.array([[-2, 1],
              [0, -1],
              [1, 3]])

D = np.array([[1, -3, 0],
              [2, -2, 2],
              [3, -1, 1]])

print("A=\n", A)
print("B=\n", B)
print("C=\n", C)
print("D=\n", D)

print("\nOPERACIONES:")

def intentar_operacion(nombre, operacion):
    try:
        print(f"\n{nombre} =")
        print(operacion())
    except:
        print(f"\n{nombre} no está definida.")


intentar_operacion("A + D", lambda: A + D)
intentar_operacion("D - A", lambda: D - A)
intentar_operacion("3B", lambda: 3*B)
intentar_operacion("A + B", lambda: A + B)
intentar_operacion("A * D (element-wise)", lambda: A * D)
intentar_operacion("A * C (element-wise)", lambda: A * C)
intentar_operacion("A / D", lambda: A / D)
intentar_operacion("A / B", lambda: A / B)
intentar_operacion("AD (multiplicación matricial)", lambda: A @ D)
intentar_operacion("AB (multiplicación matricial)", lambda: A @ B)
intentar_operacion("BC (multiplicación matricial)", lambda: B @ C)

# ==========================================================
print("\n" + "="*60)
print("EJERCICIO 2 - INVERSA DE A")
print("="*60)

A_inv = np.linalg.inv(A)
print("A_inv =")
print(A_inv)

print("\nVerificación AA_inv =")
print(A @ A_inv)

# ==========================================================
print("\n" + "="*60)
print("EJERCICIO 3 - ECUACIONES LINEALES")
print("="*60)

ecuaciones = {
    "2x - y = 7": True,
    "3x - 4 + 2z = 3y": True,
    "4√x - 2y = 10": False,
    "z/x - 4y + z = 6": False,
    "3xy - 2y + z = 4": False,
    "-x + 3y - sin(z) = 2": False
}

for eq, es_lineal in ecuaciones.items():
    print(f"{eq} -> {'Lineal' if es_lineal else 'No lineal'}")

# ==========================================================
print("\n" + "="*60)
print("EJERCICIO 4 - SISTEMA 2x2")
print("="*60)

A4 = np.array([[2, -1],
               [3, 2]])

b4 = np.array([5, 4])

sol4 = np.linalg.solve(A4, b4)
print("Solución:", sol4)

# ==========================================================
print("\n" + "="*60)
print("EJERCICIO 5 - SISTEMA 4x4")
print("="*60)

A5 = np.array([
    [1, -3, 2, -1],
    [2, -4, 5, 2],
    [-1, 3, -1, 3],
    [3, 2, -1, -1]
])

b5 = np.array([6, 13, -23, 6])

sol5 = np.linalg.solve(A5, b5)

print(f"x = {sol5[0]:.3f}")
print(f"y = {sol5[1]:.3f}")
print(f"z = {sol5[2]:.3f}")
print(f"w = {sol5[3]:.3f}")

# ==========================================================
print("\n" + "="*60)
print("EJERCICIO 6 - SISTEMA 3x3")
print("="*60)

A6 = np.array([
    [1, -3, 2],
    [2, -4, 5],
    [-1, 3, -2]
])

b6 = np.array([6, 13, -23])

try:
    sol6 = np.linalg.solve(A6, b6)
    print("Solución única:", sol6)
except:
    rango = np.linalg.matrix_rank(A6)
    rango_ext = np.linalg.matrix_rank(np.column_stack((A6, b6)))
    
    print("El sistema no tiene solución única.")
    print("Rango A =", rango)
    print("Rango matriz aumentada =", rango_ext)
    
    if rango == rango_ext:
        print("Sistema compatible indeterminado (infinitas soluciones).")
    else:
        print("Sistema incompatible (sin solución).")