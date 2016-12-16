# -*- coding: utf-8 -*-
"""
Created on Nov 3 

@author: Felipe Leno
Environment for the predator-prey domain
"""
import random 
import math
from scipy.spatial import distance

import time
import actions

class PredatorPreyEnvironment(object):
    #Environment Size    
    sizeX = 10
    sizeY = 10
    

    
    #Default Environment Rewards
    capturedReward = None
    defaultReward = None  
    
    rewardType = None
    
    outGridValue = None
    
    invertedAction = None
    
    agentVisualDepth = None
    
    reward = None
    lastTerminal = False
    
    numberAgents = None
    numberPreys = None
    agents = None
    
    agentPositions = None
    preyPositions = None
    caught = None

    
    #Agent class objects
    agents = None
    
    changeTransition = None
    

    storedInitialPositions = None
    lastEvalEps = 0
    agentActions = None
    
    
    #Controls the state transition (for agents running in parallel)
    completedTransition = None
    
    def __init__(self,numberAgents,agents,preys,evalEpisodes,depth, rewardType,invertedAction,changeTransition):
        """Prepares the environment class:
            numberAgents = the number of agents in the simulation
            agents = the agents objects (subclass of Agent)
            evalEpisodes = the number of evaluation episodes
            depth = the visual depth
            rewardType = 1 - reward only when prey is captured, 2 - reward proportional to distance
            invertedAction = inverts the effect of actions
            changeTransition = change the transition function to change agent movements
        """
        self.numberAgents = numberAgents
        self.numberPreys = preys
        self.agents = agents
        self.agentVisualDepth = depth
        self.rewardType = rewardType
        
        if rewardType == 1:
            self.capturedReward = 1
            self.defaultReward = 0
        else:
            self.capturedReward = 100
            self.defaultReward = 0
        self.invertedAction = invertedAction
        self.changeTransition = changeTransition
           
        self.agentActions = [None]*numberAgents
        self.reward = [None]*numberAgents
        
        self.agentPositions = [None]*numberAgents
        self.storedInitialPositions = [None]*evalEpisodes
        self.preyPositions = [None]*preys
        self.caught = [None]*preys
        
        self.build_eval_eps(evalEpisodes)
        self.outGridValue = -99
        


        
    def act(self,agentID,action):
        """Performs an action.
        This function performs nothing until the last agent chooses its action.
        Then, the state transition is activated"""
        self.agentActions[agentID] = action
        
        
    def step(self,agentID):
        """Waits until all the agents applied their actions and the state transition is completed
           The return is statePrime.action,reward"""              
        statePrime = self.get_state(agentID)           
        reward = self.observe_reward(agentID)        
        action = self.agentActions[agentID]
        
        return statePrime,action,reward
    
    def finish_state_transition(self):
        """Executed when all agents completed their state transition procedures"""
        self.state_transition()        
        #self.agentActions = [None]*self.numberAgents

        
        
    def state_transition(self):
        """Executes the state transition"""
        preyIndex = 0        
        
        #Process the prey movement
        for preyP in self.preyPositions:
            #No need to move a captured prey            
            if self.caught[preyIndex]:
                if preyP[0] != self.outGridValue:
                    self.preyPositions[preyIndex][0] = self.outGridValue
                    self.preyPositions[preyIndex][1] = self.outGridValue
            else: #The prey was not captured yet        
                preyMove = random.randint(0,actions.preyActions-1)
                offsetX = 0
                offsetY = 0
                if  (preyMove == actions.NORTH):
                    offsetX = 0
                    offsetY = 1
                elif(preyMove == actions.SOUTH):
                    offsetX = 0
                    offsetY = -1           
                elif(preyMove == actions.EAST):
                    offsetX = 1
                    offsetY = 0 
                elif(preyMove == actions.WEST):
                    offsetX = -1
                    offsetY = 0
                    
                self.preyPositions[preyIndex][0] = self.preyPositions[preyIndex][0] + offsetX
                self.preyPositions[preyIndex][1] = self.preyPositions[preyIndex][1] + offsetY
                
                #movements towards walls
                if(self.preyPositions[preyIndex][0] <= 0):
                    self.preyPositions[preyIndex][0] = 1
                elif(self.preyPositions[preyIndex][0] > self.sizeX):
                    self.preyPositions[preyIndex][0] = self.sizeX
                    
                if(self.preyPositions[preyIndex][1] <= 0):
                    self.preyPositions[preyIndex][1] = 1
                elif(self.preyPositions[preyIndex][1] > self.sizeY):
                    self.preyPositions[preyIndex][1] = self.sizeY
            preyIndex += 1
        
        # Move all agents
        agentIndex = 0
        for agentP in self.agentPositions:
            agtMove = self.agentActions[agentIndex]
            
            offsetX,offsetY = self.getAgentOffset(agtMove) 

            self.agentPositions[agentIndex][0] = self.agentPositions[agentIndex][0] + offsetX
            self.agentPositions[agentIndex][1] = self.agentPositions[agentIndex][1] + offsetY
            
            #movements towards walls
            if(self.agentPositions[agentIndex][0] <= 0):
                self.agentPositions[agentIndex][0] = 1
            elif(self.agentPositions[agentIndex][0] > self.sizeX):
                self.agentPositions[agentIndex][0] = self.sizeX
                
            if(self.agentPositions[agentIndex][1] <= 0):
                 self.agentPositions[agentIndex][1] = 1
            elif(self.agentPositions[agentIndex][1] > self.sizeY):
                 self.agentPositions[agentIndex][1] = self.sizeY
            agentIndex += 1
        #Updates the terminal state variable
        self.check_terminal()
        
        #Updating captured prey
        for i in range(self.numberPreys): 
            if self.caught[i]:
                if self.preyPositions[i][0] != self.outGridValue:
                    self.preyPositions[i][0] = self.outGridValue
                    self.preyPositions[i][1] = self.outGridValue
        
        for i in range(self.numberAgents):        
            if self.reward[i] == 0:
                if self.rewardType == 1:
                    self.reward[i] = self.defaultReward
                else:
                    self.reward[i] = self.nearestPreyReward(i)
                
    def nearestPreyReward(self,agentIndex):
        """Calculates a reward based on the distance of the nearest prey"""
        selfP = self.agentPositions[agentIndex]   
        dist = distance.euclidean(selfP,min(self.preyPositions,key=lambda i: distance.euclidean(i,selfP)))
        rew = math.sqrt(self.capturedReward) / dist
        return rew
        
    def getAgentOffset(self,agtMove):
        """Returns the effect of agent actions (takes into account the inverted action parameter)"""
        if  (agtMove == actions.NORTH):                       
             offsetX = 0 if not self.changeTransition else 1             
             offsetY = 1 if not self.invertedAction else -1
        elif(agtMove == actions.SOUTH):
             offsetX = 0 if not self.changeTransition else -1
             offsetY = -1 if not self.invertedAction else 1          
        elif(agtMove == actions.EAST):
             offsetX = 1 if not self.invertedAction else -1
             offsetY = 0 if not self.changeTransition else -1 
        elif(agtMove == actions.WEST):
             offsetX = -1 if not self.invertedAction else 1
             offsetY = 0 if not self.changeTransition else 1
        return offsetX,offsetY
        

            
    def check_terminal(self):
        """Checks if the current state is terminal"""
        allCaught = True
        for i in range(self.numberAgents):        
            self.reward[i] = 0        
        preyIndex = 0
        
        for preyP in self.preyPositions:
            if not self.caught[preyIndex]:            
                agentIndex = 0
                while not self.caught[preyIndex] and agentIndex < self.numberAgents:
                    if(preyP[0] == self.agentPositions[agentIndex][0] and
                    preyP[1] == self.agentPositions[agentIndex][1]):
                       for i in range(self.numberAgents):        
                           self.reward[i] += self.capturedReward
                       self.caught[preyIndex] = True
                    else:
                       allCaught = False                        
                    agentIndex += 1
            preyIndex += 1
            
                
                
        self.lastTerminal = allCaught
        return allCaught
            

                 
            
        
        
    def get_state(self,agentID,sortFriends=True):
        """Returns the state for a given agent"""
        
        if self.lastTerminal:
            return tuple('end')
        #   ret = [0,0]
        #   for i in range(self.numberAgents-1):
        #       ret.append(float('inf'))
        #       ret.append(float('inf'))
        #   return tuple(ret)
        
        selfP = self.agentPositions[agentID]
        selfx = selfP[0]
        selfy = selfP[1]
        
        sensations = []
        
        preys = self.preyPositions
        
        if sortFriends:
            sortedPreys = sorted(preys,key=lambda i: distance.euclidean(i,selfP))
        else:
            sortedPreys = preys
        notFoundPreys = 0
        #preyx = self.preyPositions[0]        
        #preyy = self.preyPositions[1]
        for i in range(self.numberPreys):
            preyx = sortedPreys[i][0]
            preyy = sortedPreys[i][1]
            
            #sensations related to the prey
            offsetX = preyx - selfx
            offsetY = preyy - selfy
            
            if(math.fabs(offsetX)<= self.agentVisualDepth and math.fabs(offsetY)<= self.agentVisualDepth):
                 sensations.append(offsetX)
                 sensations.append(offsetY)
            else:
                if sortFriends:
                    notFoundPreys +=1
                else:
                 sensations.append(float('inf'))
                 sensations.append(float('inf'))
        if sortFriends:
            for i in range(notFoundPreys):
                sensations.append(float('inf'))
                sensations.append(float('inf'))
                


        #End of prey sensations

        #sensations related to other agents
        otherAg = [x for i,x in enumerate(self.agentPositions) if i!=agentID]
        
        #sort agents by distance
        if sortFriends:
            sortedAg = sorted(otherAg,key=lambda i: distance.euclidean(i,selfP))
        else:
            sortedAg = otherAg
        
        notUsedAg = 0
        for i in range(self.numberAgents-1):
             offsetX = sortedAg[i][0] - selfx
             offsetY = sortedAg[i][1] - selfy
             if(math.fabs(offsetX)<= self.agentVisualDepth and math.fabs(offsetY)<= self.agentVisualDepth):
                 sensations.append(offsetX)
                 sensations.append(offsetY)
             else:
                 notUsedAg += 1
        
        #Agents outside the visual depth
        for i in range(notUsedAg):
            sensations.append(float('inf'))
            sensations.append(float('inf'))
            
        
        
        sensations = tuple(sensations)
        
        return sensations
             
        
        
             
        
    def observe_reward(self,agentID):
        """Returns the reward for the agent"""
        return self.reward[agentID]
        
    def is_terminal_state(self):
        return self.lastTerminal
        
    def start_evaluation_episode(self):
        """Start next evaluation episode"""
        randomState = random.getstate()
        
        import copy
        epInfo = copy.deepcopy(self.storedInitialPositions[self.lastEvalEps])
        self.load_episode(epInfo)
        #Prepares pointer for the next episode
        self.lastEvalEps = (self.lastEvalEps + 1) % len(self.storedInitialPositions)
        #Preys in random position
        notChosen = range(len(self.preyPositions))

        preyPosic = []        
        while len(notChosen) != 0:
            index = random.choice(notChosen)
            preyPosic.append(self.preyPositions[index])
            notChosen.remove(index)
        
        self.preyPositions = preyPosic
        
        #Agents in random position
        notChosen = range(len(self.agentPositions))

        agPosic = []        
        while len(notChosen) != 0:
            index = random.choice(notChosen)
            agPosic.append(self.agentPositions[index])
            notChosen.remove(index)
        
        self.agentPositions = agPosic
        
        self.caught = [False]*self.numberPreys        
        
        random.setstate(randomState)
        
            
                
        
        
        
    def start_learning_episode(self):
        """Starts episode with random initial positions"""
        epInfo = self.generate_episode_information()
        #epInfo = random.choice(self.storedInitialPositions) # ---
        self.load_episode(epInfo)
        self.caught = [False]*self.numberPreys
          

        
    def load_episode(self,episodeInfo):
        """Starts an episode geerated by the generate_episode_information() method"""
        self.preyPositions = episodeInfo[0]
        self.agentPositions = episodeInfo[1]
        self.reward = [None]*self.numberAgents #No last step reward
        self.lastTerminal = False
        
    def build_eval_eps(self,numEps):
        """Prepares the evaluation episodes for posterior use"""
        #self.storedInitialPositions = [[[5,5],[[1,1],[10,10],[1,10]]]]        
        for i in range(numEps):        
            self.storedInitialPositions[i] = self.generate_episode_information()
            
            
    def generate_episode_information(self):
        """Generates a random Episode"""
        
        allPreysPos = []
        for i in range(self.numberPreys):
            xprey = random.randint(1,self.sizeX)
            yprey = random.randint(1,self.sizeY)
            #Prey random initial Position        
            preyP = [xprey,yprey]
            allPreysPos.append(preyP)
        
        
        allAgentsP = []
        #Agents random initial position
        for i in range(self.numberAgents):
            #No terminal state is generated
            repeat = True
            while repeat:
                repeat = False
                index = 0
                xagent = random.randint(1,self.sizeX)
                yagent = random.randint(1,self.sizeY)
                while not repeat and index<self.numberPreys:
                    if allPreysPos[index][0]==xagent and \
                        allPreysPos[index][1]==yagent:
                            repeat = True
                    index = index+1
            agentP = [xagent,yagent]
            allAgentsP.append(agentP)

        return [allPreysPos,allAgentsP]
            
        
            
            
        
    
    
        
        
        