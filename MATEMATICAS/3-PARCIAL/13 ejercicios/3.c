import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Datos completos
years = np.array([1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995])
expenditures = np.array([731, 782, 833, 886, 956, 1049, 1159, 1267, 1367, 1436, 1505])

# Datos para extrapolación
x_data = np.arange(len(years))
y_data = expenditures

# Diferentes métodos
methods = {
    'Lineal': 1,
    'Cuadrático': 2,
    'Cúbico': 3,
    'Grado 4': 4
}

plt.figure(figsize=(12, 6))
plt.scatter(years, expenditures, color='black', s=50, zorder=5, label='Datos reales')
plt.axvline(x=1980, color='red', linestyle='--', alpha=0.5, label='Año 1980')
plt.axhline(y=492, color='green', linestyle='--', alpha=0.5, label='Valor real 1980 (492)')

colors = ['blue', 'orange', 'purple', 'brown']

for (name, degree), color in zip(methods.items(), colors):
    coef = np.polyfit(x_data, y_data, degree)
    poly = np.poly1d(coef)
    
    # Extrapolar a 1980 (índice -5)
    x_1980 = -5
    estimate_1980 = poly(x_1980)
    
    # Curva de ajuste
    x_plot = np.linspace(-5, len(years)-1, 100)
    years_plot = x_plot + 1985
    plt.plot(years_plot, poly(x_plot), color=color, label=f'{name}: {estimate_1980:.0f}', alpha=0.7)
    
    print(f"{name}: Estimación 1980 = {estimate_1980:.2f}")

# Spline cúbico (extrapolación lineal)
spline = CubicSpline(x_data, y_data, bc_type='natural')
x_1980 = -5
estimate_1980_spline = spline(x_1980)
plt.plot(years_plot, spline(x_plot), 'm-', label=f'Spline: {estimate_1980_spline:.0f}', alpha=0.7)
print(f"Spline: Estimación 1980 = {estimate_1980_spline:.2f}")

plt.xlabel('Año')
plt.ylabel('Gastos (billones de dólares)')
plt.title('APP3: Extrapolación hacia atrás a 1980')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(1978, 1997)
plt.tight_layout()
plt.show()