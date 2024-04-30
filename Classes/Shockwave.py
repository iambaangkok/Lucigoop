import sys
import pygame
from Classes.Object import *
from Classes.HitBox import *

class Shockwave(Object):
    def __init__(self,image,posX,posY,width,height,parent,name,damage,speed,attackRange,g):
        self.image = image
        self.parent = parent
        self.name = name
        self.damage = damage
        self.width = width
        self.height = height
        self.collidingWith = []
        self.damageDealth = False
        if parent != 0:
            self.startPosX = self.posX = parent.posX+posX
            self.posY = posY
        else:
            self.startPosX = posX
            self.posX = posX
            self.posY = posY
        self.hitBox = HitBox(posX,posY,width,height,parent,name,type,g)
        self.speed = speed
        self.attackRange = attackRange

    def UpdateShockWave(self,g):
        if g.timeScale == 0:
            return
        #Update Shockwave
        if abs(self.startPosX - self.posX) > self.attackRange or self.damageDealth == True:
            self.posY = 100000
            self.updateHitBox()
            return
        self.collidingWith.clear()
        if g.attacked:
            self.move()
        #Check Collision
        self.collidingWith = self.hitBox.checkCollision(g)
        for i in self.collidingWith:
            if self.damageDealth == False and i.type == "Enemy":
                i.parent.takeDamage(self.damage)
                #self.playHitEffect
                self.damageDealth = True
        if g.attacked:
            self.updateHitBox()
        

    def move(self):
        self.posX += self.speed

    def updateHitBox(self):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()

    def DrawShockWave(self,g):
        if g.attacked:
            g.DISPLAY.blit(self.image,(self.posX-25,self.posY))
        