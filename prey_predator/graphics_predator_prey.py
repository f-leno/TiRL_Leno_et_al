# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:08:16 2016
Graphic representation of the Predator-Prey world
@author: Leno
"""

import Tkinter
import os
from PIL import Image, ImageTk

class GraphicsPredatorPrey():
    width = 800
    height = 800    
    window = None
    canvas = None
    imageFolder = os.path.dirname(os.path.abspath(__file__))
    
    squareX = None
    squareY = None
    sizeX = None
    sizeY = None
    
    
    def __init__(self,sizeX,sizeY):
        """Initiate the Screen"""
        self.window = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.window,width=self.width, height=self.height)
        
        self.sizeX = sizeX
        self.sizeY = sizeY
        #Calculates size of each square
        self.squareX = self.width / sizeX
        self.squareY = self.height / sizeY
        
        image = Image.open(self.imageFolder + "/predator.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.predator = ImageTk.PhotoImage(image)
        
        image = Image.open(self.imageFolder +  "/prey.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.prey = ImageTk.PhotoImage(image)
        
        
        self.draw_lines(sizeX,sizeY)
        self.update_screen()
        
        

    def draw_lines(self,sizeX,sizeY):
        for i in range(1,sizeX):
            self.canvas.create_line(self.squareX*i,0,self.squareX*i,self.height)
            
        for i in range(1,sizeY):
            self.canvas.create_line(0,self.squareY*i,self.width,self.squareY*i)
            
    def update_state(self,preyPositions,predatorPositions):
        self.clear()
        self.draw_lines(self.sizeX,self.sizeY)

        for prey in preyPositions:
            self.print_obj(prey[0],prey[1],self.prey)
        for predator in predatorPositions:
            self.print_obj(predator[0],predator[1],self.predator)        
        self.update_screen()
        
    def update_screen(self):
        self.canvas.pack()
        self.canvas.update()
        self.window.update()
        
        #self.window.mainloop()
        
            
    def print_obj(self,x,y,image):
        if x>=1 and x<=self.sizeX and y>=1 and y<=self.sizeY:
            realX = self.squareX*(x-1)
            realY = self.squareY*(y-1)
            self.canvas.create_image(realX, realY, image = image, anchor = Tkinter.NW,tags = 'obj')

    def clear(self):
        self.canvas.delete('obj')
        
        
        
      
    def close(self):
        self.window.destroy()
        
r = GraphicsPredatorPrey(10,10)
r.update_state([[1,1],[2,2]],[[2,1],[1,5]])
r.update_state([[5,5],[6,6]],[[7,9],[10,10]])
r.close()
  
    #update_prey(self,preyPosic):
        
        

