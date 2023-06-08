close all
clear
clc

syms a_4 a_3 a_2 d_1 theta1 theta2 theta3 theta4

tx = cos(theta1) * (a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2));
ty = sin(theta1) * (a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2));
tz = a_4*sin(theta2+theta3+theta4) + a_3*sin(theta2+theta3) + a_2*sin(theta2) + d_1;

diff(tx, theta1)
diff(tx, theta2)
diff(tx, theta3)
diff(tx, theta4)
diff(ty, theta1)
diff(ty, theta2)
diff(ty, theta3)
diff(ty, theta4)
diff(tz, theta1)
diff(tz, theta2)
diff(tz, theta3)
diff(tz, theta4)

