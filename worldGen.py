import matplotlib, sys
matplotlib.use('TkAgg')
import random
from PIL import Image
import time
from functools import partial
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
# FIRST LAND LEVEL IS 85

class Application:
    def __init__(self):
        self.board = Board()
        self.root = Tk.Tk()
        self.root.wm_title("PROJECT - MAP GENERATOR")
        self.availableColorModes = ["tropical","snow","simple","heatmap"]
        self.colorMode = "snow"
        self.initializeUI()
        self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
        self.updateCanvas()
        # self.initializeLayout()
        Tk.mainloop()


    def initializeUI(self):


        self.cityImg = Tk.PhotoImage(file='img/city2.png')
        self.caveImg = Tk.PhotoImage(file='img/cave.png')
        self.canvas = Tk.Canvas(self.root, bg="#03113d", height=600, width=600); 
        self.canvas.pack()

        # ---------------------------------------
        # CREATE TK LAYOUT
        # ---------------------------------------

        # h = Scrollbar(root, orient = 'horizontal')
        # scrollbar = Tk.ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.layoutFrame = Tk.Frame(self.root, width=33, height=33, bg='#04154D',pady=11,padx=11)
        # self.leftFrame = Tk.Frame(self.root, width=33, height=33, bg='green',pady=1,padx=1)
        # self.caveMapPresetsFrame = Tk.Frame(self.root, width=33, height=33, bg='grey',pady=1,padx=1)
        self.layoutFrame.pack() 
        # self.leftFrame.pack(side=Tk.LEFT) 

        # self.rightscrollbar = Tk.Scrollbar( self.layoutFrame, orient='vertical',command=self.layoutFrame.yview)
        # self.rightscrollbar.pack(side="right",fill="y")

        # self.leftFrame = Tk.Scrollbar( self.leftFrame, orient='vertical')
        # self.leftFrame.pack(side="right",fill="y")
        # self.worldMapPresetsFrame['yscrollcommand'] = self.scrollbar.set

        # self.cityMapPresetsFrame.pack(side = Tk.LEFT)
        # self.caveMapPresetsFrame.pack(side = Tk.LEFT) 
        # self.worldMapPresetsFrame.pack(side = Tk.LEFT)

        # ---------------------------------------
        # CREATE TK VARIABLES
        # ---------------------------------------
        
        self.heightVar = Tk.StringVar()
        self.widthVar = Tk.StringVar()
        self.spawnChanceVar = Tk.StringVar()
        self.heightVar.set(str(self.board.height))
        self.widthVar.set(str(self.board.width))
        self.spawnChanceVar.set(str(self.board.spawnchance*100))

        # ---------------------------------------
        # CREATE TK LABELS AND ENTRIES
        # ---------------------------------------
        
        self.labelWVar = Tk.StringVar()
        self.labelWVar.set("WIDTH (25-300): ")
        self.labelW = Tk.Label( self.layoutFrame, textvariable=self.labelWVar,bg='#fff' ).grid(row=7, column=4)
        self.widthEntry = Tk.Entry(master = self.layoutFrame, textvariable = self.widthVar).grid(row=8, column=4)
        
        self.labelHVar = Tk.StringVar()
        self.labelHVar.set("HEIGHT (25-300): ")
        self.labelH = Tk.Label( self.layoutFrame, textvariable=self.labelHVar,bg='#fff' ).grid(row=7, column=5)
        self.heightEntry = Tk.Entry(master = self.layoutFrame, textvariable = self.heightVar).grid(row=8, column=5)
        
        # self.labelOVar = Tk.StringVar()
        # self.labelOVar.set("SPAWN CHANCE (0-100): ")
        # self.labelO = Tk.Label( self.layoutFrame, textvariable=self.labelOVar,bg='#fff' ).grid(row=7, column=6)
        # self.spawnchanceEntry = Tk.Entry(master = self.layoutFrame, textvariable = self.spawnChanceVar).grid(row=8, column=6)
        
        self.labelErrorVar = Tk.StringVar()
        self.labelErrorVar.set("")
        self.labelError = Tk.Label( self.root, textvariable=self.labelErrorVar,bg='#fff', fg='#FF0000',pady=10, padx=10, font=22 )


        # ---------------------------------------
        # CREATE TK TESTING BUTTONS
        # ---------------------------------------
        
        # self.buttonIterateBasicEight = Tk.Button(master = self.layoutFrame, text = 'Iterate Board * 1', command=  self.iterateBoard).grid(row=1, column=1)
        # self.buttonIterateBoardTimes10 = Tk.Button(master = self.layoutFrame, text = 'Iterate Board * 10', command=  self.iterateBoardTimes10).grid(row=1, column=2)
        # self.buttonIterateBoardTimes45 = Tk.Button(master = self.layoutFrame, text = 'Iterate Board * 45', command=  self.iterateBoardTimes45).grid(row=1, column=3)


        # ---------------------------------------
        # CREATE TK WORLD MAP GENERATION BUTTONS
        # ---------------------------------------

        self.buttonPresetWorldSmallIslands = Tk.Button(self.layoutFrame, text = 'Generate map :  SMALL ISLANDS', command =lambda: self.generatePresets("islandsSmall")).grid(row=1, column=1)
        self.buttonPresetWorldMediumIslands = Tk.Button(master = self.layoutFrame, text = 'Generate map :  MEDIUM ISLANDS', command =lambda:  self.generatePresets("islandsMedium")).grid(row=1, column=2)
        self.buttonPresetWorldLargeIslands = Tk.Button(master = self.layoutFrame, text = 'Generate map : LARGE ISLANDS', command =lambda:  self.generatePresets("islandsLarge")).grid(row=1, column=3)
        # self.buttonPresetWorldLargeLakesContinent = Tk.Button(master = self.layoutFrame, text = 'Generate map : continent with large lakes', command =lambda:  self.generatePresets("continentLargeLakes")).grid(row=1, column=4)
        # self.buttonPresetWorldMediumLakesContinent = Tk.Button(master = self.layoutFrame, text = 'Generate map : continent with medium lakes', command =lambda:  self.generatePresets("continentMediumLakes")).grid(row=1, column=5)
        self.buttonPresetWorldContinent = Tk.Button(master = self.layoutFrame, text = 'Generate map : CONTINENT', command = lambda: self.generatePresets("continent")).grid(row=1, column=6)
        self.buttonGenerateCity = Tk.Button(master=self.layoutFrame, text = 'Generate city', command=  self.callGenerateCity).grid(row=3, column=1)
        self.buttonGenerateCave = Tk.Button(master=self.layoutFrame, text = 'Generate cave', command=  self.callGenerateCave).grid(row=3, column=2)

        # ---------------------------------------
        # CREATE TK GENERAL BUTTONS
        # ---------------------------------------

        self.buttonQuit = Tk.Button(master = self.root, text = 'Quit', command = quit, pady=10, padx=10,font=10,fg="red")
        self.buttonReset = Tk.Button(master = self.layoutFrame, text = 'Change map dimensions', command=  self.callResetBoard).grid(row=9, column=5)
        self.buttonSaveImage = Tk.Button(master = self.layoutFrame, text = 'Save as png', command=  self.saveImage).grid(row=9, column=1)
        self.buttonSwapColorMode = Tk.Button(master = self.layoutFrame, text = 'Swap color mode (4 modes)', command=  self.swapColorMode).grid(row=9, column=2)

        self.buttonQuit.pack(side=Tk.LEFT)
        self.labelError.pack()

    def callResetBoard(self):
        self.labelErrorVar.set("UPDATING MAP DIMENSIONS")
        self.canvas.update()

        self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
        self.updateCanvas()
    
    def callGenerateCity(self):
        self.labelErrorVar.set("GENERATING A CITY")
        self.canvas.update()
        self.board.generateCity(self.labelErrorVar)
        self.labelErrorVar.set("")
        self.updateCanvas()

    def callGenerateCave(self):
        self.labelErrorVar.set("GENERATING A CAVE")
        self.canvas.update()
        self.board.generateCave(self.labelErrorVar)
        self.labelErrorVar.set("")
        self.updateCanvas()

    # def initializeLayout(self):
          
        # ---------------------------------------
        # PACK EVERY COMPONENT IN THE TK WINDOW
        # ---------------------------------------

        # self.worldMapPresetsFrame.pack(side=Tk.LEFT)
        # self.cityMapPresetsFrame.pack(side=Tk.LEFT)
        # self.caveMapPresetsFrame.pack(side=Tk.LEFT)

        # ---------------------------------------
        # PACK WORLD MAP GENERATION BUTTONS
        # ---------------------------------------

        # self.buttonGenerateCity.pack()
        # self.buttonPresetWorldSmallIslands.pack()
        # self.buttonPresetWorldMediumIslands.pack()
        # self.buttonPresetWorldLargeIslands.pack()
        # self.buttonPresetWorldLargeLakesContinent.pack() 
        # self.buttonPresetWorldMediumLakesContinent.pack()
        # self.buttonPresetWorldSmallLakesContinent.pack()

        # self.buttonIterateBasicEight.pack(side=Tk.LEFT)
        # self.buttonIterateBoardTimes10.pack(side=Tk.LEFT)
        # self.buttonIterateBoardTimes45.pack(side=Tk.LEFT)
        # self.buttonReset.pack()
        # self.buttonSaveImage.pack()
        # self.buttonSwapColorMode.pack()


        # self.widthEntry.pack(side=Tk.RIGHT)
        # self.labelW.pack(side=Tk.RIGHT)

        # self.heightEntry.pack(side=Tk.RIGHT)
        # self.labelH.pack(side=Tk.RIGHT)

        # self.spawnchanceEntry.pack(side=Tk.RIGHT)
        # self.labelO.pack(side=Tk.RIGHT)


    def updateCanvas(self):
        self.canvas.delete('all')

        for row in range(self.board.height):
            for col in range(self.board.width):
                # print(row,col)
                # print(self.board.board)
                color = self.getTileColor(self.board.board[row][col])
                self.canvas.create_rectangle(col*2,row*2,col*2+2,row*2+2, fill= color, outline= color)
                
        for (row,col) in self.board.activeCities:
            self.canvas.create_image(col*2,row*2,image=self.cityImg)

        for (row,col) in self.board.activeCaves:
            self.canvas.create_image(col*2,row*2,image=self.caveImg)

        self.canvas.update()

    def saveImage(self):
        fileName = str(time.time())
        self.canvas.postscript(file=""+fileName+".eps", colormode='color')
        img = Image.open(fileName + '.eps') 
        img.save(fileName + '.png', 'png') 

    def swapColorMode(self):
        # self.availableColorModes 
        index = self.availableColorModes.index(self.colorMode)
        if index == len(self.availableColorModes) - 1:
            index = 0
        else:
            index += 1
        self.colorMode = self.availableColorModes[index]
        self.updateCanvas()


    def generatePresets(self,presetName):
        match presetName:
            case "islandsSmall":
                self.spawnChanceVar.set(37)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
                self.drawCities()
                self.drawCaves()
            case "islandsMedium":
                self.spawnChanceVar.set(41)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
                self.drawCities()
                self.drawCaves()
            case "islandsLarge":
                self.spawnChanceVar.set(43)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
                self.drawCities()
                self.drawCaves()

            case "continent":
                self.spawnChanceVar.set(50)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(40):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
                self.drawCities()
                self.drawCaves()


    def quit(self):
        print ('quit button press...')
        self.root.quit()     
        self.root.destroy() 

    def getTileColor(self,tileValue):

        color=""

        match self.colorMode:
            case "tropical":
                if (tileValue>215):
                    color="#283801"
                elif (tileValue>175):
                    color="#334701"
                elif (tileValue>165):
                    color="#496604"
                elif (tileValue>150):
                    color="#608508"
                elif (tileValue>140):
                    color="#719c0c"
                elif (tileValue>120):
                    color="#87B911"
                elif (tileValue>100):
                    color="#E4E28B"
                elif (tileValue>85):
                    color="#BBBB61"
                elif (tileValue>45):
                    color="#1090b3"    
                elif (tileValue>28):
                    color="#065696"
                else :
                    color="#04154D"
                return color
            
            case "snow":
                if (tileValue>215):
                    color="#1A1F1A"
                elif (tileValue>175):
                    color="#313931"
                elif (tileValue>165):
                    color="#9D9181"
                elif (tileValue>150):
                    color="#947B5B"
                elif (tileValue>140):
                    color="#686C8D"
                elif (tileValue>120):
                    color="#B1BDD9"
                elif (tileValue>100):
                    color="#BDA171"
                elif (tileValue>85):
                    color="#573E15"
                elif (tileValue>50):
                    color="#007DB9"    
                elif (tileValue>35):
                    color="#44a8b3"
                elif (tileValue>31):
                    color="#60D1DD"
                elif (tileValue>27):
                    color="#002C65"
                else :
                    color="#04154D"
                return color

            case "simple":
                if (tileValue>165):
                    color="#025c1e"
                elif (tileValue>135):
                    color="#04802a"
                elif (tileValue>100):
                    color="#9ea603"
                elif (tileValue>70):
                    color="#042387"
                else :
                    color="#04154D"
                return color
            
            case "heatmap":
                if (tileValue>180):
                    color="#FFFFFF"
                elif (tileValue>170):
                    color="#FFFFB0"
                elif (tileValue>160):
                    color="#FFFF02"
                elif (tileValue>150):
                    color="#FFEE00"
                elif (tileValue>140):
                    color="#FFD901"
                elif (tileValue>130):
                    color="#FFBF00"
                elif (tileValue>120):
                    color="#FFA001"
                elif (tileValue>110):
                    color="#FF7901"
                elif (tileValue>100):
                    color="#FF4700"
                elif (tileValue>90):
                    color="#FF0050"
                elif (tileValue>80):
                    color="#EB0050"
                elif (tileValue>70):
                    color="#D10187"
                elif (tileValue>60):
                    color="#B000B0"
                elif (tileValue>50):
                    color="#8700D1"
                elif (tileValue>40):
                    color="#5001EB"
                elif (tileValue>30):
                    color="#0001C2"
                elif (tileValue>20):
                    color="#000099"
                elif (tileValue>10):
                    color="#000170"
                else :
                    color="#04154D"
                return color
       
    def drawCities(self):
        for (row,col) in self.board.activeCities:
            self.canvas.create_image(col*2,row*2,image=self.cityImg)
        self.canvas.update()

    def drawCaves(self):
        for (row,col) in self.board.activeCaves:
            self.canvas.create_image(col*2,row*2,image=self.caveImg)
        self.canvas.update()
        
