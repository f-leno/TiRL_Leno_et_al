# -*- coding: utf-8 -*-
"""
Created on May 29th, 8:57
Q-learning simple implementation
@author: Felipe Leno
"""

import random
import math

from .agent import Agent
from common_features import Agent_Utilities


import domain.actions as actions

class QLearning(Agent):
    
    
    
    alpha = None

    
    epsilon = None

    
    functions = None
    policy = None
    
    qTable = None
    
    initQ = None #Value to initiate Q-table

    

    def __init__(self, seed=12345,alpha=0.9,epsilon=0.1):
        
        self.functions = Agent_Utilities()
        self.alpha = alpha
        self.epsilon = epsilon
        self.qTable = {}
        
        
        super(QLearning, self).__init__(seed=seed)
        self.activatedTL = False
        
        
             
        

            
    
    def select_action(self, state):
        """ When this method is called, the agent executes an action based on its Q-table """
        
        #If exploring, an exploration strategy is executed
        if self.exploring:
            action =  self.exp_strategy(state)
        #Else the best action is selected
        else:
            #action =  self.exp_strategy(state)
            action = self.policy_check(state)
        
        return action

        
        
    def policy_check(self,state):
        """In case a fixed action is included in the policy cache, that action is returned
        else, the maxQ action is returned"""
        return self.max_Q_action(state)
        
        
    def max_Q_action(self,state):
        """Returns the action that corresponds to the highest Q-value"""
        actions = self.getPossibleActions()
        v,a =  self.functions.get_max_Q_value_action(self.qTable,state,actions,self.exploring,self)
        return a
    def get_max_Q_value(self,state):
        """Returns the maximum Q value for a state"""
        actions = self.getPossibleActions()
        v,a =  self.functions.get_max_Q_value_action(self.qTable,state,actions,self.exploring,self)
        return v
        
        
        
    def exp_strategy(self,state):
        """Returns the result of the exploration strategy"""
        useBoltz = False        
        allActions = self.getPossibleActions()
        if useBoltz:
            #Boltzmann exploration strategy
            valueActions = []
            sumActions = 0
            
            for action in allActions:
                qValue = self.readQTable(state,action)
                vBoltz = math.pow(math.e,qValue/self.T)
                valueActions.append(vBoltz)
                sumActions += vBoltz
            
            probAct = []
            for index in range(len(allActions)):
                probAct.append(valueActions[index] / sumActions)
            
            rndVal = random.random()
            
            sumProbs = 0
            i=-1
            
            while sumProbs <= rndVal:
                i = i+1
                sumProbs += probAct[i]
            
            return allActions[i]
        else:
            prob = random.random()
            if prob <= self.epsilon:
                return random.choice(allActions)
            return self.max_Q_action(state)
           

    
    def get_Q_size(self):
        """Returns the size of the QTable"""
        return len(self.qTable)
        
    
    def observe_reward(self,state,action,statePrime,reward):
        """Performs the standard Q-Learning Update"""
        if self.exploring:
            qValue= self.readQTable(state,action)
            V = self.get_max_Q_value(statePrime)      
            newQ = qValue + self.alpha * (reward + self.gamma * V - qValue)
            self.qTable[(state,action)] = newQ
 
        
        
        
        
#        if self.exploring:   
#            qValue= self.readQTable(state,action)
#            V = self.get_max_Q_value(statePrime)        
#            TDError = reward + self.gamma * V - qValue
#            self.stateActionTrace[(state, action)] = self.stateActionTrace.get((state, action), 0) + 1            
#            for stateAction in self.stateActionTrace:
#                # update update ALL Q values and eligibility trace values
#                newQ = qValue + self.alpha * TDError * self.stateActionTrace.get(stateAction, 0)
#                self.qTable[stateAction] = newQ
#                # update eligibility trace Function for state and action
#                self.stateActionTrace[stateAction] = self.gamma * self.decayRate * self.stateActionTrace.get(stateAction, 0)
#            if self.environment.is_terminal_state():
#                    self.stateActionTrace = {} 
#                    self.epsilon = self.epsilon #* self.epsilonDecay

            
            
           
#        if self.exploring:
#            qValue= self.readQTable(state,action)
#            V = self.get_max_Q_value(statePrime)        
#            newQ = qValue + self.alpha * (reward + self.gamma * V - qValue)
#            self.qTable[(state,action)] = newQ
#        
        
    
    def getPossibleActions(self):
        """Returns the possible actions"""
        
        return actions.all_agent_actions()

 