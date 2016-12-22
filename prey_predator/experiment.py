#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import argparse
import sys

import csv
import random
from environment import PredatorPreyEnvironment,GoldMineEnvironment
import os
#from cmac import CMAC
from graphics_predator_prey import GraphicsPredatorPrey

#from agents.agent import Agent

debugImage = False
graphicHandler = None
debugEvaluation = [0]        


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--number_agents',type=int, default=3)
    parser.add_argument('-p','--number_preys',type=int, default=1)
    parser.add_argument('-a','--agent',  default='Dummy') #Here, one agent class controls everything
    parser.add_argument('-t','--learning_trials',type=int, default=2500)
    parser.add_argument('-i','--evaluation_interval',type=int, default=10)
    parser.add_argument('-d','--evaluation_duration',type=int, default=100)
    parser.add_argument('-s','--seed',type=int, default=12345)
    parser.add_argument('-l','--log_file',default='/home/leno/gitProjects/TiRL_Leno_et_al/log/')
    parser.add_argument('-q','--q_folder',default='/home/leno/gitProjects/TiRL_Leno_et_al/qtables/')
    parser.add_argument('-et','--end_trials',type=int, default=1000)
    parser.add_argument('-it','--initial_trial',type=int, default=1)
    parser.add_argument('-te','--type_exp',choices=['saveQ','reuseQ','none'], default='none')
    parser.add_argument('-de','--depth',type=int, default=2)
    #Modifications in the environment:
    # reward = changes in the reward function
    parser.add_argument('-m','--modification',choices=['reward','none','negative','transition','goldmine'], default='none')
    

    return parser.parse_args()


def build_agents():
    """Builds and returns the agent object as specified by the arguments"""
    agents = []
    
    
    parameter = get_args()
    
    for i in range(parameter.number_agents):
        agentName = getattr(parameter,"agent")
        print "AgentName: "+agentName
        try:
            AgentClass = getattr(
               __import__('agents.' + (agentName).lower(),
                          fromlist=[agentName]),
                          agentName)
        except ImportError:
               sys.stderr.write("ERROR: missing python module: " +agentName + "\n")
               sys.exit(1)
        
        print "Creating agent"
        if parameter.modification == 'goldmine' and parameter.type_exp == 'reuseQ':
            AGENT = AgentClass(seed=parameter.seed, numAg = parameter.number_agents, sourcePrey = False)
        else:
            AGENT = AgentClass(seed=parameter.seed, numAg = parameter.number_agents)
        print "OK Agent"
        agents.append(AGENT)
        
    return agents
    

