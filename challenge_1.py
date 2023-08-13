import matplotlib.pyplot as plt

from data import *

plt.plot([x**(3/2) for x in SEMI_MAJOR_AXIS], ORBITAL_PERIOD, ls='', marker='x')
plt.plot([0.0, 250.0], [0.0, 250.0], color="r")
plt.xlabel("(a / Au) ^ (3/2)")
plt.ylabel("T / Yr")
plt.show()
