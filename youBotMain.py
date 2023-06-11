# Beto <--> Edna <--> Ian

import timeit
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from colorama import init
from colorama.ansi import Fore
from kuka import Kuka, link
from dibujarKuka import dibujar_kuka
pi = np.pi
sq2 = np.sqrt(2)

init(autoreset=True)

l1 = link(pi/2, 0.0, 0.147, 0.0)
l2 = link(0.0, 0.155, 0.0, 0.0)
l3 = link(0.0, 0.135, 0.0, 0.0)
l4 = link(0.0, 0.217, 0.0, 0.0)

kuka = Kuka(19999, np.vstack((l1, l2, l3, l4)))
L = 0.471/2
l = 0.3/2
S = 16

x_d = np.array([1.0, -0.3, 0.5]).reshape(-1, 1)
k = np.diag([0.8, 0.8, 0.8])

pi_plot = np.array([[], [], []])
qi_plot = np.array([[], [], [], []])
xd_plot = np.array([[], [], []])
xi_plot = np.array([[], [], []])
e_plot = np.array([[], [], []])
v_plot = np.array([[], [], [], []])
qDot_plot = np.array([[], [], [], []])
t_plot = np.array([])

start = timeit.default_timer()
end = start

while end-start <= S:
    q_i = kuka.getPose().ravel()
    p_i = q_i[:3]
    x_i = kuka.fkine(q_i)

    e = x_d - x_i
    if np.mean(abs(e)) < 0.01:
        break
    J = kuka.jacob(q_i)
    q_dot = np.matmul(np.linalg.pinv(J), np.matmul(k, e))

    alpha = p_i[2] + (pi/4)
    m = np.array([[sq2*np.sin(alpha), -sq2*np.cos(alpha), -(L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), (L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), -(L+l)],
                  [sq2*np.sin(alpha), -sq2*np.cos(alpha), (L+l)]])
    v = np.matmul(m, q_dot[:3])
    q = q_i[3:].reshape(-1, 1) + q_dot[3:]*0.1

    kuka.setJointVelocity(v, q)

    end = timeit.default_timer()
    pi_plot = np.hstack((pi_plot, p_i.reshape(-1, 1)))
    qi_plot = np.hstack((qi_plot, q_i[3:].reshape(-1, 1)))
    xi_plot = np.hstack((xi_plot, x_i))
    xd_plot = np.hstack((xd_plot, x_d))
    e_plot = np.hstack((e_plot, e))
    v_plot = np.hstack((v_plot, v))
    qDot_plot = np.hstack((qDot_plot, q_dot[3:]))
    t_plot = np.hstack((t_plot, end-start))

kuka.stopSimulation()
print(Fore.YELLOW + "[!] Conexion terminada")
print(x_i)

dibujar_kuka(q_i[:3], q_i[3:], p_plot=pi_plot, x_plot=xi_plot)

plt.figure(2)
plt.grid()

plt.plot(t_plot, xd_plot[0, :], '--', linewidth=2)
plt.plot(t_plot, xd_plot[1, :], '--', linewidth=2)
plt.plot(t_plot, xd_plot[2, :], '--', linewidth=2)
plt.plot(t_plot, xi_plot[0, :], linewidth=2)
plt.plot(t_plot, xi_plot[1, :], linewidth=2)
plt.plot(t_plot, xi_plot[2, :], linewidth=2)

plt.title("Efector final", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('$x_d$/$x_i$', fontsize=15)
plt.legend(['$x_d$', '$y_d$', '$z_d$', '$x_i$', '$y_i$', '$z_i$'])

plt.figure(3)
plt.grid()

plt.plot(t_plot, pi_plot[0, :], linewidth=2)
plt.plot(t_plot, pi_plot[1, :], linewidth=2)
plt.plot(t_plot, pi_plot[2, :], linewidth=2)

plt.title("Plataforma", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('$p_i$', fontsize=15)
plt.legend(['$x_i$', '$y_i$', '$\\theta_i$'])

plt.figure(4)
plt.grid()

plt.plot(t_plot, qi_plot[0, :], linewidth=2)
plt.plot(t_plot, qi_plot[1, :], linewidth=2)
plt.plot(t_plot, qi_plot[2, :], linewidth=2)
plt.plot(t_plot, qi_plot[3, :], linewidth=2)

plt.title("$q_i$", fontsize=20)
plt.xlabel('Timepo (s)', fontsize=15)
plt.ylabel('$q_i$', fontsize=15)
plt.legend(['$q_1$', '$q_2$', '$q_3$', '$q_4$'])

plt.figure(5)
plt.grid()

plt.plot(t_plot, e_plot[0, :], linewidth=2)
plt.plot(t_plot, e_plot[1, :], linewidth=2)
plt.plot(t_plot, e_plot[2, :], linewidth=2)

plt.title("Error", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('error', fontsize=15)
plt.legend(['$e_x$', '$e_y$', '$e_z$'])

plt.figure(6)
plt.grid()

plt.plot(t_plot, v_plot[0, :], linewidth=2)
plt.plot(t_plot, v_plot[1, :], linewidth=2)
plt.plot(t_plot, v_plot[2, :], linewidth=2)
plt.plot(t_plot, v_plot[3, :], linewidth=2)

plt.title("Velocidades de ruedas", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('v', fontsize=15)
plt.legend(['$motor_1$', '$motor_2$', '$motor_3$', '$motor_4$'])

plt.figure(7)
plt.grid()

plt.plot(t_plot, qDot_plot[0, :], linewidth=2)
plt.plot(t_plot, qDot_plot[1, :], linewidth=2)
plt.plot(t_plot, qDot_plot[2, :], linewidth=2)
plt.plot(t_plot, qDot_plot[3, :], linewidth=2)

plt.title("$q_{dot}$", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('$q_dot$', fontsize=15)
plt.legend(['$qDot_1$', '$qDot_2$', '$qDot_3$', '$qDot_4$'])

plt.show()

