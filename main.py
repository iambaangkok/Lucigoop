import pygame
from pygame.locals import *
import pygame.mixer
from pygame.mixer import *
import sys
import os
import Classes
import random
from math import floor
from Classes import *
from Classes import Object
from Classes.Object import *
from Classes import HitBox
from Classes.HitBox import *
from Classes import Player
from Classes.Player import *
from Classes import Enemy
from Classes.Enemy import *
from Classes import Platform
from Classes.Platform import *
from Classes import Background
from Classes.Background import *
from Classes import Lettuce
from Classes.Lettuce import *
from Classes import Boar
from Classes.Boar import *
from Classes import Chicken
from Classes.Chicken import *
from Classes import Tree
from Classes.Tree import *
from Classes import TreeFire
from Classes.TreeFire import *
from Classes import Statue
from Classes.Statue import *
from Classes import Cupid
from Classes.Cupid import *
from Classes import Devil
from Classes.Devil import *
from Classes import Fire
from Classes.Fire import *
from Classes import Spawner
from Classes.Spawner import *

#print(1042+85+41+141+143+143+138+145+168+47+170+13+76+345+63+141+142+160+63) = 3266

class Game:
    def __init__(self):
        ###############Start 
        self.posX = 0
        self.posY = 0
        self.speed = 300
        self.bottomMoveBorder = 280
        self.topMoveBorder = 160
        self.imagePath = "Images/"
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.timeScale = 1
        self.t = 0
        self.deltaTime = 0
        self.getTicksLastFrame = 0
        self.timeSinceLastAttack = 0
        self.attacked = False
        self.timeSinceLastFrame = 0
        pygame.init()
        self.screenWidth = 1280
        self.screenHeight = 720
        self.DISPLAY = pygame.display.set_mode((self.screenWidth,self.screenHeight),0,16)
        pygame.display.set_caption("LUCIGOOP - Stable Build")
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",16)

        self.col_BLACK = (0,0,0)
        self.col_WHITE = (255,255,255)
        self.col_RED = (255,0,0)
        self.col_GREEN = (0,255,0)
        self.col_BLUE = (0,0,255)
        self.col_YELLOW = (0,0,0)
        self.gravity = 100
        self.allHitBoxes = []
        self.allEnemies = []
        self.allPlatforms = []
        self.allKeyHoles = [[] for i in range(0,3)]
        #print(len(self.allKeyHoles[0]), " ", len(self.allKeyHoles[1]), " ",len(self.allKeyHoles[2]))
        self.allbgs = []
        self.allKeys = []
        self.allKeysPosX = []
        self.keysCollected = [0,0,0]
        self.allSpawners = []
        plats = [           "********************",#HEAVEN
                            "********************",
                            "L***************SS**",
                            "*LMMMMMMMMMMR**LMMMR",
                            "********************",
                            "********************",
                            "*******LMMMMR*******",
                            "***e****************",
                            "***LMR*********e**S*",
                            "************LMMMMMMR",
                            "******LMR***********",
                            "*********s********s*",
                            "******************s*",
                            "**********LMMMMMMR**",
                            "**e*****************",
                            "*****K**************",
                            "*LMMMMMMMR**********",
                            "********************",
                            "********************",
                            "**********LMMR***LMR",
                            "*********s**********",
                            "***e****s***********",
                            "**LMMR********LMR***",
                            "********************",
                            "********************",
                            "*******LMMMR*****e**",
                            "****************LMR*",
                            "***e****************",
                            "LMMMMMR*************",
                            "*********LMMMMMR****",
                            "****e***************",
                            "DDDLMMMMMR**********",
                            "***DDDDDDDDDDLMRDDDD",
                            "********************",#EARTH
                            "LMMMMMR*********LMR*",
                            "***********LMMMR****",
                            "********************",
                            "**e****LMMR****e****",
                            "**S**********LMMMSMR",
                            "**S**************S**",
                            "LMMMMMR**********S**",
                            "***********LR****S**",
                            "*e************LMMR**",
                            "LMMMMMMMMR**********",
                            "****************e***",
                            "**e******LMMMMMMMMR*",
                            "LMMMR*************M*",
                            "*****s*********K**M*",
                            "******s**********s**",
                            "*******s*****LMMR***",
                            "********************",
                            "****e****LMR********",
                            "LMMMMMR*************",
                            "**************LMMMR*",
                            "**LMMMMMR***********",
                            "********************",
                            "********************",
                            "********LMMR****eLMR",
                            "****e*******s***s***",
                            "LMMMMMR******s******",
                            "*******s******s*****",
                            "********s***********",
                            "**e*************S***",
                            "LMMMMMMMMR****LMMMMR",
                            "**********LR********",
                            "********************",
                            "LMMMMMMRDDDDLMMMMMMR",
                            "********************",#HELL
                            "*******LMR**********",
                            "*****e********LMMMMR",
                            "***********LMR******",
                            "****LMMMMMR****K****",
                            "********************",
                            "**e**********LMR*e**",
                            "LMMMR******LMMMMMR**",
                            "*****LR**********S**",
                            "*******LR*******SS*s",
                            "*********LMMMMMMM***",
                            "**SSS***************",
                            "LMMMMMR*********e***",
                            "*******s*****LMMMMMR",
                            "********s***********",
                            "*******e*S**********",
                            "****LMMMMMR*********",
                            "*****************LMR",
                            "****e*********LMR***",
                            "**LMMMMMMMMMMR******",
                            "************e*******",
                            "*********e**********",
                            "LMMMMMMMMMMMMMMMMR**",
                            "********************",
                            "****e***************",
                            "LMMR************LMMR",
                            "****LMMR****LMMR****",
                            "********************",
                            "LMMMMMMMDDDDMMMMMMMR",
                            "********************",
                        ]

        for i in range(0,97):
            for j in range(0,20):
                if plats[i][j] == 'L':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "heaven_block01.png"),64,64,self,"Level"+str(i),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "earth_block01.png"),64,64,self,"Level"+str(i),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "hell_block01.png"),64,64,self,"Level"+str(i),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allPlatforms.append(self.l)
                elif plats[i][j] == 'M':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "heaven_block02.png"),64,64,self,"Level"+str(i),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "earth_block02.png"),64,64,self,"Level"+str(i),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "hell_block02.png"),64,64,self,"Level"+str(i),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allPlatforms.append(self.l)
                elif plats[i][j] == 'R':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "heaven_block03.png"),64,64,self,"Level"+str(i),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "earth_block03.png"),64,64,self,"Level"+str(i),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "hell_block03.png"),64,64,self,"Level"+str(i),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allPlatforms.append(self.l)
                elif plats[i][j] == 'S':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "heaven_block04.png"),64,64,self,"Level"+str(i),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "stone0" + str(random.randint(2,3)) + ".png"),64,64,self,"Level"+str(i),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "stone0" + str(random.randint(2,3)) + ".png"),64,64,self,"Level"+str(i),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allPlatforms.append(self.l)
                elif plats[i][j] == 's':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "heaven_block04.png"),64,64,self,"Level"+str(i),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "earth block0" + str(random.randint(4,5)) + ".png"),64,64,self,"Level"+str(i),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "stone0" + str(random.randint(2,3)) + ".png"),64,64,self,"Level"+str(i),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allPlatforms.append(self.l)
                elif plats[i][j] == 'D':
                    mode = ""
                    if j+1 < 20 and plats[i][j+1] == '*' or j+1 < 20 and plats[i][j+1] == 'K' or j+1 < 20 and plats[i][j+1] == 'e':
                        mode += "R"
                    if j-1 >= 0 and plats[i][j-1] == '*' or j-1 >= 0 and plats[i][j-1] == 'K' or j-1 >= 0 and plats[i][j-1] == 'e':
                        mode += "L"
                    if i-0 >= 0 and plats[i-1][j] == '*' or i-0 >= 0 and plats[i-1][j] == 'K' or i-0 >= 0 and plats[i-1][j] == 'e':
                        mode += "T"
                    if i+1 < 96 and plats[i+1][j] == '*' or i+1 < 96 and plats[i+1][j] == 'K' or i+1 < 96 and plats[i+1][j] == 'e':
                        mode += "B"
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "keyhole.png"),64,64,self,"Level"+str(i),self,mode)
                        self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                        self.allKeyHoles[0].append(self.l)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "keyhole.png"),64,64,self,"Level"+str(i),self,mode)
                        self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                        self.allKeyHoles[1].append(self.l)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "keyhole.png"),64,64,self,"Level"+str(i),self,mode)
                        self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                        self.allKeyHoles[2].append(self.l)
                    #print(len(self.allKeyHoles[0]), " ", len(self.allKeyHoles[1]), " ",len(self.allKeyHoles[2]))
                elif plats[i][j] == 'K':
                    if i >= 0 and i <= 32:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "key.png"),64,64,self,"Key"+str(1),self,mode)
                    elif i >= 33 and i <= 66:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "key.png"),64,64,self,"Key"+str(2),self,mode)
                    else:
                        self.l = Platform(j*64,i*64,pygame.image.load(self.imagePath + "key.png"),64,64,self,"Key"+str(3),self,mode)
                    self.l.image = pygame.transform.scale(self.l.image,(self.l.width,self.l.height))
                    self.allKeys.append(self.l)
                    self.allKeysPosX.append(j*64)
                elif plats[i][j] == 'e':
                    if i >= 0 and i <= 32:
                        self.l = Spawner(j*64,i*64,64,64,self,"Spawner"+str(1),self,random.randint(0,2))
                    elif i >= 33 and i <= 66:
                        self.l = Spawner(j*64,i*64,64,64,self,"Spawner"+str(2),self,random.randint(3,5))
                    else:
                        self.l = Spawner(j*64,i*64,64,64,self,"Spawner"+str(3),self,random.randint(6,8))
                    self.allSpawners.append(self.l)
        #print(len(self.allKeyHoles[0]), " ", len(self.allKeyHoles[1]), " ",len(self.allKeyHoles[2]))

        #pygame.draw.polygon(DISPLAY,col_RED,((100,100),(200,200),(300,100)))
        #pygame.draw.line(DISPLAY,col_RED,(100,200),(350,250),5)
        #pygame.draw.circle(DISPLAY,col_RED,(100,250),10,1)

        ###############Asset Imports
        #BACKGROUND
        self.bg = Background(0,0,pygame.image.load(self.imagePath + "heavenBG.JPG"),self.screenWidth,2160,self,"BG",self)
        self.bg.image = pygame.transform.scale(self.bg.image,(self.screenWidth,self.screenHeight*3))
        self.allbgs.append(self.bg)
        self.bg = Background(0,720*3,pygame.image.load(self.imagePath + "earthBG.png"),self.screenWidth,2160,self,"BG2",self)
        self.bg.image = pygame.transform.scale(self.bg.image,(self.screenWidth,self.screenHeight*3))
        self.allbgs.append(self.bg)
        self.bg = Background(0,720*6,pygame.image.load(self.imagePath + "hellBG.png"),self.screenWidth,2160,self,"BG3",self)
        self.bg.image = pygame.transform.scale(self.bg.image,(self.screenWidth,self.screenHeight*3))
        self.allbgs.append(self.bg)
        #PLAYER
        pAnim = []
        for i in range(1,6):
            self.p = pygame.image.load(self.imagePath + "Luci walk png "+str(i)+".png")
            self.p = pygame.transform.scale(self.p,(128,64))
            pAnim.append(self.p)
        self.p = pygame.image.load(self.imagePath + "Luci attack png 4.png")
        self.p = pygame.transform.scale(self.p,(128,64))
        pAnim.append(self.p)
        self.p = pygame.image.load(self.imagePath + "Luci attack png 3.png")
        self.p = pygame.transform.scale(self.p,(128,64))
        pAnim.append(self.p)
        self.p = pygame.image.load(self.imagePath + "Luci attack png 2.png")
        self.p = pygame.transform.scale(self.p,(128,64))
        pAnim.append(self.p)
        self.p = pygame.image.load(self.imagePath + "Luci attack png 1.png")
        self.p = pygame.transform.scale(self.p,(128,64))
        pAnim.append(self.p)
        for i in range(1,6):
            self.p = pygame.image.load(self.imagePath + "Jump png "+str(i)+".png")
            self.p = pygame.transform.scale(self.p,(128,64))
            pAnim.append(self.p)
        for i in range(1,7):
            self.p = pygame.image.load(self.imagePath + "DIE png "+str(i)+".png")
            self.p = pygame.transform.scale(self.p,(128,64))
            pAnim.append(self.p)

        self.p = Player(500,0,pygame.image.load(self.imagePath + "z.png"),64,64,200,350,900,self,"Player",self,pAnim)
        self.pFacing = 1
        self.p.image = pygame.transform.scale(self.p.image,(self.p.width,self.p.height))
        self.p.attack(1,self)
        self.p.jump(0)
        #ENEMY
        EnimE = 0
        if EnimE:
            eAnim = []
            for i in range(1,6):
                self.e = pygame.image.load(self.imagePath + "lettuce0"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(80,80))
                eAnim.append(self.e)
            self.e = Lettuce(1000,400,pygame.image.load(self.imagePath + "z.png"),64,64,180,1000,self,"Enemy01",self,eAnim)
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,5):
                self.e = pygame.image.load(self.imagePath + "boar"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(128,64))
                eAnim.append(self.e)
            self.e = Boar(50,500,pygame.image.load(self.imagePath + "z.png"),64,64,200,1000,self,"Enemy01",self,eAnim)
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,9):
                self.e = pygame.image.load(self.imagePath + "chicken0"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(80,80))
                eAnim.append(self.e)
            self.e = Chicken(250,500,pygame.image.load(self.imagePath + "z.png"),64,64,180,1000,self,"Enemy01",self,eAnim)
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,8):
                self.e = pygame.image.load(self.imagePath + "tree"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(150,300))
                eAnim.append(self.e)
            self.e = Tree(50,500,pygame.image.load(self.imagePath + "z.png"),64,128,50,1000,self,"Enemy01",self,eAnim)
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,8):
                self.e = pygame.image.load(self.imagePath + "firetree"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(150,300))
                eAnim.append(self.e)
            self.e = TreeFire(700,500,pygame.image.load(self.imagePath + "z.png"),64,128,50,1000,self,"Enemy01",self,eAnim)
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,10):
                self.e = pygame.image.load(self.imagePath + "statue0"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(96,96))
                eAnim.append(self.e)
            for i in range(10,18):
                self.e = pygame.image.load(self.imagePath + "statue"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(96,96))
                eAnim.append(self.e)
            self.e = Statue(250,100,pygame.image.load(self.imagePath + "Alien.png"),64,96,300,1000,self,"Enemy01",self,eAnim)
            self.e.image = pygame.transform.scale(self.e.image,(self.e.width,self.e.height))
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,4):
                self.e = pygame.image.load(self.imagePath + "cupid"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(96,192))
                eAnim.append(self.e)
            self.e = Cupid(250,500,pygame.image.load(self.imagePath + "Alien.png"),64,64,70,1000,self,"Cupid",self,eAnim)
            self.e.image = pygame.transform.scale(self.e.image,(self.e.width,self.e.height))
            self.allEnemies.append(self.e)
            
            eAnim = []
            for i in range(1,4):
                self.e = pygame.image.load(self.imagePath + "devil"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(96,192))
                eAnim.append(self.e)
            self.e = Devil(50,100,pygame.image.load(self.imagePath + "Alien.png"),64,64,130,1000,self,"Devil",self,eAnim)
            self.e.image = pygame.transform.scale(self.e.image,(self.e.width,self.e.height))
            self.allEnemies.append(self.e)

            eAnim = []
            for i in range(1,7):
                self.e = pygame.image.load(self.imagePath + "fire0"+str(i)+".png")
                self.e = pygame.transform.scale(self.e,(96,96))
                eAnim.append(self.e)
            self.e = Fire(700,100,pygame.image.load(self.imagePath + "Alien.png"),64,80,200,1000,self,"Enemy01",self,eAnim)
            self.e.image = pygame.transform.scale(self.e.image,(self.e.width,self.e.height))
            self.allEnemies.append(self.e)
        #LEVEL
        #self.l2 = Platform(200,self.screenHeight-256,pygame.image.load(self.imagePath + "BrownOnly_Middle_01.png"),self.screenWidth,32,self,"Level02",self)
        #self.l2.image = pygame.transform.scale(self.l2.image,(self.l2.width,self.l2.height))
        #self.allPlatforms.append(self.l2)

        ###############KEYFLAG
        self.P_w = 0
        self.P_a = 0
        self.P_s = 0
        self.P_d = 0
        self.P_space = 0
        self.P_mouse = 0
        self.P_esc = 0
        self.P_1 = 0
        self.P_2 = 0
        self.P_3 = 0
        ###############GAME STATE
        self.leveling = False

    ###############Update LOOP
    def Update(self):
        
        ###############Get Delta Time
        self.t = pygame.time.get_ticks()
        self.deltaTime = (self.t - self.getTicksLastFrame) / 1000.0 * self.timeScale
        self.getTicksLastFrame = self.t
        self.timeSinceLastAttack += self.deltaTime
        self.timeSinceLastFrame += self.deltaTime
        if self.timeScale == 0:
            self.deltaTime = 0
            self.P_w = 0
            self.P_a = 0
            self.P_s = 0
            self.P_d = 0
            self.P_space = 0
            self.P_mouse = 0
            self.P_esc = 0
            self.P_1 = 0
            self.P_2 = 0
            self.P_3 = 0
            return
        ###############Get Event/Input
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    #print ("W ")
                    self.P_w = 1
                    self.p.jump(self.p.jumpForce)
                if event.key == K_a:
                    #print("A ")
                    self.P_a = 1
                if event.key == K_s:
                    #print("S ")
                    self.P_s = 1
                if event.key == K_d:
                    #print("D ")
                    self.P_d = 1
                if event.key == K_SPACE:
                    self.P_space = 1
                if event.key == K_ESCAPE:
                    self.P_esc = 1
                if event.key == K_1:
                    self.P_1 = 1
                if event.key == K_2:
                    self.P_2 = 1
                if event.key == K_3:
                    self.P_3 = 1
            if event.type == KEYUP:
                if event.key == K_w:
                    #print ("W ")
                    self.P_w = 0
                if event.key == K_a:
                    #print("A ")
                    self.P_a = 0
                if event.key == K_s:
                    #print("S ")
                    self.P_s = 0
                if event.key == K_d:
                    #print("D ")
                    self.P_d = 0
                if event.key == K_SPACE:
                    self.P_space = 0
                if event.key == K_ESCAPE:
                    self.P_esc = 0
                if event.key == K_1:
                    self.P_1 = 0
                if event.key == K_2:
                    self.P_2 = 0
                if event.key == K_3:
                    self.P_3 = 0
            if event.type == MOUSEBUTTONDOWN:
                self.P_mouse = 1
            if event.type == MOUSEBUTTONUP:
                self.P_mouse = 0

        ###############Handle Event
        #QUIT
        if self.P_esc:
            pygame.quit()
            sys.exit()
        #PLAYER
        self.p.UpdatePlayer(self)
        #SHOCKWAVE
        self.p.shockWave.UpdateShockWave(self)
        #ENEMY
        for e in self.allEnemies:
            e.updateEnemy(self.p,self)
            #ARROW
            if e.name == "Cupid" or e.name == "Devil":
                e.arrow.UpdateShockWave(self)
        #BG
        for i in self.allbgs:
            i.UpdateBackground(self)
        #LEVEL
        for l in self.allPlatforms:
            l.UpdateLevel(self)
        for l in range(0,3):
            if self.keysCollected[l]:
                for i in self.allKeyHoles[l]:
                    i.posX = 10000
                    i.UpdateLevel(self)
                pass
            else:
                for i in self.allKeyHoles[l]:
                    i.UpdateLevel(self)
        for l in range(0,3):
            if floor((self.p.currentLevel)/3) > l and self.keysCollected[floor((self.p.currentLevel)/3)-1] == False:
                self.allKeys[l].posX = self.allKeysPosX[l]
                self.allKeys[l].UpdateLevel(self)
            else:
                self.allKeys[l].posX = 10000
                self.allKeys[l].UpdateLevel(self)
        #SPAWNERS
        for l in self.allSpawners:
            if str(floor((self.p.currentLevel)/3)+1) == l.name[7]:
                l.UpdateLevel(self)
        ###############Draw
        self.DISPLAY.fill(self.col_WHITE)
        for i in self.allbgs:
            i.Draw(self)
        #PLAYER
        self.p.Draw(self);
        #SHOCKWAVE
        self.p.shockWave.DrawShockWave(self)
        #ENEMY
        for e in self.allEnemies:
            e.Draw(self)
            #ARROW
            if e.name == "Cupid" or e.name == "Devil":
                e.arrow.DrawShockWave(self)

        #LEVEL
        for l in self.allPlatforms:
            l.Draw(self)
        for l in range(0,3):
            if self.keysCollected[l]:
                pass
            else:
                for i in self.allKeyHoles[l]:
                    i.Draw(self)
            
        for l in range(0,3):
            if floor((self.p.currentLevel+1)/3) > l and self.keysCollected[floor((self.p.currentLevel+1)/3)-1] == False:
                self.allKeys[l].Draw(self)
        
        drawHB = 0
        if drawHB:
            #pygame.draw.rect(DISPLAY,col_RED,Rect(p.posX,p.posY,p.width,p.height))
            self.p.hitBox.drawHitBox(self.DISPLAY,self.col_RED,2)
            #self.p.bottomHitBox.drawHitBox(self.DISPLAY,self.col_RED,2)
            if self.attacked:
                self.p.shockWave.hitBox.drawHitBox(self.DISPLAY,self.col_RED,2)
            for e in self.allEnemies:
                e.hitBox.drawHitBox(self.DISPLAY,self.col_RED,2)
                #ARROW
                if e.name == "Cupid" or e.name == "Devil":
                    e.arrow.hitBox.drawHitBox(self.DISPLAY,self.col_RED,2)
            for l in self.allPlatforms:
                l.hitBox.drawHitBox(self.DISPLAY,self.col_GREEN,2)
                for i in l.mode:
                    if i == 'L':
                        l.leftHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                    elif i == 'R':
                        l.rightHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                    elif i == 'T':
                        l.topHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                    elif i == 'B':
                        l.bottomHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)

            for l in range(0,3):
                if self.keysCollected[l]:
                    pass
                else:
                    for i in self.allKeyHoles[l]:
                        i.hitBox.drawHitBox(self.DISPLAY,self.col_GREEN,2)
                        for j in i.mode:
                            if j == 'L':
                                i.leftHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                            elif j == 'R':
                                i.rightHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                            elif j == 'T':
                                i.topHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
                            elif j == 'B':
                                i.bottomHitBox.drawHitBox(self.DISPLAY,self.col_BLUE,2)
            for l in range(0,3):
                if floor((self.p.currentLevel+1)/3) > l and self.keysCollected[floor((self.p.currentLevel+1)/3)-1] == False:
                    self.allKeys[l].hitBox.drawHitBox(self.DISPLAY,self.col_GREEN,2)
            for l in self.allSpawners:
                if str(floor((self.p.currentLevel+1)/3)+1) == l.name[7]:
                    l.hitBox.drawHitBox(self.DISPLAY,self.col_BLACK,2)
        ##UI DISPLAY
        #RECT BG
        sc = pygame.Surface((300,200))  # the size of your rect
        sc.set_alpha(128)                # alpha level
        sc.fill((255, 255, 255))           # this fills the entire surface
        self.DISPLAY.blit(sc, (30,30))
        #Enemies Until Next Level
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",20)
        textSurfaceObj = self.fontObj.render("Enemies Until Next Level :" + str(self.p.enemiesUntilNextLevel),True,self.col_BLACK,None)
        textRectObj = textSurfaceObj.get_rect()
        self.DISPLAY.blit(textSurfaceObj,(40,40))
        #CurrLEVEL
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",20)
        textSurfaceObj = self.fontObj.render("Level :" + str(self.p.currentLevel+1),True,self.col_BLACK,None)
        textRectObj = textSurfaceObj.get_rect()
        self.DISPLAY.blit(textSurfaceObj,(40,70))
        #HP
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",20)
        textSurfaceObj = self.fontObj.render("HP",True,(200,0,0),None)
        textRectObj = textSurfaceObj.get_rect()
        self.DISPLAY.blit(textSurfaceObj,(40,120))
        for i in range(1,self.p.maxHp[self.p.maxHpLevel]+1):
            pygame.draw.rect(self.DISPLAY,(10,10,10),Rect(i*30 + 48,123,24,24))
        for i in range(1,self.p.currentHp+1):
            pygame.draw.rect(self.DISPLAY,(200,0,0),Rect(i*30 + 50,125,20,20))
        #KEY Infos
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",20)
        if (self.p.currentLevel)%3 == 0 and self.p.currentLevel != 0 and self.keysCollected[floor((self.p.currentLevel+1)/3)-1] == False:
            textSurfaceObj = self.fontObj.render("Key Has Spawned!", True, self.col_YELLOW, None)
        elif self.p.currentLevel >= 8 and self.keysCollected[floor((self.p.currentLevel+1)/3)-1] == True:
            textSurfaceObj = self.fontObj.render("Go Jump Into The Sacred Pool!", True, self.col_YELLOW, None)
        else:
            textSurfaceObj = self.fontObj.render("Kill Enemies To Level Up!", True, self.col_YELLOW, None)
        textRectObj = textSurfaceObj.get_rect()
        self.DISPLAY.blit(textSurfaceObj,(40,150))
        #LEVELUP
       
        if self.leveling:
            sc = pygame.Surface((1280,720))  # the size of your rect
            sc.set_alpha(128)                # alpha level
            sc.fill((0, 0, 0))           # this fills the entire surface
            self.DISPLAY.blit(sc, (0,0))
            self.cur = 1
            while self.cur < 4:
                self.fontObj = pygame.font.Font("Kanit-Medium.ttf",22)
                if self.randed[self.cur-1] == "DMG":
                    self.num[self.cur] = pygame.image.load(self.imagePath + "attack powerup.png")
                    self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                    self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                    textSurfaceObj = self.fontObj.render("Attack Damage + 10%",True,self.cl,self.cl2)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h2)
                    self.DISPLAY.blit(textSurfaceObj,textRectObj)
                elif self.randed[self.cur-1] == "RATE":
                    self.num[self.cur] = pygame.image.load(self.imagePath + "swing speed.png")
                    self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                    self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                    textSurfaceObj = self.fontObj.render("Attack Rate + 10%",True,self.cl,self.cl2)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h2)
                    self.DISPLAY.blit(textSurfaceObj,textRectObj)
                elif self.randed[self.cur-1] == "RNG":
                    self.num[self.cur] = pygame.image.load(self.imagePath + "shockwave power up.png")
                    self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                    self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                    textSurfaceObj = self.fontObj.render("Shockwave Range + 33%",True,self.cl,self.cl2)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h2)
                    self.DISPLAY.blit(textSurfaceObj,textRectObj)
                elif self.randed[self.cur-1] == "MHP":
                    self.num[self.cur] = pygame.image.load(self.imagePath + "HP powerup.png")
                    self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                    self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                    textSurfaceObj = self.fontObj.render("Max HP + 1",True,self.cl,self.cl2)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h2)
                    self.DISPLAY.blit(textSurfaceObj,textRectObj)
                elif self.randed[self.cur-1] == "REG":
                    self.num[self.cur] = pygame.image.load(self.imagePath + "heal.png")
                    self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                    self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                    textSurfaceObj = self.fontObj.render("Refill HP",True,self.cl,self.cl2)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h2)
                    self.DISPLAY.blit(textSurfaceObj,textRectObj)
                textSurfaceObj = self.fontObj.render("PRESS " + str(self.cur),True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (self.gB*self.cur + self.gB2*self.cur + 100,self.h3)
                self.DISPLAY.blit(textSurfaceObj,textRectObj)
                self.cur += 1
                
            pressed = 0
            if self.P_1:
                if self.randed[0] == "DMG":
                    self.p.attackDamageLevel += 1
                elif self.randed[0] == "RATE":
                    self.p.attackDelayLevel += 1
                elif self.randed[0] == "RNG":
                    self.p.attackRangeLevel += 1
                elif self.randed[0] == "MHP":
                    self.p.maxHpLevel += 1
                    self.p.currentHp = min(self.p.currentHp+1,self.p.maxHp[self.p.maxHpLevel])
                elif self.randed[0] == "REG":
                    self.p.currentHp = self.p.maxHp[self.p.maxHpLevel]
                pressed = 1
            elif self.P_2:
                if self.randed[1] == "DMG":
                    self.p.attackDamageLevel += 1
                elif self.randed[1] == "RATE":
                    self.p.attackDelayLevel += 1
                elif self.randed[1] == "RNG":
                    self.p.attackRangeLevel += 1
                elif self.randed[1] == "MHP":
                    self.p.maxHpLevel += 1
                    self.p.currentHp = min(self.p.currentHp+1,self.p.maxHp[self.p.maxHpLevel])
                elif self.randed[1] == "REG":
                    self.p.currentHp = self.p.maxHp[self.p.maxHpLevel]
                pressed = 1
            elif self.P_3:
                if self.randed[2] == "DMG":
                    self.p.attackDamageLevel += 1
                elif self.randed[2] == "RATE":
                    self.p.attackDelayLevel += 1
                elif self.randed[2] == "RNG":
                    self.p.attackRangeLevel += 1
                elif self.randed[2] == "MHP":
                    self.p.maxHpLevel += 1
                    self.p.currentHp = min(self.p.currentHp+1,self.p.maxHp[self.p.maxHpLevel])
                elif self.randed[2] == "REG":
                    self.p.currentHp = self.p.maxHp[self.p.maxHpLevel]
                pressed = 1
            if pressed:
                self.leveling = 0
        ##FPSDISPLAY
        self.fontObj = pygame.font.Font("Kanit-Medium.ttf",16)
        textSurfaceObj = self.fontObj.render(str(self.fpsClock.get_fps()),True,self.col_GREEN,None)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (200,150)
        self.DISPLAY.blit(textSurfaceObj,(self.screenWidth-30,0))
        textSurfaceObj = self.fontObj.render(str(self.deltaTime),True,self.col_GREEN,None)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (200,150)
        self.DISPLAY.blit(textSurfaceObj,(self.screenWidth-60,30))

        
        pygame.display.update()
        ###############Do FPS Thingy
        
        self.fpsClock.tick(self.fps)
             
    def moveY(self,speed):
        if self.timeScale == 0:
            return
        self.posY -= speed*self.deltaTime
        if self.posY < -self.screenHeight*8:
            self.posY = -self.screenHeight*8
        elif self.posY > 0:
            self.posY = 0

    def levelUp(self):
        
        #self.timeScale = 0
        stats = ["DMG","RATE","RNG","MHP","REG"]
        self.randed = []
        while len(self.randed) < 3:
            pick = random.randint(0,4)
            if self.randed.count(stats[pick]) == 0:
                self.randed.append(stats[pick])
        self.num = [0,0,0,0]
        self.cur = 1
        self.gB = 90
        self.gB2 = 190
        self.h = 200
        self.h2 = self.h + 230
        self.h3 = self.h + 260
        self.cl = self.col_WHITE
        self.cl2 = None
        #pygame.draw.rect(self.DISPLAY,self.cl,Rect(0,0,self.screenWidth,self.screenHeight))
        while self.cur < 4:
            self.fontObj = pygame.font.Font("Kanit-Medium.ttf",22)
            if self.randed[self.cur-1] == "DMG":
                self.num[self.cur] = pygame.image.load(self.imagePath + "Crate_Wood_01.png")
                self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                textSurfaceObj = self.fontObj.render("Attack Damage + 10%",True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h2))
            elif self.randed[self.cur-1] == "RATE":
                self.num[self.cur] = pygame.image.load(self.imagePath + "Crate_Wood_01.png")
                self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                textSurfaceObj = self.fontObj.render("Attack Rate + 10%",True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h2))
            elif self.randed[self.cur-1] == "RNG":
                self.num[self.cur] = pygame.image.load(self.imagePath + "Crate_Wood_01.png")
                self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                textSurfaceObj = self.fontObj.render("Shockwave Range + +33%",True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h2))
            elif self.randed[self.cur-1] == "MHP":
                self.num[self.cur] = pygame.image.load(self.imagePath + "Crate_Wood_01.png")
                self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                textSurfaceObj = self.fontObj.render("Max HP + 1",True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h2))
            elif self.randed[self.cur-1] == "REG":
                self.num[self.cur] = pygame.image.load(self.imagePath + "Crate_Wood_01.png")
                self.num[self.cur] = pygame.transform.scale(self.num[self.cur],(200,200))
                self.DISPLAY.blit(self.num[self.cur],(self.gB*self.cur + self.gB2*self.cur ,self.h))
                textSurfaceObj = self.fontObj.render("Refill HP",True,self.cl,self.cl2)
                textRectObj = textSurfaceObj.get_rect()
                self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h2))
            textSurfaceObj = self.fontObj.render("PRESS " + str(self.cur),True,self.cl,self.cl2)
            textRectObj = textSurfaceObj.get_rect()
            self.DISPLAY.blit(textSurfaceObj,(self.gB*self.cur + self.gB2*self.cur,self.h3))
            self.cur += 1
            
        pygame.display.update()
        self.leveling = True;


