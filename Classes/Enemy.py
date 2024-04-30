import sys
import pygame
import random
from pygame.mixer import *
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Player import *

imagePath = "Images/"
soundPath = "Sound Effects/"

pygame.mixer.init()

class Enemy(Player):
    soundLib = []
    soundLib.append(pygame.mixer.Sound(soundPath+"damaged.wav"))
    speedY = 0
    speedX = 0
    facing = 1
    movementX = 0
    movementY = 0
    attackDamage = [1,1,1,1,1,1,1,1,1]
    attackDamageLevel = 0
    maxHp = [130,130,130,170,170,170,200,200,200]
    maxHpLevel = 0
    currentHp = maxHp[maxHpLevel]
    frameTime = 0.11
    timeSinceLastFrame = 0
    currAnim = 0
    animStart = 0
    animStop = 5
    def __init__(self):
        Object.__init__(self)

    def __init__(self,posX,posY,image,width,height,maxSpeedX,maxSpeedY,parent,name,g,anim):
        self.parent = parent
        if parent != 0:
            self.posX = parent.posX + posX
            self.posY = parent.posY + posY
        else:
            self.posX = posX
            self.posY = posY
        self.width = width
        self.height = height
        self.image = image
        self.maxSpeedX = maxSpeedX
        self.speedX = random.randint(0,1)
        if self.speedX == 0:
            self.speedX = -1
        self.speedX *= self.maxSpeedX
        self.maxSpeedY = maxSpeedY
        self.name = name
        self.hitBox = HitBox(posX,posY,width,height,self,"Enemy","Enemy",g)
        #self.bottomHitBox = HitBox(posX,posY+height-10,width,11,self,"Enemy","EnemyBOTTOM",g)
        self.anim = anim
    def updateEnemy(self,player,g):
        if g.timeScale == 0:
            self.speedX = self.movementX = self.movementY = self.speedY = 0
            return
        #IF DED DO NOTHING
        if self.currentHp == 0:
            self.posY = 100000
            self.updateHitBox(g)
            return
        
        self.timeSinceLastFrame += g.deltaTime
        #SIMPLE AI Calculate X movement
        #if player.posX < self.posX:
        #    self.speedX = -self.maxSpeedX
        #else:
        #    self.speedX = self.maxSpeedX
        self.movementX = self.speedX*g.deltaTime
        #Calculate Y movement
        self.speedY = self.speedY+(g.gravity)
        self.movementY = self.speedY*g.deltaTime
        
        #Handle Animation
        if self.movementX == 0:
            self.animStart = 0
            self.animStop = 2
        else:
            self.animStart = 0
            self.animStop = 5
        ##print(self.timeSinceLastFrame ," " , self.frameTime)
        if self.timeSinceLastFrame > self.frameTime:
            ##print("FUCK")
            self.timeSinceLastFrame = 0
            self.currAnim += 1
            if self.currAnim >= self.animStop or self.currAnim+1 < self.animStart:
                self.currAnim = self.animStart-1
            self.image = self.anim[max(min(self.currAnim,self.animStop-1),self.animStart)]
            if self.facing == -1:
                self.image = pygame.transform.flip(self.image,True,False)
        #Check Collsion with Level
        self.collidingWith = self.hitBox.checkCollision(g)
        for i in self.collidingWith:
            if i.type == "LevelTOP" :
                self.posY = i.posY-self.height+1
                if self.movementY > 0:
                    self.movementY = 0
                self.speedY = 0
            if i.type == "LevelLEFT":
                self.speedX = -self.maxSpeedX
            if i.type == "LevelRIGHT":
                self.speedX = +self.maxSpeedX
            if i.type == "Player":
                i.parent.takeDamage(self.attackDamage[self.attackDamageLevel])

        #Check Out Of Bounds
        if self.posY > g.screenHeight:
            self.posY = 0-self.height
            self.movementY = 0
            self.speedY = 0
            self.moveXY(self.movementX,0)
        else:
            self.moveXY(self.movementX,self.movementY)
        #Check Bounds BOUNCE
        if self.posX+self.width < 0:
            self.speedX = self.maxSpeedX
        elif self.posX > g.screenWidth:
            self.speedX = -self.maxSpeedX
        #Check Facing
        if self.movementX > 0:
            if self.facing < 0:
                self.image = pygame.transform.flip(self.image,True,False)
                self.facing = 1
        elif self.movementX < 0:
            if self.facing > 0:
                self.image = pygame.transform.flip(self.image,True,False)
                self.facing = -1
        
        self.updateHitBox(g)
        
    def takeDamage(self,damage):
        self.soundLib[0].play()
        self.currentHp = max(self.currentHp - damage,0)
        if self.currentHp == 0:
            self.parent.p.currentKills += 1
            pass#print(self.currentHp, " YouDIED")

    def Draw(self,g):
        g.DISPLAY.blit(self.image,(self.posX,self.posY))
        pygame.draw.rect(g.DISPLAY,g.col_BLACK,Rect(self.posX, self.posY-8, self.width+2, 4))
        pygame.draw.rect(g.DISPLAY,g.col_RED,Rect(self.posX-1, self.posY-7, self.width*self.currentHp/self.maxHp[self.maxHpLevel], 2))