def main():
    parameter = get_args()
    print parameter

    #print('***** %s: %s Agent online' % (str(AGENT.unum), str(parameter.agent)))
    print('***** %s: Agents online --> %s')
   # print('***** %s: Agents online --> %s' % (str(AGENT.unum), str(AGENT)))
   # print('***** %s: Setting up train log files' % str(AGENT.unum))
    #train_csv_file = open(parameter.log_file + "_" + str(AGENT.unum) + "_train", "wb")
    print "Agent Classes OK"
    
    isGold =  parameter.modification == 'goldmine' and parameter.type_exp != 'reuseQ'
    if debugImage:
        graphicHandler = GraphicsPredatorPrey(10,10,not isGold)    
    
    #Including name of doman
    if parameter.modification == 'goldmine':
        parameter.q_folder += 'gold/'
    else:
        parameter.q_folder += 'prey/'
    
    
    #Initiate agent Threads    
    #global okThread
    #okThread = True
    for trial in range(parameter.initial_trial,parameter.end_trials+1):
        print('***** %s: Start Trial' % str(trial))            
        random.seed(parameter.seed+trial)
        agents = build_agents()
        
        if parameter.type_exp == 'reuseQ':
            for agent in agents:
                agent.loadQTable(parameter.q_folder,trial)
  
        #The seed for initial state gneration must always be the same
        random.seed(parameter.seed)
        
        if(parameter.modification == 'reward'):
            rewardType = 2 #Second type of reward, distance-based
        else:
            rewardType = 1
            
        if(parameter.modification == 'negative'):
            invertedAction = True
        else:
            invertedAction = False
            
        if(parameter.modification == 'transition'):
            changeTransition = True
        else:
            changeTransition = False
        
        if isGold:
            environment = GoldMineEnvironment(numberAgents = parameter.number_agents,agents = agents,depth=parameter.depth,
                                              preys=parameter.number_preys, evalEpisodes = parameter.evaluation_duration)
        else:
            environment = PredatorPreyEnvironment(numberAgents = parameter.number_agents,agents = agents,depth=parameter.depth,
                                              preys=parameter.number_preys, evalEpisodes = parameter.evaluation_duration, rewardType=rewardType,
                                              invertedAction=invertedAction,changeTransition=changeTransition)    
        
        for i in range(parameter.number_agents):
             agents[i].connectEnv(environment,i)   
             
        random.seed(parameter.seed+trial)
        
        originalGamma = agents[0].gamma

                
        train_csv_writers = [None]*len(agents)
        train_csv_files = [None]*len(agents)
        eval_csv_writers = [None]*len(agents)
        eval_csv_files = [None]*len(agents)
        for i in range(len(agents)):
            logFolder = parameter.log_file + getattr(parameter,"agent")+"-"+str(parameter.number_preys)+"-"+parameter.type_exp+"-"+parameter.modification
            if not os.path.exists(logFolder):
                os.makedirs(logFolder)
            logFolder = logFolder + "/_0_"+str(trial)+"_AGENT_"+str(i+1)+"_RESULTS"
            train_csv_files[i] = open(logFolder + "_train", "wb")
            train_csv_writers[i] = csv.writer(train_csv_files[i])
            train_csv_writers[i].writerow(("trial","steps_captured","reward"))
            train_csv_files[i].flush()
            eval_csv_files[i] = open(logFolder + "_eval", "wb")
            eval_csv_writers[i] = csv.writer(eval_csv_files[i])
            eval_csv_writers[i].writerow(("trial","steps_captured","reward"))
            eval_csv_files[i].flush()
    
        print("******* OK Output File Creation*********")
        
        
        
        
  
        for episode in range(0,parameter.learning_trials+1):
                        

                # perform an evaluation trial
                if(episode % parameter.evaluation_interval == 0):
#                    print environment.storedInitialPositions[0]
#                    print environment.storedInitialPositions[1]
#                    print environment.storedInitialPositions[2]
                
