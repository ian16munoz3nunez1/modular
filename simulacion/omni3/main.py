#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from dibujarOmni3 import dibujarOmni3
pi = np.pi

t = 0.01
S = 10
N = int(S/t)

L = 0.5
x_i = np.array([0.0, 0.0, 0.0]).reshape(-1, 1)
x_dot = np.array([0.8, 0.0, 0.0]).reshape(-1, 1)
x_d = np.array([-0.8, 0.5, pi]).reshape(-1, 1)
k = np.diag([0.8, 0.8, 0.8])

x_plot = np.array([[], [], []])

for _ in range(N):
    x_i = x_i.ravel()
    m = np.array([[-np.sin(x_i[2]), np.cos(x_i[2]), L],
                  [-np.sin(x_i[2]+2*pi/3), np.cos(x_i[2]+2*pi/3), L],
                  [-np.sin(x_i[2]+4*pi/3), np.cos(x_i[2]+4*pi/3), L]])
    x_i = x_i.reshape(-1, 1)

    x_e = x_d - x_i
    v = np.matmul(m, np.matmul(k, x_e))
    # v = np.matmul(m, x_dot)
    x_dot = np.matmul(np.linalg.inv(m), v)
    x_i = x_i + x_dot*t

    x_plot = np.hstack((x_plot, x_i))

print(x_i)

plt.figure(1)
dibujarOmni3(x_i.ravel(), L)
plt.plot(x_plot[0, :], x_plot[1, :], 'g-', linewidth=2)

plt.figure(2)
plt.grid()
plt.plot(x_plot[0, :], linewidth=2)
plt.plot(x_plot[1, :], linewidth=2)
plt.plot(x_plot[2, :], linewidth=2)
plt.legend(['x', 'y', '$\\theta$'])

plt.show()