class Board:
    def __init__(self,width = 100,height = 100,spawnchance = 0.43):
        self.width = width
        self.height = height
        self.spawnchance = spawnchance
        self.board = []
        self.activeCities = []
        self.activeCaves = []
        

    def resetBoard(self,widthVar,heightVar,spawnChanceVar,labelErrorVar): 
        self.board = []
        # print(widthVar.get(),heightVar.get(),spawnChanceVar.get())

        try:
            if(int(widthVar.get()) < 25 or int(widthVar.get()) > 300 or int(heightVar.get()) < 25 or int(heightVar.get()) > 300 or float(spawnChanceVar.get())<0 or float(spawnChanceVar.get())>100):
                labelErrorVar.set("ERROR - WRONG VALUES")

                return
            else:
                self.width = int(widthVar.get())
                self.height = int(heightVar.get())
                self.spawnchance = float(spawnChanceVar.get())/100   

        except:
            labelErrorVar.set("ERROR OCCURED")

            return

        for row in range(self.height):
            x = [0] * self.width
            self.board.append(x)
        # print(len(self.board))
    
        for row in range(5,self.height-5):
            for col in  range(5,self.width-5): 
                if random.random() <= self.spawnchance:
                    self.board[row][col] = 60
                else:
                    self.board[row][col] = 10
        labelErrorVar.set("")
        self.activeCities = []
        self.activeCaves = []
        # print(len(self.board))


    
    def iterateBasicEight(self,deathFactor):
        newBoard = [[0]*self.width for i in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                totalNeighbours = 0
                for rowNeighbourIndex in range(row-1,row+2):
                    for colNeighbourIndex in range(col-1,col+2):
                        if((row,col) != (rowNeighbourIndex,colNeighbourIndex) and 0<=rowNeighbourIndex<self.height and 0<=colNeighbourIndex<self.width):
                            totalNeighbours += self.board[rowNeighbourIndex][colNeighbourIndex]
                totalNeighbours = totalNeighbours/8
                if totalNeighbours < deathFactor :
                    if(totalNeighbours - self.board[row][col] < 0):
                        newBoard[row][col]=self.board[row][col] - random.randint(0,int(abs(totalNeighbours - self.board[row][col])))
                    else:
                        newBoard[row][col]=self.board[row][col] + random.randint(0,int(totalNeighbours - self.board[row][col]))
                elif self.board[row][col] > totalNeighbours:
                    newBoard[row][col]=self.board[row][col] + random.randint(-10,10)
                else:
                    newBoard[row][col]=self.board[row][col] + random.randint(0,int(totalNeighbours/5))
        self.board = newBoard

    
    def generateCity(self,labelErrorVar):
        city = False
        iterations = 0

        while city == False and iterations < 1000 :
            randomRow = random.randint(0,self.height-1) 
            randomCol = random.randint(0,self.width-1) 

            if self.board[randomRow][randomCol] > 100:
                if len(self.activeCities) == 0:
                    self.activeCities.append((randomRow,randomCol))
                    city = True
                else:
                    canDraw = True
                    for (existingCityRow,existingCityCol) in self.activeCities:
                        if abs(existingCityRow-randomRow) < 15 and abs(existingCityCol-randomCol) < 15:
                            canDraw = False

                    if canDraw:
                        self.activeCities.append((randomRow,randomCol))
                        city = True
                        labelErrorVar.set("")

            iterations += 1

        if city == False:
            labelErrorVar.set("ERROR - COUDLNT FIND A PLACE TO GENERATE A CITY")

            
    def generateCave(self,labelErrorVar):
        cave = False
        iterations = 0

        while cave == False and iterations < 1000 :
            randomRow = random.randint(0,self.height-1) 
            randomCol = random.randint(0,self.width-1) 

            if self.board[randomRow][randomCol] > 100:
                if len(self.activeCaves) == 0:
                    self.activeCaves.append((randomRow,randomCol))
                    cave = True
                else:
                    canDraw = True
                    for (existingCaveRow,existingCaveCol) in self.activeCaves:
                        if abs(existingCaveRow-randomRow) < 15 and abs(existingCaveCol-randomCol) < 15:
                            canDraw = False

                    if canDraw:
                        self.activeCaves.append((randomRow,randomCol))
                        cave = True
                        labelErrorVar.set("")

            iterations += 1

        if cave == False:
            labelErrorVar.set("ERROR - COUDLNT FIND A PLACE TO GENERATE A CAVE")

        
if __name__ == "__main__":
    application = Application()


# PRESETY