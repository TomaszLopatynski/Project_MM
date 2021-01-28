import math
import os
from tkinter import *
import random
from itertools import chain
import io
import PIL
from PIL import Image, EpsImagePlugin
from operator import itemgetter
from ctypes import windll


def rgb(x, y, z):
    return "#%02x%02x%02x" % (x, y, z)


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.Frame1 = Frame(self.master)
        self.Frame1.grid(row=0, column=0, padx=5, pady=5, sticky=W + E + N + S)
        self.Frame2 = Frame(self.master)
        self.Frame2.grid(row=0, column=1, padx=5, pady=5, sticky=W + E + N + S)

        self.MiniMaxiFrame1 = Frame(self.Frame2)
        self.MiniMaxiFrame1.grid(row=0, column=0, pady=15, sticky=W + E + N + S)

        self.MiniMaxiFrame2 = Frame(self.Frame2)
        self.MiniMaxiFrame2.grid(row=1, column=0, pady=15, sticky=W + E + N + S)

        self.MiniMaxiFrame3 = Frame(self.Frame2)
        self.MiniMaxiFrame3.grid(row=2, column=0, pady=15, sticky=W + E + N + S)

        self.MiniFrame1 = Frame(self.MiniMaxiFrame1, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame1.grid(row=0, column=0, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame2 = Frame(self.MiniMaxiFrame1, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame2.grid(row=0, column=1, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame3 = Frame(self.MiniMaxiFrame2, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame3.grid(row=0, column=0, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame5 = Frame(self.MiniMaxiFrame2, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame5.grid(row=0, column=1, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame4 = Frame(self.Frame2, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame4.grid(row=3, column=0, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame6 = Frame(self.Frame2, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame6.grid(row=4, column=0, padx=15, pady=15, sticky=W + E + N + S)

        self.MiniFrame7 = Frame(self.Frame2, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        self.MiniFrame7.grid(row=5, column=0, padx=15, pady=15, sticky=W + E + N + S)

        self.b = Canvas()
        self.grainColour = []
        self.clickedColours = []

        self.entryX = Entry(self.MiniFrame1)
        self.entryY = Entry(self.MiniFrame1)
        self.entryNode = Entry(self.MiniFrame1)
        self.entryGrains = Entry(self.MiniFrame2)
        self.entryInclusionsAmount = Entry(self.MiniFrame3)
        self.entryInclusionsSize = Entry(self.MiniFrame3)
        self.entryPercentage = Entry(self.MiniFrame6)
        self.entryBorderSize = Entry(self.MiniFrame5)

        self.varNeighbor = StringVar(self.MiniFrame6)
        self.varBoundary = StringVar(self.MiniFrame6)
        self.varInclusions = StringVar(self.MiniFrame3)
        self.varSimulations = StringVar(self.MiniFrame6)
        self.varStructure = StringVar(self.MiniFrame4)

        self.nodeSize = 5
        self.sizeX = 100
        self.sizeY = 100
        self.grains = 0
        self.inclusions = 0
        self.rectangle = []

        self.menu()
        self.selSize()
        self.grainsNumber()
        self.inclusionsDef()
        self.structureDef()
        self.bordersDef()
        self.simulateChooseDef()
        self.simulateDef()
        self.board(self.sizeX * self.nodeSize, self.sizeY * self.nodeSize)

    def menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu, tearoff=0)

        export = Menu(fileMenu, tearoff=0)
        export.add_command(label="Data file", command=self.expTXT)
        export.add_command(label="Bitmap file", command=self.expBMP)

        imp = Menu(fileMenu, tearoff=0)
        imp.add_command(label="Data file", command=self.impTXT)
        imp.add_command(label="Bitmap file", command=self.impBMP)

        microstructureMenu = Menu(fileMenu, tearoff=0)
        microstructureMenu.add_cascade(label='Import', menu=imp)
        microstructureMenu.add_cascade(label='Export', menu=export)

        fileMenu.add_cascade(label='Microstructure', menu=microstructureMenu)
        fileMenu.add_command(label="Exit", command=self.exitProgram)

        menu.add_cascade(label="File", menu=fileMenu)

    def board(self, width, height):
        self.b = Canvas(self.Frame1, width=width, height=height, highlightthickness=0)
        self.b.grid(row=0, column=0, sticky=E + W + S + N)
        self.createRectangle()
        self.b.bind('<Button-1>', self.click)

    def selSize(self):
        Label(self.MiniFrame1, text='x:').grid(row=0, column=0, sticky=W)
        self.entryX.grid(row=0, column=1, sticky=W)

        Label(self.MiniFrame1, text='y:').grid(row=1, column=0, sticky=W)
        self.entryY.grid(row=1, column=1, sticky=W)

        selectSize = Button(self.MiniFrame1, text="Select", command=self.size)
        selectSize.grid(row=1, padx=5, pady=5, column=4)

        Label(self.MiniFrame1, text='Node size:').grid(row=2, column=0, sticky=W)
        self.entryNode.grid(row=2, column=1)

        selectNode = Button(self.MiniFrame1, text="Select", command=self.node)
        selectNode.grid(row=2, padx=5, pady=5, column=4)

    def grainsNumber(self):
        Label(self.MiniFrame2, text='Number of Grains').grid(row=0, column=0, sticky=W)
        self.entryGrains.grid(row=0, column=1)

        selectGrains = Button(self.MiniFrame2, text="Select", command=self.randomGrain)
        selectGrains.grid(row=0, padx=10, column=2)

    def inclusionsDef(self):
        inclusions = ["Square", "Circular"]
        self.varInclusions.set(inclusions[0])

        Label(self.MiniFrame3, text='Amount of inclusions:').grid(row=0, column=0, sticky=W)
        self.entryInclusionsAmount.grid(row=0, column=1)

        Label(self.MiniFrame3, text='Size of inclusions:').grid(row=1, column=0, sticky=W)
        self.entryInclusionsSize.grid(row=1, column=1)

        option = OptionMenu(self.MiniFrame3, self.varInclusions, *inclusions)
        option.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        selectInclusions = Button(self.MiniFrame3, text="Select", command=self.addInclusions)
        selectInclusions.grid(row=1, column=2, padx=5, pady=5)

    def structureDef(self):
        selection = ["Substructure", "Dual-Phase"]
        self.varStructure.set(selection[0])

        option = OptionMenu(self.MiniFrame4, self.varStructure, *selection)
        option.grid(row=0, column=0, padx=5, sticky=W)

    def bordersDef(self):
        Label(self.MiniFrame5, text='Border size:').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.entryBorderSize.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        simulate = Button(self.MiniFrame5, text="Borders", command=self.borders)
        simulate.grid(row=0, column=2, padx=5, sticky=W)

        clearSpace = Button(self.MiniFrame5, text="Clear", command=self.clearSpace)
        clearSpace.grid(row=0, column=3, padx=5, sticky=W)

    def simulateChooseDef(self):
        neighborhoodChoose = ["Moore", "VonNeumann", "PentagonalRandom", "HexagonalRandom"]
        boundary = ["Absorbing", "Periodic"]
        simulations = ["CA", "SC"]

        self.varNeighbor.set(neighborhoodChoose[0])
        self.varBoundary.set(boundary[0])
        self.varSimulations.set(simulations[0])

        option = OptionMenu(self.MiniFrame6, self.varNeighbor, *neighborhoodChoose)
        option.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        option = OptionMenu(self.MiniFrame6, self.varBoundary, *boundary)
        option.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        option = OptionMenu(self.MiniFrame6, self.varSimulations, *simulations)
        option.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        Label(self.MiniFrame6, text='SC percentage:').grid(row=0, column=3, sticky=W)
        self.entryPercentage.grid(row=0, column=4, sticky=W)

    def simulateDef(self):
        simulate = Button(self.MiniFrame7, text="Simulate", command=self.grainGrowth)
        simulate.config(font=16)
        simulate.grid(row=0, column=0, padx=5)

        simulateStructure = Button(self.MiniFrame7, text="Simulate with structure", command=self.structure)
        simulateStructure.config(font=16)
        simulateStructure.grid(row=0, column=1, padx=5)

        clear = Button(self.MiniFrame7, text="Clear", command=self.clear)
        clear.config(font=16)
        clear.grid(row=0, column=2, padx=5)

    def size(self):
        try:
            self.sizeX = int(self.entryX.get())
            self.sizeY = int(self.entryY.get())
        except ValueError:
            self.sizeX = 0
            self.sizeY = 0
        self.board(self.sizeX * self.nodeSize, self.sizeY * self.nodeSize)

    def node(self):
        try:
            self.nodeSize = int(self.entryNode.get())
        except ValueError:
            self.nodeSize = 0
        self.board(self.sizeX * self.nodeSize, self.sizeY * self.nodeSize)

    def createRectangle(self):
        self.rectangle = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                x1 = i * self.nodeSize
                y1 = j * self.nodeSize
                x2 = x1 + self.nodeSize
                y2 = y1 + self.nodeSize
                self.rectangle[i][j] = self.b.create_rectangle(x1, y1, x2, y2, fill="white", width=0)

    def randomGrain(self):
        try:
            self.grains = int(self.entryGrains.get())
        except ValueError:
            self.grains = 0
        for i in range(self.grains):
            state = True
            while state:
                rand = random.randint(0, (self.sizeX * self.sizeY) - 1)
                state = False
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        if self.b.itemcget(self.rectangle[i][j], "fill") == "white":
                            state = True
                            break
                if self.b.itemcget(self.rectangle[(rand % self.sizeX)][(int(rand / self.sizeY))], "fill") != "white":
                    continue
                else:
                    colour = self.random_color()
                    self.grainColour.append(colour)
                    self.b.itemconfig(self.rectangle[(rand % self.sizeX)][(int(rand / self.sizeY))], fill=colour, stipple="")
                    state = False

    def clear(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                self.b.itemconfig(self.rectangle[i][j], fill="white")
        self.clickedColours = []

    def grainGrowth(self):
        varSimulation = self.varSimulations.get()
        state = True
        if varSimulation == "CA":
            boolMatrix = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
            rnd = self.rndChoose()
            while state:
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        if self.b.itemcget(self.rectangle[i][j], "fill") != "white" and self.b.itemcget(
                                self.rectangle[i][j], "fill") != "#010000":
                            boolMatrix[i][j] = True
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        if self.b.itemcget(self.rectangle[i][j], "fill") != "white" and boolMatrix[i][j] and self.b.itemcget(self.rectangle[i][j], "fill") not in self.clickedColours:
                            self.neighbourhood(i, j, self.b.itemcget(self.rectangle[i][j], "fill"), rnd)
                state = not all(chain(*boolMatrix))
                self.b.update()
        elif varSimulation == "SC":
            colArr = []
            try:
                percentage = int(self.entryPercentage.get())
            except ValueError:
                percentage = 100
            while state:
                state = False
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        if self.b.itemcget(self.rectangle[i][j], "fill") == "white" and self.b.itemcget(self.rectangle[i][j], "fill") not in self.clickedColours:
                            state = True
                            col = self.shapeControl(i, j, percentage)
                            colArr.append([i, j, col])
                for i in colArr:
                    self.b.itemconfig(self.rectangle[i[0]][i[1]], fill=i[2], stipple="")
                self.b.update()

    def mooreAbs(self, i, j, colour):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                    if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                        self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")

    def moorePer(self, i, j, colour):
        boundI = 0
        boundJ = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                    if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                        self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                else:
                    if i + x < 0:
                        boundI = self.sizeX - 1
                    elif i + x >= 0:
                        boundI = i + x - 1

                    if i + x > self.sizeX:
                        boundI = 0
                    elif i + x < self.sizeX:
                        boundI = i + x - 1

                    if j + y < 0:
                        boundJ = self.sizeY - 1
                    elif j + y >= 0:
                        boundJ = j + y - 1

                    if j + y > self.sizeY:
                        boundJ = 0
                    elif j + y < self.sizeY:
                        boundJ = j + y - 1

                    if self.b.itemcget(self.rectangle[boundI][boundJ], "fill") == "white":
                        self.b.itemconfig(self.rectangle[boundI][boundJ], fill=colour, stipple="")

    def vonNeumannAbs(self, i, j, colour):
        arr = [1, 3, 4, 5, 7]
        counter = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                counter = counter + 1

    def vonNeumannPer(self, i, j, colour):
        arr = [1, 3, 4, 5, 7]
        counter = 0
        boundI = 0
        boundJ = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                    else:
                        if i + x < 0:
                            boundI = self.sizeX - 1
                        elif i + x >= 0:
                            boundI = i + x - 1

                        if i + x > self.sizeX:
                            boundI = 0
                        elif i + x < self.sizeX:
                            boundI = i + x - 1

                        if j + y < 0:
                            boundJ = self.sizeY - 1
                        elif j + y >= 0:
                            boundJ = j + y - 1

                        if j + y > self.sizeY:
                            boundJ = 0
                        elif j + y < self.sizeY:
                            boundJ = j + y - 1

                        if self.b.itemcget(self.rectangle[boundI][boundJ], "fill") == "white":
                            self.b.itemconfig(self.rectangle[boundI][boundJ], fill=colour, stipple="")
                counter = counter + 1

    def pentagonalAbs(self, i, j, colour, rnd):
        if rnd == 0:
            arr = [0, 1, 2, 3, 4, 5]
        elif rnd == 1:
            arr = [3, 4, 5, 6, 7, 8]
        elif rnd == 2:
            arr = [1, 2, 4, 5, 7, 8]
        else:
            arr = [0, 1, 3, 4, 6, 7]
        counter = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                counter = counter + 1

    def pentagonalPer(self, i, j, colour, rnd):
        if rnd == 0:
            arr = [0, 1, 2, 3, 4, 5]
        elif rnd == 1:
            arr = [3, 4, 5, 6, 7, 8]
        elif rnd == 2:
            arr = [1, 2, 4, 5, 7, 8]
        else:
            arr = [0, 1, 3, 4, 6, 7]
        counter = 0
        boundI = 0
        boundJ = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                    else:
                        if i + x < 0:
                            boundI = self.sizeX - 1
                        elif i + x >= 0:
                            boundI = i + x - 1

                        if i + x > self.sizeX:
                            boundI = 0
                        elif i + x < self.sizeX:
                            boundI = i + x - 1

                        if j + y < 0:
                            boundJ = self.sizeY - 1
                        elif j + y >= 0:
                            boundJ = j + y - 1

                        if j + y > self.sizeY:
                            boundJ = 0
                        elif j + y < self.sizeY:
                            boundJ = j + y - 1

                        if self.b.itemcget(self.rectangle[boundI][boundJ], "fill") == "white":
                            self.b.itemconfig(self.rectangle[boundI][boundJ], fill=colour, stipple="")
                counter = counter + 1

    def hexagonalAbs(self, i, j, colour, rnd):
        if rnd == 0:
            arr = [1, 2, 3, 4, 5, 6, 7]
        else:
            arr = [0, 1, 3, 4, 5, 7, 8]
        counter = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                counter = counter + 1

    def hexagonalPer(self, i, j, colour, rnd):
        if rnd == 0:
            arr = [1, 2, 3, 4, 5, 6, 7]
        else:
            arr = [0, 1, 3, 4, 5, 7, 8]
        counter = 0
        boundI = 0
        boundJ = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if counter in arr:
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") == "white":
                            self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour, stipple="")
                    else:
                        if i + x < 0:
                            boundI = self.sizeX - 1
                        elif i + x >= 0:
                            boundI = i + x - 1

                        if i + x > self.sizeX:
                            boundI = 0
                        elif i + x < self.sizeX:
                            boundI = i + x - 1

                        if j + y < 0:
                            boundJ = self.sizeY - 1
                        elif j + y >= 0:
                            boundJ = j + y - 1

                        if j + y > self.sizeY:
                            boundJ = 0
                        elif j + y < self.sizeY:
                            boundJ = j + y - 1

                        if self.b.itemcget(self.rectangle[boundI][boundJ], "fill") == "white":
                            self.b.itemconfig(self.rectangle[boundI][boundJ], fill=colour, stipple="")
                counter = counter + 1

    def rndChoose(self):
        var = self.varNeighbor.get()
        if var == "PentagonalRandom":
            return random.randint(0, 3)
        elif var == "HexagonalRandom":
            return random.randint(0, 1)
        else:
            return

    def neighbourhood(self, i, j, colour, rnd):
        varNeighbor = self.varNeighbor.get()
        varBoundary = self.varBoundary.get()
        if varBoundary == "Absorbing":
            if varNeighbor == "Moore":
                self.mooreAbs(i, j, colour)
            elif varNeighbor == "VonNeumann":
                self.vonNeumannAbs(i, j, colour)
            elif varNeighbor == "PentagonalRandom":
                self.pentagonalAbs(i, j, colour, rnd)
            elif varNeighbor == "HexagonalRandom":
                self.hexagonalAbs(i, j, colour, rnd)
        elif varBoundary == "Periodic":
            if varNeighbor == "Moore":
                self.moorePer(i, j, colour)
            elif varNeighbor == "VonNeumann":
                self.vonNeumannPer(i, j, colour)
            elif varNeighbor == "PentagonalRandom":
                self.pentagonalPer(i, j, colour, rnd)
            elif varNeighbor == "HexagonalRandom":
                self.hexagonalPer(i, j, colour, rnd)

    def shapeControl(self, i, j, percentage):
        colArrR1 = [None] * 8
        colArrR2 = [None] * 4
        colArrR3 = [None] * 4
        counterR1 = 0
        counterR2 = 0
        counterR3 = 0
        uniqueCol = []
        rule2 = [1, 3, 4, 6]
        rule3 = [0, 2, 5, 7]
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0):
                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                        col = self.b.itemcget(self.rectangle[i + x][j + y], "fill")
                        if col != "white" and col not in self.clickedColours:
                            colArrR1[counterR1] = col
                            if counterR2 in rule2:
                                colArrR2[counterR2] = col
                                counterR2 = counterR2 + 1
                            if counterR3 in rule3:
                                colArrR3[counterR3] = col
                                counterR3 = counterR3 + 1
                    counterR1 = counterR1 + 1

        for i in colArrR1:
            if i not in uniqueCol and i is not None:
                uniqueCol.append(i)

        for i in range(len(uniqueCol)):
            counter = 0
            for j in range(len(colArrR1)):
                if uniqueCol[i] == colArrR1[j]:
                    counter = counter + 1
            uniqueCol[i] = [uniqueCol[i], counter]

        uniqueCol = sorted(uniqueCol, key=itemgetter(1), reverse=True)

        # Rule 1
        uniqueColR4 = uniqueCol
        if uniqueCol:
            if uniqueCol[0][1] >= 5:
                return uniqueCol[0][0]

        # Rule 2
        uniqueCol = []
        for i in colArrR2:
            if i not in uniqueCol and i is not None:
                uniqueCol.append(i)
        for i in range(len(uniqueCol)):
            counter = 0
            for j in range(len(colArrR2)):
                if uniqueCol[i] == colArrR2[j]:
                    counter = counter + 1
            uniqueCol[i] = [uniqueCol[i], counter]

        uniqueCol = sorted(uniqueCol, key=itemgetter(1), reverse=True)

        if uniqueCol:
            if uniqueCol[0][1] >= 3:
                return uniqueCol[0][0]

        # Rule 3
        uniqueCol = []
        for i in colArrR3:
            if i not in uniqueCol and i is not None:
                uniqueCol.append(i)
        for i in range(len(uniqueCol)):
            counter = 0
            for j in range(len(colArrR3)):
                if uniqueCol[i] == colArrR3[j]:
                    counter = counter + 1
            uniqueCol[i] = [uniqueCol[i], counter]

        uniqueCol = sorted(uniqueCol, key=itemgetter(1), reverse=True)

        if uniqueCol:
            if uniqueCol[0][1] >= 3:
                return uniqueCol[0][0]

        # Rule 4
        if uniqueColR4:
            rand = random.randint(1, 100)
            if rand <= percentage:
                return uniqueColR4[0][0]

    def addInclusions(self):
        state = False
        colour = "#010000"
        try:
            size = int(self.entryInclusionsSize.get())
        except ValueError:
            size = 0
        sizeCircular = size * self.nodeSize
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if self.b.itemcget(self.rectangle[i][j], "fill") == "white":
                    state = True
                    break
        try:
            self.inclusions = int(self.entryInclusionsAmount.get())
        except ValueError:
            self.inclusions = 0
        rand = random.sample(range(0, self.sizeX * self.sizeY), self.inclusions)
        if state:
            if size > 1:
                if self.varInclusions.get() == "Square":
                    self.squareBegin(size, rand, colour)
                elif self.varInclusions.get() == "Circular":
                    self.circularBegin(sizeCircular, rand, colour)
            else:
                for i in range(self.inclusions):
                    self.b.itemconfig(self.rectangle[(rand[i] % self.sizeX)][(int(rand[i] / self.sizeY))],
                                      fill=colour)
        else:
            boolMatrix = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
            for i in range(1, self.sizeX - 1):
                for j in range(1, self.sizeY - 1):
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if self.b.itemcget(self.rectangle[i + x][j + y], "fill") != self.b.itemcget(
                                    self.rectangle[i][j], "fill"):
                                boolMatrix[i][j] = True
            counter = 0
            for x in range(1, self.sizeX - 1):
                for y in range(1, self.sizeY - 1):
                    if boolMatrix[x][y]:
                        counter = counter + 1
            rand = random.sample(range(0, counter), self.inclusions)
            rand.sort()
            counter = 0
            ctrI = 0
            for x in range(1, self.sizeX - 1):
                for y in range(1, self.sizeY - 1):
                    if boolMatrix[x][y]:
                        if counter == rand[ctrI]:
                            if size > 1:
                                if self.varInclusions.get() == "Square":
                                    self.squareAfter(size, colour, x, y)
                                elif self.varInclusions.get() == "Circular":
                                    self.circularAfter(sizeCircular, colour, x, y)
                            else:
                                for i in range(self.inclusions):
                                    self.b.itemconfig(self.rectangle[x][y], fill=colour)
                            if ctrI < len(rand) - 1:
                                ctrI = ctrI + 1
                        counter = counter + 1

    def squareBegin(self, size, rand, colour):
        for i in range(self.inclusions):
            for x in range(-size + 1, size - 1):
                for y in range(-size + 1, size - 1):
                    if self.sizeX > (rand[i] % self.sizeX) + x >= 0 and self.sizeY > (
                            int(rand[i] / self.sizeY)) + y >= 0:
                        self.b.itemconfig(
                            self.rectangle[(rand[i] % self.sizeX) + x][(int(rand[i] / self.sizeY)) + y],
                            fill=colour)

    def circularBegin(self, size, rand, colour):
        for i in range(self.inclusions):
            centerInclusionX = rand[i] % self.sizeX * self.nodeSize + int(self.nodeSize / 2)
            centerInclusionY = (int(rand[i] / self.sizeY)) * self.nodeSize + int(self.nodeSize / 2)
            for x in range(self.sizeX):
                for y in range(self.sizeY):
                    centerNodeX = x * self.nodeSize + int(self.nodeSize / 2)
                    centerNodeY = y * self.nodeSize + int(self.nodeSize / 2)
                    dist = math.sqrt(
                        ((centerNodeX - centerInclusionX) ** 2) + ((centerNodeY - centerInclusionY) ** 2))
                    if dist <= size:
                        self.b.itemconfig(self.rectangle[x][y], fill=colour)

    def squareAfter(self, size, colour, i, j):
        for x in range(-size + 1, size - 1):
            for y in range(-size + 1, size - 1):
                if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                    self.b.itemconfig(self.rectangle[i + x][j + y], fill=colour)

    def circularAfter(self, size, colour, a, b):
        centerInclusionX = a * self.nodeSize + int(self.nodeSize / 2)
        centerInclusionY = b * self.nodeSize + int(self.nodeSize / 2)
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                centerNodeX = x * self.nodeSize + int(self.nodeSize / 2)
                centerNodeY = y * self.nodeSize + int(self.nodeSize / 2)
                dist = math.sqrt(((centerNodeX - centerInclusionX) ** 2) + ((centerNodeY - centerInclusionY) ** 2))
                if dist <= size:
                    self.b.itemconfig(self.rectangle[x][y], fill=colour)

    @staticmethod
    def random_color():
        x = random.randint(1, 255)
        y = random.randint(1, 255)
        z = random.randint(1, 255)
        return rgb(x, y, z)

    def click(self, event):
        state = True
        dc = windll.user32.GetDC(0)
        rgbColour = windll.gdi32.GetPixel(dc, event.x_root, event.y_root)
        r = rgbColour & 0xff
        g = (rgbColour >> 8) & 0xff
        b = (rgbColour >> 16) & 0xff
        if self.rgb2hex(r, g, b) not in self.clickedColours and self.rgb2hex(r, g, b) != "#f0f0f0":
            self.clickedColours.append(self.rgb2hex(r, g, b))
            state = False
        if self.rgb2hex(r, g, b) in self.clickedColours and state:
            self.clickedColours.remove(self.rgb2hex(r, g, b))
        if len(self.clickedColours) >= int(self.entryGrains.get()):
            self.clickedColours = []
        self.selection()

    def rgb2hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def selection(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if self.b.itemcget(self.rectangle[i][j], "fill") in self.clickedColours:
                    self.b.itemconfig(self.rectangle[i][j], stipple="")
                if self.b.itemcget(self.rectangle[i][j], "fill") not in self.clickedColours:
                    self.b.itemconfig(self.rectangle[i][j], stipple="gray50")
                if not self.clickedColours:
                    self.b.itemconfig(self.rectangle[i][j], stipple="")

    def structure(self):
        varStructure = self.varStructure.get()
        if varStructure == "Substructure":
            self.clearWithoutColour()
            self.randomGrain()
            self.grainGrowth()
            self.clickedColours = []
        elif varStructure == "Dual-Phase":
            for i in range(self.sizeX):
                for j in range(self.sizeY):
                    if self.b.itemcget(self.rectangle[i][j], "fill") in self.clickedColours:
                        self.b.itemconfig(self.rectangle[i][j], fill="#010000")
                    else:
                        self.b.itemconfig(self.rectangle[i][j], stipple="")
            self.clickedColours = []

    def clearWithoutColour(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if self.b.itemcget(self.rectangle[i][j], "fill") not in self.clickedColours:
                    self.b.itemconfig(self.rectangle[i][j], fill="white")

    def borders(self):
        try:
            size = int(self.entryBorderSize.get())
        except ValueError:
            size = 1
        if not self.clickedColours:
            remembered = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
            for a in range(size):
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                                    if self.b.itemcget(self.rectangle[i + x][j + y], "fill") != self.b.itemcget(self.rectangle[i][j], "fill"):
                                        remembered[i][j] = True
            for i in range(self.sizeX):
                for j in range(self.sizeY):
                    if remembered[i][j]:
                        self.b.itemconfig(self.rectangle[i][j], fill="#010000")
        else:
            remembered = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
            for a in range(size):
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        if self.b.itemcget(self.rectangle[i][j], "fill") in self.clickedColours:
                            for x in range(-1, 2):
                                for y in range(-1, 2):
                                    if self.sizeX > (i + x) >= 0 and self.sizeY > (j + y) >= 0:
                                        if self.b.itemcget(self.rectangle[i + x][j + y], "fill") != self.b.itemcget(self.rectangle[i][j], "fill"):
                                            remembered[i][j] = True
            for i in range(self.sizeX):
                for j in range(self.sizeY):
                    if remembered[i][j]:
                        self.b.itemconfig(self.rectangle[i][j], fill="#010000", stipple="")
            self.clickedColours = []
            for i in range(self.sizeX):
                for j in range(self.sizeY):
                    self.b.itemconfig(self.rectangle[i][j], stipple="")

    def clearSpace(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if self.b.itemcget(self.rectangle[i][j], "fill") != "#010000":
                    self.b.itemconfig(self.rectangle[i][j], fill="white")

    def impTXT(self):
        file = open("./export/txt/text.txt", "r")
        lines = []
        for line in file:
            lines.append(line)

        lastLine = lines[len(lines) - 1]

        self.sizeX = int(lastLine.split(" ")[0]) + 1
        self.sizeY = int(lastLine.split(" ")[0]) + 1
        self.board(self.sizeX * self.nodeSize, self.sizeY * self.nodeSize)

        counter = 0
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                self.b.itemconfig(self.rectangle[i][j], fill=str(lines[counter].split(" ")[3]))
                counter = counter + 1

    def impBMP(self):
        img = PIL.Image.open('./export/bmp/bitmap.bmp')
        rgb_im = img.convert('RGB')

        colours = []
        counter = 0
        ctr = 0

        for i in range(1, rgb_im.size[0]):
            for j in range(rgb_im.size[1]):
                if rgb_im.getpixel((i, j - 1)) == (0, 0, 0) and rgb_im.getpixel((i, j)) != (0, 0, 0) and rgb_im.getpixel((i - 1, j)) == (0, 0, 0):
                    colours.append(rgb(rgb_im.getpixel((i, j))[0],
                                       rgb_im.getpixel((i, j))[1],
                                       rgb_im.getpixel((i, j))[2]))
                    if counter == 0:
                        ctr = ctr + 1
            counter = counter + 1

        self.sizeX = int(len(colours) / ctr)
        self.sizeY = ctr
        self.board(self.sizeX * self.nodeSize, self.sizeY * self.nodeSize)

        counter = 0
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                self.b.itemconfig(self.rectangle[i][j], fill=str(colours[counter]))
                counter = counter + 1

    def expTXT(self):
        file = open("./export/txt/text.txt", "w")
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                file.write(str(i) + " ")
                file.write(str(j) + " ")
                file.write(str(self.rectangle[i][j]) + " ")
                file.write(str(self.b.itemcget(self.rectangle[i][j], "fill")) + " ")
                file.write("\n")
        file.close()

    def expBMP(self):
        ps = self.b.postscript(colormode='color')
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save('./export/bmp/bitmap.bmp')

    @staticmethod
    def exitProgram():
        exit()


def startGUI():
    EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'
    root = Tk()
    GUI(root)
    root.wm_title("Multiscale Modeling Project - Tomasz Łopatyński")
    root.mainloop()


if __name__ == '__main__':
    startGUI()
