from pygame_functions import *
from math import sin, cos, pi
import time
from random import randint

setAutoUpdate(False)

screenWidth = 1800
screenHeight = 1000

class Car:
    def __init__(self, num):
        self.speed = 0
        if num == 1:
            self.drive = ["w", "s", "d", "a"]
            self.sprite = makeSprite("aacar1.png")
            self.xpos = 100  # cos
            self.ypos = 500
            self.direction = 180  # 0 - 360
        elif num == 2:
            self.drive = ["up", "down", "right", "left"]
            self.sprite = makeSprite("aacar2.png")
            self.xpos = 1700  # cos
            self.ypos = 500
            self.direction = 0  # 0 - 360
        showSprite(self.sprite)
        self.update()

    def update(self):
        if keyPressed(self.drive[0]):
            self.speed += 0.5
        if keyPressed(self.drive[1]):
            self.speed -= 0.5
        if self.speed > 3 or self.speed < -3:
            if keyPressed(self.drive[2]):
                self.direction += 3
            if keyPressed(self.drive[3]):
                self.direction -= 3

        if self.speed > 5:
            self.speed = 5
        elif self.speed < -5:
            self.speed = -5

        if self.speed > 0:
            self.speed -= 0.1
        elif self.speed < 0:
            self.speed += 0.1
        else:
            self.speed = 0

        if 0.2 > self.speed > -0.2:
            self.speed = 0

        if self.direction >= 360:
            self.direction = self.direction - 360
        elif self.direction < 0:
            self.direction = 360 + self.direction

        if self.direction < 90:
            self.xpos -= cos(self.direction * (math.pi / 180)) * self.speed
            self.ypos -= sin(self.direction * (math.pi / 180)) * self.speed
        elif self.direction == 90:
            self.ypos -= self.speed

        elif self.direction < 180:
            self.xpos += cos((180 - self.direction) * (math.pi / 180)) * self.speed
            self.ypos -= sin((180 - self.direction) * (math.pi / 180)) * self.speed
        elif self.direction == 180:
            self.xpos += self.speed

        elif self.direction < 270:
            self.xpos += cos((self.direction - 180) * (math.pi / 180)) * self.speed
            self.ypos += sin((self.direction - 180) * (math.pi / 180)) * self.speed
        elif self.direction == 270:
            self.ypos += self.speed

        elif self.direction < 360:
            self.xpos -= cos((360 - self.direction) * (math.pi / 180)) * self.speed
            self.ypos += sin((360 - self.direction) * (math.pi / 180)) * self.speed
        elif self.direction == 360:
            self.xpos += self.speed

        if self.xpos > screenWidth + 100:
            self.xpos -= screenWidth + 200
        elif self.xpos < -100:
            self.xpos += screenWidth + 200

        if self.ypos > screenHeight + 100:
            self.ypos -= screenHeight + 200
        elif self.ypos < -100:
            self.ypos += screenHeight + 200

        moveSprite(self.sprite, self.xpos, self.ypos, True)
        transformSprite(self.sprite, self.direction, 0.5)

class Wall:
    def __init__(self, xpos, ypos, rotation):
        self.xpos = xpos
        self.ypos = ypos
        self.rotation = rotation
        self.sprite = makeSprite("barrier.png")
        showSprite(self.sprite)
        moveSprite(self.sprite, xpos, ypos, True)
        transformSprite(self.sprite, self.rotation, 1)

