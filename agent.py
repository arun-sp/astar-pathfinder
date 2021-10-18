class Agent:

  def __init__(self, gridworld, type):
    self.gridworld = gridworld
    self.type = type
    self.goal = self.gridworld.goal
    self.position = self.gridworld.start
    self.path = []
    self.gridworld.agent = self
    if self.type == 3:
      self.gridworld.setSensing()
    print ('New agent created...')