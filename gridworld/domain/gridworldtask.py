#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 14:18:58 2017

Class to store all task parameters (can be built from text files)

@author: Felipe Leno
"""
from task import Task
class GridWorldTask(Task):
    
    #Task Parameters and initial state
    sizeX     = None
    sizeY     = None
    pits      = None
    fires     = None
    treasures = None
    initState = None
    
    #Relevant classes for transfer potential computation
    relevantClasses = ["fire",'pit']

    
    taskString = None
    
    def __init__(self, filePath=None,taskName="noName",taskData=None):
        """ The source file must be a text file specified as follows:
            <sizeX>;<sizeY>;<objects>
            where <objects> is any number of objects separated with commas and obeying the format:
            <type>:<xPosic>-<yPosic>,<type>:<xPosic>-<yPosic>
            
        """
        super(GridWorldTask, self).__init__(filePath,taskName,taskData)
        self.name = taskName
        #Read task file
        if filePath != None:
            with open(filePath, 'r') as content_file:
                content = content_file.read()
        else:
            #Read task data
            content = taskData
            
        #get size the grid size
        sep = content.split(';')
            
        self.sizeX = int(sep[0])
        self.sizeY = int(sep[1])
        
        self.initState = self.load_task_state(sep[2])
        
        #Used for recovering the initial state
        self.taskString = sep[2]
        
        #Extracts the number of objects of each type.
        self.treasures = sep[2].count('treasure')
        self.pits = sep[2].count('pit')
        self.fires = sep[2].count('fire')
        
    def num_pits(self):
        return self.pits
    def task_features(self):
        return (self.fires,self.pits)
        
    def num_fires(self):
        return self.fires
        
    def get_sizeX(self):
        return self.sizeX
        
    def get_sizeY(self):
        return self.sizeY
        
    def num_treasures(self):
        return self.treasures
    def init_state(self):
        return self.initState
       
   
    def __hash__(self):
        """Returns a hash for the task"""
        #taskTuple = tuple([self.sizeX,self.sizeY,tuple(self.initState)])
        taskTuple = tuple([self.sizeX,self.sizeY,self.name])
        return hash(taskTuple)
    

    
    def load_task_state(self,taskState):
        """Load a textual description of the state to an internal state
            Objects are separated by commas, in the format <type>:<xPosic>-<yPosic>
            type can be: 'agent', 'treasure',pit, or fire
        """
        objects = taskState.split(',')
        
        taskInfo = []
        for obj in objects:
            clasSpt = obj.split(":")
            posics = clasSpt[1].split('-') 
            taskInfo.append([clasSpt[0],int(posics[0]),int(posics[1])])
            
        import operator
        taskInfo.sort(key=operator.itemgetter(0, 1, 2))
    
        return taskInfo
        
        


