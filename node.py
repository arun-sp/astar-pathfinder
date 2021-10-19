class Node:
        
    def __init__(self, position, gridworld):
        self.position = position # Position as a tuple (a, b)
        self.gridworld = gridworld # Gridworld the node belongs to
        self.block = None # Can be None (unconfimed or hidden), True (blocked) or False (unblocked)
        self.parent = None # Parent node
        self.visited = False # Can take on 2 values - True (visited) or False (not visited)
        self.g = 0 # g(x)
        self.h = self.hofn() # h(x)
        
    def hofn(self):
        return self.manhattan_distance()

    def manhattan_distance(self):
        # Manhattan distance it's the best performing one
        return abs(self.gridworld.goal[0] - self.position[0]) + abs(self.gridworld.goal[1] - self.position[1])

    def fofn(self):
        self.f = self.g + self.h # f(x) = g(x) + h(x)

    # For comparing two nodes
    def __lt__(self, other): 
      return self.f < other.f
    def __eq__(self, other):
      return self.position == other.position

     # For A*. Children will be the 4 nodes in N, S, E, W directions. 
    # Only if they are hidden/unconfirmed or unblocked
    def generateChildren(self):      
      self.children = []
      for i in [(self.position[0]-1, self.position[1]),
                (self.position[0]+1, self.position[1]),
                (self.position[0], self.position[1]-1),
                (self.position[0], self.position[1]+1)]:
          if i[0] >= 0 and i[1] >= 0 and i[0] < self.gridworld.dim and i[1] < self.gridworld.dim:
              if self.gridworld.grid[i].block != True: # Check if it's confirmed to be blocked
                  self.children.append(self.gridworld.grid[i])
      return self.children    

    # Takes a node and follows the its parent in chain to get the path as list of positions
    def pathFinder(self):

      path = [self.position]
      parent = self.parent
        
      while parent is not None:
        path.append(parent.position)
        parent = parent.parent
        
      return path[::-1]

    # For inferencing agent. 
    # Neighbours will be the nodes in the 8 sorrounding directions 
    def getNeighbours(self):
      neighbours = []
      for i in [-1,0,1]:
        for j in [-1,0,1]:
          if (i != 0 or j != 0):
            neighbour = (self.position[0] + i, self.position[1] + j)
            if neighbour[0] >= 0 and neighbour[1] >= 0 and neighbour[0] < self.gridworld.dim and neighbour[1] < self.gridworld.dim:
              neighbours.append(self.gridworld.grid[neighbour])
      return neighbours
     
    # Initialize sensing variables nx, cx, bx, ex, hx for the inferencing agent
    def setSensing(self):
      self.neighbours = self.getNeighbours()
      self.nx = len(self.neighbours)
      # self.visited = False
      self.cx = None
      self.bx = None
      self.ex = None
      self.hx = None

    def getC(self): # Count of neighbours that are sensed to be blocked
      c = 0
      for i in self.neighbours:
        if self.gridworld.gridworld_goal.grid[i.position].block == True:
          c += 1
      return c

    def getBEH(self):  
      b = e = h = 0

      for i in self.neighbours:
        if i.block == True: b += 1 # Count of neighbours that are confirmed to be blocked
        elif i.block == False: e += 1 # Count of neighbours that are confirmed to be unblocked
        elif i.block == None: h += 1 # Count of neighbours that are still hidden/unconfirmed
      return b, e, h      

    def updateSensing(self): # Update sensing variables on every step

      self.cx = self.getC()
      self.bx, self.ex, self.hx = self.getBEH()
    
    def updateInference(self):

      updatedNodes = [] # To keep track of nodes that are found to be blocked/unblocked using Inference Engine
      if self.hx == 0: # Nothing more to solve
        pass
      elif self.cx == self.bx: # All remaining nodes are unblocked 
        for i in self.neighbours:
          if i.block == None: 
            i.block = False
            updatedNodes.append(i)

      elif (self.nx - self.cx) == self.ex:# All remaining notes are blocked
        for i in self.neighbours:
          if i.block == None: 
            i.block = True
            updatedNodes.append(i)

      return updatedNodes
