from pygame_functions import *

screen_width = 800
screen_height = 800
setAutoUpdate(False)

class Player():
    def __init__(self, type=int):
        self.xpos = screen_width / 2
        self.ypos = screen_height / 2
        self.speed = 5
        self.sprite = makeSprite("playerRight.png")
        addSpriteImage(self.sprite, "playerLeft.png")
        showSprite(self.sprite)
        self.lives = 3
        self.route = type
        self.xdir = 0
        self.ydir = 0
        self.lastBulletTime = clock()

    def move(self):
        if keyPressed("left"):
            self.xpos -= self.speed
            if self.xpos < 0:
                self.xpos = 0
            changeSpriteImage(self.sprite,1)
            self.xdir = -1
        elif keyPressed("right"):
            self.xpos += self.speed
            if self.xpos > screen_width - 64:
                self.xpos = 800 - 64
            changeSpriteImage(self.sprite, 0)
            self.xdir = 1
        else:
            self.xdir = 0
        if keyPressed("up"):
            self.ypos -= self.speed
            if self.ypos < 10:
                self.ypos = 10
            self.ydir = -1
        elif keyPressed("down"):
            self.ypos += self.speed
            if self.ypos > screen_height - 74:
                self.ypos = 800 - 74
            self.ydir = 1
        else:
            self.ydir = 0
        moveSprite(self.sprite, self.xpos, self.ypos)

    def update(self):
        self.move()
        if keyPressed("space"):
            if clock() > self.lastBulletTime + 30:
                if self.xdir != 0 or self.ydir != 0:
                    bullets.append(Projectile(self.xpos, self.ypos, self.xdir * 10 , self.ydir * 10, 1))
                self.lastBulletTime = clock()

class Projectile():
    def __init__(self, xpos, ypos, xspeed, yspeed, damage):
        self.xpos = xpos + 32
        self.ypos = ypos + 32
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.damage = damage
        self.sprite = makeSprite("dot.png")
        self.move()
        showSprite(self.sprite)

    def move(self):
        self.xpos += self.xspeed
        self.ypos += self.yspeed
        if self.xpos < 0 or self.xpos > screen_width or self.ypos < 0 or self.ypos > screen_height:
            return False
        moveSprite(self.sprite, self.xpos, self.ypos)

screenSize(screen_width, screen_height)
p = Player(0)
bullets = []

while True:
    p.update()
    for bullet in bullets:
        if bullet.move() == False:
            hideSprite(bullet.sprite)
            bullets.remove(bullet)
    tick(60)
    updateDisplay()
endWait()
