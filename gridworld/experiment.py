#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import argparse
import sys

import csv
import random
#from environment import PredatorPreyEnvironment,GoldMineEnvironment
from domain.gridworldenvironment import GridWorldEnvironment

import os
#from cmac import CMAC
#from graphics_predator_prey import GraphicsPredatorPrey

#from agents.agent import Agent

debugImage = False
graphicHandler = None
debugEvaluation = [0,1,2]        


def get_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-n','--number_agents',type=int, default=3)
    parser.add_argument('-ta','--task_path', default='./tasks/')
    parser.add_argument('-a','--algorithm',  default='Dummy') 
    parser.add_argument('-t','--learning_trials',type=int, default=15000)
    parser.add_argument('-eu','--exp_unit',choices=['episodes','steps'], default='steps')
    parser.add_argument('-i','--evaluation_interval',type=int, default=100)
    parser.add_argument('-d','--evaluation_duration',type=int, default=1)
    parser.add_argument('-s','--seed',type=int, default=12345)
    parser.add_argument('-l','--log_folder',default='./log/')
    parser.add_argument('-q','--q_folder',default='./qtables/')
    parser.add_argument('-et','--end_trials',type=int, default=100)
    parser.add_argument('-it','--initial_trial',type=int, default=1)
    parser.add_argument('-te','--type_exp',choices=['saveQ','reuseQ','none'], default='none')
    #Modifications in the environment:
    # reward = changes in the reward function
    parser.add_argument('-m','--modification',choices=['reward','none','negative','transition','goldmine'], default='none')
    

    return parser.parse_args()


def build_agent():
    """Builds and returns the agent object as specified by the arguments"""
    
    
    
    parameter = get_args()
    
    agentName = getattr(parameter,"algorithm")
    print "AgentName: "+agentName
    try:
        AgentClass = getattr(
               __import__('agents.' + (agentName).lower(),
                          fromlist=[agentName]),
                          agentName)
    except ImportError as error:
           sys.stderr.write(str(error)+'\n')
           sys.exit(1)
    
    AGENT = AgentClass(seed=parameter.seed)
    print "OK Agent"

    return AGENT
    

