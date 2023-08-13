import matplotlib.pyplot as plt
from matplotlib import collections as mc
from matplotlib.widgets import RadioButtons, Slider, TextBox
import numpy as np
import mpld3

from data import *
from math_utils import *

PLANETS = {
    "Mercury": 0,
    "Venus": 1,
    "Earth": 2,
    "Mars": 3,
    "Jupiter": 4,
    "Saturn": 5,
    "Uranus": 6,
    "Neptune": 7,
    "Pluto": 8
}

N = 10 # Number of orbits of PLANET_B
PLANET_A = 7
PLANET_B = 8 # PLANET_B > PLANET_A

fig = plt.figure()
ax = fig.add_subplot()
lc = mc.LineCollection([])
ax.add_collection(lc)
fig.subplots_adjust(left=0.25)

allowed_planets = [0, 1, 2, 3, 4, 5, 6, 7, 8]
ax_p1 = fig.add_axes([0.02, 0.25, 0.0725, 0.63])
ax_p2 = fig.add_axes([0.1, 0.25, 0.0725, 0.63])
axbox = fig.add_axes([0.02, 0.2, 0.15, 0.04])
text_box = TextBox(axbox, '', initial="10")

sp1 = RadioButtons(ax_p1, NAMES)
sp2 = RadioButtons(ax_p2, NAMES)

p1l = None
p2l = None

def update(_):
    global lc
    global p1l
    global p2l
    lc.remove()
    if p1l is not None and p2l is not None:
        p1l.remove()
        p2l.remove()

    PLANET_A = PLANETS[sp1.value_selected]
    PLANET_B = PLANETS[sp2.value_selected]
    try:
        N = int(text_box.text)
    except Exception:
        N = 10

    data = []
    for time_elapsed in np.linspace(0, ORBITAL_PERIOD[PLANET_B] * N, 1234):
        theta = (2*np.pi * time_elapsed) / ORBITAL_PERIOD[PLANET_A]
        x_a, y_a = calculate_xy(theta, SEMI_MAJOR_AXIS[PLANET_A], ECCENTRICITY[PLANET_A])
        theta = (2*np.pi * time_elapsed) / ORBITAL_PERIOD[PLANET_B]
        x_b, y_b = calculate_xy(theta, SEMI_MAJOR_AXIS[PLANET_B], ECCENTRICITY[PLANET_B])
        data.append([(x_a, y_a), (x_b, y_b)])

    def plot_orbit(semi_major_axis, eccentricity, color, label):
        points_x = []
        points_y = []
        for theta in np.linspace(0, 2*np.pi, 5000):
            x, y = calculate_xy(theta, semi_major_axis, eccentricity)
            points_x.append(x)
            points_y.append(y)
        return ax.plot(points_x, points_y, color=color, label=label)

    p1l, = plot_orbit(SEMI_MAJOR_AXIS[PLANET_A], ECCENTRICITY[PLANET_A], COLORS[PLANET_A], NAMES[PLANET_A])
    p2l, = plot_orbit(SEMI_MAJOR_AXIS[PLANET_B], ECCENTRICITY[PLANET_B], COLORS[PLANET_B], NAMES[PLANET_B])

    lc = mc.LineCollection(data, linewidths=0.2, color="#000000")
    ax.add_collection(lc)
    ax.legend()
    fig.canvas.draw_idle()

update(10)
sp1.on_clicked(update)
sp2.on_clicked(update)
text_box.on_text_change(update)

#ax.grid(color='lightgray', linestyle='-')
# plt.xlabel("x / Au")
# plt.ylabel("y / Au")
#plt.gca().set_aspect('equal')

#plt.show()
#mpld3.show()
mpld3.save_html(fig, "result.html")

