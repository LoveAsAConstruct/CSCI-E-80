from tools import *
import math
import pygame

WIDTH = 800
HEIGHT = 800

class Agent:
    def __init__(self, position, velocity, cohesion = 75, repulsion = 25, speed = 5):
        self.position = position  # A tuple (x, y)
        self.velocity = velocity  # A tuple (dx, dy)
        self.acceleration = (0, 0)  # A tuple (ax, ay)
        self.cohesion = cohesion
        self.repulsion = repulsion
        self.speed = speed;
        
    def update(self, agents, window = None):
        # Check for wall reflection:
        if self.position[0] >= WIDTH or self.position[0] <= 0:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.position=tadd(self.position, tmult(tnrml(self.velocity),(self.speed,self.speed)))
        if self.position[1] >= WIDTH or self.position[1] <= 0:
            self.velocity = (self.velocity[0], -self.velocity[1])
            self.position=tadd(self.position, tmult(tnrml(self.velocity),(self.speed,self.speed)))
        
        # Update the agent's velocity and position based on its acceleration
        self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
        self.position = tadd(self.position, tmult((self.velocity),(self.speed,self.speed)))
        
        
        nearby = set()
        for agent in agents:
            if agent == self:
                    continue
            if math.dist(self.position, agent.position) < self.cohesion:
                nearby.add(agent)
                if window:
                    pygame.draw.line(window, (0,0,255), self.position, agent.position)
                self.velocity = tmod(agent.velocity, self.velocity, 50)
            if math.dist(self.position, agent.position) < self.repulsion:
                scalar = 1 - math.dist(self.position, agent.position)/self.repulsion
                self.velocity = tmod(tsub(self.position, agent.position),self.velocity, 500*(1-scalar))
        if nearby:
            com = (0,0)
            for agent in nearby:
                com = tadd(com, agent.position)
            com = tdiv(com, (len(nearby), len(nearby)))
            self.velocity = tmod(tsub(com, self.position), self.velocity, 750)
            
    def steer(self, target, strength, multiplier = 1):
        # Calculate desired velocity towards relative position
        desired_velocity = tnrml(tsub(target, self.position))
        
        # Calculate steering force
        steering_force = tmult(limit(tsub(desired_velocity, self.velocity), strength),(multiplier,multiplier))
        
        # Apply steering force
        self.velocity = tadd(self.velocity, steering_force)

    def draw(self, window):
        
        # Draw the agent as a circle
        pygame.draw.circle(window, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 5)
        pygame.draw.line(window, (255,0,0), (self.position[0], self.position[1]), (self.position[0]+5*self.velocity[0], self.position[1] + 5*self.velocity[1]))