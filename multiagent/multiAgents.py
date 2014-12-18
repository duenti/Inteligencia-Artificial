# -*- coding: cp1252 -*-
# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodList = newFood.asList()
    
    "*** YOUR CODE HERE ***"
    h = 0

    distFantasmas = []
    for fant in newGhostStates:
      distFantasmas += [manhattanDistance(fant.getPosition(),newPos)]

    distComidas = []
    for f in foodList:
      distComidas += [manhattanDistance(newPos,f)]

    if len(distComidas) > 0:
      h = (min(distFantasmas)/(min(distComidas)))

    h += successorGameState.getScore()

    return h

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

  def isFinalState(self,state,depth):
    if depth == (self.depth*self.agentCount) or state.isWin() or state.isLose():
      return True
    else:
      return False

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def minimax(self, state, agent, depth):
    pontuacao = 0

    if agent == self.agentCount:
      agent = self.index

    if self.isFinalState(state,depth):
      pontuacao = self.evaluationFunction(state)
    elif agent == self.index:#PONTUAÇÃO MAX
      pontuacao = -999999999
      acoes = state.getLegalActions(agent)
      acoes.remove(Directions.STOP)#TESTAR
      for a in acoes:
        pontuacao = max(pontuacao, self.minimax(state.generateSuccessor(agent,a),agent+1,depth+1))
    else:#PONTUAÇÃO MIN
      pontuacao = 999999999
      for a in state.getLegalActions(agent):
        pontuacao = min(pontuacao, self.minimax(state.generateSuccessor(agent,a),agent+1,depth+1))

    return pontuacao    
  
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    self.agentCount = gameState.getNumAgents()
    depth = 0
    agent = self.index #0 = pacman, >0 é fantasma
    actionDic = {}
    actions = gameState.getLegalActions(agent)
    actions.remove(Directions.STOP)
    for a in actions:
      pontuacao = self.minimax(gameState.generateSuccessor(agent,a),agent+1,depth+1)
      actionDic[pontuacao] = a

    return actionDic[max(actionDic)]
      
    

    
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def alfabeta(self,state,agent,depth,action,alfa,beta):
    pontuacao = []
    if agent == self.agentCount:
      agent = self.index

    if self.isFinalState(state,depth):
      pontuacao = [self.evaluationFunction(state),action]
      #print "TTTTTTTTTTTTTTTTT",pontuacao
    elif agent == self.index:#MAX
      pontuacao = [-999999999, Directions.STOP]
      acoes = state.getLegalActions(agent)
      acoes.remove(Directions.STOP)
      for a in acoes:
        temp = self.alfabeta(state.generateSuccessor(agent,a),agent+1,depth+1,a,alfa,beta)
        temp[1] = a
        pontuacao = max(pontuacao,temp)
        if pontuacao[0] >= beta:
          return pontuacao
        alfa = max(alfa,pontuacao[0])
      return pontuacao
    else:#MIN
      pontuacao = [999999999, Directions.STOP]
      for a in state.getLegalActions(agent):
        temp = self.alfabeta(state.generateSuccessor(agent,a),agent+1,depth+1,a,alfa,beta)
        temp[1] = a
        pontuacao = min(pontuacao,temp)
        if pontuacao[0] <= alfa:
          return pontuacao
        beta = min(beta,pontuacao[0])
      return pontuacao
    return pontuacao

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    self.agentCount = gameState.getNumAgents()
    depth = 0
    agent = self.index
    alfa = -999999999
    beta = 999999999
    action = Directions.STOP
    pontuacao = self.alfabeta(gameState,agent,depth,action,alfa,beta)
    return pontuacao[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return self.expectimax(gameState,1,0)

  def expectimax(self,state,depth,agent):
    if depth > self.depth or state.isWin() or state.isLose():
      return self.evaluationFunction(state)

    moves = []

    for a in state.getLegalActions(agent):
      if a != "Stop":
        moves.append(a)

    nextAgent = agent + 1
    nextDepth = depth

    if nextAgent >= state.getNumAgents():
      nextAgent = 0
      nextDepth += 1
    
    resultados = []
    for a in moves:
      resultados.append(self.expectimax(state.generateSuccessor(agent,a),nextDepth,nextAgent))

    if agent == 0 and depth == 1:
      bestMove = max(resultados)

      indices = []
      for i in range(len(resultados)):
        if(resultados[i] == bestMove):
          indices.append(i)
      indice = random.choice(indices)
      return moves[indice]

    if agent == 0:
      bestMove = max(resultados)
      return bestMove
    else:
      #Vez do fantasma, retorna uma média esperada
      bestMove = sum(resultados)/len(resultados)
      return bestMove

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  #Inicialização das váriaveis
  lab = currentGameState.getPacmanPosition() #Posições do labirinto
  comida = currentGameState.getFood() #Posições de comida
  estadoFantasmas = currentGameState.getGhostStates()
  listaComida = comida.asList() #lista de todos as posições onde há comida

  h = 0

  #Calcula a distância de manhattan para posição de cada fantasma
  distanciaFantasmas = []
  for e in estadoFantasmas:
    distanciaFantasmas.append(manhattanDistance(e.getPosition(),lab))

  #Calcula as distâncias de manhattan para cada comida
  distanciaComidas = []
  for c in listaComida:
    distanciaComidas.append(manhattanDistance(lab,c))

  #Calcula a posição da comida mais perto
  menorDistComida = 0
  if len(distanciaComidas) > 0:
    menorDistComida = min(distanciaComidas)

  if (menorDistComida == 0):
    h = currentGameState.getScore()
  else:
    h = (min(distanciaFantasmas)/(menorDistComida)) + currentGameState.getScore()

  return h



    
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

