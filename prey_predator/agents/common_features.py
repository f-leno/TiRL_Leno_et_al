# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 08:17:02 2016
Common functions for all algorithms
@author: Felipe Leno
"""
from tilecoding import TileCoding
import random
class Agent_Utilities():
    lowerBoundVariables = None
    upperBoundVariables = None
    tilesNumber = None
    tilesWidth = None
    
    tileCoding = None    
    def __init__(self,lowerBoundVariables = -1,upperBoundVariables = +1,tilesNumber = 10,tilesWidth = 0.2):
        self.tileCoding = TileCoding(lowerBoundVariables = lowerBoundVariables, 
            upperBoundVariables = upperBoundVariables, tilesNumber = tilesNumber, tileWidth=tilesWidth)
        self.lowerBoundVariables = lowerBoundVariables
        self.upperBoundVariables = upperBoundVariables
        self.tilesNumber = tilesNumber
        self.tilesWidth = tilesWidth

    def discretize_state(self,stateFeatures):
        """Returns a tuple that represents a discretized description of the state"""
        quantVar =  self.tileCoding.quantize(stateFeatures)  
        data = []
        #len(quantVar[0]) is the number of variables
        for i in range(0,len(quantVar[0])):
            #Transforms n tuples into a single array
            for var in quantVar:
                #copy each tuple value to the output
                data.append(var[i])
        #returns the output as a tuple
        return tuple(data)
        
        
    def check_various_max_Q(self,qTable,state,allActions):
        """Returns if the state has more than 1 action if the same max value"""
        maxActions = []
        maxValue = -float('Inf')
        
        for act in allActions:
            #print str(type(state))+" - "+str(type(act))
            qV = qTable.get((state,act),0)
            if(qV>maxValue):
                maxActions = [act]
                maxValue = qV
            elif(qV==maxValue):
                maxActions.append(act)
                
        return len(maxActions)>1
        
    def get_max_Q_value_action(self,qTable,state,allActions,exploring,agent):
        """Returns the maximum Q value and correspondent action to a given state"""
        maxActions = []
        maxValue = -float('Inf')
        
        for act in allActions:
            #print str(type(state))+" - "+str(type(act))
            qV = agent.readQTable(state,act)
            if(qV>maxValue):
                maxActions = [act]
                maxValue = qV
            elif(qV==maxValue):
                maxActions.append(act)
        
        
        
        #if exploring:
        action = random.choice(maxActions)
        #else:
        #    action = maxActions[0]

        
        return maxValue,action