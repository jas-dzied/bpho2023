import numpy as np
import matplotlib.pyplot as plt

with open("./horizons_results.txt", "r") as file:
    lines = file.read().splitlines()

lines = [
    list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip(), 
                line.split(" ")
            )
        )
    )[2:] for line in lines if not line.startswith("@") and line.strip() != ""]

lines = [(float(line[0]), float(line[2])) for line in lines]

data_x = []
data_y = []
for (theta, r) in lines:
    theta = np.deg2rad(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    data_x.append(x)
    data_y.append(y)

plt.plot(data_x, data_y)
plt.grid(color='lightgray', linestyle='--')
plt.plot([0.0], [0.0], marker="o", color="#ffec17", markersize=4)
plt.legend()
plt.gca().set_aspect('equal')
plt.show()