#                    
#                    print environment.lastEvalEps
                    for agentIndex in range(len(agents)):
                        agents[agentIndex].set_exploring(False)
                    stepsToCapture = 0
                    

                    for eval_trials in range(1,parameter.evaluation_duration+1):
                        gamma = 1.0
                        sumR = [0.0] * len(agents)
                        eval_step = 0
                        environment.start_evaluation_episode()

                        terminal = False
                        #For all steps...
                        limit = 500
                        while not terminal and eval_step <= limit:
                            eval_step += 1
                            if debugImage and episode in debugEvaluation:
                                graphicHandler.update_state(environment.preyPositions,environment.agentPositions)
                                
                            #if episode>200:
                            #   print agents[0].state_importance(environment.get_state(0))
                            state = [None]*len(agents)
                            #Defines the action of each agent
                            for agentIndex in range(len(agents)):
                                state[agentIndex],action = agents[agentIndex].action(agentIndex)
                            #Process state transition
                            environment.finish_state_transition()        
                            
                            
                            
                            
                            #Updates reward                            
                            for agentIndex in range(len(agents)):
                                    statePrime, action, reward = environment.step(agentIndex) 
                                    sumR[agentIndex] += reward * gamma
                                    agents[agentIndex].observe_reward(state[agentIndex],action,statePrime,reward,agentIndex)  
                            gamma = gamma * originalGamma                                    
                            
                            terminal = environment.is_terminal_state()
            
                        stepsToCapture += eval_step
                    
                    stepsToCapture = float(stepsToCapture) / parameter.evaluation_duration
                    for agentIndex in range(len(agents)):
                        #if episode != 0:
                        eval_csv_writers[agentIndex].writerow((episode,"{:.2f}".format(stepsToCapture),"{:.15f}".format(sumR[agentIndex])))
                        eval_csv_files[agentIndex].flush()
                        agents[agentIndex].set_exploring(True)
                    print("*******Eval OK: "+str(episode)+" - Duration: "+str(stepsToCapture))
                 
                gamma = 1.0
                sumR = [0.0] * len(agents)
                stepsToCapture = 0       
                eval_step = 0
                environment.start_learning_episode()
                terminal = False
                #For all steps...
                while not terminal:
                    eval_step += 1
                    state = [None]*len(agents)
                    #Defines the action of each agent
                    for agentIndex in range(len(agents)):
                        state[agentIndex],action = agents[agentIndex].action(agentIndex)
                    #Process state transition
                    environment.finish_state_transition() 
                    
                    
                    
                    #Updates reward                            
                    for agentIndex in range(len(agents)):
                         statePrime, action, reward = environment.step(agentIndex) 
                         sumR[agentIndex] += reward * gamma                              
                         agents[agentIndex].observe_reward(state[agentIndex],action,statePrime,reward,agentIndex) 
                    terminal = environment.is_terminal_state()
                    gamma = gamma * originalGamma
                    
                for agentIndex in range(len(agents)):
                    train_csv_writers[agentIndex].writerow((episode,"{:.2f}".format(eval_step),"{:.15f}".format(sumR[agentIndex])))
                    train_csv_files[agentIndex].flush()
                    
                    
        print('***** %s: END Trial' % str(trial)) 
        if parameter.type_exp == 'saveQ':
            i = trial % len(agents)
            agents[i].saveQTable(parameter.q_folder,trial)
            
    for agentIndex in range(len(agents)):
                    eval_csv_files[agentIndex].close()
                    train_csv_files[agentIndex].close()    
    
    
        
    if debugImage:
        graphicHandler.close()
        
    
    
    
    
    
    
    
    
    
    
    #agentThreads = []
