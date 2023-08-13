import gi
from matplotlib.animation import FuncAnimation
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, GdkPixbuf
import sys
from enum import Enum

from matplotlib.backends.backend_gtk4agg import (
    FigureCanvasGTK4Agg as FigureCanvas)
from matplotlib.backends.backend_gtk4 import (
    NavigationToolbar2GTK4 as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np
from matplotlib import collections as mc
from matplotlib.widgets import RadioButtons, Slider, TextBox
import time

from data import *
from math_utils import *

css_provider = Gtk.CssProvider()
css_provider.load_from_path('style.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class Screen(Enum):
    About = 1
    Paper = 2
    C1 = 3
    C2 = 4
    C3 = 5
    C4 = 6
    C5 = 7
    C6 = 8
    C7 = 9

class Application(Gtk.ApplicationWindow):
    def draw_c1(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 1")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)

        ax = fig.add_subplot()
        ax.plot([x**(3/2) for x in SEMI_MAJOR_AXIS], ORBITAL_PERIOD, ls='', marker='x')
        ax.plot([0.0, 250.0], [0.0, 250.0], color="r")
        ax.set_xlabel("(a / Au) ^ (3/2)")
        ax.set_ylabel("T / Yr")

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        sw.set_child(canvas)
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c2(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 2")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        self.all_lines = []

        START_PLANET = 4
        END_PLANET = 9

        rax = fig.add_axes([0.02, 0.4, 0.12, 0.2])
        bts = RadioButtons(rax, ["Inner planets", "Outer planets"])
        
        def draw_all(_):

            if bts.value_selected == "Outer planets":
                START_PLANET = 4
                END_PLANET = 9
            else:
                START_PLANET = 0
                END_PLANET = 4

            ax.clear()

            for ln in self.all_lines:
                try:
                    ln.remove()
                except:
                    pass

            def plot_orbit(semi_major_axis, eccentricity, color, label):
                points_x = []
                points_y = []
                for theta in np.linspace(0, 2*np.pi, 5000):
                    x, y = calculate_xy(theta, semi_major_axis, eccentricity)
                    points_x.append(x)
                    points_y.append(y)
                ln, = ax.plot(points_x, points_y, color=color, label=label)
                self.all_lines.append(ln)

            for i in range(START_PLANET, END_PLANET):
                plot_orbit(SEMI_MAJOR_AXIS[i], ECCENTRICITY[i], COLORS[i], NAMES[i])

            ax.grid(color='lightgray', linestyle='--')
            ax.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)
            ax.legend()
            ax.set_aspect('equal')
            fig.canvas.draw_idle()

        bts.on_clicked(draw_all)
        draw_all(10)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        sw.set_child(canvas)
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c3(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 3")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        self.canvas = FigureCanvas(fig)

        rax = fig.add_axes([0.02, 0.4, 0.12, 0.2])
        bts = RadioButtons(rax, ["Inner planets", "Outer planets"])

        def init_all(_):
            ax.clear()
            if bts.value_selected == "Outer planets":
                TARGET_PLANET = 4
                START_PLANET = 4
                END_PLANET = 9
            else:
                TARGET_PLANET = 2
                START_PLANET = 0
                END_PLANET = 4

            ANIMATION_SPEED = ORBITAL_PERIOD[TARGET_PLANET]

            ax.grid(color='lightgray', linestyle='--')

            self.planets = [(), (), (), (), (), (), (), (), ()]
            self.animations = []

            for i in range(START_PLANET, END_PLANET):
                orbit_x = []
                orbit_y = []
                for theta in np.linspace(0, 2*np.pi, 500):
                    x, y = calculate_xy(theta, SEMI_MAJOR_AXIS[i], ECCENTRICITY[i])
                    orbit_x.append(x)
                    orbit_y.append(y)

                point, = ax.plot([], [], marker="o", markersize=4, color=COLORS[i])
                ax.plot(orbit_x, orbit_y, color=COLORS[i], label=NAMES[i])
                self.planets[i] = point

            ax.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)

            start_time = time.time()

            def create_init(index):
                def init():
                    return self.planets[index],
                return init

            def create_update(index):
                def update(_):
                    time_elapsed = (time.time_ns() - start_time) / 1000000000
                    theta = (2*np.pi * time_elapsed) * ANIMATION_SPEED / ORBITAL_PERIOD[index] * DIRECTION[index]
                    x, y = calculate_xy(theta, SEMI_MAJOR_AXIS[index], ECCENTRICITY[index])
                    if not isinstance(self.planets[index], tuple):
                        self.planets[index].set_data([x], [y])
                        self.canvas.draw()
                    return self.planets[index],
                return update

            for i in range(START_PLANET, END_PLANET):
                ani = FuncAnimation(fig, create_update(i), frames=[0], init_func=create_init(i))
                self.animations.append(ani)

            ax.legend()
            ax.set_aspect('equal')
            ax.set_xlabel("(Au)")
            fig.canvas.draw_idle()

        init_all(10)
        bts.on_clicked(init_all)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        self.canvas.set_size_request(800, 600)
        sw.set_child(self.canvas)
        toolbar = NavigationToolbar(self.canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c4(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 4")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(projection="3d")
        self.canvas = FigureCanvas(fig)

        rax = fig.add_axes([0.02, 0.4, 0.12, 0.2])
        bts = RadioButtons(rax, ["Inner planets", "Outer planets"])

        # Use 2, 0, 4 for inner planets
        # Use 4, 4, 9 for outer planets
        TARGET_PLANET = 2
        START_PLANET = 0
        END_PLANET = 4

        def init_all(_):
            ax.clear()
            if bts.value_selected == "Outer planets":
                TARGET_PLANET = 4
                START_PLANET = 4
                END_PLANET = 9
            else:
                TARGET_PLANET = 2
                START_PLANET = 0
                END_PLANET = 4

            ANIMATION_SPEED = ORBITAL_PERIOD[TARGET_PLANET]

            ax.grid(color='lightgray', linestyle='--')

            self.planets = [(), (), (), (), (), (), (), (), ()]
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
                self.planets[i] = point

            # Sun
            ax.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)

            start_time = time.time()

            def create_init(index):
                def init():
                    return self.planets[index],
                return init

            def create_update(index):
                def update(_):
                    time_elapsed = (time.time_ns() - start_time) / 1000000000
                    theta = (2*np.pi * time_elapsed) * ANIMATION_SPEED / ORBITAL_PERIOD[index] * DIRECTION[index]
                    x, y, z = calculate_xyz(theta, SEMI_MAJOR_AXIS[index], ECCENTRICITY[index], BETA[index])
                    if not isinstance(self.planets[index], tuple):
                        self.planets[index].set_data([x], [y])
                        self.planets[index].set_3d_properties([z])
                        self.canvas.draw()
                    return self.planets[index],
                return update

            self.animations = []
            for i in range(START_PLANET, END_PLANET):
                ani = FuncAnimation(fig, create_update(i), frames=[0], init_func=create_init(i), blit=True)
                self.animations.append(ani)

            ax.set_xlabel("x / Au")
            ax.set_ylabel("y / Au")
            ax.set_zlabel("z / Au")
            ax.legend()
            fig.canvas.draw_idle()

        bts.on_clicked(init_all)
        init_all(10)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        self.canvas.set_size_request(800, 600)
        sw.set_child(self.canvas)
        toolbar = NavigationToolbar(self.canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c5(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 5")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        canvas = FigureCanvas(fig)

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
        ax.plot(x_data, y_data, label="Orbit without eccentricity")

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
        ax.plot(x_data, y_data, color="r", label="Orbit with eccentricity")

        ax.grid(color='lightgray', linestyle='--')
        ax.set_xlabel("time /years")
        ax.set_ylabel("orbit polar angle /rad")
        ax.legend()

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        canvas.set_size_request(800, 600)
        sw.set_child(canvas)
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c6(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 6")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)

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

        ax = fig.add_subplot()
        self.lc = mc.LineCollection([])
        ax.add_collection(self.lc)
        fig.subplots_adjust(left=0.25)

        allowed_planets = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        ax_p1 = fig.add_axes([0.02, 0.25, 0.0725, 0.63])
        ax_p2 = fig.add_axes([0.1, 0.25, 0.0725, 0.63])
        axbox = fig.add_axes([0.02, 0.2, 0.15, 0.04])
        text_box = TextBox(axbox, '', initial="10")

        sp1 = RadioButtons(ax_p1, NAMES)
        sp2 = RadioButtons(ax_p2, NAMES)

        self.p1l = None
        self.p2l = None

        def update(_):
            self.lc.remove()
            if self.p1l is not None and self.p2l is not None:
                self.p1l.remove()
                self.p2l.remove()
            ax.clear()
            ax.set_aspect('equal')

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

            self.p1l, = plot_orbit(SEMI_MAJOR_AXIS[PLANET_A], ECCENTRICITY[PLANET_A], COLORS[PLANET_A], NAMES[PLANET_A])
            self.p2l, = plot_orbit(SEMI_MAJOR_AXIS[PLANET_B], ECCENTRICITY[PLANET_B], COLORS[PLANET_B], NAMES[PLANET_B])

            self.lc = mc.LineCollection(data, linewidths=0.2, color="#000000")
            ax.add_collection(self.lc)
            ax.legend()
            fig.canvas.draw_idle()

        update(10)
        sp1.on_clicked(update)
        sp2.on_clicked(update)
        text_box.on_text_change(update)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        sw.set_child(canvas)
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_c7(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        title = Gtk.Label(label="Challenge 7")
        title.set_css_classes(['p1'])
        vbox.append(title)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(projection="3d")
        canvas = FigureCanvas(fig)

        rax = fig.add_axes([0.02, 0.4, 0.12, 0.2])
        bts = RadioButtons(rax, ["Inner planets", "Outer planets"])

        # Use 2, 0, 4 for inner planets
        # Use 4, 4, 9 for outer planets
        TARGET_PLANET = 2
        START_PLANET = 0
        END_PLANET = 4

        def init_all(_):
            ax.clear()
            if bts.value_selected == "Outer planets":
                TARGET_PLANET = 5
                START_PLANET = 4
                END_PLANET = 9
            else:
                TARGET_PLANET = 2
                START_PLANET = 0
                END_PLANET = 4

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
            ax.set_aspect('equal')
            fig.canvas.draw_idle()

        bts.on_clicked(init_all)
        init_all(10)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        vbox.append(sw)
        canvas.set_size_request(800, 600)
        sw.set_child(canvas)
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)
        self.set_child(vbox)

    def draw_about(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=8)
        vbox.append(self.header)
        paragraph = Gtk.Label(label="Our BPhO 2023 computational challenge submission")
        paragraph.set_css_classes(['p1'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="by Jan Dziedziak and Sasan Hapuarachchi")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Technical explanation of challenges")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 1")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Using, the data provided in the challenge document, we gathered a set of points by taking the semi-major axis of each planet, taking it to the power of (3/2) \nand using that as the x coordinate, and then using the corresponding orbital period for the y axis.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="After plotting all the points, we could then just plot a line of x=y to compare to.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 2")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="We started by systematically sampling a set of points on the interval 0 to 2pi.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="For each of these, we used the sampled value as an angle, theta, and used the following formula to calculate the corresponding distance from the origin at each point:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="r = a(1 - epsilon^2) / (1 - epsilon * cos(theta))")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="This provided us polar coordinates for a set of points on the planet's orbit, which could then be converted to cartesion coordinates simply:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="x = r * cos(theta)")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="y = r * sin(theta)")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="This gave us a set of coordinates we could plot using any plotting library. In our case, we chose to use matplotlib.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 3")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="For challenge 3, as it required an animation, we chose to keep a global clock that measured the time passed since the program started.\nWhenever a new frame was rendered, the time passed was calculated, and then the percentage of the orbit that had been completed could be calculated by dividing by the orbital period.\nFinally, multiplying by 2pi would then give a polar angle, and a similar method to challenge 2 was used to calculate the planet's coordinates.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 4")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="This challenge was very similar to the previous one, meaning only a very small change was requierd.\nThe process of finding theta and r were the same, but different equations were used to find the x, y and z coordinates:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="x = r * cos(theta) * cos(beta)")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="y = r * sin(theta)")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="z = r * cos(theta) * sin(beta)")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 5")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="First, we simply drew a straight line plotting the orbit of a planet without eccentricity.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="For the second line, we used simpson's rule of integration, with the following python code:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        text = """def simpsons_integral(a, b, h, f):
    num_strips = int((b - a) / h)
    y = lambda x: f(a + x*h)

    strips = []
    strips.append(y(0))
    for i in range(1, num_strips-1):
        coefficient = (i % 2) * 2 + 2
        strips.append(coefficient * y(i))
    strips.append(y(num_strips-1))

    return 1/3 * h * sum(strips)"""
        paragraph = Gtk.Label(label=text)
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="We gathered several samples over the interval 0 to 6pi, and calculated the time at each point using the formula:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="t = P(1 - epsilon^2)^(3/2) * 1/2pi * ∫ dtheta / (1 - epsilon * cos(theta))^2")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Using 0 as the lower bound for the integral and the current angle as the upper bound.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Finally, we sampled the dataset using points from the interval 0 to 3x the orbital period of the planet, which gave us the data to plot out graph.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 6")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="For challenge 6, similar to challenge 3, we calculated the position of the two selected planets at a given time, but this time using a set of points regularly sampled over an interval.\nFor each sample, we calculated the two positions, and drew a line between them on our graph.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="On top of the lines, we chose to also draw the orbits of the two planets, to give a clearer view.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="Challenge 7")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="For this challenge, we used a very similar method to challenge 2.\nHowever, instead of just calculating the plantes position at the given angle, we also calculated the position of the centre planet, which meant we could find the relative coordinates:")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="relative x = x - target x")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="relative y = y - target y")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)
        paragraph = Gtk.Label(label="relative z = z - target z")
        paragraph.set_css_classes(['p2'])
        vbox.append(paragraph)

        paragraph = Gtk.Label(label="This gave us a set of coordinates that we could easily plot.")
        paragraph.set_css_classes(['p3'])
        vbox.append(paragraph)

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        sw.set_child(vbox)
        self.set_child(sw)

    def clear_all(self):
        self.animations = []
        self.planets = []
        try:
            if self.canvas is not None:
                self.canvas.destroy()
        except:
            pass

    def draw_screen(self):
        self.clear_all()
        self.header = Gtk.Overlay()
        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=False, spacing=8)
        self.header_box.set_css_classes(['headerbox'])
        self.button_1 = Gtk.Button(label="Challenge 1")
        self.button_2 = Gtk.Button(label="Challenge 2")
        self.button_3 = Gtk.Button(label="Challenge 3")
        self.button_4 = Gtk.Button(label="Challenge 4")
        self.button_5 = Gtk.Button(label="Challenge 5")
        self.button_6 = Gtk.Button(label="Challenge 6")
        self.button_7 = Gtk.Button(label="Challenge 7")
        self.button_9 = Gtk.Button(label="About")

        self.button_1.connect('clicked', self.button_1_clicked)
        self.button_2.connect('clicked', self.button_2_clicked)
        self.button_3.connect('clicked', self.button_3_clicked)
        self.button_4.connect('clicked', self.button_4_clicked)
        self.button_5.connect('clicked', self.button_5_clicked)
        self.button_6.connect('clicked', self.button_6_clicked)
        self.button_7.connect('clicked', self.button_7_clicked)
        self.button_9.connect('clicked', self.button_9_clicked)

        self.header_box.append(self.button_1)
        self.header_box.append(self.button_2)
        self.header_box.append(self.button_3)
        self.header_box.append(self.button_4)
        self.header_box.append(self.button_5)
        self.header_box.append(self.button_6)
        self.header_box.append(self.button_7)
        self.header_box.append(self.button_9)
        self.header_box.append(Gtk.Label(label="BPhO Computational Challenge 2023"))
        self.header.set_child(self.header_box)

        if self.screen == Screen.About:
            self.draw_about()
        elif self.screen == Screen.Paper:
            self.draw_paper()
        elif self.screen == Screen.C1:
            self.draw_c1()
        elif self.screen == Screen.C2:
            self.draw_c2()
        elif self.screen == Screen.C3:
            self.draw_c3()
        elif self.screen == Screen.C4:
            self.draw_c4()
        elif self.screen == Screen.C5:
            self.draw_c5()
        elif self.screen == Screen.C6:
            self.draw_c6()
        elif self.screen == Screen.C7:
            self.draw_c7()

    def button_1_clicked(self, *args):
        self.screen = Screen.C1
        self.draw_screen()
    def button_2_clicked(self, *args):
        self.screen = Screen.C2
        self.draw_screen()
    def button_3_clicked(self, *args):
        self.screen = Screen.C3
        self.draw_screen()
    def button_4_clicked(self, *args):
        self.screen = Screen.C4
        self.draw_screen()
    def button_5_clicked(self, *args):
        self.screen = Screen.C5
        self.draw_screen()
    def button_6_clicked(self, *args):
        self.screen = Screen.C6
        self.draw_screen()
    def button_7_clicked(self, *args):
        self.screen = Screen.C7
        self.draw_screen()
    def button_9_clicked(self, *args):
        self.screen = Screen.About
        self.draw_screen()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 300)
        self.set_title("BPho Computational challenge")

        self.screen = Screen.About
        self.draw_screen()

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = Application(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
