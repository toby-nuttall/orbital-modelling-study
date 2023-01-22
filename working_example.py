#the example is dogshit, lets just start from scratch and make my own, ill do a basic solar system first, then ill make my rendezvous

import matplotlib . pyplot as plt
import numpy as np
import matplotlib . animation as animation
from mpl_toolkits . mplot3d import Axes3D

class space():

    def __init__(self):
        self.size = 1000
        self.bodies = []
        
        #defining matplotlib objects
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)
        self.fig.add_axes(self.ax)
        self.dT = 1
    
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
        
    
    def move(self):
        self.position = (self.position[0] + self.velocity[0] * Solarsys.dT, 
        self.position[1] + self.velocity[1] * Solarsys.dT, 
        self.position[2] + self.velocity[2] * Solarsys.dT)

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
            acceleration = np . divide ( force , body . mass )
            acceleration = np . multiply ( force , Solarsys.dT*switch)
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


mars = body(Solarsys, mass = 10, position = ( -100 , -50 , 150), velocity = (-4,0,0))

Sun = sun(Solarsys)

def animate(i):
    print (" The frame is : ", i)
    Solarsys.gravity_planets()
    Solarsys.update_planet()
    Solarsys.fix_axes()

anim = animation.FuncAnimation( Solarsys.fig , animate ,frames =100 , interval =100)
writergif = animation.PillowWriter(fps = 30)
anim.save(r"C:\Users\tobyc\OneDrive\python\planets\animation.gif",writer = writergif)
plt.show()

    

#OMFG it actaully works, this is momentous, it is also completely trash
    



