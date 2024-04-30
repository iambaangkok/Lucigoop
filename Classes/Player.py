import sys
import pygame
import pygame.mixer
from pygame.mixer import *
from math import floor
from Classes.Object import * 
from Classes.HitBox import *
from Classes.Shockwave import *
from Classes.Arrow import *

pygame.mixer.init()
imagePath = "Images/"
soundPath = "Sound Effects/"
class Player(Object):
    soundLib = []
    soundLib.append(pygame.mixer.Sound(soundPath + 'Jump2 w.wav'))
    soundLib.append(pygame.mixer.Sound(soundPath + "Rake_Swing_Whoosh_Close c.wav"))
    soundLib.append(pygame.mixer.Sound(soundPath + "retro_ouch.wav"))
    speedY = 0
    speedX = 0
    isAttacking = False
    isJumping = False
    isSmthRight = False
    isSmthLeft = False
    currentJumpForce = 0
    jumpForceDecayRate = 2500
    maxJumpForceDecayRate = 2500

    attackDamage = [80,89,98,107,116,125,134,143,152,161]
    attackDamageLevel = 0
    
    rateOfAttack = [80,89,98,107,116,125,134,143,152,161]
    attackDelay = [0.75, 0.67, 0.61, 0.56, 0.51, 0.48, 0.44, 0.41, 0.39, 0.37]
    for i in range(0,9):
        attackDelay[i] = 60/rateOfAttack[i]/2
    attackDelayLevel = 0
    
    attackRange = [100,133,166,200,220,240,260,270,280,290]
    for i in range(0,10):
        attackRange[i] *= 2
    attackRangeLevel = 0

    maxHp = [3,4,5,6,7,8,9,10,11,12]
    for i in range(0,10):
        maxHp[i] += 2
        maxHpLevel = 0
    heal = 2
    currentHp = maxHp[maxHpLevel]

    levelUpKillsNeeded = [5,10,15,21,27,33,40,47,54,1000,1000,1000]
    for i in range(0,9):
        levelUpKillsNeeded[i] = floor(levelUpKillsNeeded[i]/1.5)
    currentLevel = 0
    currentKills = 0
    enemiesUntilNextLevel = 5
    shockWaveSpeed = 30

    frameTime = 0.11
    originalFrameTime = 0.11
    timeSinceLastFrame = 0

    timeSinceLastDamaged = 0
    immuneTime = 2.5
    def __init__(self):
        Object.__init__(self)

    def __init__(self,posX,posY,image,width,height,maxSpeedX,maxSpeedY,jumpForce,parent,name,g,anim):
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
        self.maxSpeedY = maxSpeedY
        self.jumpForce = jumpForce
        self.name = name
        self.hitBox = HitBox(posX,posY,width,height,self,"Player","Player",g)
        #self.bottomHitBox = HitBox(posX,posY+height-20,width,21,self,"Player","PlayerBOTTOM",g)
        self.currAnim = 0
        self.anim = anim
        self.animStart = 0
        self.animStop = 5

    def UpdatePlayer(self,g):
        self.timeSinceLastFrame += g.deltaTime
        self.timeSinceLastDamaged += g.deltaTime
        if g.P_space:
            pass#self.currentHp -= 1
        if self.currentHp <= 0:
            self.movementX = 0
            self.animStart = 14
            self.animStop = 20
            if self.timeSinceLastFrame > self.frameTime and self.currAnim != 19:
                self.timeSinceLastFrame = 0
                self.currAnim += 1
                if self.currAnim >= self.animStop or self.currAnim+1 < self.animStart:
                    self.currAnim = self.animStart-1
                self.image = self.anim[max(min(self.currAnim,self.animStop-1),self.animStart)]
                if g.pFacing == -1:
                    self.image = pygame.transform.flip(self.image,True,False)
            return
        if g.timeScale == 0:            
            return
        if self.levelUpKillsNeeded[self.currentLevel] - self.currentKills <= 0:
            self.currentLevel += 1
            g.levelUp()
            self.speedX = self.movementX = self.movementY = self.speedY = self.isAttacking = 0
            return
        else:
            self.enemiesUntilNextLevel = self.levelUpKillsNeeded[self.currentLevel] - self.currentKills
        #IF DED DO NOTHING
        if self.currentHp == 0:
            return
        
        #Check Attack
        if (g.P_mouse == True or g.P_space == True ) and g.timeSinceLastAttack > self.attackDelay[self.attackDelayLevel]:
            self.currAnim = 4
            g.p.attack(g.pFacing,g)
            g.attacked = True
            g.timeSinceLastAttack = 0
        #Check jump()
        self.currentJumpForce = max(self.currentJumpForce - (self.jumpForceDecayRate*g.deltaTime),0)
        if self.isJumping:
            self.jumpForceDecayRate *= 200*g.deltaTime
            if self.jumpForceDecayRate > self.maxJumpForceDecayRate:
                self.jumpForceDecayRate = self.maxJumpForceDecayRate
        #if g.P_w == True and self.isJumping == False:
        #    self.jump(self.jumpForce)
        #MoveXY
        if self.currentJumpForce != 0:
            self.speedY = -self.currentJumpForce
        else:
            self.speedY = self.speedY+(g.gravity)
            
        self.movementX = self.maxSpeedX*(g.P_d-g.P_a)*g.deltaTime
        if self.isJumping:
            self.movementX = self.maxSpeedX*(g.P_d-g.P_a)*g.deltaTime*1.2
        self.movementY = self.speedY*g.deltaTime
        #Handle Animation
        if self.movementX == 0:
            self.animStart = 0
            self.animStop = 2
        else:
            self.animStart = 0
            self.animStop = 5
        if g.timeSinceLastAttack < self.attackDelay[self.attackDelayLevel]:
            self.isAttacking = True
        else:
            self.isAttacking = False
        if self.isAttacking:
            ##############print("ATKing ", self.frameTime)
            self.frameTime = self.attackDelay[self.attackDelayLevel]/4
            self.animStart = 5
            self.animStop = 9
        else:
            self.frameTime = self.originalFrameTime
        if self.isJumping:
            self.animStart = 9
            self.animStop = 14

            ##############print("NOATKing ", self.frameTime)
        ##################print("N ",min(self.currAnim,self.animStop-1), " ", self.animStart, " ",self.animStop," ", g.timeSinceLastFrame)
        if self.timeSinceLastFrame > self.frameTime:
            ##############print("YES")
            self.timeSinceLastFrame = 0
            if self.isJumping and self.currAnim == 13:
                pass
            else:
                self.currAnim += 1
            if self.currAnim >= self.animStop or self.currAnim+1 < self.animStart:
                self.currAnim = self.animStart-1
            #############print(min(self.currAnim,self.animStop-1), " ", self.animStop)
            self.image = self.anim[max(min(self.currAnim,self.animStop-1),self.animStart)]
            if g.pFacing == -1:
                self.image = pygame.transform.flip(self.image,True,False)
        #Check Facing
        if self.movementX > 0:
            if g.pFacing < 0:
                self.image = pygame.transform.flip(self.image,True,False)
                g.pFacing = 1
        elif self.movementX < 0:
            if g.pFacing > 0:
                self.image = pygame.transform.flip(self.image,True,False)
                g.pFacing = -1
        #Update HitBox
        self.updateHitBox(g)
        #Check Collision With Level
        #self.collidingWithBottom = self.bottomHitBox.checkCollision(g)
        self.collidingWith = self.hitBox.checkCollision(g)
        collidedBottom = False
        collidedRight = False
        collidedLeft = False
        collidedTop = False
        for i in self.collidingWith:
            if i.type == "LevelTOP":
                collidedBottom = True
                if self.movementY > 0:
                    self.posY = i.posY-self.height+1
                    self.movementY = 0
                    self.speedY = 0
                    self.currentJumpForce = 0
                    self.isJumping = False
            if i.type == "LevelLEFT":
                collidedRight = True
                if self.movementX > 0:
                    self.posX = i.posX-self.width
                    self.movementX = 0
                    self.speedX = 0
            if i.type == "LevelRIGHT":
                collidedLeft = True
                if self.movementX < 0:
                    self.posX = i.posX+i.width
                    self.movementX = 0
                    self.speedX = 0
            if i.type == "LevelBOTTOM":
                collidedTop = True
                if self.movementY < 0:
                    self.posY = i.posY+i.height+1
                    self.movementY = 0
                    self.speedY = 0
                    self.currentJumpForce = 0
            if i.type == "Level" and i.parent.name[0] == 'K':
                g.keysCollected[floor((self.currentLevel+1)/3)-1] = 1
        if collidedBottom:
            pass
        else:
            self.isJumping = True

        if collidedRight:
            self.isSmthRight = True
        else:
            self.isSmthRight = False
        if collidedLeft:
            self.isSmthLeft = True
        else:
            self.isSmthLeft = False
            #if self.damageDealth == False and i.type == "Enemy":
                #i.parent.takeDamage(self.damage)
                #self.playHitEffect
                #self.damageDealth = True
        #Check Out Of Bounds
        if self.isJumping == False:
            self.movementY = 0
        if self.isSmthRight == True:
            if self.movementX > 0:
                self.movementX = 0
        if self.isSmthLeft == True:
            if self.movementX < 0:
                self.movementX = 0
        #print (self.movementX," ",self.movementY," ",self.currentJumpForce," ")
        if self.movementY > self.maxSpeedY*g.deltaTime:
            self.movementY = self.maxSpeedY*g.deltaTime
        if g.posY < -g.screenHeight*8 and self.posY+self.height+self.movementY > g.screenHeight-g.bottomMoveBorder+1:
            self.movementY = 0
            self.speedY = 0
            self.moveXY(self.movementX,self.movementY/2)
            #self.isJumping = False
        elif g.posY > g.topMoveBorder and self.posY+self.movementY < g.topMoveBorder-1:
            self.movementY = 0
            self.speedY = 0
            self.moveXY(self.movementX,self.movementY/2)
        else:
            self.moveXY(self.movementX,self.movementY)
        if self.posX+self.width < 30:
            self.posX = g.screenWidth-30
        elif self.posX > g.screenWidth-30:
            self.posX = 0-self.width+30

        

    def moveXY(self, movementX, movementY):
        self.moveX(movementX)
        self.moveY(movementY)

    def moveX(self, movementX):
        if movementX < 0:
            self.isSmthRight = False
        if movementX > 0:
            self.isSmthRight = False
        self.posX += movementX

    def moveY(self, movementY):
        if movementY > self.maxSpeedY:
            movementY = self.maxSpeedY
        if movementY < -self.maxSpeedY:
            movementY = -self.maxSpeedY
        self.posY += movementY
    
    def jump(self,jumpForce):
        if self.isJumping == False:
            self.soundLib[0].play()
            self.currAnim = 10
            self.jumpForceDecayRate = 1
            self.movementY = 0
            self.speedY = 0
            self.posY -= 2
            self.isJumping = True
            self.currentJumpForce = jumpForce
            #print("JUMP!")
    
    def updateHitBox(self,g):
        self.hitBox.parent = self
        self.hitBox.posX = self.posX
        self.hitBox.posY = self.posY 
        self.hitBox.width = self.width
        self.hitBox.height = self.height
        self.hitBox.updateHitBox()
        #self.bottomHitBox.parent = self
        #self.bottomHitBox.posX = self.posX
        #self.bottomHitBox.posY = self.posY+self.height-20
        #self.bottomHitBox.width = self.width
        #self.bottomHitBox.height = 21
        #self.bottomHitBox.updateHitBox()

    def attack(self,facing,g):
        self.soundLib[1].play()
        if facing < 0:
            self.shockWave = Shockwave(pygame.transform.flip(pygame.image.load(imagePath + "slash.png"),True,False),self.posX+self.width/2,self.posY,20,64,g,"Shockwave",self.attackDamage[self.attackDamageLevel],-self.shockWaveSpeed,self.attackRange[self.attackRangeLevel],g)
            self.shockWave.image = pygame.transform.scale(self.shockWave.image,(64,64))
        elif facing > 0:
            self.shockWave = Shockwave(pygame.image.load(imagePath + "slash.png"),self.posX+self.width/2,self.posY,20,64,g,"Shockwave",self.attackDamage[self.attackDamageLevel],+self.shockWaveSpeed,self.attackRange[self.attackRangeLevel],g)
            self.shockWave.image = pygame.transform.scale(self.shockWave.image,(64,64))

    def Draw(self,g):
        g.DISPLAY.blit(self.image,(self.posX-32,self.posY))

    def takeDamage(self,damage):
        if self.timeSinceLastDamaged > self.immuneTime:
            self.soundLib[2].play()
            self.timeSinceLastDamaged = 0
            self.currentHp = max(self.currentHp - damage,0)
            if self.currentHp == 0:
                self.currAnim = 13
                #print(self.currentHp, " YouDIED")
            self.knockBack(400)
    def knockBack(self,movementY):
        self.movementY = 0
        self.speedY = 0
        self.posY -= 2
        self.currentJumpForce = movementY