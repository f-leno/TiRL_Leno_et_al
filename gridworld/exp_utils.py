
# Author: Ruben Glatt
# Modified by Felipe Leno
# This code countains functions to open .csv files and print graphs. Adaptation of the code published in:
#  Silva et al. Simultaneously Learning and Advising in Multiagent Reinforcement Learning. AAMAS-2017.
#This is an auxiliary source to be used together with the jupyter notebook file as explained in the README file.
#
import argparse
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict
sns.set(style="darkgrid")

import scipy as sp
import scipy.stats

def collect_experiment_data(source='/', runs=2, servers=1, agents=1):
    # load all agent data
    evalSteps = defaultdict(list)
    evalReward = defaultdict(list)
    evalTrials = np.array([])


    goodRuns = 0
    for server in range(servers):
        for agent in range(1, agents+1):
            for run in range(0, runs):
                evalFile = os.path.join(source, "_"+ str(server) +"_"+ str(run+1) +"_AGENT_"+ str(agent) +"_RESULTS_eval")
                
                #print evalFile
                if os.path.isfile(evalFile):
                    try:
                        _etime, _estep, _ereward = np.loadtxt(open(evalFile, "rb"), skiprows=1, delimiter=",", unpack=True)

                    except:
                        continue
                    if sum(evalTrials)==0:
                        evalTrials = _etime
                        #
                    #if sum(_etime.shape) == sum(evalTrials.shape):
                    goodRuns += 1
                    for i in range(len(_etime)):
                            evalSteps[(agent,_etime[i])].append(_estep[i])
                            evalReward[(agent,_etime[i])].append(_ereward[i])
                    #else:
                    #    print("Error " + str(run+1) + " - "+ str(sum(_etime.shape))+" , "+str(sum(evalTrials.shape)))
    with open(os.path.join(source, "_"+ str(0) +"_"+ str(1) +"_AGENT_"+ str(1) +"_RESULTS_eval"), 'r') as f:
        first_line = f.readline()    
    if first_line.split(',')[0]=='steps':
        episodes = False
    else:
        episodes = True
    goodRuns = int(goodRuns / agents)
    print('Could use %d runs from expected %d' % (goodRuns, runs)) 
 
    #print('len(evalGoalPercentages) %d --> %s %s' % (len(evalGoalPercentages), str(type(evalGoalPercentages[(1,20)])), str(evalGoalPercentages[(1,20)]) ))
    #print('len(evalGoalTimes) %d --> %s %s' % (len(evalGoalTimes), str(type(evalGoalTimes[(1,20)])), str(evalGoalTimes[(1,20)]) ))
    


    headerLine = []
    headerLine.append("episodes" if episodes else "steps")
    for run in range(1, runs+1):
        headerLine.append("Run"+str(run))

    with open(os.path.join(source, "__EVAL_steps"), 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow((headerLine))
            csvfile.flush()
            for key in evalSteps.keys():
                newrow = [key[1]]
                for i in evalSteps[key]:
                    newrow.append("{:.2f}".format(i))
                csvwriter.writerow((newrow))
                csvfile.flush()
    
    with open(os.path.join(source, "__EVAL_rewards"), 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow((headerLine))
            csvfile.flush()
            for key in evalReward.keys():
                newrow = [key[1]]
                for i in evalReward[key]:
                    newrow.append("{:.2f}".format(i))
                csvwriter.writerow((newrow))
                csvfile.flush()



    

def summarize_data(data, confidence=0.95):
    n = len(data)
    m = np.nanmean(data,axis=1)
    import scipy.stats as stats
    se = stats.sem(data,axis=1,nan_policy='omit')
    h = se * stats.t._ppf((1+confidence)/2., n-1)
    return np.asarray([m, m-h, m+h])


def summarize_experiment_data(source):
    values = ["__EVAL_steps", "__EVAL_rewards"]
    
    for value in values:
        evalFile = os.path.join(source, value)
        #print(evalFile)
        #evalFileContent = np.loadtxt(open(evalFile, "rb"), skiprows=1, delimiter=",", unpack=True)
        evalFileContent = pd.read_csv(open(evalFile, "rb"), skiprows=0, delimiter=",")
        values = evalFileContent.values
        import operator
        listToSort = values.tolist()
        listToSort.sort(key=operator.itemgetter(0))
        values = np.array(listToSort)
        trials = values[:,0]
        data = values[:,1:]
        update = summarize_data(data)
        headerLine = []
        
        with open(evalFile, 'r') as f:
            first_line = f.readline()    
        if first_line.split(',')[0]=='steps':
            episodes = False
        else:
            episodes = True
        
        if episodes:
            headerLine.append("episodes")
        else:
            headerLine.append("step")
        headerLine.append("mean")
        headerLine.append("ci_down")
        headerLine.append("ci_up")

        value = value.replace("EVAL","SUMMARY")
        with open(os.path.join(source, value), 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow((headerLine))
            csvfile.flush()

            for i in range(sum(trials.shape)):
                newrow = [trials[i]]
                for j in update.T[i]:
                    newrow.append("{:.2f}".format(j))
                csvwriter.writerow((newrow))
                csvfile.flush()
                
def cumulative_experiment_data(source,startingFrom=0):
    values = ["__EVAL_steps", "__EVAL_rewards"]
    #values = ["__EVAL_goalpercentages", "__EVAL_goaltimes"]
    for value in values:
        evalFile = os.path.join(source, value)
        #print(evalFile)
        #evalFileContent = np.loadtxt(open(evalFile, "rb"), skiprows=1, delimiter=",", unpack=True)
        evalFileContent = pd.read_csv(open(evalFile, "rb"), skiprows=0, delimiter=",")
        values = evalFileContent.values
        import operator
        listToSort = values.tolist()
        listToSort.sort(key=operator.itemgetter(0))
        values = np.array(listToSort)
        trials = values[:,0]
        data = values[:,1:]
        
        for rep in range(1,data.shape[0]):
            if trials[rep] > startingFrom:
                for index in range(data.shape[1]):
                    data[rep][index] = data[rep-1][index] + data[rep][index]
        
        
        update = summarize_data(data)
        headerLine = []
        
        with open(evalFile, 'r') as f:
            first_line = f.readline()    
        if first_line.split(',')[0]=='steps':
            episodes = False
        else:
            episodes = True
        
        if episodes:
            headerLine.append("episodes")
        else:
            headerLine.append("step")
        headerLine.append("mean")
        headerLine.append("ci_down")
        headerLine.append("ci_up")

        value = value.replace("EVAL","CUMULATIVE")
        with open(os.path.join(source, value), 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow((headerLine))
            csvfile.flush()

            for i in range(sum(trials.shape)):
                newrow = [trials[i]]
                for j in update.T[i]:
                    newrow.append("{:.2f}".format(j))
                csvwriter.writerow((newrow))
                csvfile.flush()
                

def draw_graph(source1 = None, name1 = "Algo1", significant1=None,
               source2 = None, name2 = "Algo2",significant2=None,
               source3 = None, name3 = "Algo3",significant3=None,
               source4 = None, name4 = "Algo4",significant4=None,
               source5 = None, name5 = "Algo5",significant5=None,
               source6 = None, name6 = "Algo5",significant6=None,
               what = "__SUMMARY_rewards", ci = True,nCol = 1,
               #Parameters introduced to allow plot control
               xMin = None, xMax = None, yMin=None, yMax=None,bigFont=False
               ):
    plt.figure(figsize=(20,6), dpi=300)
    #Background
    plt.gca().set_axis_bgcolor('white')
    plt.grid(True,color='0.8')
    
    lineWidth = 8.0 if bigFont else 4.0   
    
    with open(os.path.join(source1, what), 'r') as f:
            first_line = f.readline()    
    if first_line.split(',')[0]=='steps':
            episodes = False
    else:
            episodes = True
    
    if source1 != None:
        summary1File = os.path.join(source1, what)
        summary1Content = np.loadtxt(open(summary1File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X1 = summary1Content[0]
        Y11, Y12, Y13 = summary1Content[1],summary1Content[2],summary1Content[3]
        if ci:
            plt.fill_between(X1, Y11, Y12, facecolor='#7570b3', alpha=0.2)
            plt.fill_between(X1, Y11, Y13, facecolor='#7570b3', alpha=0.2)
        if(not significant1 is None):
           plt.plot(X1,Y11,label=name1, color='#7570b3', linewidth=lineWidth,markevery=significant1,marker="d",markersize=8)
        else:
            plt.plot(X1,Y11,label=name1, color='#7570b3', linewidth=lineWidth)

    if source2 != None:
        summary2File = os.path.join(source2, what)
        summary2Content = np.loadtxt(open(summary2File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X2 = summary2Content[0]
        Y21, Y22, Y23 = summary2Content[1],summary2Content[2],summary2Content[3]
        if ci:
            plt.fill_between(X2, Y21, Y22, facecolor='#e7298a', alpha=0.2)
            plt.fill_between(X2, Y21, Y23, facecolor='#e7298a', alpha=0.2)
        if(not significant2 is None):
            plt.plot(X2,Y21,label=name2, color='#e7298a', linewidth=lineWidth,markevery=significant2,marker="+",markersize=8)
        else:
            plt.plot(X2,Y21,label=name2, color='#e7298a', linewidth=lineWidth)

    if source3 != None:
        summary3File = os.path.join(source3, what)
        summary3Content = np.loadtxt(open(summary3File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X3 = summary3Content[0]
        Y31, Y32, Y33 = summary3Content[1],summary3Content[2],summary3Content[3]
        if ci:
            plt.fill_between(X3, Y31, Y32, facecolor='#66a61e', alpha=0.2)
            plt.fill_between(X3, Y31, Y33, facecolor='#66a61e', alpha=0.2)
        if(not significant3 is None):
            plt.plot(X3,Y31,label=name3, color='#66a61e', linewidth=lineWidth,marker="o",markevery=significant3,markersize=8)
        else:
            plt.plot(X3,Y31,label=name3, color='#66a61e', linewidth=lineWidth)

    if source4 != None:
        summary4File = os.path.join(source4, what)
        summary4Content = np.loadtxt(open(summary4File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X4 = summary4Content[0]
        Y41, Y42, Y43 = summary4Content[1],summary4Content[2],summary4Content[3]
        if ci:
            plt.fill_between(X4, Y41, Y42, facecolor='#e6ab02', alpha=0.2)
            plt.fill_between(X4, Y41, Y43, facecolor='#e6ab02', alpha=0.2)
        if(not significant4 is None):
            plt.plot(X4,Y41,label=name4, color='#e6ab02', linewidth=lineWidth,markevery=significant4,marker="H",markersize=8)
        else:
            plt.plot(X4,Y41,label=name4, color='#e6ab02', linewidth=lineWidth)

    if source5 != None:
        summary5File = os.path.join(source5, what)
        summary5Content = np.loadtxt(open(summary5File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X5 = summary5Content[0]
        Y51, Y52, Y53 = summary5Content[1],summary5Content[2],summary5Content[3]
        if ci:
            plt.fill_between(X5, Y51, Y52, facecolor='black', alpha=0.2)
            plt.fill_between(X5, Y51, Y53, facecolor='black', alpha=0.2)
        if(not significant5 is None):
            plt.plot(X5,Y51,label=name5, color='black', linewidth=lineWidth,markevery=significant5,marker="x",markersize=8)
        else:
            plt.plot(X5,Y51,label=name5, color='black', linewidth=lineWidth)
            
    if source6 != None:
        summary6File = os.path.join(source6, what)
        summary6Content = np.loadtxt(open(summary6File, "rb"), skiprows=1, delimiter=",", unpack=True)
        X6 = summary6Content[0]
        Y61, Y62, Y63 = summary6Content[1],summary6Content[2],summary6Content[3]
        if ci:
            plt.fill_between(X6, Y61, Y62, facecolor='black', alpha=0.2)
            plt.fill_between(X6, Y61, Y63, facecolor='black', alpha=0.2)
        if(not significant6 is None):
            plt.plot(X6,Y61,label=name6, color='#999999', linewidth=lineWidth,markevery=significant6,marker="^",markersize=8)
        else:
            plt.plot(X6,Y61,label=name6, color='#999999', linewidth=lineWidth)
            
    if not yMin is None:
            plt.ylim([yMin,yMax])
    if not xMin is None:
            plt.xlim([xMin,xMax])
            
    axisSize = 26 if bigFont else 18
    fontSize = 32 if bigFont else 20
    

    if what == "__SUMMARY_steps":
        #plt.title('Goal Percentage per Trial')
        plt.ylabel('Steps until completed', fontsize=fontSize, fontweight='bold')
    elif what == "__SUMMARY_rewards":
        #plt.title('Goal Percentage per Trial')
        plt.ylabel('Cumulative Reward', fontsize=fontSize, fontweight='bold')
    else:
        #plt.title('Unknown')
        plt.ylabel('Unknown')

    if episodes:
        plt.xlabel('Training Episodes', fontsize=fontSize, fontweight='bold')
    else:
        plt.xlabel('Training Steps', fontsize=fontSize, fontweight='bold')
    plt.legend(loc='best',prop={'size':fontSize, 'weight':'bold'},ncol=nCol)
    plt.tick_params(axis='both', which='major', labelsize=axisSize)
    plt.show()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--source',default='/home/leno/gitProjects/SURL_Leno_2017/python_implement/log/QLearning-NoneCurriculum')
    parser.add_argument('-r','--runs',type=int, default=5)
    return parser.parse_args()

def main():
    parameter = get_args()
    #collect_experiment_data(source=parameter.source, runs=parameter.runs)
    
    cumulative_experiment_data(parameter.source)

if __name__ == '__main__':
    main()