class Bullet:
    def __init__(self, xpos, ypos, dir):
        self.xpos = xpos
        self.ypos = ypos
        self.direction = dir
        self.speed = 10
        self.sprite = makeSprite("bullet.png")
        showSprite(self.sprite)
        self.update()

    def update(self):
        if self.direction < 90:
            self.xpos -= cos(self.direction * (math.pi / 180)) * self.speed
            self.ypos -= sin(self.direction * (math.pi / 180)) * self.speed
        elif self.direction == 90:
            self.ypos -= self.speed

        elif self.direction < 180:
            self.xpos += cos((180 - self.direction) * (math.pi / 180)) * self.speed
            self.ypos -= sin((180 - self.direction) * (math.pi / 180)) * self.speed
        elif self.direction == 180:
            self.xpos += self.speed

        elif self.direction < 270:
            self.xpos += cos((self.direction - 180) * (math.pi / 180)) * self.speed
            self.ypos += sin((self.direction - 180) * (math.pi / 180)) * self.speed
        elif self.direction == 270:
            self.ypos += self.speed

        elif self.direction < 360:
            self.xpos -= cos((360 - self.direction) * (math.pi / 180)) * self.speed
            self.ypos += sin((360 - self.direction) * (math.pi / 180)) * self.speed
        elif self.direction == 360:
            self.xpos += self.speed

        moveSprite(self.sprite, self.xpos, self.ypos, True)
        transformSprite(self.sprite, self.direction, 0.5)

screenSize(screenWidth,screenHeight)

while True:
    C = [Car(1), Car(2)]

    outerWalls = []
    walls = []
    bullets = [[], []]
    score = [0, 0]
    clicked = False
    playing = True
    labels = [newLabel("Blue: " + str(score[0]), 40, "Arial", "white", 100, 100, "clear"),
              newLabel("Green: " + str(score[1]), 40, "Arial", "white", 1500, 100, "clear")]
    showLabel(labels[0])
    showLabel(labels[1])

    for xpos in range(0, screenWidth + 50, 20):
        outerWalls.append(Wall(xpos, 0, 0))
        outerWalls.append(Wall(xpos, screenHeight, 0))

    for ypos in range(0, screenHeight + 50, 20):
        outerWalls.append(Wall(0, ypos, 0))
        outerWalls.append(Wall(screenWidth, ypos, 0))

    lastWallTime = time.time()
    lastBulletTime = [time.time(), time.time()]

    while playing:
        for car in C:
            car.update()

        if mousePressed() and not clicked:
            walls.append(Wall(mouseX(), mouseY(), 0))
            clicked = True
        elif not mousePressed():
            clicked = False

        for i in range(0,2):
            if time.time() - lastBulletTime[i] > 1:
                if C[i].speed > 2:
                    bullets[i].append(Bullet(C[i].xpos, C[i].ypos, C[i].direction))
                    lastBulletTime[i] = time.time()

            for wall in walls + outerWalls:
                if touching(C[i].sprite, wall.sprite):
                    score[i] -= 5
                    if wall in walls:
                        hideSprite(wall.sprite)
                        walls.remove(wall)
                    else:
                        playing = False
                        break

            for bullet in bullets[i]:
                bullet.update()
                for wall in walls:
                    if touching(bullet.sprite, wall.sprite):
                        hideSprite(wall.sprite)
                        walls.remove(wall)
                        score[i] += 1
                for outerWall in outerWalls:
                    if touching(bullet.sprite, outerWall.sprite):
                        hideSprite(bullet.sprite)
                        if bullet in bullets:
                            bullets.remove(bullet)

        if time.time() - lastWallTime > 0.3:
            xtemp = randint(20, screenWidth - 20)
            ytemp = randint(20, screenHeight - 20)
            while C[0].xpos - 200 < xtemp < C[0].xpos + 200 and C[0].ypos - 200 < ytemp < C[0].ypos + 200 or C[1].xpos - 200 < xtemp < C[1].xpos + 200 and C[1].ypos - 200 < ytemp < C[1].ypos + 200:
                xtemp = randint(20, screenWidth - 20)
                ytemp = randint(20, screenHeight - 20)
            walls.append(Wall(xtemp, ytemp, 0))
            lastWallTime = time.time()

        changeLabel(labels[0], "Blue: " + str(score[0]))
        changeLabel(labels[1], "Green: " + str(score[1]))

        updateDisplay()
        tick(60)

    for sprite in [*C , *walls , *outerWalls]:
        hideSprite(sprite.sprite)

    for i in range(0, 2):
        for bullet in bullets[i]:
            hideSprite(bullet.sprite)
        hideLabel(labels[i])