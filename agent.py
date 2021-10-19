class Agent:

  def __init__(self, gridworld, type):

    # Gridworld that the agent is linked to. Initially it will be an empty grid
    self.gridworld = gridworld 
    # Type 1 - Blindfolded, Type 2 - Can see on 4 directions, Type 3 - Example Inference agent
    self.type = type # Type 1, 2, 3

    # Start and goal of the agent 
    self.goal = self.gridworld.goal
    self.position = self.gridworld.start
  
    self.path = [] # For storing path, once the agent starts moving
    self.gridworld.agent = self # Doubly linking this agent to its griworld

    # Set up sensing variables - nx, cx, bx, ex, hx for agent type 3 
    if self.type == 3:
      self.gridworld.setSensing()
