import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

def link(alpha, a, d, theta):
    return np.array([alpha, a, d, theta])

class YouBot:
    def __init__(self, dh):
        self.alpha = dh[:, 0]
        self.a = dh[:, 1]
        self.d = dh[:, 2]
        self.theta = dh[:, 3]

    def fkine(self, q=None):
        alpha = self.alpha
        a = self.a
        d = self.d
        q = self.theta if q is None else q


        #### Matriz T01
        # Fila 1
        t11 = np.cos(q[0])
        t12 = 0.0
        t13 = np.sin(q[0])
        t14 = 0.0
        # Fila 2
        t21 = np.sin(q[0])
        t22 = 0.0
        t23 = -np.cos(q[0])
        t24 = 0.0
        # Fila 3
        t31 = 0.0
        t32 = 1.0
        t33 = 0.0
        t34 = d[0]
        # Fila 4
        t41 = 0.0
        t42 = 0.0
        t43 = 0.0
        t44 = 1.0
        # Matriz T01
        self.t01 = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]])


        #### Matriz T02
        # Fila 1
        t11 = np.cos(q[0])*np.cos(q[1])
        t12 = -np.cos(q[0])*np.sin(q[1])
        t13 = np.sin(q[0])
        t14 = a[1]*np.cos(q[0])*np.cos(q[1])
        # Fila 2
        t21 = np.sin(q[0])*np.cos(q[1])
        t22 = -np.sin(q[0])*np.sin(q[1])
        t23 = -np.cos(q[0])
        t24 = a[1]*np.sin(q[0])*np.cos(q[1])
        # Fila 3
        t31 = np.sin(q[1])
        t32 = np.cos(q[1])
        t33 = 0.0
        t34 = a[1]*np.sin(q[1]) + d[0]
        # Fila 4
        t41 = 0.0
        t42 = 0.0
        t43 = 0.0
        t44 = 1.0
        # Matriz T02
        self.t02 = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]])


        #### Matriz T03
        # Fila 1
        t11 = np.cos(q[0])*np.cos(q[1]+q[2])
        t12 = -np.cos(q[0])*np.sin(q[1]+q[2])
        t13 = np.sin(q[0])
        t14 = a[2]*np.cos(q[0])*np.cos(q[1]+q[2]) + a[1]*np.cos(q[0])*np.cos(q[1])
        # Fila 2
        t21 = np.sin(q[0])*np.cos(q[1]+q[2])
        t22 = -np.sin(q[0])*np.sin(q[1]+q[2])
        t23 = -np.cos(q[0])
        t24 = a[2]*np.sin(q[0])*np.cos(q[1]+q[2]) + a[1]*np.sin(q[0])*np.cos(q[1])
        # Fila 3
        t31 = np.sin(q[1]+q[2])
        t32 = np.cos(q[1]+q[2])
        t33 = 0.0
        t34 = a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) + d[0]
        # Fila 4
        t41 = 0.0
        t42 = 0.0
        t43 = 0.0
        t44 = 1.0
        # Matriz T03
        self.t03 = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]])

        #### Matriz de transformacion T04
        # Fila 1
        t11 = np.cos(q[0])*np.cos(q[1]+q[2]+q[3])
        t12 = -np.cos(q[0])*np.sin(q[1]+q[2]+q[3])
        t13 = np.sin(q[0])
        t14 = np.cos(q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        # Fila 2
        t21 = np.sin(q[0])*np.cos(q[1]+q[2]+q[3])
        t22 = -np.sin(q[0])*np.sin(q[1]+q[2]+q[3])
        t23 = -np.cos(q[0])
        t24 = np.sin(q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        # Fila 3
        t31 = np.sin(q[1]+q[2]+q[3])
        t32 = np.cos(q[1]+q[2]+q[3])
        t33 = 0.0
        t34 = a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) + d[0]
        # Fila 4
        t41 = 0.0
        t42 = 0.0
        t43 = 0.0
        t44 = 1.0
        # Matriz de transformacion T04
        self.t04 = np.array([[t11, t12, t13, t14],
                      [t21, t22, t23, t24],
                      [t31, t32, t33, t34],
                      [t41, t42, t43, t44]])

        return self.t04

    def jacob(self, q=None):
        alpha = self.alpha
        a = self.a
        d = self.d
        q = self.theta if q is None else q

        # Fila 1
        j11 = -np.sin(q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        j12 = -np.cos(q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) )
        j13 = -np.cos(q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) )
        j14 = -a[3]*np.cos(q[0])*np.sin(q[1]+q[2]+q[3])

        # Fila 2
        j21 = np.cos(q[0]) * ( a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1]) )
        j22 = -np.sin(q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) + a[1]*np.sin(q[1]) )
        j23 = -np.sin(q[0]) * ( a[3]*np.sin(q[1]+q[2]+q[3]) + a[2]*np.sin(q[1]+q[2]) )
        j24 = -a[3]*np.sin(q[0])*np.sin(q[1]+q[2]+q[3])

        # Fila 3
        j31 = 0.0
        j32 = a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2]) + a[1]*np.cos(q[1])
        j33 = a[3]*np.cos(q[1]+q[2]+q[3]) + a[2]*np.cos(q[1]+q[2])
        j34 = a[3]*np.cos(q[1]+q[2]+q[3])

        # Fila 4
        j41 = 0.0
        j42 = np.sin(q[0])
        j43 = np.sin(q[0])
        j44 = np.sin(q[0])

        # Fila 5
        j51 = 0.0
        j52 = -np.cos(q[0])
        j53 = -np.cos(q[0])
        j54 = -np.cos(q[0])

        # Fila 6
        j61 = 1.0
        j62 = 0.0
        j63 = 0.0
        j64 = 0.0

        # Jacobiano
        J = np.array([[j11, j12, j13, j14],
                      [j21, j22, j23, j24],
                      [j31, j32, j33, j34]])

        return J

    def workspace(self):
        workSpace = np.array([[], [], []])
        i = 0
        while i <= 2*pi:
            j = 0
            while j <= 2*pi:
                q = np.array([i, j, 0.0, 0.0]).reshape(-1, 1)
                self.fkine(q.ravel())
                x_i = self.getPosition()
                workSpace = np.hstack((workSpace, x_i))
                j += 0.1
            i += 0.1

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(workSpace[0, :], workSpace[1, :], workSpace[2, :], c='r', marker='o')
        plt.show()

    def getPosition(self):
        return self.t04[0:3, 3].reshape(-1, 1)

    def plot(self, animation=None):
        pos = np.array([[], [], []])
        pos = np.hstack((pos, np.array([[0.0], [0.0], [0.0]])))
        pos = np.hstack((pos, self.t01[0:3, 3].reshape(-1, 1)))
        pos = np.hstack((pos, self.t02[0:3, 3].reshape(-1, 1)))
        pos = np.hstack((pos, self.t03[0:3, 3].reshape(-1, 1)))
        pos = np.hstack((pos, self.t04[0:3, 3].reshape(-1, 1)))

        fig = plt.figure(1)
        ax = fig.add_subplot(111, projection='3d')

        ax.axis('equal')
        ax.set_xlim(-0.6, 0.6)
        ax.set_ylim(-0.6, 0.6)
        ax.set_zlim(0, 0.6)
        ax.set_title("YouBot", fontsize=20)
        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('y', fontsize=15)
        ax.set_zlabel('z', fontsize=15)

        ax.plot(pos[0, :], pos[1, :], pos[2, :], 'y-o', linewidth=4)
        if animation == 1:
            fig.canvas.draw()
            fig.canvas.flush_events()
        if animation == 0:
            plt.show()

