import matplotlib.pyplot as plt
import numpy as np

from data import *
from math_utils import *

# Use 8 for pluto
PLANET = 8

PLANET_ECCENTRICITY = ECCENTRICITY[PLANET]
PLANET_ORBITAL_PERIOD = ORBITAL_PERIOD[PLANET]

# Straight line approximation
polar_angles = []
times = []

for theta in np.linspace(0.0, 25.0, 200):
    time = PLANET_ORBITAL_PERIOD * (theta / (2*np.pi))
    polar_angles.append(theta)
    times.append(time)

x_data = []
y_data = []
for time in np.linspace(0.0, PLANET_ORBITAL_PERIOD * 3, 1000):
    x_data.append(time)
    y_data.append(np.interp(time, times, polar_angles))
plt.plot(x_data, y_data, label="Orbit without eccentricity")

# Accurate plot
polar_angles = []
times = []

for theta in np.linspace(0.0, 6 * np.pi, 200):

    f = lambda x: 1 / ((1 - PLANET_ECCENTRICITY * np.cos(x))**2)

    time = 1
    time *= PLANET_ORBITAL_PERIOD
    time *= ((1 - PLANET_ECCENTRICITY**2)**(3/2))
    time *= (1/(2*np.pi))
    time *= simpsons_integral(0.0, theta, 0.001, f)

    polar_angles.append(theta)
    times.append(time)

x_data = []
y_data = []
for time in np.linspace(0.0, PLANET_ORBITAL_PERIOD * 3.0, 1000):
    x_data.append(time)
    y_data.append(np.interp(time, times, polar_angles))
plt.plot(x_data, y_data, color="r", label="Orbit with eccentricity")

plt.grid(color='lightgray', linestyle='--')
plt.xlabel("time /years")
plt.ylabel("orbit polar angle /rad")
plt.legend()
plt.show()
