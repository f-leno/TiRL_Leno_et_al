# -*- coding: utf-8 -*-
"""
Created on Thu May 26 08:00
Agent base class for implementation of all algorithm
this class defines the signature of the methods to interact with the environment
@author: Felipe Leno
"""



import abc

class Agent(object):
    """ This is the base class for all agent implementations.

    """
    __metaclass__ = abc.ABCMeta
    
    environment = None
    
    
    exploring = None
    seed = None
    training_steps_total = None
    currentTask = None
    curriculum = None
    initQ = None
    
    
    gamma = 0.9#0.9  #Discount factor for comparing proposals
    
    def __init__(self, seed=12345):
        """ Initializes an agent. """
        self.seed = seed
        self.exploring = True
        self.training_steps_total = 0
        self.initQ = 0
        

       
    def connect_env(self,environment):
        """Connects to the domain environment"""
        self.environment = environment        
        

    @abc.abstractmethod
    def select_action(self, state):
        """ When this method is called, the agent chooses an action. """
        pass
     
        
    @abc.abstractmethod
    def observe_reward(self,state,action,statePrime,reward):
        """ After executing an action, the agent is informed about the state-action-reward-state tuple """
        if self.exploring:
            self.training_steps_total += 1
        
    
    
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
             self.storedQTable = [cPickle.load(myFile)]
        self.activatedTL = True

     
    def readQTable(self,state,action):
        """Read Q Table and do the appropriate initialization in a case of TL"""
        if self.activatedTL and hasattr(self, 'storedQTable'):
            if (state,action) in self.qTable:
                return self.qTable[(state,action)]
            else:
                self.qTable[(state,action)] = self.initiateFromTL(state,action)
        
        return self.qTable.get((state,action),self.initQ)
    def initiateFromTL(self,state,action):
        """The default TL initialization is to return 0.0"""
        return 0.0

    def finish_episode(self):
        """ Informs the agent about the end of an episode """""
        pass
    def finish_learning(self):
        """End of one task"""
        pass