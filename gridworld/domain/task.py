#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:38:57 2017
 Abstract Class for Task Classes
@author: Felipe Leno
"""
import abc

class Task(object):
    """Abstract class describing a task"""
    name      = None
    
    @abc.abstractmethod      
    def init_state(self):
        pass
    @abc.abstractmethod      
    def load_task_state(self,taskState):
        """Loads a textual description of the state to an internal state
            Objects are separated by commas, in the format <type>:<xPosic>-<yPosic>
            type can be: 'agent', 'treasure',pit, or fire for the gridworlddomain
        """
        pass
    def __str__(self):
        return self.name  
    
    def __init__(self, filePath=None,taskName="noName",taskData=None):
        self.name = taskName
        
        
        
        
        
        
def transfer_potential(sourceTask,targetTask):
    """Calculates the transfer potential between two tasks"""
    sizeXSource = sourceTask.get_sizeX()
    sizeYSource = sourceTask.get_sizeY()
    
    sizeXTarget = targetTask.get_sizeX()
    sizeYTarget = targetTask.get_sizeY()
    
    locationTraceSource = []
    locationTraceTarget = []
    #For all possible position, calculates the distance between the objects
    for x in range(1,sizeXSource+1):
        for y in range(1,sizeYSource+1):
            distances = []
            #Iterates over all objects in the source task
            for obj in sourceTask.init_state():
                #If it is an obstacle, stores the distance
                if obj[0] in sourceTask.relevantClasses :
                    distances.append([(x - obj[1],y - obj[2],obj[0])]) 
            #Stores distances for that position
            locationTraceSource.append(distances)
    #Now, the same thing is done for the targetTask
    
    for x in range(1,sizeXTarget+1):
        for y in range(1,sizeYTarget+1):
            distances = []
            #Iterates over all objects in the source task
            for obj in targetTask.init_state():
                #If it is an obstacle, stores the distance
                if obj[0] in targetTask.relevantClasses :
                    distances.append([(x - obj[1],y - obj[2],obj[0])]) 
            #Stores distances for that position
            locationTraceTarget.append(distances)
    
    applicable = 0
    for distSource in locationTraceSource:
        for distTarget in locationTraceTarget:
            #If equivalent state exists
            if all(x in distTarget for x in distSource):
                applicable += 1
                
    #Now, calculates potential
    pot = float(applicable) / (1 + sizeXTarget*sizeYTarget - sizeXSource*sizeYSource)
    return pot
    
    
def is_contained(featuresSource,featuresTarget):
    """Returns if the features of the target task contains all features from the
    source task"""
    return featuresSource[0] <= featuresTarget[0] and featuresSource[1] <= featuresTarget[1] 