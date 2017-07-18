# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:43:23 2016
Implementation of the Bias transfer
@author: Leno
"""


from .qbasetl import QBaseTL
import actions
import PITAMUtil


class QBias(QBaseTL):
    bias = None
    
    def __init__(self, seed=12345,alpha=0.9,bias=1):        
        super(QBias, self).__init__(seed=seed,alpha=alpha)
        self.bias = bias
        self.activatedTL = True
        
        
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        sourceStates = self.translate_state(state)
        
        #Defines the PITAM Mapping
        okStates,totalSimilarityValue = PITAMUtil.pitam_mappings(sourceStates,self.storedQTable)       
        
        #Finds best action according to PITAM
        maxQ = -float('inf')
        bestAct = None
        for act in actions.all_agent_actions():
            q = self.calculateQValue(okStates,act,totalSimilarityValue)
            if maxQ<q:
                maxQ = q
                bestAct = act
        #Initiates Q-entries
        for act in actions.all_agent_actions():
            self.qTable[(state,act)] = maxQ
        #Only the best one receives the bias
        self.qTable[(state,bestAct)] = self.bias + maxQ
                
        return self.qTable[(state,action)]
    
    def calculateQValue(self,sourceStates,action,totalSim):
        """Calculates the QValue to be added in the new Q-table (QAverage)"""
        q = 0.0
        for sState in sourceStates:
            if (sState[0],action) in self.storedQTable[0]:
                q = q + self.storedQTable[0][sState[0],action] * sState[1]/ totalSim
        #if len(sourceStates)>0:
        #    q = q/len(sourceStates)
            
        return q
        