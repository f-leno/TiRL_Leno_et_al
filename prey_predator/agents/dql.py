# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:42:52 2016
Distributed Q-Learning implementation
@author: Felipe Leno
"""

from .dooq import DOOQ

import copy


class DQL(DOOQ):
    
    
    

    def __init__(self, seed=12345,numAg = 3,gamma=0.9,T=0.4):
        super(DQL, self).__init__(seed=seed,numAg = numAg,gamma=gamma,T=T)
        
        
        
    def initiate_agent_refs(self,numAg,seed):
        """ Create the references to be executed by experiment.py """
        agents = []
        for i in range(numAg):        
            agents.append(copy.deepcopy(self))
            agents[i].sortFriends = False #Don't use OO representation        
        return agents

