import sys
import pygame
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Player import *

imagePath = "Images/"

class Platform(Object):
    def __init__(self):
        Object.__init__(self)

    def __init__(self,posX,posY,image,width,height,parent,name,g,mode):
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
        self.mode = mode
        for i in mode:
            if i == 'L':
                self.leftHitBox = HitBox(-1,15,1,height-30,self,name+"LEFT","LevelLEFT",g)
            elif i == 'R':
                self.rightHitBox = HitBox(width-9,15,1,height-30,self,name+"RIGHT","LevelRIGHT",g)
            elif i == 'T':
                self.topHitBox = HitBox(15,0,width-30,10,self,name+"TOP","LevelTOP",g)
            elif i == 'B':
                self.bottomHitBox = HitBox(15,0,width-30,10,self,name+"TOP","LevelBOTTOM",g)
    def UpdateLevel(self,g):
        self.updateHitBox()

    def updateHitBox(self):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY + self.parent.posY
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()
        for i in self.mode:
            if i == 'L':
                self.leftHitBox.parent = self
                self.leftHitBox.posX = self.posX - 1
                self.leftHitBox.posY = self.posY + self.parent.posY+15
                self.leftHitBox.width = 1
                self.leftHitBox.updateHitBox()
            elif i == 'R':
                self.rightHitBox.parent = self
                self.rightHitBox.posX = self.posX+self.width+1
                self.rightHitBox.posY = self.posY + self.parent.posY+15
                self.rightHitBox.width = 1
                self.rightHitBox.updateHitBox()
            elif i == 'T':
                self.topHitBox.parent = self
                self.topHitBox.posX = self.posX+15
                self.topHitBox.posY = self.posY + self.parent.posY
                self.topHitBox.width = self.width-30
                self.topHitBox.updateHitBox()
            elif i == 'B':
                self.bottomHitBox.parent = self
                self.bottomHitBox.posX = self.posX+15
                self.bottomHitBox.posY = self.posY + self.height-10 + self.parent.posY
                self.bottomHitBox.width = self.width-30
                self.bottomHitBox.updateHitBox()
        
    
    def Draw(self,g):
        if self.posY+g.posY <= g.screenHeight and self.posY-g.posY-self.height > 0:
            g.DISPLAY.blit(self.image,(self.posX,self.posY+ self.parent.posY))