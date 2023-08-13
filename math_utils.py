import numpy as np

def calculate_xy(theta, semi_major_axis, eccentricity):
    magnitude = (semi_major_axis * (1 - (eccentricity ** 2))) / (1 - eccentricity * np.cos(theta))
    x = magnitude * np.cos(theta)
    y = magnitude * np.sin(theta)
    return x, y

def calculate_xyz(theta, semi_major_axis, eccentricity, beta):
    magnitude = (semi_major_axis * (1 - (eccentricity ** 2))) / (1 - eccentricity * np.cos(theta))
    x = magnitude * np.cos(theta) * np.cos(np.radians(beta))
    y = magnitude * np.sin(theta)
    z = magnitude * np.cos(theta) * np.sin(np.radians(beta))
    return x, y, z

def simpsons_integral(a, b, h, f):
    num_strips = int((b - a) / h)
    y = lambda x: f(a + x*h)

    strips = []
    strips.append(y(0))
    for i in range(1, num_strips-1):
        coefficient = (i % 2) * 2 + 2
        strips.append(coefficient * y(i))
    strips.append(y(num_strips-1))

    return 1/3 * h * sum(strips)
