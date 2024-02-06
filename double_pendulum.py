import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def changeAngle(theta):
    return theta

def convertAngle(theta):
    return theta-0.5*np.pi

def firstPendulumPos():
  return x0 + np.cos(changeAngle(theta1))*l1, y0 + np.sin(changeAngle(theta1))*l1

def secondPendulumPos():
  return x1 + np.cos(changeAngle(theta2))*l2, y1 + np.sin(changeAngle(theta2))*l2

def lerp(x0, y0, x1, y1):
  return np.linspace(x0, x1, 1000), np.linspace(y0, y1, 1000)

def updateDoublePendulumPos():
  global x1, y1, x2, y2
  x1, y1 = firstPendulumPos()
  x2, y2 = secondPendulumPos()
  
def showDoublePendulum():
  updateDoublePendulumPos()
  plt.scatter(x1, y1, s = r1*aspect, color = 'blue' )
  plt.scatter(x2, y2, s = r2*aspect, color = 'red' )

  fixed_bar_x, fixed_bar_y = np.linspace(-1.25*(l1+l2+r2), 1.25*(l1+l2+r2), 1000), np.zeros(1000)
  plt.plot(fixed_bar_x, fixed_bar_y,  color = 'black');

  first_rope_x, first_rope_y = lerp(x0, y0, x1, y1)
  plt.plot(first_rope_x, first_rope_y,  color = 'green');

  second_rope_x, second_rope_y = lerp(x1, y1, x2, y2)
  plt.plot(second_rope_x, second_rope_y,  color = 'green');

  plt.xlim( -1.25*(l1+l2+r2) , 1.25*(l1+l2+r2) )
  plt.ylim( -1.25*(l1+l2+r2) , 1.25*(l1+l2+r2) )
 
  plt.show()

def saveDoublePendulumPos():
  global x1_data, y1_data, x2_data, y2_data
  x1_data.append(x1)
  y1_data.append(y1)
  x2_data.append(x2)
  y2_data.append(y2)

def radius(m):
  return 0.3*m

g = -9.81
m1 = 9
m2 = 10
r1 = radius(m1)
r2 = radius(m2)


theta1 = 80*np.pi/180
theta2 = 20*np.pi/180
#convertAngle(theta1)
#convertAngle(theta2)


theta1_dot = 0
theta2_dot = 0
l1 = 15
l2 = 10  
x0, y0 = 0, 0
x1, y1 = 0, 0
x2, y2 = 0, 0

x1_data = list()
y1_data = list()
x2_data = list()
y2_data = list()
aspect = 1000

t = 0
dt = 1/60

while t<50:
  #rate(1000)
  a = -(m1+m2)*g*r1*np.sin(convertAngle(theta1))-m2*r1*r2*(theta2_dot**2)*np.sin(theta1-theta2)
  b = (m1+m2)*(r1**2)
  c = m2*r1*r2*np.cos(theta1-theta2)

  f = -m2*g*r2*np.sin(convertAngle(theta2))+m2*r1*r2*(theta1_dot**2)*np.sin(theta1-theta2)
  k = m2*(r2**2)
  w = m2*r1*r2*np.cos(theta1-theta2)

  theta2_ddot = (f-a*w/b)/(k-c*w/b)
  theta1_ddot = a/b - c*theta2_ddot/b

  theta1_dot += theta1_ddot*dt
  theta2_dot += theta2_ddot*dt

  theta1 += theta1_dot*dt
  theta2 += theta2_dot*dt
  
  updateDoublePendulumPos()
  saveDoublePendulumPos()

  #print(theta1, theta2, x1, y1, x2, y2)
  t += dt
  #showDoublePendulum()


nsteps = len(x1_data)
trayectory1_x = [[x1_data[i],x1_data[i+1]] for i in range(nsteps-1)]
trayectory1_y = [[y1_data[i],y1_data[i+1]] for i in range(nsteps-1)]
trayectory2_x = [[x2_data[i],x2_data[i+1]] for i in range(nsteps-1)]
trayectory2_y = [[y2_data[i],y2_data[i+1]] for i in range(nsteps-1)]
# Initialize the animation plot. Make the aspect ratio equal so it looks right.
fig = plt.figure()
ax = fig.add_subplot(aspect='equal')
# The pendulum rod, in its initial position.
line1, = ax.plot([x0, x1], [y0, y1], lw=3, c='k')
line2, = ax.plot([x1, x2], [y1, y2], lw=3, c='k')

trayectory1, = ax.plot([0,0], [0,0], lw=1, c='b')
trayectory2, = ax.plot([0,0], [0,0], lw=1, c='r')
# The pendulum bob: set zorder so that it is drawn over the pendulum rod.
circle1 = ax.add_patch(plt.Circle((x1, y1), r1, fc='b', zorder=3))
circle2 = ax.add_patch(plt.Circle((x2, y2), r2, fc='r', zorder=3))
# Set the plot limits so that the pendulum has room to swing!
ax.set_xlim( -1.25*(l1+l2+r2) , 1.25*(l1+l2+r2) )
ax.set_ylim( -1.25*(l1+l2+r2) , 1.25*(l1+l2+r2) )

def animate(i):
    minimumi = 0
    if i > 200:
      minimumi = i-200
    x1, y1 = x1_data[i], y1_data[i]
    x2, y2 = x2_data[i], y2_data[i]
    line1.set_data([x0, x1], [y0, y1])
    circle1.set_center((x1, y1))
    line2.set_data([x1, x2], [y1, y2])
    circle2.set_center((x2, y2))
    trayectory1.set_xdata(trayectory1_x[minimumi:i])
    trayectory1.set_ydata(trayectory1_y[minimumi:i])
    trayectory2.set_xdata(trayectory2_x[minimumi:i])
    trayectory2.set_ydata(trayectory2_y[minimumi:i])

nframes = nsteps
interval = 1
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=True, interval=interval)
writerv = animation.FFMpegWriter(fps=60)
#ani.save('C:\\Users\\alf20\\Desktop\\LaTeX\\Semestre 5\\Métodos - soluciones\\pendulo.mp4', writer=writerv)
plt.show()
