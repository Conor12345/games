from pygame_functions import *
from random import randint
screen_width = 800
screen_height = 800
setAutoUpdate(False)
enemyTypes = ["enemy.gif", "enemy2.gif"]

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
        self.lastSprayTime = clock()

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
        if keyPressed("s") and clock() > self.lastBulletTime + 30:
            if self.xdir != 0 or self.ydir != 0:
                bullets.append(Projectile(self.xpos, self.ypos, self.xdir * 10 , self.ydir * 10, 1))
            self.lastBulletTime = clock()
        if keyPressed("c") and clock() > self.lastSprayTime + 1000:
            for i in range(3):
                bullets.append(Projectile(self.xpos, self.ypos, 0, -10, 1))
                bullets.append(Projectile(self.xpos, self.ypos, -10, -10, 1))
                bullets.append(Projectile(self.xpos, self.ypos, -10, 0, 1))
                bullets.append(Projectile(self.xpos, self.ypos, -10, 10, 1))
                bullets.append(Projectile(self.xpos, self.ypos, 0, 10, 1))
                bullets.append(Projectile(self.xpos, self.ypos, 10, 10, 1))
                bullets.append(Projectile(self.xpos, self.ypos, 10, 0, 1))
                bullets.append(Projectile(self.xpos, self.ypos, 10, -10, 1))
            self.lastSprayTime = clock()
        self.move()
        for enemy in enemies:
            if self.xpos < enemy.xpos and self.xpos + 48 > enemy.xpos and self.ypos < enemy.ypos and self.ypos + 48 > enemy.ypos:
                self.lives -= 1
                print("Lives remaining:", self.lives)
                hideSprite(enemy.sprite)
                enemies.remove(enemy)

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

class Enemy():
    def __init__(self, speed, damage, type, lives):
        self.xpos = randint(0, screen_width)
        self.ypos = randint(0, screen_height)
        self.speed = speed
        self.xspeed = randint(-speed, speed)
        self.yspeed = randint(-speed, speed)
        self.damage = damage
        self.type = type
        self.sprite = makeSprite(enemyTypes[self.type])
        self.lives = lives
        self.label = makeLabel(str(self.lives), 12, self.xpos, self.ypos + 20, fontColour="black", font="Consolas")
        self.move()
        showSprite(self.sprite)
        showLabel(self.label)

    def move(self):
        if self.type == 0:
            # Random path finding
            self.xpos += self.xspeed
            self.ypos += self.yspeed
            if self.xpos < 0:
                self.xspeed = randint(0, self.speed)
            elif self.xpos > 800 - 48:
                self.xspeed = randint(-self.speed, 0)
            if self.ypos < 0:
                self.yspeed = randint(0, self.speed)
            elif self.ypos > 800 - 48:
                self.yspeed = randint(-self.speed, 0)
            for bullet in bullets:
                if self.xpos < bullet.xpos and self.xpos + 48 > bullet.xpos and self.ypos < bullet.ypos and self.ypos + 48 > bullet.ypos:
                    self.lives -= 1
                    if self.lives == 0:
                        hideSprite(bullet.sprite)
                        bullets.remove(bullet)
                        return False

        if self.type == 1:
            # Path finds to player
            if p.xpos < self.xpos:
                self.xpos -= self.speed
            elif p.xpos > self.xpos:
                self.xpos += self.speed
            if p.ypos < self.ypos:
                self.ypos -= self.speed
            elif p.ypos > self.ypos:
                self.ypos += self.speed
            for bullet in bullets:
                if self.xpos < bullet.xpos and self.xpos + 48 > bullet.xpos and self.ypos < bullet.ypos and self.ypos + 48 > bullet.ypos:
                    self.lives -= 1
                    if self.lives == 0:
                        hideSprite(bullet.sprite)
                        bullets.remove(bullet)
                        return False
        moveSprite(self.sprite, self.xpos, self.ypos)
        changeLabel(self.label, str(self.lives))
        moveLabel(self.label,self.xpos, self.ypos + 20)

screenSize(screen_width, screen_height)
setBackgroundColour("white")
p = Player(0)
bullets = []

scoreLabel = makeLabel("Score: 0", 20, 10, 10, fontColour="black", font="Consolas")
livesLabel = makeLabel("Lives: 3", 20, 150, 10, fontColour="black", font="Consolas")
showLabel(scoreLabel)
showLabel(livesLabel)

enemies = []
times = []
for i in range(4):
    times.append(clock())
score = 0

for i in range(10):
    enemies.append(Enemy(5, 1, 0, 5))

while True:
    p.update()
    for bullet in bullets:
        if bullet.move() == False:
            hideSprite(bullet.sprite)
            bullets.remove(bullet)
    for enemy in enemies:
        if enemy.move() == False:
            hideSprite(enemy.sprite)
            enemies.remove(enemy)
            score += 1
            print("Score:", score)
    if clock() > times[0] + 500:
        enemies.append(Enemy(10, 1, 0, 1))
        times[0] = clock()
    if clock() > times[1] + 1000 and score > 20:
        enemies.append(Enemy(5, 1, 1, 1))
        times[1] = clock()
    if clock() > times[2] + 1000 and score > 40:
        enemies.append(Enemy(8, 1, 1, 1))
        times[2] = clock()
    if clock() > times[3] + 1000 and score > 60:
        enemies.append(Enemy(8, 1, 1, 2))
        times[3] = clock()
    if p.lives == 0:
        break
    changeLabel(scoreLabel, "Score: " + str(score))
    changeLabel(livesLabel, "Lives: " + str(p.lives))
    tick(60)
    updateDisplay()
endWait()
