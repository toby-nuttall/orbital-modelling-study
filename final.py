import matplotlib . pyplot as plt
import numpy as np
import matplotlib . animation as animation
from mpl_toolkits . mplot3d import Axes3D
import math

class space():

    def __init__(self):
        self.size = 1000
        self.bodies = []
        
        #defining matplotlib objects
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)
        self.fig.add_axes(self.ax)
        self.dT = 1

        self.ax.set_xlabel('x')
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        self.ax.view_init(40,30)
    
    def add_body(self,body):
        self.bodies.append(body)
    
    def update_planet(self):
        self.ax.clear()
        for body in self.bodies:
            body.move()
            body.draw()

    def fix_axes(self):
        self.ax.set_xlim((-self.size/2,self.size/2))
        self.ax.set_zlim((-self.size/2,self.size/2))
        self.ax.set_ylim((-self.size/2,self.size/2))
    
    def gravity_planets(self):
        for i , first in enumerate ( self . bodies ) :
            for second in self . bodies [ i + 1 :]:
                first . gravity ( second )

class body():

    def __init__(self, space, mass, position = (0,0,0), velocity = (0,0,0)):
        self.space = space
        self.mass = mass
        self.position = position
        self.velocity = velocity 
        self.colour = "black"

        self.space.add_body(self)
    

    #this method takes the axis of rotation and the position of a planet and makes its orbit circular about the given axis
    def circular_velocity(self,other,axis):
        axis_hat = axis * 1/(np.linalg.norm(axis))
        position_hat = self.position * 1/(np.linalg.norm(self.position))
        v_hat = np.cross(axis_hat,position_hat)

        self.velocity = math.sqrt((other.mass)/(np.linalg.norm(self.position))) * v_hat

    def impulse(self,deltav):
        
        velocity_hat = float(1/math.sqrt(self.velocity[0]**2 + self.velocity[1]**2 + self.velocity[2]**2)) * self.velocity

        self.velocity = self.velocity + deltav * velocity_hat
    

    def hoghman_transfer(self,axis,R,r,other,i):

        v2 = math.sqrt((2 * other.mass * r)/((r + R) * R))
        v1 = math.sqrt((2 * other.mass * R)/((R + r)*r))
        v0 = math.sqrt(other.mass/r)
        v00 = math.sqrt(other.mass/R)

        if i == 1:
            self.circular_velocity(other,axis)

        if i == 2:
            dV = v1 - v0
            self.impulse(dV)

        if round(np.linalg.norm(self.velocity),2) == round(v2,2):
            dv2 = v00 - v2
            self.impulse(dv2)


        


#implemented leapfrog, from external tests it worked the best
    def move(self):
        self.position = (self.position[0] + self.velocity[0] *0.5*Solarsys.dT, 
        self.position[1] + self.velocity[1] *0.5*Solarsys.dT, 
        self.position[2] + self.velocity[2] *0.5*Solarsys.dT)

    def draw(self):
        self.space.ax.plot(self.position[0],self.position[1],self.position[2], marker = "o", markersize = 10, color = self.colour)
    
    def gravity(self, other):
        distance = np.subtract ( other.position , self.position )
        distanceMag = np.linalg . norm ( distance )
        distanceUnit = np . divide ( distance , distanceMag )
        forceMag = self . mass * other . mass / ( distanceMag **2)
        force = np . multiply ( distanceUnit , forceMag )
        switch = 1
        for body in self , other :
            acceleration = np . divide ( force , body.mass )     
            acceleration = np . multiply ( acceleration, Solarsys.dT*switch)
            body.velocity = np.add(body.velocity,acceleration)
            switch *= -1

class sun(body):
    def __init__(self, space, mass = 1000, position = (0,0,0), velocity = (0,0,0)):
        super(sun, self).__init__(space, mass, position, velocity)
        self.colour = "yellow"
    
    def move(self):
        self.position = self.position




#intialising the actualy solarsystem
Solarsys = space()
Sun = sun(Solarsys)

satalite = body(Solarsys, mass = 0.01, position = ( 100,0,0), velocity = (0,3,0))

satalite2 = body(Solarsys, mass = 0.01, position = ( -200 , 0 , 0), velocity = (0,10,0))
satalite2.circular_velocity(Sun,(1,1,1))

satalite3 = body(Solarsys,mass = 0.01, position = (150,50,-100), velocity = (-3.0,0,0))


#making the animation
def animate(i):
    print (" The frame is : ", i)
    
    #apply leapfrog method
    Solarsys.update_planet()
    Solarsys.gravity_planets()
    Solarsys.update_planet()

    Solarsys.fix_axes()

    #must call the hoghman function repeatedly:
    satalite.hoghman_transfer((1,-1,1),300,100,Sun,i)
    

anim = animation.FuncAnimation( Solarsys.fig , animate ,frames =1000 , interval =100)
writergif = animation.PillowWriter(fps = 60)
anim.save(r"C:\Users\tobyc\OneDrive\python\planets\final.gif",writer = writergif)
plt.show()

