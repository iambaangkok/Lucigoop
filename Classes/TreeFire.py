import sys
import pygame
import random
from pygame.mixer import *
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Player import *
from Classes.Enemy import *
from Classes.Tree import*

imagePath = "Images/"
soundPath = "Sound Effects/"

pygame.mixer.init()

class TreeFire(Tree):
    soundLib = []
    soundLib.append(pygame.mixer.Sound(soundPath+"Fire spirit c.wav"))
    speedY = 0
    speedX = 0
    facing = -1
    movementX = 0
    movementY = 0
    attackDamage = [1,1,1,1,1,1,1,1,1]
    attackDamageLevel = 0
    maxHp = [600,600,600]
    maxHpLevel = 0
    currentHp = maxHp[maxHpLevel]
    timeSinceLastFrame = 0
    currAnim = 0
    animStart = 0
    animStop = 5
    
    isWalking = False
    timeSinceLastWalk = 0
    timeWalking = 0
    walkInterval = 1.3
    walkTime = 3
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