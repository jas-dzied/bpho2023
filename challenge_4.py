import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

from data import *
from math_utils import *

# Use 2, 0, 4 for inner planets
# Use 4, 4, 9 for outer planets
TARGET_PLANET = 2
START_PLANET = 0
END_PLANET = 4

ANIMATION_SPEED = ORBITAL_PERIOD[TARGET_PLANET]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.grid(color='lightgray', linestyle='--')

planets = [(), (), (), (), (), (), (), (), ()]
for i in range(START_PLANET, END_PLANET):
    orbit_x = []
    orbit_y = []
    orbit_z = []
    for theta in np.linspace(0, 2*np.pi, 500):
        x, y, z = calculate_xyz(theta, SEMI_MAJOR_AXIS[i], ECCENTRICITY[i], BETA[i])
        orbit_x.append(x)
        orbit_y.append(y)
        orbit_z.append(z)

    point, = ax.plot([], [], [], marker="o", markersize=4, color=COLORS[i])
    ax.plot(orbit_x, orbit_y, orbit_z, color=COLORS[i], label=NAMES[i])
    planets[i] = point

# Sun
plt.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)

start_time = time.time()

def create_init(index):
    def init():
        return planets[index],
    return init

def create_update(index):
    def update(_):
        time_elapsed = (time.time_ns() - start_time) / 1000000000
        theta = (2*np.pi * time_elapsed) * ANIMATION_SPEED / ORBITAL_PERIOD[index]
        x, y, z = calculate_xyz(theta, SEMI_MAJOR_AXIS[index], ECCENTRICITY[index], BETA[index])
        planets[index].set_data([x], [y])
        planets[index].set_3d_properties([z])
        return planets[index],
    return update

animations = []
for i in range(START_PLANET, END_PLANET):
    ani = FuncAnimation(fig, create_update(i), frames=[0], init_func=create_init(i), blit=True, interval=1)
    animations.append(ani)

ax.set_xlabel("x / Au")
ax.set_ylabel("y / Au")
ax.set_zlabel("z / Au")
ax.legend()
plt.show()
