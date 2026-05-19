
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