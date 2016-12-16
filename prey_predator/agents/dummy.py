# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:07:14 2016
Random agent in HFO
@author: Felipe Leno
"""


import random
import copy
import actions
from .agent import Agent


class Dummy(Agent):

    def __init__(self, seed=12345,numAg = 3):
        super(Dummy, self).__init__(seed=seed,numAg = numAg)
        self.sortFriends = True
        
        
    def initiate_agent_refs(self,numAg,seed):
        """ Create the references to be executed by experiment.py """
        agents = []
        for i in range(numAg):        
            agents.append(copy.deepcopy(self))
            
        
        return agents
        
    def select_action(self, state,agentIndex):
        """ When this method is called, the agent executes an action. """
        return random.choice(actions.all_agent_actions())
    
    def get_proc_state(self,agentIndex):
        """ Returns a processed version of the current state """
        pass
   
       

    def observe_reward(self,state,action,statePrime,reward,agentIndex):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass
    
    def get_Q_size(self,agentIndex):
        """Returns the size of the QTable"""
        return 0

    