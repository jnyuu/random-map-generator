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
        self.colorMode = "default"
        self.initializeUI()
        self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
        self.updateCanvas()
        Tk.mainloop()


    def initializeUI(self):


        self.canvas = Tk.Canvas(self.root, bg="#141414", height=600, width=600); 
        self.canvas.pack()


        # ---------------------------------------
        # CREATE TK LAYOUT
        # ---------------------------------------

       
        self.layoutFrame = Tk.Frame(self.root, width=33, height=33, bg='black',pady=11,padx=11)
        self.layoutFrame.pack() 


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

        self.buttonPresetWorldSmallIslands = Tk.Button(self.layoutFrame, text = 'Generate map :  SMALL CAVES', command =lambda: self.generatePresets("cavesSmall")).grid(row=1, column=1)
        self.buttonPresetWorldMediumIslands = Tk.Button(master = self.layoutFrame, text = 'Generate map :  MEDIUM CAVES', command =lambda:  self.generatePresets("cavesMedium")).grid(row=1, column=2)
        self.buttonPresetWorldLargeIslands = Tk.Button(master = self.layoutFrame, text = 'Generate map : LARGE CAVES', command =lambda:  self.generatePresets("cavesLarge")).grid(row=1, column=3)
      

        # ---------------------------------------
        # CREATE TK GENERAL BUTTONS
        # ---------------------------------------

        self.buttonQuit = Tk.Button(master = self.root, text = 'Quit', command = quit, pady=10, padx=10,font=10,fg="red")
        self.buttonReset = Tk.Button(master = self.layoutFrame, text = 'Change map dimensions', command=  self.callResetBoard).grid(row=9, column=5)
        self.buttonSaveImage = Tk.Button(master = self.layoutFrame, text = 'Save as png', command=  self.saveImage).grid(row=9, column=1)

        self.buttonQuit.pack(side=Tk.LEFT)
        self.labelError.pack()

    def callResetBoard(self):
        self.labelErrorVar.set("UPDATING MAP DIMENSIONS")
        self.canvas.update()
        self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
        self.updateCanvas()
    


    def updateCanvas(self):
        self.canvas.delete('all')

        for row in range(self.board.height):
            for col in range(self.board.width):
                color = self.getTileColor(self.board.board[row][col])
                self.canvas.create_rectangle(col*2,row*2,col*2+2,row*2+2, fill=color, outline=color)
                

        self.canvas.update()

    def saveImage(self):
        fileName = str(time.time())
        self.canvas.postscript(file=""+fileName+".eps", colormode='color')
        img = Image.open(fileName + '.eps') 
        img.save(fileName + '.png', 'png') 




    def generatePresets(self,presetName):
        match presetName:
            case "cavesSmall":
                self.spawnChanceVar.set(37)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
            case "cavesMedium":
                self.spawnChanceVar.set(41)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()
            case "cavesLarge":
                self.spawnChanceVar.set(43)
                self.board.resetBoard(self.widthVar,self.heightVar,self.spawnChanceVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                for i in range(45):
                    self.board.iterateBasicEight(40)
                self.labelErrorVar.set("")
                self.updateCanvas()


    def quit(self):
        print ('quit button press...')
        self.root.quit()     
        self.root.destroy() 

    def getTileColor(self,tileValue):
        color=""
        match self.colorMode:
            case "default":
                if (tileValue>215):
                    color="#706459"
                elif (tileValue>140):
                    color="#706459"
                elif (tileValue>100):
                    color="#423c36"
                elif (tileValue>65):
                    color="#2e2a26"    
                else :
                    color="#000000"
                return color
            
        
class Board:
    def __init__(self,width = 100,height = 100,spawnchance = 0.43):
        self.width = width
        self.height = height
        self.spawnchance = spawnchance
        self.board = []
        

    def resetBoard(self,widthVar,heightVar,spawnChanceVar,labelErrorVar): 
        self.board = []

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
        print(len(self.board))
    
        for row in range(5,self.height-5):
            for col in  range(5,self.width-5): 
                if random.random() <= self.spawnchance:
                    self.board[row][col] = 60
                else:
                    self.board[row][col] = 10
        labelErrorVar.set("")


    
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

        
if __name__ == "__main__":
    application = Application()


# PRESETY