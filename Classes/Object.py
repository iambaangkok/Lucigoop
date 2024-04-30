import sys
import pygame

class Object:
    def __init__(self,posX,posY,parent,name):
        self.parent = parent
        self.name = name
        if parent != 0:
            self.posX = parent.posX+posX
            self.posY = parent.posY+posY
        else:
            self.posX = posX
            self.posX = posY