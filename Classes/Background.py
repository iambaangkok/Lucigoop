import sys
import pygame
from Classes.Object import *

class Background(Object):
    def __init__(self,posX,posY,image,width,height,parent,name,g):
        self.image = pygame.transform.scale(image,(width,height))
        self.parent = parent
        self.name = name
        self.width = width
        self.height = height
        if parent != 0:
            self.startPosX = self.posX = parent.posX+posX
            self.posY = parent.posY+posY
        else:
            self.startPosX = posX
            self.posX = posX
            self.posY = posY

    def UpdateBackground(self,g):
        if self.posY+g.posY <= g.screenHeight and self.posY+g.posY+2160 >= 0:
            print(self.name)
        if g.timeScale == 0:
            return
        #Check Boundaries
        if g.p.posY+g.p.height > g.screenHeight-g.bottomMoveBorder:
            g.moveY(g.speed)
        elif g.p.posY < g.topMoveBorder:
            if g.p.currentJumpForce > 0 and g.posY < -g.topMoveBorder:
                g.p.posY = g.topMoveBorder
            g.moveY(-g.speed)
        #self.posY = g.posY
        
        
   
    def Draw(self,g):
        if self.posY+g.posY <= g.screenHeight and self.posY+g.posY+2160 >= 0:
            g.DISPLAY.blit(self.image,(self.posX,self.posY+g.posY))
        else:
            pass#print(self.name)
        