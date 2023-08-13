import matplotlib.pyplot as plt
import numpy as np

from data import *
from math_utils import *

# Use 2, 0, 4 for inner planets
# Use 5, 4, 9 for outer planets
TARGET_PLANET = 5
START_PLANET = 4
END_PLANET = 9

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.grid(color='lightgray', linestyle='--')

for i in range(START_PLANET, END_PLANET):
    data_x = []
    data_y = []
    data_z = []
    for time_elapsed in np.linspace(0.0, ORBITAL_PERIOD[TARGET_PLANET] * 50, 10000):

        theta = (2*np.pi * time_elapsed) / ORBITAL_PERIOD[i]
        x, y, z = calculate_xyz(theta, SEMI_MAJOR_AXIS[i], ECCENTRICITY[i], BETA[i])

        theta = (2*np.pi * time_elapsed) / ORBITAL_PERIOD[TARGET_PLANET]
        target_x, target_y, target_z = calculate_xyz(theta, SEMI_MAJOR_AXIS[TARGET_PLANET], ECCENTRICITY[TARGET_PLANET], BETA[TARGET_PLANET])

        relative_x = x - target_x
        relative_y = y - target_y
        relative_z = z - target_z

        data_x.append(relative_x)
        data_y.append(relative_y)
        data_z.append(relative_z)

    ax.plot(data_x, data_y, data_z, color=COLORS[i], label=NAMES[i], linewidth=0.4)

# Plot sun
data_x = []
data_y = []
data_z = []
for time_elapsed in np.linspace(0.0, ORBITAL_PERIOD[TARGET_PLANET] * 50, 10000):
    theta = (2*np.pi * time_elapsed) / ORBITAL_PERIOD[TARGET_PLANET]
    target_x, target_y, target_z = calculate_xyz(theta, SEMI_MAJOR_AXIS[TARGET_PLANET], ECCENTRICITY[TARGET_PLANET], BETA[TARGET_PLANET])
    relative_x = -target_x
    relative_y = -target_y
    relative_z = -target_z
    data_x.append(relative_x)
    data_y.append(relative_y)
    data_z.append(relative_z)
ax.plot(data_x, data_y, data_z, color="y", label="Sun", linewidth=1)

ax.plot([0.0], [0.0], marker="o", markersize=4, color=COLORS[TARGET_PLANET])

ax.legend()
plt.gca().set_aspect('equal')
plt.show()
