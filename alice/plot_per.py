import matplotlib.pyplot as plt
import numpy as np
x = [20, 32, 40, 50, 60, 70, 80, 90]
y = [7e8, 6.4e8, 7.1e8, 7.4e8, 7.8e8, 8.1e8, 8.3e8, 8.4e8]
plt.plot(x, y, color='blue', linestyle="-", linewidth="2", markersize="16", marker=".")
plt.xlabel('Clock Period(ns)')
plt.ylabel('Performance')
plt.ylim(4e8, 12e8)
ax = plt.gca()
ax.ticklabel_format(style='sci', scilimits = (-1, 2), axis='y')
plt.grid()
plt.savefig('perfor')