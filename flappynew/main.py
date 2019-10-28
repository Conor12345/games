from pygame_functions import *
from random import randint
from time import time

setAutoUpdate(False)
multiple = 1

class Bird:
    def __init__(self):
        self.ypos = 300
        self.yspeed = 0
        self.sprite = makeSprite("birdi.png")
        showSprite(self.sprite)

    def move(self):
        self.ypos += self.yspeed
        self.yspeed += 1 * multiple
        moveSprite(self.sprite, 150, self.ypos, True)

    def flap(self):
        self.yspeed = -15
        self.ypos += self.yspeed * multiple
        moveSprite(self.sprite, 150, self.ypos, True)

class Pipe:
    def __init__(self):
        self.xpos = 610
        self.height = 100 + randint(0,400)
        self.gap = 280
        self.score = 1

        self.botSprite = makeSprite("pipe_bottom.png")
        showSprite(self.botSprite)

        self.topSprite = makeSprite("pipe_top.png")
        showSprite(self.topSprite)

        self.move()

    def move(self):
        self.xpos -= 4 * multiple
        moveSprite(self.botSprite, self.xpos, 900 - self.height)
        moveSprite(self.topSprite, self.xpos, 900 - self.height - self.gap - 600)

screenSize(600, 900)
setBackgroundColour("white")

timeText = newLabel("", 80,"Roboto", "Black", 250, 50, "clear")

f = open("highscore.txt", "r")
for line in f:
    currenthighscore = int(line.strip())

highScoreText = newLabel("High Score: " + str(currenthighscore), 30, "Roboto", "Black", 50, 50, "clear")
showLabel(highScoreText)

running = True

while running:
    B = Bird()
    B.move()

    playing = True
    released = True
    multiple = 1

    ground = makeSprite("ground.png")
    showSprite(ground)
    moveSprite(ground, 0, 850)

    roof = makeSprite("ground.png")
    showSprite(roof)
    moveSprite(roof, 0, -50)

    pipes = [Pipe()]

    startText = newLabel("Press space to start", 40, "Roboto", "black", 150, 450, "clear")
    showLabel(startText)

    extraText = newLabel('Press "A" for automatic', 30, "Roboto", "black", 170, 500, "clear")
    showLabel(extraText)

    updateDisplay()
    running = True

    while True:
        if keyPressed("space"):
            automatic = False
            break
        elif keyPressed("a"):
            automatic = True
            break
        elif keyPressed("q"):
            playing = False
            running = False
            f = open("highscore.txt", "w")
            f.write(str(currenthighscore))
            break

    hideLabel(startText)
    hideLabel(extraText)
    hideLabel(timeText)


    startTime = time()
    score = 0
    timeText = newLabel(str(score), 80, "Roboto", "Black", 250, 50, "clear")
    showLabel(timeText)



    while playing:
        if keyPressed("space") and released:
            B.flap()
            released = False
        elif not keyPressed("space"):
            B.move()
            released = True
        else:
            B.move()

        if keyPressed("q"):
            playing = False
            running = False
            f = open("highscore.txt", "w")
            f.write(str(currenthighscore))

        if automatic:
            if len(pipes) == 1:
                if B.ypos > 900 - pipes[0].height - 100:
                    B.flap()
            else:
                if pipes[0].xpos < 20:
                    if B.ypos > 900 - pipes[1].height - 50:
                        B.flap()
                else:
                    if B.ypos > 900 - pipes[0].height - 50:
                        B.flap()

        for pipe in pipes:
            pipe.move()
        if pipes[-1].xpos < 200:
            pipes.append(Pipe())
        if pipes[0].xpos < -100:
            pipes.pop(0)

        for pipe in pipes:
            if touching(pipe.topSprite, B.sprite) or touching(pipe.botSprite, B.sprite):
                playing = False
                break

        if touching(B.sprite, ground):
            playing = False
        if touching(B.sprite, roof):
            playing = False

        if pipes[0].xpos < 80:
            score += pipes[0].score
            pipes[0].score = 0

        changeLabel(timeText, str(score))

        multiple = 1 + (score / 50)

        updateDisplay()
        tick(60)

    if score > currenthighscore:
        currenthighscore = score
        hideLabel(highScoreText)
        highScoreText = newLabel("High Score: " + str(currenthighscore), 30, "Roboto", "Black", 50, 50, "clear")
        showLabel(highScoreText)

    hideSprite(B.sprite)
    for pipe in pipes:
        hideSprite(pipe.topSprite)
        hideSprite(pipe.botSprite)
    hideSprite(ground)
    hideSprite(roof)
