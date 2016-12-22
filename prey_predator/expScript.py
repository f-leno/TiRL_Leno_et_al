# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:02:08 2016

@author: leno
"""
import subprocess
from threading import Thread
def execThread(command):
    subprocess.call(command, shell=True)

batches = [
  [    "-m goldmine -it 51 -a=QLearning -et=60 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 61 -a=QLearning -et=70 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 71 -a=QLearning -et=80 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 81 -a=QLearning -et=90 -te=saveQ -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 91 -a=QLearning -et=100 -te=saveQ -n=3 -p=1 -de=3 -t 2500",   
        "-m goldmine -it 50 -a=Dummy -et=65 -te=none -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 66 -a=Dummy -et=85 -te=none -n=3 -p=1 -de=3 -t 2500",
        "-m goldmine -it 86 -a=Dummy -et=100 -te=none -n=3 -p=1 -de=3 -t 2500"
   ],
  [    "-m none -it 1 -a=Dummy -et=13 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 14 -a=Dummy -et=26 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 27 -a=Dummy -et=39 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 40 -a=Dummy -et=52 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 53 -a=Dummy -et=65 -te=none -n=4 -p=2 -de=4 -t 4500",   
        "-m none -it 66 -a=Dummy -et=78 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 79 -a=Dummy -et=90 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 91 -a=Dummy -et=100 -te=none -n=4 -p=2 -de=4 -t 4500"
   ],
   [    "-m none -it 3 -a=QLearning -et=20 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 4 -a=QAverage -et=17 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 4 -a=QBias -et=17 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 3 -a=QManualMapping -et=14 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 15 -a=QManualMapping -et=20 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",   
        "-m none -it 21 -a=QLearning -et=26 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 30 -a=Dummy -et=45 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 46 -a=Dummy -et=60 -te=none -n=4 -p=2 -de=4 -t 4500"
   ],
   [    "-m none -it 91 -a=Dummy -et=100 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 7 -a=QAverage -et=17 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 9 -a=QBias -et=17 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 5 -a=QManualMapping -et=10 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m goldmine -it 11 -a=QManualMapping -et=17 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",   
        "-m goldmine -it 18 -a=QAverage -et=25 -te=reuseQ -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 61 -a=Dummy -et=75 -te=none -n=4 -p=2 -de=4 -t 4500",
        "-m none -it 76 -a=Dummy -et=90 -te=none -n=4 -p=2 -de=4 -t 4500"
   ]

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
    