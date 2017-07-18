# -*- coding: utf-8 -*-
"""
Created on May 29th 9:03
Common functions for all algorithms
@author: Felipe Leno
"""

import random
class Agent_Utilities():

    def __init__(self):
        pass
   
        
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