f = open("highscore.txt", "r")
for line in f:
    currenthighscore = int(line.strip())

print(currenthighscore)
currenthighscore = 8

f = open("highscore.txt", "w")
f.write(str(currenthighscore))