# -*- coding: cp1252 -*-
# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def gerarCaminho(t):
  lsEstados = []
  lsAcoes = []
  tupla = t
  while tupla[2] is not None:
    lsEstados.append(tupla[0])
    lsAcoes.append(tupla[2])
    tupla = tupla[1]
  lsAcoes.reverse()
  return lsAcoes

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from util import Stack
  
  pilha = Stack()
  explorados = []
  acoes = []
  inicial = (problem.getStartState(),None,None,0)
  "(Estado atual, Estado Pai, Ação, Custo)"
  pilha.push(inicial)

  while pilha.isEmpty() == False:
    noAtual = pilha.pop()
    explorados.append(noAtual[0])
    if problem.isGoalState(noAtual[0]):
      return gerarCaminho(noAtual)
    else:
      for item in problem.getSuccessors(noAtual[0]):
        est = item[0]
        aco = item[1]
        cus = item[2]
        if est not in explorados:
          tupla = (est,noAtual,aco,cus)
          pilha.push(tupla)
  
def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  from util import Queue

  fila = Queue()
  colorir = []
  acoes = []
  inicial = (problem.getStartState(),None,None,0)
  "Tupla formada por (Estado atual, Estado Pai, Ação, Custo)"
  fila.push(inicial)
  colorir.append(inicial)

  while fila.isEmpty() == False:
    noAtual = fila.pop()
    
    if problem.isGoalState(noAtual[0]):
      return gerarCaminho(noAtual)
    else:
      for item in problem.getSuccessors(noAtual[0]):
        est = item[0]
        aco = item[1]
        cus = item[2]
        if est not in colorir:
          colorir.append(est)
          tupla = (est,noAtual,aco,cus)
          fila.push(tupla)

def qtdAcoesAlcancar(tupla):
  pai = tupla[1]
  if pai[3] == None:
    return []
  else:
    temp = pai[3][:]
    temp.append(tupla[2])
    return temp
    
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from util import PriorityQueue
  
  fila = PriorityQueue()
  colorir = []
  inicial = (problem.getStartState(),None,None,[])
  "Tupla formada por (Estado atual, Estado Pai, Ação, Distancia)"
  fila.push(inicial,0)
  colorir.append(inicial)
  
  while fila.isEmpty() == False:
    noAtual = fila.pop()
    
    if problem.isGoalState(noAtual[0]):
      return noAtual[3]
    else:
      for item in problem.getSuccessors(noAtual[0]):
        est = item[0]
        aco = item[1]
        cus = item[2]
        if est not in colorir:
          no1 = (est,noAtual,aco)
          acoesAlcancar = qtdAcoesAlcancar(no1)
          no2 = (est,noAtual,aco,acoesAlcancar)
          fila.push(no2,problem.getCostOfActions(no2[3]))
          colorir.append(est)
  
def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from util import PriorityQueue

  fila = PriorityQueue()
  colorir = []
  inicial = (problem.getStartState(),None,None,[])
  "Tupla formada por (Estado atual, Estado Pai, Ação, Distancia)"
  fila.push(inicial,heuristic(problem.getStartState(),problem))
  colorir.append(inicial)

  while fila.isEmpty() == False:
    noAtual = fila.pop()
    if problem.isGoalState(noAtual[0]):
      return noAtual[3]
    else:
      for item in problem.getSuccessors(noAtual[0]):
        est = item[0]
        aco = item[1]
        cus = item[2]
        if est not in colorir:
          no1 = (est,noAtual,aco)
          acoesAlcancar = qtdAcoesAlcancar(no1)
          no2 = (est,noAtual,aco,acoesAlcancar)
          fila.push(no2,heuristic(est,problem) + problem.getCostOfActions(no2[3]))
          colorir.append(est)
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
