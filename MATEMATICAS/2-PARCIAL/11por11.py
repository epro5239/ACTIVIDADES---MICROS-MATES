#escribe un codigo para resolver un sistema de ecuaciones 11 por 11 es decir, 11 filas y 11 columnas en una matriz usando el metodo de la inversa, comienzado con la importación de numpy, luego define la matriz A y el vector b, después calcula la inversa de A, multiplica la inversa por b para obtener la solución, y finalmente muestra los resultados y una verificación del sistema.
import numpy as np  
import sympy as sp

# Definir la matriz A (11x11) y el vector b (11x1)
A = np.array([[2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [-1, 2, -1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, -1, 2, -1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, -1, 2, -1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, -1, 2, -1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, -1, 2, -1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, -1, 2, -1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, -1, 2, -1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0,-1 ,2 , -1 ,0  ],
              [0 , 1,  2 , 3  , 4  , 5  , 6  , 7  ,-1 ,2 ,-1],
              [ 1  , 2  , 3  , 4  , 5  , 6  , 7  , 8  ,-1 ,2 ,-1]])

b = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
# Calcular la inversa de A
A_inv = np.linalg.inv(A)
# Multiplicar la inversa por b para obtener la solución
x = A_inv @ b
# Mostrar los resultados
print("Solución del sistema:")
for i in range(11):
    print(f"x{i+1} = {x[i]:.8f}")
# Verificación del sistema
verif = A @ x
print("\nVerificación (A·x debería ser b):")
for i in range(11):
    print(f"Ecuación {i+1}: {verif[i]:.8f} ≈ {b[i]:.8f} | Error: {abs(verif[i]-b[i]):.2e}")