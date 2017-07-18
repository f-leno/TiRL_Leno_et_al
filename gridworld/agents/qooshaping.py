# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:39:44 2017
Tests the reward shapping  with OO mapping
@author: leno
"""





from .qbasetl import QBaseTL



class QOOShaping(QBaseTL):
    
    def __init__(self, seed=12345,numAg = 3,alpha=0.1,sourcePrey=True):        
        super(QOOShaping, self).__init__(seed=seed,numAg = numAg,alpha=alpha,sourcePrey=sourcePrey)
        
    def initiateFromTL(self,state,action):
        pass
        
    
    def readQTable(self,state,action):
        """The QValues are composed of the source and target Q values"""
        if self.activatedTL and state != ('e','n','d') and state != tuple('blind'):
           sourceStates = self.translate_state(state)
           qValue = 0
           for st in sourceStates:
               count = 0
               if (st,action) in self.storedQTable:
                   count = count + 1
                   qValue += self.storedQTable[(st,action)]

           if count>0:
                qValue /= count
           qValue += self.qTable.get((state,action),0.0)
           return qValue
        
        if state == tuple('blind'):
            return self.qTable.get((tuple('blind'),action),0.0)
            
        
        return self.qTable.get((state,action),0.0)       
   
    

                
       
        
  