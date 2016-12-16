# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:06:45 2016
Agent Class for evaluation
@author: Felipe Leno
"""



import abc

class Agent(object):
    """ This is the base class for all agent implementations.

    """
    __metaclass__ = abc.ABCMeta
    
    environment = None
    activatedTL = None
    
    numAg = None
    sortFriends = None
    qTable = None
    storedQTable = None    
    
    references = None
    seed = None
    agentIndex = None
    
    gamma = None
    
    
    def __init__(self, seed=12345,numAg = 3,gamma=0.9):
        """ Initializes an agent for a given environment. """
        self.qTable = {}
        self.seed = seed
        self.exploring = True
        self.training_steps_total = 0
        self.numAg = numAg
        self.activatedTL = False
        self.gamma = gamma
       
    def connectEnv(self,environment,agentIndex):
        """Connects to the prey-predator environment"""
        self.environment = environment
        self.agentIndex = agentIndex
        
        

    @abc.abstractmethod
    def select_action(self, state,agentIndex):
        """ When this method is called, the agent executes an action. """
        pass
    @abc.abstractmethod
    def get_proc_state(self,agentIndex):
        """ Returns a processed version of the current state """
        pass
    def action(self,agentIndex):
        """Defines the action to be executed and returns the action and the 
        state in the point of view of the agent"""
        state = self.get_proc_state(agentIndex)
        action = self.select_action(state,agentIndex)
        self.environment.act(agentIndex,action)
        return state,action
    
      
        
    @abc.abstractmethod
    def observe_reward(self,state,action,statePrime,reward,agentIndex):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        pass
    @abc.abstractmethod
    def get_Q_size(self,agentIndex):
        """Returns the size of the QTable"""
        pass

    
    def step(self):
        """ Perform a complete training step """
        status = self.hfo.step()
        return status,self.get_discretized_state()
        

    def set_exploring(self, exploring):
        """ The agent keeps track if it should explore in the current state (used for evaluations) """
        self.exploring = exploring


    def saveQTable(self,folder,trial):
        """ Saves the Q-table for posterior reuse"""
        fileToWrite = folder + "qtable"+str(trial)+".txt"
        import cPickle
        #Stores the Q-table for posterior reuse
        with open(fileToWrite,"wb") as qFile:
            cPickle.dump(self.qTable, qFile)

    def loadQTable(self,folder,trial):
        """Restores a previously saved Q-table for Transfer Learning"""
        fileToWrite = folder + "qtable"+str(trial)+".txt"
        import cPickle
        with open(fileToWrite, "rb") as myFile:
             self.storedQTable = cPickle.load(myFile)
        self.activatedTL = True

     
    def readQTable(self,state,action):
        """Read Q Table and do the appropriate initialization in a case of TL"""
        if self.activatedTL:
            if (state,action) in self.qTable:
                return self.qTable[(state,action)]
            else:
                self.qTable[(state,action)] = self.initiateFromTL(state,action)
        
        return self.qTable.get((state,action),0.0)
    def initiateFromTL(self,state,action):
        """The default TL initialization is to return 0.0"""
        return 0.0
    def finish_training(self):
        """End the training"""
        pass