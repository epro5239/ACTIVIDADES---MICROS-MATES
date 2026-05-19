import numpy as np
#creamos una matrix 
np.set_printoptions(precision=3, suppress=1, floatmode='fixed') #para mostrar solo 2 decimales

A= np.array([[1,2,3,4],[-2,4,-3,5],[-1,3,-3,4]])

print("A =")
print(A)

#obtenemos la transpuesta de A
m,n =np.shape(A)
print("filas = {}, columnas = {}"
.format(m,n))

#accedemos a la segunda fila y tercer columna 
a23 = A[1,2]
print("El valor de la segunda fila y tercer columna es" , a23)

#Encontramos la tercera fila de la matriz 
fila3 =A[2,:]
print("La tercera fila de la matriz es" , fila3)

#encontramos la segunda columna de la matriz 
columna2= A[:,1]
print("La segunda columna de la matriz es" , columna2)

B=A

#cambiamos los valores de B
B[0,0]=2

print("B =")
print(B)

print("A =")
print(A)

#Para crear una copia de A y modificarla sin afectar a A, usamos la función copy()
B = A.copy()
B[0,0] = 2


print("B =")
print(B)

print("A =")
print(A)


#operaciones: suma y resta de matrices
x = np.array([[1,2],[3,4]])
y = np.array([[-1,3],[2,-5]])

print("x =")
print(x)
print("y =")
print(y)

#hacemos suma de x e y
suma = x + y    
print("La suma de x e y es:")
print(suma)

      
#hacemos resta de x e y
resta = x - y    
print("La resta de x e y es:")
print(resta)

#operaciones basicas: multiplicacion de matrices
#hacemos la multiplicacion de x e y
multi = x * y    
print("La multiplicacion de x e y es:")
print(multi)

#operaciones basicas: multiplicacion de matrices
#hacemos la division de x e y
div = x / y    
print("La division de x e y es:")
print(div)

#multiplicacion escalar con matriz
escalar = 10
multi_escalar = escalar * x
print("La multiplicacion de x por el escalar es:")
print(multi_escalar)

#producto punto de A con B
A = np.array([[1,2,3],[-1,2,-3]])
B = np.array([[1,2],[0,4],[-3,2]])
producto_punto = np.dot(A,B)
print("A =")
print(A)
print("B =")
print(B)
print("El producto punto de A con B es:")
print(producto_punto)

#Tarea 5 multiplicaciones producto punto
C = np.array([[1,0,2],[-1,3,1],])
D = np.array([[2,1],[0,-1],[1,2]])
producto_punto_CD = np.dot(C,D)     
print("C =")
print(C)    
print("D =")
print(D)        
print("El producto punto de C con D es:")
print(producto_punto_CD)

E = np.array([[1,2,3],[0,-1,0],[-2,1,0]])
F = np.array([[2,0,1],[-1,3,2],[0,1,4]])
producto_punto_EF = np.dot(E,F)     
print("E =")
print(E)    
print("F =")
print(F)        
print("El producto punto de E con F es:")
print(producto_punto_EF)

G = np.array([[1,0,2],[-1,3,1],[0,2,-1]])
H = np.array([[2,1],[0,-1],[1,2]])          
producto_punto_GH = np.dot(G,H)
print("G =")
print(G)
print("H =")
print(H)
print("El producto punto de G con H es:")
print(producto_punto_GH)

I = np.array([[1,2,3],[0,-1,0],[-2,1,0]])
J = np.array([[2,0,1],[-1,3,2],[0,1,4]])
producto_punto_IJ = np.dot(I,J) 
print("I =")
print(I)
print("J =")
print(J)
print("El producto punto de I con J es:")
print(producto_punto_IJ)    

#---------------------------------------------------
#----------MATRIZ IDENTIDAD ------------------------

I3 = np.array([[1,0,0],[0,1,0],[0,0,1]])
I2 = np.array([[1,0],[0,1]])

D1 = np.dot(I2,A)
print("El producto punto de I POR A es:")
print(D1)

#---------------------------------------------------
#----------------INVERSA DE UNA MATRIZ -------------

MAT = np.array([[1,2,3],[-1,2,-3],[0,2,5]])
print("la matriz es:")
print(MAT)

MAT_INV = np.linalg.inv(MAT)
print("La inversa de la matriz es:")
print(MAT_INV)

#Verificamos que la inversa sea correcta invirtiendola para regresar a la matriz original

MAT2_INV = np.linalg.inv(MAT_INV)
print("La inversa de la inversa de la matriz es:")
print(MAT2_INV)

#Multiplicando la inversa con la matriz para obtener la matriz identidad

Identi = np.dot(MAT, MAT_INV)
print("El producto punto de la matriz con su inversa es:")
print(Identi)

#-----------------------------------
#-----------------------------------
#------EJERCICIO--------------------
#-----------------------------------

