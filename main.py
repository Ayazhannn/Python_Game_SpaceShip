import os
import random
import winsound
from tkinter import messagebox

#python library that provides easy and intuitive way to draw shapes
import turtle
import time
turtle.fd(0) # to show the window
turtle.speed(0) #speed of animation
turtle.bgcolor("black") #change the bg color
turtle.title("SpaceClash")
turtle.bgpic("./template/starfield.gif") #change the bg image
turtle.ht() # to hide default turtle
turtle.setundobuffer(1) #saves memory
turtle.tracer(0)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 0 #start sprite speed


    # Default movement function
    def move(self):
        self.fd(self.speed)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    #detect location
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
            (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() <= (other.ycor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)):
            return True
        else:
            return False



class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4 # start player speed
        self.lives = 3

    def turn_left(self):
        self.lt(45)# degrees

    def turn_right(self):
        self.rt(45)

    #increase the speed
    def accelerate(self):
        self.speed += 2

    # decrease the speed
    def decelerate(self):
        self.speed -= 1

    def hyperspace(self):
        mp3_bg = './sound/music.wav'
        winsound.PlaySound(mp3_bg, winsound.SND_ASYNC)
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        self.goto(x, y)
        self.setheading(random.randint(0, 360))
        self.speed *= 0.5

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0,360))
        degrees = random.randint(20, 60)
        if self.xcor() > 290:
            self.setx(290)
            self.rt(degrees)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(degrees)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(degrees)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(degrees)

class Weapon(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3,stretch_len=0.5, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "ready":
            # Sound of the weapon
            mp3_weapon = './sound/weapon.wav'
            winsound.PlaySound(mp3_weapon, winsound.SND_ASYNC)
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000,1000)

        if self.status == "firing":
            self.fd(self.speed)

        #Border Check
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() >290:
            self.goto(-1000,1000)
            self.status = "ready"

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)
        degrees = random.randint(20,60)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(degrees)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(degrees)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(degrees)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(degrees)

    def avoid(self, other):
            if (self.xcor() >= (other.xcor() - 40)) and \
                    (self.xcor() <= (other.xcor() + 40)) and \
                    (self.ycor() >= (other.ycor() - 40)) and \
                    (self.ycor() <= (other.ycor() + 40)):
                self.lt(30)

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame != 0:
            self.fd(18 - self.frame)
            self.frame += 1

            if self.frame < 6:
                self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)
            elif self.frame < 11:
                self.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
            else:
                self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)

            if self.frame > 18:
                self.frame = 0
                self.goto(-1000, -1000)
                turtle.tracer(6)


# Keep all game information
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        #Draw border
        self.pen.speed(0) #animation speed
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()

        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()

    def show_status(self):
        self.pen.undo()
        if game.lives > 0:
            msg = "Level: %s Lives: %s Score: %s " % (self.level, self.lives, self.score)
        else:
            msg = "Game Over Score: %s" % (self.score)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.write(msg, font=("Arial", 16, "normal"))


# Create game object
game = Game()

# Draw the game border
game.draw_border()

# Show the game status
game.show_status()

# Create my sprites
player = Player("triangle", "white", 0,0)
#enemy = Enemy("circle", "red", -100,0)
weapon = Weapon("triangle", "green", 0,0)
#ally = Ally("square", "blue", 100,0)

enemies =[]
for i in range(10):
    enemies.append(Enemy("circle", "red", -100, 0))

allies =[]
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))


# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(weapon.fire, "space")
turtle.listen()

# Main loop
while True:
    turtle.update()
    time.sleep(0.02)
    if game.state == "restart":
        game.lives = 3
        game.score = 0
        player.speed = 0
        player.goto(0, 0)
        player.setheading(0)

        for enemy in enemies:
            enemy.goto(random.randint(-200, 200), random.randint(-200, 200))

        for ally in allies:
            ally.goto(random.randint(-200, 200), random.randint(-200, 200))

        game.state = "playing"

    if game.state == "playing":
        player.move()
        weapon.move()

        for enemy in enemies:
            enemy.move()

            # Check collisions
            if player.is_collision(enemy):
                mp3_explosion = './sound/explosion.wav'
                winsound.PlaySound(mp3_explosion, winsound.SND_ASYNC)
                player.color("red")
                for particle in particles:
                    particle.explode(enemy.xcor(), enemy.ycor())
                player.rt(random.randint(100, 200))
                enemy.goto(random.randint(-200, 200), random.randint(-200, 200))
                enemy.speed += 1
                game.lives -= 1
                if game.lives < 1:
                    game.state = "gameover"
                game.show_status()
                player.color("white")

            if weapon.is_collision(enemy):
                mp3_explosion = './sound/explosion.wav'
                winsound.PlaySound(mp3_explosion, winsound.SND_ASYNC)
                for particle in particles:
                    particle.explode(enemy.xcor(), enemy.ycor())

                weapon.status = "ready"
                enemy.goto(random.randint(-200, 200), random.randint(-200, 200))
                enemy.speed += 1
                game.score += 100
                game.show_status()

        for ally in allies:
            ally.move()

            # Avoid enemy
            for enemy in enemies:
                ally.avoid(enemy)

            # Allies should avoid player as well
            ally.avoid(player)

            # Check collisions
            if weapon.is_collision(ally):
                mp3_explosion = './sound/explosion.wav'
                winsound.PlaySound(mp3_explosion, winsound.SND_ASYNC)
                for particle in particles:
                    particle.explode(ally.xcor(), ally.ycor())
                weapon.status = "ready"
                ally.goto(random.randint(-200, 200), random.randint(-200, 200))
                ally.speed += 1
                game.score -= 50
                game.show_status()

    for particle in particles:
        particle.move()

    if game.state == "gameover":
        for i in range(360):
            player.rt(1)

        if messagebox.askyesno("Game Over", "Play again?") == True:
            game.state = "restart"
        else:
            exit()



turtle.mainloop() #to keep the window open
