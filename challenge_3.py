import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

from data import *
from math_utils import *

# Use 2, 0, 4 for inner planets
# Use 4, 4, 9 for outer planets
TARGET_PLANET = 4
START_PLANET = 4
END_PLANET = 9

ANIMATION_SPEED = ORBITAL_PERIOD[TARGET_PLANET]

fig = plt.figure()
ax = fig.add_subplot()
ax.grid(color='lightgray', linestyle='--')

planets = [(), (), (), (), (), (), (), (), ()]
for i in range(START_PLANET, END_PLANET):
    orbit_x = []
    orbit_y = []
    for theta in np.linspace(0, 2*np.pi, 500):
        x, y = calculate_xy(theta, SEMI_MAJOR_AXIS[i], ECCENTRICITY[i])
        orbit_x.append(x)
        orbit_y.append(y)

    point, = ax.plot([], [], marker="o", markersize=4, color=COLORS[i])
    ax.plot(orbit_x, orbit_y, color=COLORS[i], label=NAMES[i])
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
        x, y = calculate_xy(theta, SEMI_MAJOR_AXIS[index], ECCENTRICITY[index])
        planets[index].set_data([x], [y])
        return planets[index],
    return update

animations = []
for i in range(START_PLANET, END_PLANET):
    ani = FuncAnimation(fig, create_update(i), frames=[0], init_func=create_init(i), blit=True, interval=1)
    animations.append(ani)

plt.legend()
plt.gca().set_aspect('equal')
plt.xlabel("(Au)")
plt.show()