#    random.seed(parameter.seed)
#    #try:
#        #Initiating agent
#    agentRefs = [] 
#    agentThreads = []
#    for i in range(parameter.number_agents):
#            agentRefs.append(agent.getAgRef(i))
#            
#    for i in range(parameter.number_agents):
#        agentThreads.append(Thread(target = thread_agent, args=(agentRefs[i],agentRefs,i,parameter)))
#        agentThreads[i].start()
#        sleep(3)
#        
#    for i in range(parameter.number_agents):
#        agentThreads[i].join()
#            
#            
#    #except Exception as e:
#    #    print e.__doc__
#    #    print e.message
#    #    okThread = False
#   
#    
#
#    
#
#    
#    
#def thread_agent(agentObj,allAgents,agentIndex,mainParameters):
#    """This method is executed by each thread in the system and corresponds to the control
#    of one playing agent"""
#    
#    logFolder = mainParameters.log_file + getattr(mainParameters,"agent")+"/_0_"+str(mainParameters.number_trial)+"_AGENT_"+str(agentIndex+1)+"_RESULTS"
#    
#    #Connecting agent to server 
#    print "******Connecting agent "+str(agentIndex)+"****"
#    agentObj.connectHFO()
#    #Building Log folder name
#    print "******Connected agent "+str(agentIndex)+"****"
#    
#    print logFolder + "********" 
#    train_csv_file = open(logFolder + "_train", "wb")
#    train_csv_writer = csv.writer(train_csv_file)
#    train_csv_writer.writerow(("trial","frames_trial","goals_trial","used_budget"))
#    train_csv_file.flush()
#    print('***** %s: Setting up eval log files' % str(agentIndex))
#    #eval_csv_file = open(parameter.log_file + "_" + str(AGENT.unum) + "_eval", "wb")
#    eval_csv_file = open(logFolder + "_eval", "wb")
#    eval_csv_writer = csv.writer(eval_csv_file)
#    eval_csv_writer.writerow(("trial","goal_percentage","avg_goal_time","used_budget"))
#    eval_csv_file.flush()
#    
#    print('***** %s: Start training' % str(agentIndex))
#    for trial in range(mainParameter.initial_trial,mainParameters.learning_trials+1):
#        # perform an evaluation trial
#        if(trial % mainParameters.evaluation_interval == 0):
#            #print('***** %s: Running evaluation trials' % str(AGENT.unum) )
#            agentObj.set_exploring(False)
#            goals = 0.0
#            time_to_goal = 0.0
#            for eval_trials in range(1,mainParameters.evaluation_duration+1):
#                eval_frame = 0
#                eval_status = agentObj.IN_GAME
#                while eval_status == agentObj.IN_GAME:
#                    eval_frame += 1
#                    #print "****First Action****"
#                    agentObj.applyAction()
#                    #print "****First STEP****"
#                    eval_status, statePrime = agentObj.step()
#                    if(eval_status == agentObj.GOAL):
#                        goals += 1.0
#                        time_to_goal += eval_frame
#                        #print('********** %s: GGGGOOOOOOOOOOLLLL: %s in %s' % (str(AGENT.unum), str(goals), str(time_to_goal)))
#            goal_percentage = 100*goals/mainParameters.evaluation_duration
#            #print('***** %s: Goal Percentage: %s' % (str(AGENT.unum), str(goal_percentage)))
#            if (goals != 0):
#                avg_goal_time = time_to_goal/goals
#            else:
#                avg_goal_time = 0.0
#            #print('***** %s: Average Time to Goal: %s' % (str(AGENT.unum), str(avg_goal_time)))
#            # save stuff
#            #print "****Finished****"
#            eval_csv_writer.writerow((trial,"{:.2f}".format(goal_percentage),"{:.2f}".format(avg_goal_time),str(agentObj.get_Q_size())))
#            eval_csv_file.flush()
#            agentObj.set_exploring(True)
#            # reset agent trace
#            
#           
#        
#        #print('***** %s: Starting Learning Trial %d' % (str(AGENT.unum),trial))
#        status = agentObj.IN_GAME
#        frame = 0
#        while status == agentObj.IN_GAME:
#            frame += 1
#            state = agentObj.get_discretized_state()
#            #print "****First Action****"
#            action = agentObj.applyAction()
#            #print "****First STEP****"
#            status, statePrime = agentObj.step()
#            #print "****First REWARD****"
#            reward = agentObj.get_reward(status)
#            #print "****Observe REWARD****"
#            if reward==1: #positive reward
#                statePrime = ("GOAL")
#            agentObj.observe_reward(state,action,statePrime,reward)
#        #print('***** %s: Trial ended with %s'% (str(AGENT.unum), AGENT.hfo.statusToString(status)))
#        #print('***** %s: Agent --> %s'% (str(AGENT.unum), str(AGENT)))
#        #print "****Finished****"
#        # save stuff
#        train_csv_writer.writerow((trial,frame,reward,str(agentObj.get_Q_size())))
#        train_csv_file.flush()
#        #agentObj.stateActionTrace = {}
#
#
#
#        # Quit if the server goes down
#        if status == agentObj.SERVER_DOWN:
#            #agentObj.hfo.act(QUIT)
#            agentObj.quit()
#            print('***** %s: Shutting down agent' % str(agentIndex))
#            break
#    print('***** %s: Agent --> %s'% (str(agentIndex), str(agentObj)))
#    eval_csv_file.close()
#    train_csv_writer.writerow(("-","-",str(agentObj)))
#    train_csv_file.flush()
#    train_csv_file.close()
#    agentObj.quit()
#    agentObj.finish_training()

if __name__ == '__main__':
    main()
