# Beto <--> Edna <--> Ian

import cv2 as cv
import numpy as np
from time import sleep
from colorama import init
from colorama.ansi import Fore
import sim
pi = np.pi

init(autoreset=True)

def link(alpha, a, d, theta):
    return np.array([alpha, a, d, theta])

class Kuka:
    def __init__(self, port, dh):
        self.alpha = dh[:, 0]
        self.a = dh[:, 1]
        self.d = dh[:, 2]
        self.theta = dh[:, 3]

        self.__clientID = []

        self.__kuka = []
        self.__motor1 = []
        self.__motor2 = []
        self.__motor3 = []
        self.__motor4 = []
        self.__q1 = []
        self.__q2 = []
        self.__q3 = []
        self.__q4 = []
        self.__camera = []

        self.__wl = -2.5*np.ones((4, 1))
        self.__wu = 2.5*np.ones((4, 1))

        sim.simxFinish(-1)
        self.__clientID = sim.simxStart("127.0.0.1", port, True, True, 5000, 5)

        if self.__clientID == 0:
            _, self.__kuka = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBot_ref', sim.simx_opmode_oneshot_wait)
            _, self.__motor1 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_fl', sim.simx_opmode_oneshot_wait)
            _, self.__motor2 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_fr', sim.simx_opmode_oneshot_wait)
            _, self.__motor3 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_rl', sim.simx_opmode_oneshot_wait)
            _, self.__motor4 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_rr', sim.simx_opmode_oneshot_wait)
            _, self.__q1 = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBotArmJoint0', sim.simx_opmode_oneshot_wait)
            _, self.__q2 = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBotArmJoint1', sim.simx_opmode_oneshot_wait)
            _, self.__q3 = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBotArmJoint2', sim.simx_opmode_oneshot_wait)
            _, self.__q4 = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBotArmJoint3', sim.simx_opmode_oneshot_wait)
            _, self.__camera = sim.simxGetObjectHandle(self.__clientID, '/kinect/rgb', sim.simx_opmode_oneshot_wait)

            sim.simxGetStringSignal(self.__clientID, 'measuredDataAtThisTime', sim.simx_opmode_streaming)
            sleep(1)

            print(Fore.GREEN + "[+] ok")

        else:
            print(Fore.RED + "[-] error")

    def getPose(self):
        aux = np.ones((6, 1))

        while np.sum(aux) != 0:
            if sim.simxGetConnectionId(self.__clientID) == 1:
                aux[0], position = sim.simxGetObjectPosition(self.__clientID, self.__kuka, -1, sim.simx_opmode_streaming)
                aux[1], orientation = sim.simxGetObjectOrientation(self.__clientID, self.__kuka, -1, sim.simx_opmode_streaming)
                aux[2], q1 = sim.simxGetJointPosition(self.__clientID, self.__q1, sim.simx_opmode_streaming)
                aux[3], q2 = sim.simxGetJointPosition(self.__clientID, self.__q2, sim.simx_opmode_streaming)
                q2 = q2 + (pi/2)
                aux[4], q3 = sim.simxGetJointPosition(self.__clientID, self.__q3, sim.simx_opmode_streaming)
                aux[5], q4 = sim.simxGetJointPosition(self.__clientID, self.__q4, sim.simx_opmode_streaming)
                x_i = np.array([[position[0]], [position[1]], [orientation[2]], [q1], [q2], [q3], [q4]], dtype=np.float64)

            else:
                print(Fore.RED + "[-] Conexion perdida (getPose)")
                raise RuntimeError("error")

        return x_i

    def setJointVelocity(self, w, q=None):
        R = 0.1
        w = w/R
        q = np.array([0.0, pi/2, -pi/2, -pi/2]).reshape(-1, 1) if q is None else q
        q[1] = -(pi/2)+q[1]

        if sim.simxGetConnectionId(self.__clientID) == 1:
            w = np.maximum(w, self.__wl)
            w = np.minimum(w, self.__wu)

            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor1, -w[0], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor2, -w[1], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor3, -w[2], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor4, -w[3], sim.simx_opmode_streaming)
            sim.simxSetJointTargetPosition(self.__clientID, self.__q1, q[0], sim.simx_opmode_streaming)
            sim.simxSetJointTargetPosition(self.__clientID, self.__q2, q[1], sim.simx_opmode_streaming)
            sim.simxSetJointTargetPosition(self.__clientID, self.__q3, q[2], sim.simx_opmode_streaming)
            sim.simxSetJointTargetPosition(self.__clientID, self.__q4, q[3], sim.simx_opmode_streaming)

        else:
            print(Fore.RED + "[-] Conexion perdida (setJointVelocity)")
            raise RuntimeError("error")

    def getImage(self):
        if sim.simxGetConnectionId(self.__clientID) == 1:
            ret, resolution, img = sim.simxGetVisionSensorImage(self.__clientID, self.__camera, 0, sim.simx_opmode_oneshot_wait)
            img = np.array(img, dtype=np.uint8)
            img.resize([resolution[1], resolution[0], 3])

        else:
            print(Fore.RED + "[-] Conexion perdida (getImage)")
            raise RuntimeError("error")

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img = cv.flip(img, 0)
        return img

    def stopSimulation(self):
        sim.simxStopSimulation(self.__clientID, sim.simx_opmode_oneshot_wait)

    def fkine(self, q):
        alpha = self.alpha
        a = self.a
        d = self.d
        p = q[:3]
        q = q[3:]

        t11 = np.cos(p[2]+q[0])*np.cos(q[1]+q[2]+q[3])
        t12 = -np.cos(p[2]+q[0])*np.sin(q[1]+q[2]+q[3])
        t13 = np.sin(p[2]+q[0])
        t14 = np.cos(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) ) + 0.170*np.cos(p[2]) + p[0]
        t21 = np.sin(p[2]+q[0])*np.cos(q[1]+q[2]+q[3])
        t22 = -np.sin(p[2]+q[0])*np.sin(q[1]+q[2]+q[3])
        t23 = -np.cos(p[2]+q[0])
        t24 = np.sin(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) ) + 0.170*np.sin(p[2]) + p[1]
        t31 = np.sin(q[1]+q[2]+q[3])
        t32 = np.cos(q[1]+q[2]+q[3])
        t33 = 0.0
        t34 = a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) + d[0] + 0.060
        t41 = 0.0
        t42 = 0.0
        t43 = 0.0
        t44 = 1.0
        wTe = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]])

        return wTe[:3, 3].reshape(-1, 1)

    def jacob(self, q):
        alpha = self.alpha
        a = self.a
        d = self.d
        p = q[:3]
        q = q[3:]

        j11 = 1.0
        j12 = 0.0
        j13 = -np.sin(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) ) - 0.170*np.sin(p[2])
        j14 = -np.sin(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        j15 = -np.cos(p[2]+q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) )
        j16 = -np.cos(p[2]+q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) )
        j17 = -a[3]*np.cos(p[2]+q[0])*np.sin(q[1]+q[2]+q[3])
        j21 = 0.0
        j22 = 1.0
        j23 = np.cos(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) ) + 0.170*np.cos(p[2])
        j24 = np.cos(p[2]+q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        j25 = -np.sin(p[2]+q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) )
        j26 = -np.sin(p[2]+q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) )
        j27 = -a[3]*np.sin(p[2]+q[0])*np.sin(q[1]+q[2]+q[3])
        j31 = 0.0
        j32 = 0.0
        j33 = 0.0
        j34 = 0.0
        j35 = a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1])
        j36 = a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2])
        j37 = a[3]*np.cos(q[1]+q[2]+q[3])
        J = np.array([[j11, j12, j13, j14, j15, j16, j17],
                      [j21, j22, j23, j24, j25, j26, j27],
                      [j31, j32, j33, j34, j35, j36, j37]])

        return J

