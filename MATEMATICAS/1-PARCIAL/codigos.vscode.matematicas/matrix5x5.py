import numpy as np

# Una sola matriz 5x5
A = np.array([
    [2, 1, 0, 0, 1],
    [1, 3, 1, 0, 0],
    [0, 1, 4, 1, 0],
    [0, 0, 1, 3, 1],
    [1, 0, 0, 1, 2]
])
B= np.array([
    [2, 0, 0, 0, 0],
    [0, 3, 0, 0, 0],
    [0, 0, 4, 0, 0],
    [0, 0, 0, 2, 0],
    [0, 0, 0, 0, 3]
])

print("Matriz original 1 (a):")
print(A)
A_inversa = np.linalg.inv(A)
print("\nMatriz inversa:")
print(A_inversa)

print("Matriz original 2 (b)")
print(B)
B_inversa = np.linalg.inv(B)
print("\nMatriz inversa:")
print(B_inversa)