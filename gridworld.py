from node import Node
import numpy as np

class GridWorld():
  
  def __init__(self, dim, p=0, gridworld_goal = None):
    self.dim = dim
    self.p = p
    self.start = (0,0)
    self.goal = (dim-1, dim-1)
    self.grid = self.createGrid()
    self.gridworld_goal = gridworld_goal
    self.agent = None

  def createGrid(self):
    # grid = np.empty((self.dim, self.dim))
    grid = np.ndarray((self.dim, self.dim),dtype=np.object)
    
    np.random.seed(6)
    p_grid = np.random.choice([False, True], size=(self.dim, self.dim), p=[1-self.p, self.p])

    for i in range(self.dim):
      for j in range(self.dim):
        grid[i][j] = Node((i,j), self)
        if self.p != 0: 
          grid[i][j].block = p_grid[i][j]          

    grid[self.start].block = grid[self.goal].block = False
    return grid

  def printGrid(self):
    print (np.array([[int(j.block == True) for j in i] for i in self.grid]))

  def setSensing(self):
    for i in range(self.dim):
      for j in range(self.dim):
        self.grid[i][j].setSensing()

  def tryPath(self, path, agent):

    for index, position in enumerate(path):
      agent.gridworld.grid[position].visited = True

      if agent.gridworld.grid[position].block == None:

        if self.grid[position].block == True:         
          agent.gridworld.grid[position].block = True
          agent.position = path[index - 1]
          agent.path.extend(path[:index])
          print ('Obstruction found...')
          if agent.type == 3:
            agent.gridworld.updateSensing(agent.gridworld.grid[position])
          return False

        else: 
          agent.gridworld.grid[position].block = False
          if agent.type == 3:
              agent.gridworld.updateSensing(agent.gridworld.grid[position])
    
    agent.path.extend(path)
    return True

  def updateSensing(self, node):
    neighbours = node.getNeighbours()
    for i in neighbours:
        i.updateSensing() 
        # i.updateInference() 

#   def updateInference(self):
#     for i in range(self.dim):
#       for j in range(self.dim):
#         self.grid[i][j].updateInference()
