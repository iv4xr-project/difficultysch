# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:53:45 2020

@author: mlopes
"""
import numpy as np
import pickle

from search import *


def state2x(state):
    x = [0,0]
    x[1] = state%10
    x[0] = int(state/10)
    
    return x

def x2state(x):
    return x[0]*10+x[1]
"""
class MySearchProblem(Problem):
    
    #A problem which is solved by an agent executing
    #actions, rather than by just computation.
    #Carried in a deterministic and a fully observable environment.

    def __init__(self, initial, goal, actions):
        super().__init__(initial, goal, actions)

    def actions(self, state):
        return self.actions

    def output(self, state, action):
        #print("output",state,action)
        x = state
        y = [0,0]
        if action == 2:
            y[1] = x[1] + 1
            y[0] = x[0]
        else:
            y[0] = x[0] + action
            if x[1]>=1:
                y[1] = x[1] - 1        
        
        return y

    def h(self, state):
        x = state
        #Returns least possible cost to reach a goal for the given state.
        r = (abs(x[1])+abs(x[0]))/2

        return r

    def c(self, s, a, s1):
        #Returns a cost estimate for an agent to move from state 's' to state 's1'.
        return 1

    def update_state(self, percept):
        raise NotImplementedError

    def goal_test(self, state):
        x = state
        if (x[1]==0 and x[0]==0) or x[0]>10:
            return True
        return False
 """ 
        
class RTTStarAgent:

    def __init__(self, start, goal):
        self.problem = problem  
        self.result = {}      
        self.H = {}

    def loadfromfile(self, filename):
        with open(filename, 'rb') as fid:
            self.result,self.H = pickle.load(fid)
            
    def savetofile(self, filename):
        with open(filename, 'wb') as fid:
            pickle.dump([self.result,self.H], fid)            
    

    def update(self, os, a, ons):
        s = hash(tuple(os))
                
        self.result[(s, a)] = ons
        self.H[s] = min(self.LRTA_cost(os, b, self.result[(s, b)],self.H) for b in self.problem.actions)
        
    def __call__(self, os, noise = 0):  # as of now s1 is a state rather than a percept
        

    



if __name__=="__main__":        
