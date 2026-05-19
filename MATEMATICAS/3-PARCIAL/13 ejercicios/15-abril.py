import math
 
def divided_differences(x, f):
    n = len(x)
    table = [[0 for _ in range(n)] for _ in range(n)]
 
    # Primera columna
    for i in range(n):
        table[i][0] = f[i]
 
    # Construcción de la tabla
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])
 
    return table
 
 
def print_divided_table(x, table):
    n = len(x)
 
    # Encabezados
    print(f"{'i':^5}{'xi':^10}{'fi':^12}", end="")
    for j in range(1, n):
        print(f"{'f[xi,...,xi+'+str(j)+']':^18}", end="")
    print()
 
    # Filas
    for i in range(n):
        print(f"{i:^5}{x[i]:^10.2f}", end="")
 
        for j in range(n):
            if j == 0:
                print(f"{table[i][j]:^12.4f}", end="")
            elif i < n - j:
                print(f"{table[i][j]:^18.4f}", end="")
            else:
                print(" " * 18, end="")
        print()
x = [1.70, 1.80, 2.00, 2.35, 2.50]
f = [math.exp(xi)*math.sin(xi) for xi in x]
 
table = divided_differences(x, f)
print_divided_table(x, table)