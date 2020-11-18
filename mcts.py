#!/usr/bin/env python2
import os
import gym
import sys
import random
import itertools
import time as asd
from time import time
from copy import copy
from math import sqrt, log
from main import Game

def moving_average(v, n):
    n = min(len(v), n)
    ret = [.0]*(len(v)-n+1)
    ret[0] = float(sum(v[:n]))/n
    for i in range(len(v)-n):
        ret[i+1] = ret[i] + float(v[n+i] - v[i])/n
    return ret


def ucb(node):
    expl = sqrt(2)
    return node.value / node.visits + expl*sqrt(log(node.parent.visits)/node.visits)



class Node:
    def __init__(self, parent, action,name):
        self.parent = parent
        self.action = action
        self.children = []
        self.explored_children = 0
        self.visits = 0
        self.value = 0
        self.name = name


class Runner:
    def __init__(self,loops, max_depth, playouts):

        self.loops = loops
        self.max_depth = max_depth
        self.playouts = playouts

    def print_stats(self, loop, score, avg_time):
        sys.stdout.write('\r%3d   score:%10.3f   avg_time:%4.1f s' % (loop, score, avg_time))
        sys.stdout.flush()

    def run(self):
        best_rewards = []
        start_time = time()
        env = Game(False)
        self.actions = env.space_sate
        #print(self.max_depth)
        noden = 0
        for loop in range(self.loops):
            env.new()
            root = Node(None, None,"dad")

            best_actions = []
            #best_reward = float("-inf")
            
            for ite in range(self.playouts):
                env.new()
                state = copy(env)
               
                sum_reward = 0
                node = root
                running = True
                #actions = []
                # selection
                while node.children:
                    if node.explored_children < len(node.children):
                        child = node.children[node.explored_children]
                        node.explored_children += 1
                        node = child
                        #print(child.name, ", action : ",child.action)
                        #print("next brother")
                    else:
                        node = max(node.children, key=ucb)
                        #print("doing ucb")
                    reward, running = state.step(node.action)
                    sum_reward += reward
                    #actions.append(node.action)
                print(running)
                # expansion
                if running:
                    noden +=1
                    node.children = [Node(node, a,"son"+ str(noden)) for a in self.actions]
                    random.shuffle(node.children)
                    node = node.children[0]
                    reward, running = state.step(node.action)
                    #print(len(node.children))

                # playout
                while running:
                    #asd.sleep(0.1)
                    action = random.choice(self.actions)
                    reward, running = state.step(action)
                    #print(info["life"])

                    #state.render()

                    sum_reward += reward
                    #actions.append(action)

                    #if len(actions) > self.max_depth:
                    #   print("max depth reached")
                    #   sum_reward -= 100
                    #   break
                
                print("playout ", ite," -> ", sum_reward)
                #asd.sleep(10)
                # remember best
                #if best_reward < sum_reward:
                #    best_reward = sum_reward
                #    best_actions = actions

                # backpropagate
                while node:
                    #if node.name=="dad":
                        #print("Backtracking done")
                    node.visits += 1
                    node.value += sum_reward
                    node = node.parent
                    
            


            sum_reward = 0
            for action in best_actions:
                reward, running = env.step(action)
                sum_reward += reward
                if not running:
                    break

            best_rewards.append(sum_reward)
            score = max(moving_average(best_rewards, 100))
            avg_time = (time()-start_time)/(loop+1)
            self.print_stats(loop+1, score, avg_time)

        print


def main():
    Runner(loops=100, playouts=4000, max_depth=100).run()

if __name__ == "__main__":
    main()
