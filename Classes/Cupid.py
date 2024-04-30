import sys
import pygame
import random
from pygame.mixer import *
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Player import *
from Classes.Enemy import *
from Classes.Boar import * 

imagePath = "Images/"
soundPath = "Sound Effects/"

pygame.mixer.init()

class Cupid(Boar):
    soundLib = []
    soundLib.append(pygame.mixer.Sound(soundPath+"damaged.wav"))
    speedY = 0
    speedX = 0
    facing = -1
    movementX = 0
    movementY = 0
    attackDamage = [1,1,1,1,1,1,1,1,1]
    attackDamageLevel = 0
    maxHp = [130,130,130,170,170,170,200,200,200]
    maxHpLevel = 0
    currentHp = maxHp[maxHpLevel]
    timeSinceLastFrame = 0
    currAnim = 0
    animStart = 0
    animStop = 4
    timeSinceLastAttack = 0
    attackInterval = 4
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
        img = pygame.image.load(imagePath+"cupid arrow.png")
        img = pygame.transform.scale(img,(64,64)) 
        self.arrow = Arrow(img,self.posX+self.width/2,self.posY+g.posY,32,32,g,"Arrow",1,250,500,g,g.p.posX+g.p.width/2,g.p.posY+g.p.height/2)

    def updateEnemy(self,player,g):
        #IF DED DO NOTHING
        if self.currentHp == 0:
            self.posY = 100000
            self.updateHitBox(g)
            return

        self.timeSinceLastFrame += g.deltaTime
        self.timeSinceLastAttack += g.deltaTime
        #SIMPLE AI Calculate X movement
        #if player.posX < self.posX:
        #    self.speedX = -self.maxSpeedX
        #else:
        #    self.speedX = self.maxSpeedX
        self.movementX = self.speedX*g.deltaTime
        #Handle Animation
        if self.movementX == 0:
            self.animStart = 0
            self.animStop = 1
        else:
            self.animStart = 0
            self.animStop = 3
        ##print(self.timeSinceLastFrame ," " , self.frameTime)
        if self.timeSinceLastFrame > self.frameTime:
            ##print("FUCK")
            self.timeSinceLastFrame = 0
            self.currAnim += 1
            if self.currAnim >= self.animStop or self.currAnim+1 < self.animStart:
                self.currAnim = self.animStart-1
            self.image = self.anim[max(min(self.currAnim,self.animStop-1),self.animStart)]
            if self.facing == 1:
                self.image = pygame.transform.flip(self.image,True,False)
        #Check Attack
        if self.timeSinceLastAttack > self.attackInterval:
            self.timeSinceLastAttack = 0
            img = pygame.image.load(imagePath+"cupid arrow.png")
            img = pygame.transform.scale(img,(64,64))
            #if self.posY+g.posY < g.p.posY:
            #    img = pygame.transform.flip(img,False,True)
            if self.posX < g.p.posX:
                img = pygame.transform.flip(img,1,0)
            self.arrow = Arrow(img,self.posX+self.width/2,self.posY+g.posY,32,32,g,"Arrow",1,250,500,g,g.p.posX+g.p.width/2,g.p.posY+g.p.height/2+g.posY)
        #Check Collsion with Level
        self.collidingWith = self.hitBox.checkCollision(g)
        for i in self.collidingWith:
            if i.type == "LevelLEFT":
                self.speedX = -self.maxSpeedX
            if i.type == "LevelRIGHT":
                self.speedX = +self.maxSpeedX

        #Check Out Of Bounds
        self.moveXY(self.movementX,0)
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
    
    def updateHitBox(self,g):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY + g.posY
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()

    def Draw(self,g):
        g.DISPLAY.blit(self.image,(self.posX-5,self.posY+ self.parent.posY-48))
        pygame.draw.rect(g.DISPLAY,g.col_BLACK,Rect(self.posX, self.posY+self.parent.posY-8, self.width+2, 4))
        pygame.draw.rect(g.DISPLAY,g.col_RED,Rect(self.posX-1, self.posY+ self.parent.posY-7, self.width*self.currentHp/self.maxHp[self.maxHpLevel], 2))
        
