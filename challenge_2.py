import matplotlib.pyplot as plt
import numpy as np
from math import pi

from data import *
from math_utils import *

# Use 0, 4 for inner planets
# Use 4, 9 for outer planets
START_PLANET = 4
END_PLANET = 9

def plot_orbit(semi_major_axis, eccentricity, color, label):
    points_x = []
    points_y = []
    for theta in np.linspace(0, 2*pi, 5000):
        x, y = calculate_xy(theta, semi_major_axis, eccentricity)
        points_x.append(x)
        points_y.append(y)
    plt.plot(points_x, points_y, color=color, label=label)
    plt.grid(color='lightgray', linestyle='--')

for i in range(START_PLANET, END_PLANET):
    plot_orbit(SEMI_MAJOR_AXIS[i], ECCENTRICITY[i], COLORS[i], NAMES[i])

plt.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)
plt.legend()
plt.gca().set_aspect('equal')
plt.show()
