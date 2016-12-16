# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:43:23 2016
Implementation of the Bias transfer
@author: Leno
"""


from .qbasetl import QBaseTL
import actions


class QBias(QBaseTL):
    bias = None
    
    def __init__(self, seed=12345,numAg = 3,alpha=0.1,bias=0.0001):        
        super(QBias, self).__init__(seed=seed,numAg = numAg,alpha=alpha)
        self.bias = bias   
        
        
        
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        
        #Preventing errors regarding last state transition        
        if state == ('e','n','d'):
            return 0
        sourceStates = self.translate_state(state)
        acts = actions.all_agent_actions()
        
        voteActions = [0.0]*len(acts)
        
        
        useBias = False
        
        maxV = -float('inf')
        maxAct = None
        for sState in sourceStates:
            maxV = -float('inf')
            maxAct = None
            for act in acts:
                qV = self.storedQTable.get((sState,act),0.0)
                if qV > maxV:
                    maxV = qV
                    maxAct = act

            if maxV > 0.0:
                voteActions[maxAct] += maxV
                useBias = True
                
                
        for act in acts:     
            if (state,act) not in self.qTable:
                self.qTable[(state,act)] = 0.0
        #Bias transfer
        if useBias:
            maxAct =  voteActions.index(max(voteActions))
            self.qTable[(state,maxAct)] = self.bias
        
            
        return self.qTable[(state,action)]
        