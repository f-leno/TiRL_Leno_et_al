#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:08:21 2017
Method to calculate PITAM Mappings
@author: Felipe Leno
"""

def pitam_mappings(sourceStates,qTable):
    okStates = []
    totalSimilarityValue = 0
    #Now, for all possible reconstructed source states, find states in the source QTable that have at least one object in common
    for st in sourceStates:
        #Finds objects
        filteredStates = [stateQ[0] for stateQ in qTable[0] if any(obj in st for obj in stateQ[0])]
            
        for fState in filteredStates:
          #Counts how many objects in common for latter computing the PITAM probability
          nObj = len([1 for a in fState if a in st])
          okStates.append([fState,nObj])
              
          totalSimilarityValue += nObj
    return okStates,totalSimilarityValue