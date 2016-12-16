# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:00:26 2016

Implementation of the QAverage Transfer strategy
@author: Leno
"""


from .qbasetl import QBaseTL



class QAverage(QBaseTL):
    
    def __init__(self, seed=12345,numAg = 3,alpha=0.1):        
        super(QAverage, self).__init__(seed=seed,numAg = numAg,alpha=alpha)
        
        
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        sourceStates = self.translate_state(state)
        
        okStates = []
        for st in sourceStates:
            if (st,action) in self.storedQTable:
                okStates.append(st)
        
        #calculates the resulting Q-value
        q = self.calculateQValue(okStates,action)
        
        return q
    def calculateQValue(self,sourceStates,action):
        """Calculates the QValue to be added in the new Q-table (QAverage)"""
        q = 0.0      
        for sState in sourceStates:
            q = q + self.storedQTable[(sState,action)]
        if len(sourceStates)>0:
            q = q/len(sourceStates)
            
        return q
        
        
    

                
       
        
  