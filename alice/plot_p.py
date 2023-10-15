import matplotlib.pyplot as plt
import numpy as np
x = [20, 32, 40, 50, 60, 70, 80, 90]
y = [4.32e-3, 2.78e-3, 2e-3, 1.65e-3, 1.2e-3, 1.01e-3, 0.9e-3, 0.7e-3]
plt.plot(x, y, color='blue', linestyle="-", linewidth="2", markersize="16", marker=".")
plt.xlabel('Clock Period(ns)')
plt.ylabel('Power(W)')
plt.ylim(0, 5e-3)
ax = plt.gca()
ax.ticklabel_format(style='sci', scilimits = (-1, 2), axis='y')
plt.grid()
plt.savefig('power')