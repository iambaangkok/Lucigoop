import sys
import pygame
import random
from math import floor
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Player import *
from Classes.Platform import *
from Classes.Enemy import *
from Classes.Background import *
from Classes.Lettuce import *
from Classes.Boar import *
from Classes.Chicken import *
from Classes.Tree import *
from Classes.TreeFire import *
from Classes.Statue import *
from Classes.Cupid import *
from Classes.Devil import *
from Classes.Fire import *

imagePath = "Images/"

class Spawner(Platform):

    spawnInterval = random.randint(30,60)
    timeSinceLastSpawn = spawnInterval-2
    def __init__(self):
        Object.__init__(self)

    def __init__(self,posX,posY,width,height,parent,name,g,monsterType):
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
        self.name = name
        self.hitBox = HitBox(0,0,width,height,self,name,"Level",g)
        self.monsterType = monsterType
    def UpdateLevel(self,g):
        self.timeSinceLastSpawn += g.deltaTime
        if self.timeSinceLastSpawn > self.spawnInterval:
            if self.posY+g.posY < g.screenHeight and self.posY+g.posY > 0:
                self.timeSinceLastSpawn = 0
                self.Spawn(self.monsterType,g)
        self.updateHitBox()

    def updateHitBox(self):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY + self.parent.posY
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()

    def Spawn(self,mT,g):
        if mT == 0:
            eAnim = []
            for i in range(1,9):
                e = pygame.image.load(imagePath + "chicken0"+str(i)+".png")
                e = pygame.transform.scale(e,(80,80))
                eAnim.append(e)
            e = Chicken(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,64,180,1000,g,"Enemy01",g,eAnim)
            g.allEnemies.append(e)
        elif mT == 1:
            eAnim = []
            for i in range(1,10):
                e = pygame.image.load(imagePath + "statue0"+str(i)+".png")
                e = pygame.transform.scale(e,(96,96))
                eAnim.append(e)
            for i in range(10,18):
                e = pygame.image.load(imagePath + "statue"+str(i)+".png")
                e = pygame.transform.scale(e,(96,96))
                eAnim.append(e)
            e = Statue(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,96,300,1000,g,"Enemy01",g,eAnim)
            e.image = pygame.transform.scale(e.image,(e.width,e.height))
            g.allEnemies.append(e)
        elif mT == 2:
            eAnim = []
            for i in range(1,4):
                e = pygame.image.load(imagePath + "cupid"+str(i)+".png")
                e = pygame.transform.scale(e,(96,192))
                eAnim.append(e)
            e = Cupid(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,64,70,1000,g,"Cupid",g,eAnim)
            e.image = pygame.transform.scale(e.image,(e.width,e.height))
            g.allEnemies.append(e)
        elif mT == 3:
            eAnim = []
            for i in range(1,6):
                e = pygame.image.load(imagePath + "lettuce0"+str(i)+".png")
                e = pygame.transform.scale(e,(80,80))
                eAnim.append(e)
            e = Lettuce(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,64,180,1000,g,"Enemy01",g,eAnim)
            g.allEnemies.append(e)
        elif mT == 4:
            eAnim = []
            for i in range(1,5):
                e = pygame.image.load(imagePath + "boar"+str(i)+".png")
                e = pygame.transform.scale(e,(128,64))
                eAnim.append(e)
            e = Boar(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,64,200,1000,g,"Enemy01",g,eAnim)
            g.allEnemies.append(e)
        elif mT == 5:
            eAnim = []
            for i in range(1,8):
                e = pygame.image.load(imagePath + "tree"+str(i)+".png")
                e = pygame.transform.scale(e,(150,300))
                eAnim.append(e)
            e = Tree(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,128,50,1000,g,"Enemy01",g,eAnim)
            g.allEnemies.append(e)
        elif mT == 6:
            eAnim = []
            for i in range(1,8):
                e = pygame.image.load(imagePath + "firetree"+str(i)+".png")
                e = pygame.transform.scale(e,(150,300))
                eAnim.append(e)
            e = TreeFire(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,128,50,1000,g,"Enemy01",g,eAnim)
            g.allEnemies.append(e)
        elif mT == 7:
            eAnim = []
            for i in range(1,4):
                e = pygame.image.load(imagePath + "devil"+str(i)+".png")
                e = pygame.transform.scale(e,(96,192))
                eAnim.append(e)
            e = Devil(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,64,130,1000,g,"Devil",g,eAnim)
            e.image = pygame.transform.scale(e.image,(e.width,e.height))
            g.allEnemies.append(e)
        elif mT == 8:
            eAnim = []
            for i in range(1,7):
                e = pygame.image.load(imagePath + "fire0"+str(i)+".png")
                e = pygame.transform.scale(e,(96,96))
                eAnim.append(e)
            e = Fire(self.posX,self.posY,pygame.image.load(imagePath + "blank.png"),64,80,200,1000,g,"Enemy01",g,eAnim)
            e.image = pygame.transform.scale(e.image,(e.width,e.height))
            g.allEnemies.append(e)