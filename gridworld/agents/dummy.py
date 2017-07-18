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

    def __init__(self, seed=12345):
        super(Dummy, self).__init__(seed=seed)
        
        
        
    def select_action(self, state):
        """ When this method is called, the agent executes an action. """
        return random.choice(actions.all_agent_actions())
    
  
       

    def observe_reward(self,state,action,statePrime,reward):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass
    
    def get_Q_size(self):
        """Returns the size of the QTable"""
        return 0

    