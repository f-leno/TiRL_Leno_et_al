# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:43:43 2016
Base for TL approaches
@author: leno
"""



from .qlearning import QLearning

import itertools
import abc

class QBaseTL(QLearning):
    
    transferPrey = 2
    originalPredator = 3
    transferPredator = 4    
    
    def __init__(self, seed=12345,numAg = 3,alpha=0.1,sourcePrey=True):        
        super(QBaseTL, self).__init__(seed=seed,numAg = numAg,alpha=alpha)
        if sourcePrey:
            self.originalPrey = 1
        else:
            self.originalPrey = 1
    @abc.abstractmethod    
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        pass 

        
    def translate_state(self,state):
        """Returns the translations that exist inn the source Q-table"""
        preyState =  list(state[0:self.transferPrey*2:])
        predatorState = list(state[self.transferPrey*2:])
        #Firstly analizes the Prey class
        preyPowerSet = self.powerset_objects(preyState,self.transferPrey,self.originalPrey)
        #Then analyzes Predator class
        predatorPowerSet = self.powerset_objects(predatorState,self.transferPredator,self.originalPredator-1)
        
        sourceStates = self.merge_objects(preyPowerSet,predatorPowerSet)
        return sourceStates
        

    def powerset_objects(self,attributes,originalObj,newObjects):
        """Performs the power set operation described on the paper"""
        #Divide attributes per objects
        listObj = []        
        i=0
        while i<len(attributes):
            listObj.append(attributes[i:i+2])
            i = i+2
        #power set
        els = [list(x) for x in itertools.combinations(listObj,newObjects)]
        
        return els
        
    def merge_objects(self,obj1,obj2):
        """Combines obj attributes into a state"""
        states = []        
        for att1 in obj1:
            at1proc = []
            for a in att1:
                at1proc.extend(a)
            for att2 in obj2:
                at2proc = []
                for a in att2:
                    at2proc.extend(a)
                attlist = []
                attlist.extend(at1proc)
                attlist.extend(at2proc)
                state = tuple(attlist)
                states.append(state)
        return states
                
                
       
        
  