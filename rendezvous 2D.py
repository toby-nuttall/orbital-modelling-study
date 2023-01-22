import math 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

#initialising plot
fig = plt.figure() 
axis = plt.axes(xlim =(-150000, 150000),
                ylim =(-150000, 150000)) 
  
line1, = axis.plot([], [], "k-",label = "astronaut") 
line2, = axis.plot([], [], "g-",label = "ISS") 

plt.xlabel("x")
plt.ylabel("y")
plt.title("rendezvous")
plt.legend(loc="upper left")

#defining function and parameters
R = 100000
r = 90000
G = 6.67 * math.pow(10,-11)
Me = 5.97 * math.pow(10,24)
m1 = 70
m2 = 444615

x1 = r * np.array([0.92388,-0.382683])
v1 = math.sqrt(float(G * Me)/r) * np.array([0.382683,0.92388])
x2 = R * np.array([1,0])
v2 = math.sqrt(float(G * Me)/R) * np.array([0,1])

deltat = 0.01
t = 0
def func(x1,m):
  return -(float(G * Me * m)/(math.pow((x1[0]**2 + x1[1]**2),1.5))) * (x1)

#now to loop though and make the animation 
metadata = dict(title = "planet orbit-004, astronaut problem",artist = "toby nuttall")
writer = PillowWriter(fps = 15, metadata = metadata)

x1data = []
y1data = []
x2data = []
y2data = []

N = 1500


#defining function theta:

def phi(x1,x2):
  x1mag = np.linalg.norm(x1)
  x2mag = np.linalg.norm(x2)
  return round(math.acos(float((np.dot(x1,x2)))/(x2mag * x1mag)),2)

def zdirection(x1,x2):
  return x1[0] * x2[1] - x1[1] * x2[0]

deltatheta = math.pi * (1-math.pow(((R + r)*0.5),1.5)/(math.pow(R,1.5))) 
deltav = math.sqrt((G * Me)/r) * (math.sqrt(float((2 * R)/(r + R))) -1)

counter = 0

dtheta = round(deltatheta,2)

with writer.saving(fig, "rendezvous.gif",100):
  for i in range(0,N):
    if (phi(x1,x2) == dtheta) and (zdirection(x1,x2) > 0 and counter == 0):
      
      v1 = v1 + deltav * v1 * 1/float(math.sqrt(v1[0]**2 + v1[1]**2))

      x1 = x1 + v1 * 1/2 * deltat
      x2 = x2 + v2 * 1/2 * deltat

      t = t + 1/2 * deltat

      F1 = func(x1,m1)
      F2 = func(x2,m2)

      v1 = v1 + deltat * (1/float(m1)) * F1
      v2 = v2 + deltat * (1/float(m2)) * F2

      t = t + 1/2 * deltat

      x1 = x1 + v1 * 1/2 * deltat
      x2 = x2 + v2 * 1/2 * deltat

      x1data.append(x1[0])
      y1data.append(x1[1])
      x2data.append(x2[0])
      y2data.append(x2[1])

      line1.set_data(x1data,y1data)
      line2.set_data(x2data,y2data)

      writer.grab_frame()

      counter += 1

    else:

      x1 = x1 + v1 * 1/2 * deltat
      x2 = x2 + v2 * 1/2 * deltat
      t = t + 1/2 * deltat
      F1 = func(x1,m1)
      F2 = func(x2,m2)
      v1 = v1 + deltat * (1/float(m1)) * F1
      v2 = v2 + deltat * (1/float(m2)) * F2
      t = t + 1/2 * deltat
      x1 = x1 + v1 * 1/2 * deltat
      x2 = x2 + v2 * 1/2 * deltat

      x1data.append(x1[0])
      y1data.append(x1[1])
      x2data.append(x2[0])
      y2data.append(x2[1])

      line1.set_data(x1data,y1data)
      line2.set_data(x2data,y2data)

      writer.grab_frame()

print("deltav = " + str(round(deltav)) + " m/s")
print("Iss must be ahead by: " + str(dtheta) + " radians")
