from pysr import PySRRegressor
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('qtagg')

model = PySRRegressor.from_file("./models/final0.pkl")
print(model.latex())
print("done")

for i in range(9):
    thetas = []
    features = []
    for theta in np.linspace(0, 2*np.pi):
        thetas.append(theta)
        features.append([39.509, 0.25, theta])
    rs = np.vectorize(abs)(model.predict(np.array(features), i))
    data_x = []
    data_y = []
    for (r, theta) in zip(rs, thetas):
        data_x.append(r * np.cos(theta))
        data_y.append(r * np.sin(theta))
    plt.plot(data_x, data_y, label=f"equation {i}")

def calculate_xy(theta, semi_major_axis, eccentricity):
    magnitude = (semi_major_axis * (1 - (eccentricity ** 2))) / (1 - eccentricity * np.cos(theta))
    x = magnitude * np.cos(theta)
    y = magnitude * np.sin(theta)
    return x, y

def plot_orbit(semi_major_axis, eccentricity, color, label):
    points_x = []
    points_y = []
    for theta in np.linspace(0, 2*np.pi, 5000):
        x, y = calculate_xy(theta, semi_major_axis, eccentricity)
        points_x.append(x)
        points_y.append(y)
    plt.plot(points_x, points_y, color=color, label=label, linestyle="--")
    plt.grid(color='lightgray', linestyle='--')

plot_orbit(39.509, 0.25, "blue", "Pluto orbit")

plt.grid(color='lightgray', linestyle='-')
plt.legend()
plt.gca().set_aspect('equal')
plt.show()
