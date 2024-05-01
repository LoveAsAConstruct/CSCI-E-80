from tools import *
import math
import pygame

WIDTH = 800
HEIGHT = 800

class Agent:
    def __init__(self, position, velocity, cohesion = 50, repulsion = 10):
        self.position = position  # A tuple (x, y)
        self.velocity = velocity  # A tuple (dx, dy)
        self.acceleration = (0, 0)  # A tuple (ax, ay)
        self.cohesion = cohesion
        self.repulsion = repulsion
        
    def update(self, agents, window = None):
        # Check for wall reflection:
        if self.position[0] >= WIDTH or self.position[0] <= 0:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.position = tadd(self.position, self.velocity)
        if self.position[1] >= WIDTH or self.position[1] <= 0:
            self.velocity = (self.velocity[0], -self.velocity[1])
            self.position = tadd(self.position, self.velocity)
        
        
        # Update the agent's velocity and position based on its acceleration
        self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
        self.velocity = tmult(self.velocity, (0.98, 0.98))
        self.position = tadd(self.position, (self.velocity))
        
        
        nearby = set()
        for agent in agents:
            if math.dist(self.position, agent.position) < self.repulsion:
                scalar = (1 - math.dist(self.position, agent.position)/self.repulsion)*5
                self.velocity = tadd(self.velocity, tmult(tnrml(tsub(self.position, agent.position)), (scalar,scalar)))
                if window:
                    pygame.draw.line(window, (255,255,255), self.position, agent.position)
        if nearby:
            com = (0,0)
            for agent in nearby:
                com = tadd(com, agent.position)
            com = tdiv(com, (len(nearby), len(nearby)))
            #self.velocity = tadd(tmult(tnrml(tsub(com,self.position)), (0.1,0.1)),self.velocity)
            
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