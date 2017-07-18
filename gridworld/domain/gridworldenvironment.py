# -*- coding: utf-8 -*-
"""
Created on May, 25th, 2017.

@author: Felipe Leno
Environment for the gridworld domain
"""
from scipy.spatial import distance
import actions
from gridworldtask import GridWorldTask




class GridWorldEnvironment(object):
    """ GridWorld Environment Class"""
    #Environment Size    
    sizeX = None
    sizeY = None
    
    numberTreasures = None
    numberPits = None
    numberFires = None
    
    treasurePositions = None
    pitPositions = None
    firePositions = None
    
    sensationType = None
    evalEpisodeType = None

    
    agentAction = None 
    
    #Parameter to control if the new reward function is used
    changedReward = None
    
    
    #Rewards
    capturedReward = +2000  #Getting Treasure
    pitReward      = -2500 #Falling into a pit
    nextFireReward = -250 #Getting next to an active fire
    intoFireReward = -500 #Getting into a fire    
    defaultReward  = -1 #Nothing happened
    
    reward = None
    lastTerminal = False
    
    
    
    caught = None
    
    taskInitialPositions = None
    
    limitSteps = None
    currentSteps = None
    
    outGridValue = -99
    
    
    
    def __init__(self,taskFile,limitSteps = 200,changedReward=False):
        """
            Object Constructor, all the task parameters should be specified here:

            treasures: Number of 'treasures', or gold pieces to be spread
            pits: Number of "pits", or holes that kill the agent
            fires: Number of "fires", elements that hurt the agent
            taskState: Initial state for the task
            sensationType: How does the agent perceive the environment?
                (i) 'agent-centric' - objects are perceived according to their relative position           
        """
        
        #Building the task
        task = GridWorldTask(filePath=taskFile,taskName='task')
        
        #environment parameters
        treasures=1
        pits = task.num_pits()
        fires = task.num_fires()
        sizeX = task.get_sizeX()
        sizeY = task.get_sizeY()
        taskState = task.init_state() 
        
        self.numberTreasures = treasures
        self.numberPits = pits
        self.numberFires = fires
            
        self.sizeX = sizeX
        self.sizeY = sizeY
        
        #If a evaluation episode is informed, the code loads it
        self.taskInitialPositions = taskState

        self.treasurePositions = [None]*treasures
        self.pitPositions = [None]*pits
        self.firePositions = [None]*fires
        self.agentPositions = [None]*2
                             
        self.limitSteps = limitSteps
        self.currentSteps = 0
        
        self.changedReward = changedReward
        
    

            
        
        
    def act(self,action):
        """Performs an action.
        This function performs nothing until the state transition is activated"""
        self.agentAction = action
        
        
    def step(self):
        """Performs the state transition and returns (statePrime.action,reward)"""   
        self.state_transition()           
        statePrime = self.get_state()           
        reward = self.observe_reward()        
        action = self.agentAction
        
        self.currentSteps += 1
        
        return statePrime,action,reward
    
    
    def check_terminal(self):
        """Checks if the current state is terminal and processes the reward"""
        
        
        self.reward = 0
        #Fell in pit?
        for i in range(self.numberPits):
            if(self.agentPositions[0] == self.pitPositions[i][0] and 
                  self.agentPositions[1] == self.pitPositions[i][1]):
                self.lastTerminal = True
                self.reward += self.pitReward
                return True                 
        

        #Next to or into fire?
        for fireP in self.firePositions:        
            if(self.agentPositions[0] == fireP[0] and 
                     self.agentPositions[1] == fireP[1]):
                self.reward += self.intoFireReward
            else:
                if(distance.euclidean(self.agentPositions,fireP)==1):
                         self.reward += self.nextFireReward
                         
        allCaught = True
                   
        treasureIndex = 0
        #Got treasure?
        for treasureP in self.treasurePositions:
            if not self.caught[treasureIndex]:            
                if(self.agentPositions[0] == treasureP[0] and 
                     self.agentPositions[1] == treasureP[1]):
                         self.reward += self.capturedReward
                         self.caught[treasureIndex] = True
                else:
                         allCaught = False                        
            treasureIndex += 1
                
        self.lastTerminal = allCaught
        
        if self.currentSteps > self.limitSteps:
            self.lastTerminal = True
            
        
        return allCaught
            

                 
    def blind_state(self,state):
        """Returns if the agent can see anything"""
        return False
    
    def object_reward(self,class_obj,state):
        """Returns a reward related to the object"""
        reward = 0
        
        if class_obj == 't': #treasure
            if state == (0,0):
                reward = self.capturedReward
        elif class_obj == 'f': #Fire
            if state == (0,1) or state == (1,0): #next to fire
                reward = self.nextFireReward
            if state == (0,0): #Stepped in fire
                reward = self.intoFireReward
        elif class_obj == 'p': #Pit
            if state == (0,0):
                reward = self.pitReward
        
        if reward == 0:
            reward = self.defaultReward
            
        return reward
        
    def get_state(self,orderedSens=False):
        """Returns the state in the point of view of the agent
            If onderedSens = True, returns a tuple of sensations rather than a set. Usefull to track
            changes of object states
        """
        
        #All successful states are equal
        if self.lastTerminal and not orderedSens:
            return tuple(tuple(('t',0,0)))
            
        pitClass = 'p'
        treasureClass = 't'
        fireClass = 'f'
        
        selfx = self.agentPositions[0]
        selfy = self.agentPositions[1]
        
        #Set of agent's sensations (order usually doesn't matter)
        if orderedSens:
            sensations = []
        else:
            sensations = set()       
        
        
            
        
        #Including treasure sensations
        for i in range(self.numberTreasures):
            #Positions are relative to the agent            
            offsetX = self.treasurePositions[i][0] - selfx
            offsetY = self.treasurePositions[i][1] - selfy
            if orderedSens:
                sensations.append((treasureClass,offsetX,offsetY))
            else:
                sensations.add((treasureClass,offsetX,offsetY))
            
        
        #Including pit sensations
        for i in range(self.numberPits):
            #Positions are relative to the agent            
            offsetX = self.pitPositions[i][0] - selfx
            offsetY = self.pitPositions[i][1] - selfy
            if orderedSens:
                sensations.append((pitClass,offsetX,offsetY))           
            else:
                sensations.add((pitClass,offsetX,offsetY))           
                   
            
        #Including fire sensations
        for i in range(self.numberFires):
            #Positions are relative to the agent            
            offsetX = self.firePositions[i][0] - selfx
            offsetY = self.firePositions[i][1] - selfy
            if orderedSens:
                sensations.append((fireClass,offsetX,offsetY)) 
            else:
                sensations.add((fireClass,offsetX,offsetY)) 
            
        
          
        #Making the sensation set hashable
        sensations = tuple(sensations)
        
        #Blind treatment
        if self.blind_state(sensations):
            return tuple('blind')
        
        return sensations
             
        
        
             
        
    def observe_reward(self):
        """Returns the reward for the agent"""
        return self.reward
        
    def is_terminal_state(self):
        return self.lastTerminal
        
        
    def start_episode(self):
        """Start next evaluation episode"""
        import copy
        epInfo = copy.deepcopy(self.taskInitialPositions)
        
        #Load episode in memory
        self.load_episode(epInfo)            
        self.caught = [False]*self.numberTreasures    
        self.currentSteps = 0
        
        self.lastTerminal = False
        
            

        
    def load_episode(self,episodeInfo):
        """Loads the information for a new episode
           The information is given in lists follows
           [0] = class - 'agent', 'fire', 'pit', and 'treasure'.
           [1] = x Position (int)
           [2] = y Position (int)
        """
        self.firePositions = []
        self.treasurePositions = []
        self.pitPositions = []
        
        for obj in episodeInfo:
            #Agent positions
            if obj[0] == "agent":
                self.agentPositions[0] = obj[1]
                self.agentPositions[1] = obj[2]
            #Fire positions
            if obj[0] == "fire":
                self.firePositions.append([obj[1],obj[2]])
            if obj[0] == "pit":
                self.pitPositions.append([obj[1],obj[2]])
            if obj[0] == "treasure":
                self.treasurePositions.append([obj[1],obj[2]])
                
        self.reward = None #No last step reward
        self.lastTerminal = False
        
        
        
    def state_transition(self):
        """Executes the state transition"""        

        # Move the agent
        agtMove = self.agentAction
        
        # agent movement
        offsetX,offsetY = self.getAgentOffset(agtMove) 

        self.agentPositions[0] = self.agentPositions[0] + offsetX
        self.agentPositions[1] = self.agentPositions[1] + offsetY
            
        #movements towards walls
        if(self.agentPositions[0] <= 0):
            self.agentPositions[0] = 1
        elif(self.agentPositions[0] > self.sizeX):
            self.agentPositions[0] = self.sizeX
                
        if(self.agentPositions[1] <= 0):
            self.agentPositions[1] = 1
        elif(self.agentPositions[1] > self.sizeY):
            self.agentPositions[1] = self.sizeY
           
        #Updates the terminal state variable
        self.check_terminal()
        
        #Updating captured treasure
        #for i in range(self.numberTreasures): 
        #    if self.caught[i]:
        #        if self.treasurePositions[i][0] != self.outGridValue:
        #            self.treasurePositions[i][0] = self.outGridValue
        #            self.treasurePositions[i][1] = self.outGridValue
        
        if self.reward == 0:
            if self.changedReward:
                self.reward = (self.capturedReward/100) / distance.euclidean(self.agentPositions,self.treasurePositions)
            else:
                self.reward = self.defaultReward
                
        
                 
    def getAgentOffset(self,agtMove):
            """Returns the effect of agent actions"""
            if  (agtMove == actions.NORTH):                       
                 offsetX = 0 
                 offsetY = 1
            elif(agtMove == actions.SOUTH):
                 offsetX = 0 
                 offsetY = -1         
            elif(agtMove == actions.EAST):
                 offsetX = 1 
                 offsetY = 0
            elif(agtMove == actions.WEST):
                 offsetX = -1
                 offsetY = 0 
            return offsetX,offsetY
                
                
        

"""
#Independent test for environment
state = 'agent:1-1,pit:1-2,pit:3-3,fire:8-8,fire:3-5,fire:1-9,treasure:10-10'       
env = GridWorld(1,2,3,10,10,state,sensationType='agent-centric')

from graphics_gridworld import GraphicsGridworld
graphic= GraphicsGridworld(env)

env.start_episode()


env.act(actions.EAST)
print env.step()

graphic.update_state()

print env.get_state()
"""




    

            
        
            
            
        
    
    
        
        
        