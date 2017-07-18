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
    
  
    
    def __init__(self, seed=12345,alpha=0.1):        
        super(QBaseTL, self).__init__(seed=seed,alpha=alpha)



    @abc.abstractmethod    
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        pass 

        
    def translate_state(self,state):
        """Returns the translations that exist inn the source Q-table"""
        
        if state == ('t',0,0) or not hasattr(self, 'storedQTable'):
            return []
        
        #Defines number of objects in source and target tasks
        decomposedPits,decomposedFires,agentObj = self.decomp_objects(state)
        #gets an arbirtrary state in the stored Q-table and counts the number of objects in the source task
        pitsSource,fireSource = self.count_objects(self.storedQTable[0].keys()[0][0])
        
        
        #performs the powerset of pit objects
        pitPowerSet = self.powerset_objects(decomposedPits,pitsSource)
        #Does the same for fires
        firePowerSet = self.powerset_objects(decomposedFires,fireSource)
        #Builds source states
        sourceStates = self.merge_objects(pitPowerSet,firePowerSet,agentObj)
        
        return sourceStates
        
    def count_objects(self,state):
        """Returns the number of fires and pits in the state"""
        numPit = len([t for t in state if t[0] == 'p'])
        
        numFire = len([t for t in state if t[0] == 'f'])
        
        return numPit,numFire
    def decomp_objects(self,state):
        """Receives an object-oriented state and decomposes it to a list of objects"""
        ignoredDistance = 2
        #Gets all pits (ignores far objects) 
        pits = [t for t in state if t[0] == 'p' and abs(t[1]) <= ignoredDistance and abs(t[2]) <= ignoredDistance]
        #Gets all fires (ignores far objects)
        fires = [t for t in state if t[0] == 'f' and abs(t[1]) <= ignoredDistance and abs(t[2]) <= ignoredDistance]
        #Searchs for agent
        treasure = [t for t in state if t[0] == 't']
        
        return pits,fires,treasure[0]
    
   
    def powerset_objects(self,objects,newNumberObjects):
        """Performs the power set operation described on the paper"""
              
        #power set
        els = [list(x) for x in itertools.combinations(objects,newNumberObjects)]
        
        return els
        
    def merge_objects(self,pitPowerSet,firePowerSet,treasureObj):
        """Combines obj attributes into a state"""
        states = []       
          
        
        for pitList in pitPowerSet:
            for fireList in firePowerSet:
                #Each state
                thisState = []
                #Including in the state the objects
                for pit in pitList:
                    thisState.append(pit)
                for fire in fireList:
                    thisState.append(fire)
                thisState.append(treasureObj)
                #Including this state in the final list
                states.append(thisState)
        #If no state was found
        if len(states) == 0:
            #If only pit objects exist
            for pitList in pitPowerSet:
                thisState = []
                for pit in pitList:
                    thisState.append(pit)
                thisState.append(treasureObj)
                states.append(thisState)
            #If only fire objects exist
            for fireList in firePowerSet:
                thisState = []
                for fire in fireList:
                    thisState.append(fire)
                thisState.append(treasureObj)
                states.append(thisState)
            #If no fire or pit objects exist, only the treasure is added
            if len(states) == 0:
                states.append([treasureObj])
            
                        
                
        return states
                
                
       
        
  