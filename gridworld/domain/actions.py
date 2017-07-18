# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:19:39 2016

Agent Actions for the Pre-Predator environment
@author: Felipe Leno
"""

agentActions = 4
preyActions = 4
NORTH, SOUTH, WEST, EAST, NOOP = range(5)

def all_agent_actions():
    return [NORTH, SOUTH, WEST, EAST]