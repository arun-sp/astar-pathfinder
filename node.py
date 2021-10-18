import math

class Node:
        
    def __init__(self, position, gridworld, parent = None, block=None):
        self.position = position
        self.gridworld = gridworld
        self.block = block
        self.parent = parent
        self.visited = False
        self.g = 0
        self.h = self.hofn()

    def hofn(self):
        return self.manhattan_distance()

    def manhattan_distance(self):
        return abs(self.gridworld.goal[0] - self.position[0]) + abs(self.gridworld.goal[1] - self.position[1])

    def fofn(self):
        self.f = self.g + self.h

    def __lt__(self, other):
      return self.f < other.f

    def __eq__(self, other):
      return self.position == other.position

    def generateChildren(self):
      self.children = []
      for i in [(self.position[0]-1, self.position[1]),
                (self.position[0]+1, self.position[1]),
                (self.position[0], self.position[1]-1),
                (self.position[0], self.position[1]+1)]:
          if i[0] >= 0 and i[1] >= 0 and i[0] < self.gridworld.dim and i[1] < self.gridworld.dim:
              if self.gridworld.grid[i].block != True:
                  self.children.append(self.gridworld.grid[i])
      return self.children
    
    def pathFinder(self):
      print ('pathFinder begins...')
      path = [self.position]
      parent = self.parent
      while parent is not None:
        path.append(parent.position)
        parent = parent.parent
      print ('Path estimated: {}'.format(path[::-1]))
      print ('pathFinder ends...')
      return path[::-1]

    def getNeighbours(self):
      neighbours = []
      for i in [-1,0,1]:
        for j in [-1,0,1]:
          if (i != 0 or j != 0):
            neighbour = (self.position[0] + i, self.position[1] + j)
            if neighbour[0] >= 0 and neighbour[1] >= 0 and neighbour[0] < self.gridworld.dim and neighbour[1] < self.gridworld.dim:
              neighbours.append(self.gridworld.grid[neighbour])
      return neighbours
     
    def setSensing(self):
      self.neighbours = self.getNeighbours()
      self.nx = len(self.neighbours)
      # self.visited = False
      self.cx = None
      self.bx = None
      self.ex = None
      self.hx = None

    def getC(self):
      c = 0
      for i in self.neighbours:
        if self.gridworld.gridworld_goal.grid[i.position].block == True:
          c += 1
      return c

    def getBEH(self):  
      b = e = h = 0

      for i in self.neighbours:
        if i.block == True: b += 1
        elif i.block == False: e += 1
        elif i.block == None: h += 1
      return b, e, h   

    def updateSensing(self):
      # self.visited = True
      self.cx = self.getC()
      self.bx, self.ex, self.hx = self.getBEH()
      # c = self.getC()
      # b, e, h = self.getBEH()

      # if c == self.cx and b == self.bx and e == self.ex and h == self.hx:   
      #   return
      # else: 

      #   self.cx = c
      #   self.bx, self.ex, self.hx = b, e, h
      self.updateInference()
    
    def updateInference(self):
      print ('Inference was called')
      if self.hx == 0:
        return
      elif self.cx == self.bx:
        for i in self.neighbours:
          if i.block == None: 
            i.block = False
            # self.gridworld.updateSensing(i)
      elif (self.nx - self.cx) == self.ex:
        for i in self.neighbours:
          if i.block == None: 
            i.block = True
            # self.gridworld.updateSensing(i)
      else:
        return
      # print ('Inferencing was done...')
    