def main():
    parameter = get_args()
    print parameter
    
    #isGold =  parameter.modification == 'goldmine' and parameter.type_exp != 'reuseQ'
    #if debugImage:
    #    graphicHandler = GraphicsPredatorPrey(10,10,not isGold)    

    
    #Initiate agent Threads    
    #global okThread
    #okThread = True
            #Q-table Folder
    qFolder = parameter.q_folder + parameter.algorithm+'/'
    if not os.path.exists(qFolder):
        os.makedirs(qFolder)
    
    for trial in range(parameter.initial_trial,parameter.end_trials+1):
        print('***** %s: Start Trial' % str(trial))            
        
        
        #Folder for results
        logFolder = parameter.log_folder + parameter.algorithm+"-"+parameter.type_exp+'-'+parameter.modification
        if not os.path.exists(logFolder):
                os.makedirs(logFolder)
        logFolder = logFolder + "/_0_"+str(trial)+"_AGENT_1_RESULTS"
        

        
        
        #Output Files
        eval_csv_file = open(logFolder + "_eval", "wb")
        eval_csv_writer = csv.writer(eval_csv_file)
        eval_csv_writer.writerow(('episodes',"steps_completed","reward"))
        eval_csv_file.flush()
        
                                          
        random.seed(parameter.seed+trial)
        agent = build_agent()
        
        if parameter.type_exp == 'reuseQ':
            agent.loadQTable(qFolder,trial)
            
        if parameter.type_exp == 'saveQ':
            taskFile = parameter.task_path + 'source.task'
        else:
            taskFile = parameter.task_path + 'target.task'
            
        if parameter.modification == 'reward':
            changedReward = True
        else:
            changedReward = False
  
        #The seed for initial state gneration must always be the same
        random.seed(parameter.seed+trial)
        
        #if(parameter.modification == 'reward'):
        #    rewardType = 2 #Second type of reward, distance-based
        #else:
        #    rewardType = 1
            
        #if(parameter.modification == 'negative'):
        #    invertedAction = True
        #else:
        #    invertedAction = False
            
        #if(parameter.modification == 'transition'):
        #    changeTransition = True
        #else:
        #    changeTransition = False
        environment = GridWorldEnvironment(taskFile,changedReward=changedReward)
        environment_target = GridWorldEnvironment(taskFile,changedReward=changedReward)
        agent.connect_env(environment)
        
        #if isGold:
        #    environment = GoldMineEnvironment(numberAgents = parameter.number_agents,agents = agents,depth=parameter.depth,
                                              #preys=parameter.number_preys, evalEpisodes = parameter.evaluation_duration)
        #else:
        #    environment = PredatorPreyEnvironment(numberAgents = parameter.number_agents,agents = agents,depth=parameter.depth,
                                              #preys=parameter.number_preys, evalEpisodes = parameter.evaluation_duration, rewardType=rewardType,
                                              #invertedAction=invertedAction,changeTransition=changeTransition)    
        
        
        
        
        
        
        totalSteps = 0
        episode = 0
        terminal = False
                
        keepTraining = True
        environment.start_episode()
        #Runs learning
        while keepTraining:
            #Check if it is time to policy evaluation and the agent is training in the target task
            # perform an evaluation trial
            
            if parameter.exp_unit == 'episodes' and episode % parameter.evaluation_interval == 0:
                evaluate = True
            elif parameter.exp_unit == 'steps' and totalSteps % parameter.evaluation_interval == 0:
                evaluate = True
            else:
                evaluate = False
                    
            if(evaluate):
            #--------------------------------------- Policy Evaluation---------------------------------------------
                    agent.set_exploring(False)
                    agent.connect_env(environment_target)
                    
                    stepsToFinish = 0
                    #Executes the number of testing episodes specified in the parameter
                    sumR = 0
                    for eval_episode in range(1,parameter.evaluation_duration+1):
                        curGamma = 1.0
                        eval_step = 0              
                       
                        

                        terminal_target= False
                        environment_target.start_episode()                       
                        while not terminal_target:
                            eval_step += 1
                            
                            state = environment_target.get_state()
                            environment_target.act(agent.select_action(state))
                            
                            #Process state transition
                            statePrime,action,reward = environment_target.step()        
                            sumR += reward * curGamma
                            curGamma = curGamma * agent.gamma      
                            
                            terminal_target = environment_target.is_terminal_state()
                        stepsToFinish += eval_step
                        
                    stepsToFinish = float(stepsToFinish) / parameter.evaluation_duration
                    sumR = float(sumR) / parameter.evaluation_duration
                                         
                                         
                    time = episode if parameter.exp_unit == 'episodes' else totalSteps
                    eval_csv_writer.writerow((time,"{:.2f}".format(stepsToFinish),"{:.15f}".format(sumR)))
                    eval_csv_file.flush()
                    agent.set_exploring(True) 
                    agent.connect_env(environment)
                    #print("*******Eval OK: EP:"+str(episodes)+" Steps:"+str(totalSteps)+" - Duration: "+str(stepsToFinish))
                    #-----------------------------------End Policy Evaluation---------------------------------------------
            
            
            
            
            #One larning step is performed
            totalSteps += 1
            

                
                            
            state = environment.get_state()
            environment.act(agent.select_action(state))
            #Process state transition
            statePrime,action,reward = environment.step()   
                #if debugImage:
                #    g.update_state()
            agent.observe_reward(state,action,statePrime,reward)
                    
                    
            terminal = environment.is_terminal_state()
                    
            #If the agent reached a terminal state, initiates the new episode
            if terminal:
                    environment.start_episode()
                    agent.finish_episode()
                    episode += 1
                    if parameter.exp_unit == 'episodes' and episode > parameter.learning_trials:
                        keepTraining = False

                    
            if parameter.exp_unit == 'steps' and totalSteps > parameter.learning_trials:
                        keepTraining = False
        if parameter.type_exp == 'saveQ':
               agent.saveQTable(qFolder,trial)
               
    agent.finish_learning()
        
             
        
        
    if debugImage:
                graphicHandler.close()
        
    
    
    
    
    
    
    

if __name__ == '__main__':
    main()
