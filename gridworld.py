from node import Node
import numpy as np

class GridWorld():
  
  def __init__(self, dim, p=None, gridworld_goal = None, seed = 0):

    self.dim = dim 
    self.p = p # Block density of the grid
    self.seed = seed
    self.start = (0,0)
    self.goal = (dim-1, dim-1)
    self.grid = self.createGrid()
    self.gridworld_goal = gridworld_goal # Goal grid that we want to solve
    self.agent = None

  def createGrid(self):
    # grid = np.empty((self.dim, self.dim))
    grid = np.ndarray((self.dim, self.dim),dtype=np.object) # Dim x Dim grid to be filled with Node objects
    
    for i in range(self.dim):
      for j in range(self.dim):
        grid[i][j] = Node((i,j), self)

    if self.p != None:         
      np.random.seed(self.seed)
      # Dim x Dim grid filled with True (blocked) or False (unblocked) based on p
      p_grid = np.random.choice([False, True], size=(self.dim, self.dim), p=[1-self.p, self.p])  
      for i in range(self.dim):
        for j in range(self.dim): 
          grid[i][j].block = p_grid[i][j]      

    grid[self.start].block = grid[self.goal].block = False # Making sure start and goal node are unblocked
    return grid

  def printGrid(self):
    print (np.array([[int(j.block == True) for j in i] for i in self.grid]))

  def setSensing(self):
    for i in range(self.dim):
      for j in range(self.dim):
        # Set up sensing variables on every node in the grid
        self.grid[i][j].setSensing() 

  def tryPath(self, path, agent): # Check to see if a path returned by A* is valid

    for index, position in enumerate(path):

      agent.gridworld.grid[position].visited = True # Set the node to be visited

      if self.grid[position].block == True: # If the respective position in goal grid is blocked
        agent.gridworld.grid[position].block = True # Set the same position in the agent grid to be blocked
        agent.position = path[index - 1] # Take the path until the current index
        agent.path.extend(path[:index]) # Add it to the agent path

        if agent.type == 3: 
          # Update sensing variables of the neighbours of the current node
          agent.gridworld.updateSensing(agent.gridworld.grid[position])

          return False

      else: # If the respective position in goal grid is unblocked
        agent.gridworld.grid[position].block = False # Set the same position in the agent grid to be blocked

        if agent.type == 2:
          # Update the 'block' status of the 4 neighbours as this agent is able to 'see'
          for i in agent.gridworld.grid[position].generateChildren():
            i.block = self.grid[i.position].block
            
        if agent.type == 3:
          # Update sensing variables of the neighbours of the current node
          agent.gridworld.updateSensing(agent.gridworld.grid[position])

    # Extend the path
    agent.path.extend(path)
    return True

  # Call the necessary Sensing & Inferencing functions on necessary nodes in loop
  def updateSensing(self, node):
    
    # List to keep track of nodes whose 'block' value was confirmed
    # in order to update sensing variables of its neighbours and then run inference engine on them
    changed_nodes = [node] 
    
    while len(changed_nodes) > 0:
      n = changed_nodes.pop()
      neighbours = n.getNeighbours()
      for i in neighbours:
        i.updateSensing() # Update sensing variables
      for i in neighbours:  
        # Run inference engine on them and add any nodes whose 'block' value gets confirmed due to it
        changed_nodes.extend(i.updateInference())
