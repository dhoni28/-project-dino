from tkinter import *
from tkinter import messagebox
from random import randint


class gamewindow():
    def __init__(s):
        s.root = Tk()
        s.root.title("Dinosaur Game")
        s.root.grid()

        s.canvas = Canvas(width=1900, height=600, bg="White")
        s.canvas.grid()

        s.cont = "Y"
        s.jump = "N"
        s.jumping = "N"
        s.duck = "N"
        s.ducking = "N"
        s.jumpvel = 0
        s.score = 0
        s.delay = 10
        s.recentscore = 0
        s.recentscore1 = 0
        s.hazard = list()

        s.line = s.canvas.create_line(0, 500, 1900, 500)
        s.dinohitbox = s.canvas.create_rectangle(50, 370, 100, 500, fill="Black")
        s.scorelabel = s.canvas.create_text(1700, 30, fill="Black", font="Calibri 20 bold", text=s.score)

        s.root.bind("<KeyPress>", lambda event="<KeyPress>": gamewindow.keypress(event, s))
        s.root.bind("<KeyRelease>", lambda event="<KeyRelease>": gamewindow.keyrelease(event, s))

        gamewindow.scrolling(s)
        gamewindow.ConstantRefresh(s)

        s.root.mainloop()

    def ConstantRefresh(s):  # Jumping and score

        if s.cont == "Y":
            if s.jump == "Y" and s.jumping == "N":
                s.jumpvel = 20
                s.jumping = "Y"

            dinoposition = list(s.canvas.bbox(s.dinohitbox))  # ADD COLLISION DETECTION HERE!!!
            for i in range(len(s.hazard)):
                hazardposition = list(s.canvas.bbox(s.hazard[i]))

                for x in range(2):
                    tempx = x * 2
                    if hazardposition[tempx] >= dinoposition[0] and hazardposition[tempx] <= dinoposition[2] and \
                            hazardposition[tempx + 1] >= dinoposition[1] and hazardposition[tempx + 1] <= dinoposition[
                        3]:
                        s.cont = "N"

            if s.jumping == "Y" and s.ducking == "N":

                if int(dinoposition[3]) < 501 or s.jumpvel == 20:
                    s.canvas.move(s.dinohitbox, 0, -s.jumpvel)
                    s.jumpvel -= 1

                else:
                    s.jumping = "N"

                    difference = int(dinoposition[3]) - 501
                    s.canvas.move(s.dinohitbox, 0, -difference)

            elif s.duck == "Y":
                s.duck = "N"
                s.ducking = "Y"
                s.canvas.move(s.dinohitbox, 0, 60)

            s.score += 1
            s.canvas.delete(s.scorelabel)
            s.scorelabel = s.canvas.create_text(1700, 30, fill="Black", font="Calibri 20 bold", text=int(s.score / 10))
            s.root.after(13, gamewindow.ConstantRefresh, s)

    def scrolling(s):  # scrolls the level which speeds up over time
        hazards = ["Nothing", "Small", "Large", "Birds"]

        if s.cont == "Y":
            if s.score % 2500 == 0 and s.score != s.recentscore1 and s.delay > 1:
                s.delay -= 1
                s.recentscore1 = s.score

            if s.score >= 200 and s.score % 100 == 0 and s.recentscore != s.score:
                s.recentscore = s.score
                choice = hazards[randint(0, 3)]  # Nothing, small cactus, large cactus, birds respectively
                amount = randint(1, 3)  # amount of hazard chosen (however position if bird)

                if choice != "Nothing":
                    if choice == "Small" or choice == "Large":
                        if choice == "Small":  # large cacti are almost the same height and width as the dino, small cacti are slighty over half the height and thickness of the dino
                            vertices = [1900, 420, 1950, 500]
                            gap = 60

                        if choice == "Large":
                            vertices = [1900, 360, 1960, 500]
                            gap = 65

                        for i in range(amount):
                            s.hazard.append("")
                            s.hazard[len(s.hazard) - 1] = s.canvas.create_rectangle(vertices[0] + (gap * i),
                                                                                    vertices[1],
                                                                                    vertices[2] + (gap * i),
                                                                                    vertices[3], fill="Black")

                    elif choice == "Birds":
                        position = (amount - 1) * 100
                        vertices = [1900, 240 + position, 1950, 300 + position]
                        s.hazard.append("")
                        s.hazard[len(s.hazard) - 1] = s.canvas.create_rectangle(vertices[0], vertices[1], vertices[2],
                                                                                vertices[3], fill="Blue")

            while len(s.hazard) > 9:  # only allows 9 hazards on the canvas at any given time
                s.canvas.delete(s.hazard[0])
                del s.hazard[0]

            for i in range(len(s.hazard)):
                s.canvas.move(s.hazard[i], -10, 0)

            s.root.after(s.delay, gamewindow.scrolling, s)

    def keypress(event, s):
        keypressed = event.keysym
        if (keypressed == "space" or keypressed == "Up") and s.jumping == "N":
            s.jump = "Y"

        if keypressed == "Down":
            if s.jumping == "N" and s.ducking == "N":
                s.duck = "Y"

    def keyrelease(event, s):
        keyreleased = event.keysym
        if keyreleased == "space" or keyreleased == "Up":
            s.jump = "N"
            if s.jumpvel > 0:
                s.jumpvel = 0

        if keyreleased == "Down":
            if s.ducking == "Y":
                s.ducking = "N"
                s.canvas.move(s.dinohitbox, 0, -60)
if __name__ == "__main__":
    game = gamewindow()