import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, CubicSpline
from scipy.optimize import curve_fit

# Datos
years = np.array([1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995])
expenditures = np.array([731, 782, 833, 886, 956, 1049, 1159, 1267, 1367, 1436, 1505])

# Datos para interpolación (1991-1994)
x_data = np.array([0, 1, 2, 3])  # 1991=0, 1992=1, etc.
y_data = np.array([1159, 1267, 1367, 1436])

# a) Polinomio cúbico interpolante
coef_cubic = np.polyfit(x_data, y_data, 3)
poly_cubic = np.poly1d(coef_cubic)
estimate_1995_cubic = poly_cubic(4)
print(f"a) Cúbico interpolante - Estimación 1995: {estimate_1995_cubic:.2f}")

# b) Línea de mínimos cuadrados
coef_linear = np.polyfit(x_data, y_data, 1)
poly_linear = np.poly1d(coef_linear)
estimate_1995_linear = poly_linear(4)
print(f"b) Línea mínimos cuadrados - Estimación 1995: {estimate_1995_linear:.2f}")

# c) Cuadrática de mínimos cuadrados
coef_quad = np.polyfit(x_data, y_data, 2)
poly_quad = np.poly1d(coef_quad)
estimate_1995_quad = poly_quad(4)
print(f"c) Cuadrática mínimos cuadrados - Estimación 1995: {estimate_1995_quad:.2f}")

# d) Spline cúbico
spline = CubicSpline(x_data, y_data, bc_type='natural')
estimate_1995_spline = spline(4)
print(f"d) Spline cúbico - Estimación 1995: {estimate_1995_spline:.2f}")

# Proyección al 2000
x_2000 = 9  # 1991 + 9 = 2000
proj_cubic = poly_cubic(x_2000)
proj_linear = poly_linear(x_2000)
proj_quad = poly_quad(x_2000)
proj_spline = spline(x_2000)

print(f"\nProyecciones al 2000:")
print(f"Cúbico: {proj_cubic:.2f}")
print(f"Lineal: {proj_linear:.2f}")
print(f"Cuadrático: {proj_quad:.2f}")
print(f"Spline: {proj_spline:.2f}")
print(f"Valor real 2000: 1789 billones")

# Gráfica
plt.figure(figsize=(12, 6))
x_plot = np.linspace(0, 15, 100)
years_plot = x_plot + 1991

plt.scatter(years, expenditures, color='black', s=50, label='Datos reales')
plt.plot(years_plot, poly_cubic(x_plot), 'b-', label='Cúbico interpolante', alpha=0.7)
plt.plot(years_plot, poly_linear(x_plot), 'r--', label='Línea MC', alpha=0.7)
plt.plot(years_plot, poly_quad(x_plot), 'g--', label='Cuadrática MC', alpha=0.7)
plt.plot(years_plot, spline(x_plot), 'm-', label='Spline cúbico', alpha=0.7)

plt.axvline(x=1995, color='gray', linestyle=':', alpha=0.5)
plt.axhline(y=1505, color='gray', linestyle=':', alpha=0.5)
plt.scatter([1995], [estimate_1995_cubic], color='blue', s=100, marker='s')
plt.scatter([1995], [estimate_1995_linear], color='red', s=100, marker='^')
plt.scatter([1995], [estimate_1995_quad], color='green', s=100, marker='d')
plt.scatter([1995], [estimate_1995_spline], color='magenta', s=100, marker='*')

plt.xlabel('Año')
plt.ylabel('Gastos (billones de dólares)')
plt.title('APP2: Estimación de gastos gubernamentales')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()