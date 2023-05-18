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
import math
# FIRST LAND LEVEL IS 85


class Application:
    def __init__(self):
        self.board = Board()
        self.root = Tk.Tk()
        self.root.wm_title("PROJECT - MAP GENERATOR")
        self.initializeUI()
        self.board.resetBoard(self.widthVar,self.heightVar,self.labelErrorVar)
        self.updateCanvas()
        Tk.mainloop()


    def initializeUI(self):


        self.cityBlank = Tk.PhotoImage(file='img/city-blank.png')
        self.cityEmpty1 = Tk.PhotoImage(file='img/empty-1.png')
        self.cityEmpty2 = Tk.PhotoImage(file='img/empty-2.png')
        self.cityEmpty3 = Tk.PhotoImage(file='img/empty-3.png')
        self.cityEmpty4 = Tk.PhotoImage(file='img/empty-4.png')
        self.cityEmpty5 = Tk.PhotoImage(file='img/empty-5.png')
        self.cityEmpty6 = Tk.PhotoImage(file='img/empty-6.png')
        self.cityEmpty7 = Tk.PhotoImage(file='img/empty-7.png')
        self.cityEmpty8 = Tk.PhotoImage(file='img/empty-8.png')
        self.cityEmpty9 = Tk.PhotoImage(file='img/empty-9.png')
        self.cityEmpty10 = Tk.PhotoImage(file='img/empty-10.png')
        self.cityEmpty11 = Tk.PhotoImage(file='img/empty-11.png')
        self.cityEmpty12 = Tk.PhotoImage(file='img/empty-12.png')
        self.cityEmpty13 = Tk.PhotoImage(file='img/empty-13.png')

        self.cityBuilding1 = Tk.PhotoImage(file='img/building-1.png')
        self.cityBuilding2 = Tk.PhotoImage(file='img/building-2.png')
        self.cityBuilding3 = Tk.PhotoImage(file='img/building-3.png')
        self.cityBuilding4 = Tk.PhotoImage(file='img/building-4.png')
        self.cityBuilding5 = Tk.PhotoImage(file='img/building-5.png')
        self.cityBuilding6 = Tk.PhotoImage(file='img/building-6.png')
        self.cityBuilding7 = Tk.PhotoImage(file='img/building-7.png')
        self.cityBuilding8 = Tk.PhotoImage(file='img/building-8.png')
        self.cityBuilding9 = Tk.PhotoImage(file='img/building-9.png')
        self.cityBuilding10 = Tk.PhotoImage(file='img/building-10.png')
        self.cityBuilding11 = Tk.PhotoImage(file='img/building-11.png') 
        self.cityBuilding12 = Tk.PhotoImage(file='img/building-12.png')
        self.cityBuilding13 = Tk.PhotoImage(file='img/building-13.png')
        self.cityBuilding14 = Tk.PhotoImage(file='img/building-14.png')
        self.cityBuilding15 = Tk.PhotoImage(file='img/building-15.png')
        self.cityBuilding16 = Tk.PhotoImage(file='img/building-16.png')
        self.cityBuilding17 = Tk.PhotoImage(file='img/building-17.png')
        self.cityBuilding18 = Tk.PhotoImage(file='img/building-18.png')
        self.cityBuilding19 = Tk.PhotoImage(file='img/building-19.png')
        self.cityBuilding20 = Tk.PhotoImage(file='img/building-20.png')
        self.cityBuilding21 = Tk.PhotoImage(file='img/building-21.png')
        self.cityBuilding22 = Tk.PhotoImage(file='img/building-22.png')


        self.canvas = Tk.Canvas(self.root, bg="#6ABE80", height=576, width=576); 
        self.canvas.pack()

        self.cityTileset = [self.cityBlank,self.cityEmpty1,self.cityEmpty2,self.cityEmpty3,self.cityEmpty4,self.cityEmpty5,self.cityEmpty6,self.cityEmpty7,self.cityEmpty8, 
                  self.cityEmpty9,self.cityEmpty10,self.cityEmpty11, self.cityEmpty12,self.cityEmpty13,

                   self.cityBuilding1,self.cityBuilding2,self.cityBuilding3,self.cityBuilding4,self.cityBuilding5,
                   self.cityBuilding6,self.cityBuilding7,
                   self.cityBuilding8,self.cityBuilding9,self.cityBuilding10,self.cityBuilding11,self.cityBuilding12,
                   self.cityBuilding13,self.cityBuilding14,self.cityBuilding15,self.cityBuilding16,self.cityBuilding17,
                   self.cityBuilding18,self.cityBuilding19,self.cityBuilding20,self.cityBuilding21,self.cityBuilding22]
        # ---------------------------------------
        # CREATE TK LAYOUT
        # ---------------------------------------

        self.layoutFrame = Tk.Frame(self.root, width=33, height=33, bg='#6ABE80',pady=11,padx=11)
        self.layoutFrame.pack() 


        # ---------------------------------------
        # CREATE TK VARIABLES
        # ---------------------------------------
        
        self.heightVar = Tk.StringVar()
        self.widthVar = Tk.StringVar()
        # self.spawnChanceVar = Tk.StringVar()
        self.heightVar.set(str(self.board.height))
        self.widthVar.set(str(self.board.width))
        # self.spawnChanceVar.set(str(self.board.spawnchance*100))
        
        # ---------------------------------------
        # CREATE TK LABELS AND ENTRIES
        # ---------------------------------------
        
        self.labelWVar = Tk.StringVar()
        self.labelWVar.set("WIDTH (25-200): ")
        self.labelW = Tk.Label( self.layoutFrame, textvariable=self.labelWVar,bg='#fff' ).grid(row=7, column=4)
        self.widthEntry = Tk.Entry(master = self.layoutFrame, textvariable = self.widthVar).grid(row=8, column=4)
        
        self.labelHVar = Tk.StringVar()
        self.labelHVar.set("HEIGHT (25-200): ")
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

        self.buttonPresetWorldSmallIslands = Tk.Button(self.layoutFrame, text = 'Generate city map : FEW BUILDINGS', command =lambda: self.generatePresets("fewBuildings")).grid(row=1, column=1)
        self.buttonPresetWorldMediumIslands = Tk.Button(master = self.layoutFrame, text = 'Generate city map : AVERAGE BUILDINGS', command =lambda:  self.generatePresets("averageBuildings")).grid(row=1, column=2)
        self.buttonPresetWorldLargeIslands = Tk.Button(master = self.layoutFrame, text = 'Generate city map : MANY BUILDINGS', command =lambda:  self.generatePresets("manyBuildings")).grid(row=1, column=3)
      

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
        self.board.resetBoard(self.widthVar,self.heightVar,self.labelErrorVar)
        self.updateCanvas()
    


    def updateCanvas(self):
        self.canvas.delete('all')

        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                self.canvas.create_image(col*48,row*48,image=self.cityTileset[self.board.board[row][col]],anchor='nw')

        self.canvas.update()

    def saveImage(self):
        fileName = str(time.time())
        self.canvas.postscript(file=""+fileName+".eps", colormode='color')
        img = Image.open(fileName + '.eps') 
        img.save(fileName + '.png', 'png') 

    def generatePresets(self,presetName):
        match presetName:
            case "fewBuildings":
                self.board.resetBoard(self.widthVar,self.heightVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                self.board.generateCityTiles(0.20)
                self.labelErrorVar.set("")
                self.updateCanvas()
            case "averageBuildings":
                self.board.resetBoard(self.widthVar,self.heightVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                self.board.generateCityTiles(0.50)
                self.labelErrorVar.set("")
                self.updateCanvas()
            case "manyBuildings":
                self.board.resetBoard(self.widthVar,self.heightVar,self.labelErrorVar)
                self.labelErrorVar.set("GENERATING MAP....")
                self.updateCanvas()
                self.board.generateCityTiles(0.80)
                self.labelErrorVar.set("")
                self.updateCanvas()


    def quit(self):
        print ('quit button press...')
        self.root.quit()     
        self.root.destroy() 

        
class Board:
    def __init__(self,width = 100,height = 100):
        self.width = width
        self.height = height
        self.board = []

    def resetBoard(self,widthVar,heightVar,labelErrorVar): 
        self.board = []

        try:
            if(int(widthVar.get()) < 25 or int(widthVar.get()) > 200 or int(heightVar.get()) < 25 or int(heightVar.get()) > 200):
                labelErrorVar.set("ERROR - WRONG VALUES")
                return
            else:
                self.width = int(widthVar.get())
                self.height = int(heightVar.get())
                # self.spawnchance = float(spawnChanceVar.get())/100   

        except:
            labelErrorVar.set("ERROR OCCURED")
            return

        for row in range(math.floor(self.height/16)):
            x = [0] * math.floor(self.width/16)
            self.board.append(x)
        # print(self.board)
        labelErrorVar.set("")
      
    def generateCityTiles(self,spawnchance):
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                x = random.random()
                if x > spawnchance:
                    self.board[row][col] = random.randint(1,12)
                    # EMPTY TILE
                else:
                    self.board[row][col] = random.randint(13,33)
                    # CITY TILE
                    
        
if __name__ == "__main__":
    application = Application()