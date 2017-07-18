#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:39:18 2017
Abstract class to domain generators
@author: Felipe Leno
"""

import abc

class Domain(object):
    """ This is the base class for all Domain Generators

    """
    __metaclass__ = abc.ABCMeta
    
        
    @abc.abstractmethod      
    def build_environment(self,taskFile,limitSteps,taskName = None):
        """Instantiates an object representing the environment in this domain.
            --taskFile = The path for a file containing the description of a task in this domain
            --limitSteps = The maximum number of steps to be executed per episode.
            --taskName = optional parameter defining the task name.
            returns:
                --environment: The desired environment
                --task: The task according to the given file.
        """
        pass
    @abc.abstractmethod      
    def build_environment_from_task(task,limitSteps):
        """Builds the environment from previously built tasks.
           --task = The Task Object
           --limitSteps = The maximum number of steps to be executed per episode.
           returns:
               --environment: The desired environment
        """
        pass