cutscenePlayed = False

fps = 30
fpsClock = pygame.time.Clock()
timeScale = 1
t = 0
deltaTime = 0
getTicksLastFrame = 0

curCut = 0
cuts = []
cuts.append(pygame.transform.scale(pygame.image.load(imagePath + "menu.png"),(1280,720)))
cuts.append(pygame.image.load(imagePath + "Scene 1.png"))
cuts.append(pygame.image.load(imagePath + "Scene 2.png"))
cuts.append(pygame.image.load(imagePath + "Scene 3.png"))
cuts.append(pygame.image.load(imagePath + "Scene 3-2.png"))
cuts.append(pygame.image.load(imagePath + "Scene 4.png"))
cuts.append(pygame.image.load(imagePath + "Scene 5.png"))
cuts.append(pygame.image.load(imagePath + "Introduction.png"))
cuts.append(pygame.image.load(imagePath + "Introduction.png"))
cuts.append(pygame.image.load(imagePath + "Ending scene.png"))
cuts.append(pygame.image.load(imagePath + "ending2.png"))
cuts.append(pygame.image.load(imagePath + "ending3.png"))
cuts.append(pygame.image.load(imagePath + "ending4.png"))
cuts.append(pygame.image.load(imagePath + "ending5.png"))

sty = 200
stx = 550

