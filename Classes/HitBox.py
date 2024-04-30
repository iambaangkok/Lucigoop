import sys
import pygame
from pygame import *
from Classes.Object import *

class HitBox(Object):

    colliding = 0

    posX = 0
    posY = 0
    width = 0
    height = 0
    hbRect = Rect(posX,posY,width,height)

    def __init__(self,posX,posY,width,height,parent,name,type,g):
        #print (name)
        self.parent = parent
        self.name = name
        self.type = type
        self.width = width
        self.height = height
        if parent != 0:
            self.posX = parent.posX+posX
            self.posY = parent.posY+posY
        else:
            self.posX = posX
            self.posX = posY
        hbRect = Rect(self.posX,self.posY,self.width,self.height)
        g.allHitBoxes.append(self)
    
    def updateHitBox(self):
        self.hbRect = Rect(self.posX,self.posY,self.width,self.height)

    def drawHitBox(self,surface,color,width):
        pygame.draw.rect(surface,color,self.hbRect,width)

    def checkCollision(self,g):
        collidingWith = []
        colliding = 0
        for i in g.allHitBoxes:
            #if self.posY+g.posY <= g.screenHeight and self.posY-g.posY-self.height > 0:
                if self.hbRect.colliderect(i.hbRect):
                    colliding = 1
                    collidingWith.append(i)
        
        return collidingWith
