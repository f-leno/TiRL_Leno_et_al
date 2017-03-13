# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:25:26 2017
Value reuse for handcrafted mapping

Only the readQTable method is changed from QManualMapping
@author: leno
"""





from .qmanualmapping import QManualMapping


class QManualMappingValue(QManualMapping):
    
    def __init__(self, seed=12345,numAg = 3,sourcePrey=True,alpha=0.1):        
        super(QManualMappingValue, self).__init__(seed=seed,numAg = numAg,alpha=alpha,sourcePrey=sourcePrey)
          
    
#    def readQTable(self,state,action):
#        """The QValues are composed of the source and target Q values"""
#        
#        if state == tuple('blind'):
#            return self.qTable.get((tuple('blind'),action),0.0)
#        
#        
#        return self.qTable.get((state,action),0.0)
        
        
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
        

        
  