soundPath = "Sound Effects/"
pygame.mixer.init()
soundLib = []
soundLib.append(pygame.mixer.Sound(soundPath + 'Alien_Song.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'Thunder_Crack.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'Jump_On_Soggy_Grass_copy.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'holyChorus.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'Danube.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'Hollywood_Traffic_Jam.wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'Game Over 2 (Female).wav'))
soundLib.append(pygame.mixer.Sound(soundPath + 'heaven-sound-effect c.wav'))

soundLib[0].set_volume(0.3)
soundLib[0].play(-1)
soundLib[3].set_volume(1)
soundLib[4].set_volume(0.2)
soundLib[5].set_volume(0.2)
soundLib[7].set_volume(0.5)
thundered = 0
gameovered = 0
ended = False

gameSBG = 0
game = Game()


while True:
    #CutScene
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0 * timeScale
    getTicksLastFrame = t
    if cutscenePlayed == False and curCut <= 8:
        game.DISPLAY.blit(cuts[curCut],(0,0))
        if curCut == 8:
            pygame.draw.rect(game.DISPLAY,game.col_WHITE,Rect(stx-230,sty-20,700,400))
            fontObj = pygame.font.Font("Kanit-Medium.ttf",24)
            textSurfaceObj = fontObj.render("W - Jump",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx,sty))
            textSurfaceObj = fontObj.render("A - Move Left",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx,sty+30))
            textSurfaceObj = fontObj.render("S - Move Left",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx,sty+60))
            textSurfaceObj = fontObj.render("Space - Attack",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx,sty+90))

            textSurfaceObj = fontObj.render("Fight enemies to levelup",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx-50,sty+130))
            textSurfaceObj = fontObj.render("A key will appear at level 4,7,9",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx-70,sty+160))
            textSurfaceObj = fontObj.render("Collect them to progress DOWN to find THE SACRED SPRING",True,game.col_BLACK,None)
            textRectObj = textSurfaceObj.get_rect()
            game.DISPLAY.blit(textSurfaceObj,(stx-210,sty+190))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                soundLib[2].play()
                curCut += 1
                if curCut == 3 and thundered == False:
                    soundLib[1].play()
                    thundered = 1
                if curCut > 8:
                    soundLib[0].fadeout(1)
                    cutscenePlayed = True
    elif game.p.posY <= game.screenHeight:
        #StartGameLoop
        if game.timeScale != 0:
            game.Update()
            if game.posY <= 0 and game.posY > -720*3+game.bottomMoveBorder and gameSBG != 3:
                soundLib[3].play(100)
                soundLib[4].fadeout(1)
                soundLib[5].fadeout(1)
                gameSBG = 3
            elif game.posY <= -720*3+game.bottomMoveBorder and game.posY > -720*6+game.bottomMoveBorder and gameSBG != 4:
                soundLib[3].fadeout(1)
                soundLib[4].play(100)
                soundLib[5].fadeout(1)
                gameSBG = 4
            elif game.posY <= -720*6+game.bottomMoveBorder and game.posY > -720*9+game.bottomMoveBorder and gameSBG != 5:
                soundLib[3].fadeout(1)
                soundLib[4].fadeout(1)
                soundLib[5].play(100)
                gameSBG = 5
            if game.p.currentHp <= 0:#GAMEOVER
                if gameovered == 0:
                    soundLib[6].play()
                    gameovered = 1
                img = pygame.image.load(imagePath + "gameover.png")
                img = pygame.transform.scale(img,(512,256))
                game.DISPLAY.blit(img,(game.screenWidth/2-256,game.screenHeight/2-128))
                fontObj = pygame.font.Font("Kanit-Medium.ttf",23)
                textSurfaceObj = fontObj.render("PRESS ANY BUTTON TO RESTART",True,game.col_BLACK,None)
                textRectObj = textSurfaceObj.get_rect()
                game.DISPLAY.blit(textSurfaceObj,(game.screenWidth/2-180,game.screenHeight/2+128+20))
                pressed = 0
                pygame.display.update()
                while pressed == 0:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN:
                            pressed = 1
                            gameovered = 0
                game = Game()
    else:
        soundLib[3].fadeout(1)
        soundLib[4].fadeout(1)
        soundLib[5].fadeout(1)
        if ended == False:
            soundLib[7].play(100)
            ended = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                soundLib[2].play()
                curCut += 1
                if curCut > 13:
                    pygame.quit()
                    sys.exit()
        pygame.draw.rect(game.DISPLAY,game.col_BLACK,Rect(0,0,1280,720))
        game.DISPLAY.blit(cuts[curCut],(0,0))
        pygame.display.update()
    fpsClock.tick(fps)