# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:12:00 2016

Manually defined inter-task mappings
@author: Leno
"""


from .qbasetl import QBaseTL

import itertools
import abc

class QManualMapping(QBaseTL):
    
    def __init__(self, seed=12345,numAg = 3,sourcePrey=True,alpha=0.1):        
        super(QManualMapping, self).__init__(seed=seed,numAg = numAg,alpha=alpha,sourcePrey=sourcePrey)
        
    
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

        
    def translate_state(self,state):
        """Returns the translations that exist inn the source Q-table"""
        newStates = []        
        #Translate preys
        
        equalPrey = []
        #The preys that are present in the original task are copied
        for i in range(self.originalPrey):
            equalPrey.extend([state[2*i],state[2*i+1]])
        
        changePrey = []
                
        #remainingPrey = state[(self.originalPrey-1)*2:self.transferPrey*2]
        #Copy the remaining preys        
        #for i in range(len(remainingPrey)/2):
        #    changePrey.append([remainingPrey[2*i],remainingPrey[2*i+1]])
                        
        equalPredator = []
        offset = 2*self.transferPrey
        #Same thing as for preys
        for i in range(self.originalPredator-1):
            equalPredator.extend([state[2*i+offset],state[2*i+1+offset]])
        
        changePredator = []
                
        #remainingPredator = state[(self.originalPredator-2)*2+offset:(self.transferPredator-1)*2+offset]
        #Copy the remaining preys        
        #for i in range(len(remainingPredator)/2):
        #    changePredator.append([remainingPredator[2*i],remainingPredator[2*i+1]])  
        
        #Assemble the states
        #for preyVar in changePrey:
        #for predatorVar in changePredator:
        st = []
        st.extend(equalPrey)
        #st.extend(preyVar)
        
        st.extend(equalPredator)
        # st.extend(predatorVar)
        newStates.append(tuple(st))
            
        return newStates
        

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
                
                
       
        
  