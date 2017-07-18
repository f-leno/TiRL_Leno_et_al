# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:02:08 2016

Executes all the desired experiments. The command-like parameters must be given in the batches variable. The experiments run in multiple threads

@author: Leno
"""
import subprocess
from threading import Thread
def execThread(command):
    subprocess.call(command, shell=True)


"""
-m type of experiment: none - Experiment 1 
                       reward - Experiment 2
                       transition - Experiment 3
                       goldmine - Experiment 4
-it initial trial
-et end trial
-a algorithm: Dummy - Random agent
              QLearning - Regular Q-learning
              QManualMapping - Hand-coded inter-task mapping with q-value reuse
              QAverage - PITAM (see paper)
              QBias - PITAM (see paper)
-te what to do with Q-table?: none - Q-table discarded after learning
                              reuseQ - Reuse previously learned Q-table
                              saveQ - Save Q-table after learning.
-n number of agents
-p number of preys
-de visual depth (see paper)
-t number of learning episodes.


"""

batches = [
        [    "-m none -it 1 -a=QLearning -et=50 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 1 -a=QLearning -et=50 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 1 -a=QLearning -et=50 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m none -it 1 -a=Dummy -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
         "-m reward -it 1 -a=QLearning -et=50 -te=none -n=4 -p=2 -de=4 -t 4500",
         "-m transition -it 1 -a=QLearning -et=50 -te=none -n=4 -p=2 -de=4 -t 4500"
        ],
        [    "-m none -it 1 -a=QManualMapping -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 1 -a=QAverage -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 1 -a=QBias -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m reward -it 1 -a=QManualMapping -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m reward -it 1 -a=QAverage -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m reward -it 1 -a=QBias -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        ],
        [    "-m transition -it 1 -a=QManualMapping -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m transition -it 1 -a=QAverage -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m transition -it 1 -a=QBias -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 1 -a=QManualMapping -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 1 -a=QAverage -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 1 -a=QBias -et=50 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        ],
]

baseCommand = 'python experiment.py '
for batch in batches:    
    threads = []
    for arg in batch:
        command = baseCommand + arg
        threads.append(Thread(target = execThread, args=(command,)))
        threads[len(threads)-1].start()
    for i in range(len(threads)):
           threads[i].join()
    print "BATCH FINISHED"           
    