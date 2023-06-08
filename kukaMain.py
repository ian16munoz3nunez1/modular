# Ian Mu;oz Nu;ez

import timeit
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from colorama import init
from colorama.ansi import Fore
from kuka import Kuka
from wf import WaveFront

init(autoreset=True)

kuka = Kuka(19999)
L = 0.471/2
l = 0.3/2
S = 16

# imagen = kuka.getImage()
# imagen = cv.resize(imagen, (100, 100))
# wf = WaveFront(imagen)
# 
# mask = wf.mainMask((45, 150, 150), (60, 255, 255))[0]
# 
# startNorm = wf.appMask((30, 150, 150), (40, 255, 255), 1)[1]
# startY, startX = wf.centroide(startNorm)
# start = np.array([[startY], [startX]])
# 
# goalNorm = wf.appMask((125, 150, 150), (160, 255, 255), 1)[1]
# goalY, goalX = wf.centroide(goalNorm)
# goal = np.array([[goalY], [goalX]])
# 
# path = wf.calcPath(mask, start, goal)
# xyPath = wf.cr2xy(path, 3.2, 2.5)
# wf.plotPath(path, start, goal)
# N = xyPath.shape[1]

xi_plot = np.array([[], [], []])
xd_plot = np.array([[], [], []])
e_plot = np.array([[], [], []])
v_plot = np.array([[], [], [], []])
t_plot = np.array([])

x_d = np.array([1.0, 1.0, np.pi/2]).reshape(-1, 1)
k = np.diag([1.8, 1.8, 1.8])
T = 0.4

start = timeit.default_timer()
end = start

i = 0
while end-start <= S:
    # t = end - start
    # x_d = np.array([xyPath[0, i], xyPath[1, i], 0.0]).reshape(-1, 1)
    # i = int(np.floor(t/T))

    x_i = kuka.getPose().ravel()
    alpha = x_i[2] + (np.pi/4)
    sq2 = np.sqrt(2)

    m = np.array([[sq2*np.sin(alpha), -sq2*np.cos(alpha), -(L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), (L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), -(L+l)],
                  [sq2*np.sin(alpha), -sq2*np.cos(alpha), (L+l)]])
    x_i = x_i.reshape(-1, 1)
    e = x_d - x_i
    if np.mean(e) < 0.001:
        break
    x_dot = np.matmul(m, np.matmul(k, e))

    kuka.setJointVelocity(x_dot)

    xi_plot = np.hstack((xi_plot, x_i))
    xd_plot = np.hstack((xd_plot, x_d))
    v_plot = np.hstack((v_plot, x_dot))
    e_plot = np.hstack((e_plot, e))
    end = timeit.default_timer()
    t_plot = np.hstack((t_plot, end-start))

kuka.stopSimulation()
print(Fore.YELLOW + "[!] Conexion terminada")
print(x_i)

plt.figure(1)
plt.grid()

plt.plot(t_plot, xd_plot[0, :], linewidth=2)
plt.plot(t_plot, xd_plot[1, :], linewidth=2)
plt.plot(t_plot, xd_plot[2, :], linewidth=2)
plt.plot(t_plot, xi_plot[0, :], linewidth=2)
plt.plot(t_plot, xi_plot[1, :], linewidth=2)
plt.plot(t_plot, xi_plot[2, :], linewidth=2)

plt.title("$x_d$/$x_i$ vs tiempo", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('$x_d$/$x_i$', fontsize=15)
plt.legend(['$x_d$', '$y_d$', '$\\theta_d$', '$x_i$', '$y_i$', '$\\theta_i$'])

plt.figure(2)
plt.grid()

plt.plot(t_plot, v_plot[0, :], linewidth=2)
plt.plot(t_plot, v_plot[1, :], linewidth=2)
plt.plot(t_plot, v_plot[2, :], linewidth=2)
plt.plot(t_plot, v_plot[3, :], linewidth=2)

plt.title("Velocidades", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('v', fontsize=15)
plt.legend(['$v_1$', '$v_2$', '$v_3$', '$v_4$'])

plt.figure(3)
plt.grid()

plt.plot(t_plot, e_plot[0, :], linewidth=2)
plt.plot(t_plot, e_plot[1, :], linewidth=2)
plt.plot(t_plot, e_plot[2, :], linewidth=2)

plt.title("Error", fontsize=20)
plt.xlabel('Tiempo (s)', fontsize=15)
plt.ylabel('Error', fontsize=15)
plt.legend(['$e_x$', '$e_y$', '$e_\\theta$'])

plt.show()

