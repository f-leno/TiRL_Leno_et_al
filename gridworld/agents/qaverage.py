# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:00:26 2016

Implementation of the QAverage Transfer strategy
@author: Leno
"""


from .qbasetl import QBaseTL
import PITAMUtil



class QAverage(QBaseTL):
    
    def __init__(self, seed=12345,alpha=0.9):        
        super(QAverage, self).__init__(seed=seed,alpha=alpha)
        self.activatedTL = True
        
        
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        sourceStates = self.translate_state(state)

        
        #Defines the PITAM Mapping
        okStates,totalSimilarityValue = PITAMUtil.pitam_mappings(sourceStates,self.storedQTable)
        
        #calculates the resulting Q-value
        q = self.calculateQValue(okStates,action,totalSimilarityValue)
        
        return q
    def calculateQValue(self,sourceStates,action,totalSim):
        """Calculates the QValue to be added in the new Q-table (QAverage)"""
        q = 0.0      
        for sState in sourceStates:
            if (sState[0],action) in self.storedQTable[0]:
                q = q + self.storedQTable[0][(sState[0],action)] * sState[1]/ totalSim
        #if len(sourceStates)>0:
        #    q = q/len(sourceStates)
            
        return q
        
        
    

                
       
        
  