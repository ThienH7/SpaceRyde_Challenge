#!/usr/bin/env python

import random
import numpy as np

class Plane():
    
    def __init__(self):
        start_angle = random.uniform(0, 2 * np.pi) # radians
        self.x = 500.0 * np.cos(start_angle)
        self.y = 500.0 * np.sin(start_angle)
        self.vel = 140 # m/s
        self.heading = -start_angle
        self.update_rate = 0.1 # seconds
        # self.travel_dist = self.vel * self.update_rate
        self.holding = False
        self.time = 0

    def update_pos(self):
        self.time += 1
        self.x = self.x + self.vel * self.time * np.cos(self.heading)
        self.y = self.y + self.vel * self.time * np.sin(self.heading)
        return [self.x, self.y]
    
    def update_holding(self, position):
        self.heading = np.arctan((position[1] - self.y) / (position[0] - self.x))

    def getPos(self):
        return [self.x, self.y]
