import sys
import pygame
import math
from math import atan2, cos, sin, degrees, pi, sqrt
from Classes.Object import *
from Classes.HitBox import *
from Classes.Shockwave import *

class Arrow(Shockwave):
    def __init__(self,image,posX,posY,width,height,parent,name,damage,speed,attackRange,g,tX,tY):
        self.image = image
        self.parent = parent
        self.name = name
        self.damage = damage
        self.width = width
        self.height = height
        self.collidingWith = []
        self.damageDealth = False
        if parent != 0:
            self.startPosX = self.posX = posX
            self.startPosY = self.posY = posY
        else:
            self.startPosX = posX
            self.posX = posX
            self.startPosY = posY
            self.posY = posY
        self.hitBox = HitBox(posX,posY,width,height,parent,name,type,g)
        self.speedX = speed
        
        self.attackRange = attackRange
        self.tX = tX
        self.tY = tY
        self.rads = atan2(-(posY-g.posY - (tY)), (posX - tX))
        self.rads %= 2*pi
        self.theta = degrees(self.rads)
        if self.posY+g.posY > tY:
            self.speedY = -speed
        else:
            self.speedY = speed
        #self.image = pygame.transform.rotate(self.image,self.theta)
        #print(self.theta, " " , self.rads)

    def UpdateShockWave(self,g):
        if g.timeScale == 0:
            return
        #Update Shockwave
        if sqrt((self.startPosX - self.posX)*(self.startPosX - self.posX) + (self.startPosY - self.posY)*(self.startPosY - self.posY)) > self.attackRange or self.damageDealth == True:
            self.posY = 100000
            self.updateHitBox(g)
            return
        self.collidingWith.clear()
        self.move(g)
        #Check Collision
        self.collidingWith = self.hitBox.checkCollision(g)
        for i in self.collidingWith:
            if self.damageDealth == False and i.type == "Player":
                i.parent.takeDamage(self.damage)
                #self.playHitEffect
                self.damageDealth = True
        self.updateHitBox(g)
        #print(self.posX, " ", self.posY)

    def move(self,g):
        #print(self.posY ," ", self.tY)
        self.posX -= self.speedX*cos(self.rads)*g.deltaTime
        self.posY -= self.speedY*sin(self.rads)*g.deltaTime

    def updateHitBox(self,g):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()

    def rot_center(self,image, rect, angle):
        if angle > 180:
            angle = -360+angle
            
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

    def DrawShockWave(self,g):
        g.DISPLAY.blit(self.image,(self.posX-25,self.posY-25))
        