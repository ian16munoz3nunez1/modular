# Beto <--> Edna <--> Ian

import numpy as np
import matplotlib.pyplot as plt
from colorama import init
from colorama.ansi import Fore
from youBot import YouBot, link
pi = np.pi
init(autoreset=True)

t = 0.01
S = 10
N = S/t

l1 = link(pi/2, 0.0, 0.147, 0.0)
l2 = link(0.0, 0.155, 0.0, 0.0)
l3 = link(0.0, 0.135, 0.0, 0.0)
l4 = link(0.0, 0.2175, 0.0, 0.0)

youBot = YouBot(np.vstack((l1, l2, l3, l4)))

q = np.array([0.0, pi/4, -pi/4, -pi/4]).reshape(-1, 1)
q_dot = np.array([0.0, 0.0, 0.0, 0.0]).reshape(-1, 1)
x_d = np.array([-0.2, 0.3, 0.2]).reshape(-1, 1)
k = np.diag([0.8, 0.8, 0.8])

youBot.workspace()

xi_plot = np.array([[], [], []])
xd_plot = np.array([[], [], []])
e_plot = np.array([[], [], []])
q_plot = np.array([[], [], [], []])
t_plot = np.array([])

# plt.ion()
i = 0
while i <= N:
    youBot.fkine(q.ravel())
    # youBot.plot(1)
    x_i = youBot.getPosition()
    e = x_d - x_i
    if np.mean(abs(e)) <= 0.001:
        break

    pinvJacob = np.linalg.pinv(youBot.jacob(q.ravel()))
    q_dot = np.matmul(pinvJacob, np.matmul(k, e))
    q = q + q_dot*t;

    xi_plot = np.hstack((xi_plot, x_i))
    xd_plot = np.hstack((xd_plot, x_d))
    e_plot = np.hstack((e_plot, e))
    q_plot = np.hstack((q_plot, q))
    t_plot = np.hstack((t_plot, i*t))

    i += 1
# plt.ioff()
# plt.close('all')

T = youBot.fkine(q.ravel())
print(Fore.GREEN + f"T:\n{T}")
youBot.plot()
plt.plot(xi_plot[0, :], xi_plot[1, :], xi_plot[2, :], 'g-')

plt.figure(2)
plt.grid()

plt.plot(t_plot, xi_plot[0, :], 'r-', linewidth=2)
plt.plot(t_plot, xi_plot[1, :], 'g-', linewidth=2)
plt.plot(t_plot, xi_plot[2, :], 'b-', linewidth=2)
plt.plot(t_plot, xd_plot[0, :], 'y--', linewidth=2)
plt.plot(t_plot, xd_plot[1, :], 'c--', linewidth=2)
plt.plot(t_plot, xd_plot[2, :], 'm--', linewidth=2)

plt.title("$x_i$/$x_d$", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('$x_i$/$x_d$', fontsize=15)
plt.legend(['$x_i$', '$y_i$', '$z_i$', '$x_d$', '$y_d$', '$z_d$'])

plt.figure(3)
plt.grid()

plt.plot(t_plot, e_plot[0, :], 'r-', linewidth=2)
plt.plot(t_plot, e_plot[1, :], 'g-', linewidth=2)
plt.plot(t_plot, e_plot[2, :], 'b-', linewidth=2)

plt.title("Error", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('error', fontsize=15)
plt.legend(['$e_x$', '$e_y$', '$e_z$'])

plt.figure(4)
plt.grid()

plt.plot(t_plot, q_plot[0, :], 'r-', linewidth=2)
plt.plot(t_plot, q_plot[1, :], 'g-', linewidth=2)
plt.plot(t_plot, q_plot[2, :], 'b-', linewidth=2)
plt.plot(t_plot, q_plot[3, :], 'y-', linewidth=2)

plt.title("q", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('q', fontsize=15)
plt.legend(['$q_1$', '$q_2$', '$q_3$', '$q_4$'])

plt.show()

