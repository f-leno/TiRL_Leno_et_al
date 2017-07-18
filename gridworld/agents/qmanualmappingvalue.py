# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:25:26 2017
Value reuse for handcrafted mapping

Only the readQTable method is changed from QManualMapping
@author: leno
"""





from .qmanualmapping import QManualMapping
from qbasetl import QBaseTL


class QManualMappingValue(QBaseTL):
   
    def __init__(self, seed=12345,alpha=0.9):        
        super(QManualMappingValue, self).__init__(seed=seed,alpha=alpha)
        self.activatedTL = True
          
    
#    def readQTable(self,state,action):
#        """The QValues are composed of the source and target Q values"""
#        
#        if state == tuple('blind'):
#            return self.qTable.get((tuple('blind'),action),0.0)
#        
#        
#        return self.qTable.get((state,action),0.0)
#    def readQTable(self,state,action):
#        prevValue = self.updating
#        self.updating = True
#        q = super(QManualMappingValue,self).readQTable(state,action)
#        self.updating = prevValue
#        return q
        
    def initiateFromTL(self,state,action):
        """Reuses Q-values according to the paper description"""
        qValue = 0.0
        if self.activatedTL and state != (('t',0,0)):
           sourceState = self.translate_state(state)
           
           #If the state is present in the Q-table, the entry is used, if not, the state with maximum correspondencies is used
           if (sourceState,action) in self.storedQTable[0]:
                qValue += self.storedQTable[0][(sourceState,action)]
                #print "Using previous"
           else:
               sourceSet = set(sourceState)
               #Defines state to be used (the one with the maximum of common objects)
               useState = max(self.storedQTable[0].keys(), key=lambda state_act: len(set(state_act[0]).intersection(sourceSet)))
               if len(set(useState[0]).intersection(sourceSet)) > 0:
                     qValue += self.storedQTable[0].get((useState[0],action),0.0)
          
        
        return qValue

    def translate_state(self,state):
        """Returns the translations that exist inn the source Q-table"""
        if state == ('t',0,0) or not hasattr(self, 'storedQTable'):
            return []
        
        #Defines number of objects in source and target tasks
        decomposedPits,decomposedFires,agentObj = self.decomp_objects(state)
        #gets an arbirtrary state in the stored Q-table and counts the number of objects in the source task
        pitsSource,fireSource = self.count_objects(self.storedQTable[0].keys()[0][0])
        
        
        #searchs for pit objects
        relevantPits = decomposedPits#self.nearest_obj(decomposedPits,pitsSource)
        #Does the same for fires
        relevantFires = decomposedFires#self.nearest_obj(decomposedFires,fireSource)
        
        #Builds source states
        sourceStates = []
        for pit in relevantPits:
            sourceStates.append(pit)
        for fire in relevantFires:
            sourceStates.append(fire)
        sourceStates.append(agentObj)
        
        return tuple(sourceStates)
            
    def nearest_obj(self,listObj,numObj):
       """Return the n objects with minimun distance to the agent"""
       #Sorts the objects according to the manhattan distance
       sortedD = sorted(listObj, key = lambda x: x[1]+x[2])
       
       returnObjs = []
       i = 0
       #Returns only objects that have a distance of 2 or less
       while i<numObj and len(sortedD)>i and sortedD[i][1] + sortedD[i][2] <= 2:
           returnObjs.append(sortedD[i])
           i = i+1
       
       return returnObjs
              
    def decomp_objects(self,state):
        """Receives an object-oriented state and decomposes it to a list of objects"""
        
        #Gets all pits (ignores far objects) 
        pits = [t for t in state if t[0] == 'p' and abs(t[1]) + abs(t[2])<= 1]
        #Gets all fires (ignores far objects)
        fires = [t for t in state if t[0] == 'f' and abs(t[1]) + abs(t[2])<= 2]
        #Searchs for agent
        treasure = [t for t in state if t[0] == 't']
        
        return pits,fires,treasure[0]
        
  