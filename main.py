from heapq import *
import time
from gridworld import GridWorld
from agent import Agent
import matplotlib.pyplot as plt

def AstarSearch(start, end, gridworld):
  
  # Clearning 'parent' variable of nodes that are populated from previous A* runs   
  for i in range(len(gridworld.grid)):
    for j in range(len(gridworld.grid)):
      gridworld.grid[i,j].parent = None

  #Start & end nodes initialization
  start_node = gridworld.grid[start]
  start_node.fofn()
  goal_node = gridworld.grid[end]

  #Setting up fringe (Priority Queue) & a closed list
  fringe = []
  heapify(fringe)
  closed = []

  heappush(fringe, start_node)

  while len(fringe) != 0:
      
      current_node = heappop(fringe)

      closed.append(current_node)

      if current_node == goal_node:
        return ['Success', current_node.pathFinder()]

      children = current_node.generateChildren()    

      for i in children:

          i_new_g = current_node.g + 1          
          
          if i in closed:
              continue
              
          # If the node is already in the fringe    
          if i in fringe:
              k = [j for j in fringe if j == i][0]
              # If the current (x) value of the node is less than its potential new g(x) value
              if k.g < i_new_g:
                continue
              else:
                k.parent = current_node # Update the parent
                k.g = i_new_g # Update g(x)
                k.fofn() # Update f(x)
                heapify(fringe) # Heapity (resort) the fringe

          else:      
            i.parent = current_node
            i.g = i_new_g # Update g(x)
            i.fofn() # Update f(x)
            heappush(fringe, i) # Heapity (resort) the fringe

  return ['Failed', None]

def startVoyage(gridworld_real, agent_type):

  # Check to see if the given gridworld is actually solvable
  [status, path] = AstarSearch(gridworld_real.start, gridworld_real.goal, gridworld_real)

  if status == 'Failed':
    return 'Failed', None
#   else:
#     print ('Path available for the given gridworld. Path: {}'.format(path))

  # Create a empty gridworld of same dimention. This will represent the current knowledge of the agent
  gridworld_explore = GridWorld(gridworld_real.dim, gridworld_goal=gridworld_real)

  # Creating a new agent and connecting it to the empty gridworld
  agent = Agent(gridworld_explore, agent_type)
  
  # Til the agent arrives at the goal position
  while agent.position != agent.goal:

    # Run A* with the existing knowledge of the gridworld
    [status, path] = AstarSearch(agent.position, agent.goal, agent.gridworld)
    
    # Check to see if the returned path is valid comparing it with the orginal (goal) gridworld
    status = gridworld_real.tryPath(path, agent)
    if status:
      return 'Success', agent.path

def main(dim=25, p=0.25, agent_type=1, seed = 0):
  
  gridworld_real = GridWorld(dim, p, seed = seed) # Gridworld to be solved
#   gridworld_real.printGrid()

  status, path = startVoyage(gridworld_real, agent_type)
  if status == 'Success':
    return path
  else:
    return None

def plot(ntrials):

  agents = [1,2,3]
  densities = np.linspace(0, 0.33, 16)
  ntrials = ntrials

  time_data = []
  path_length_data = []
  solvability_data = []

  for agent in agents:

    time_data.append([])
    path_length_data.append([])
    solvability_data.append([])

    for p in densities:

      total_time = 0
      success_count = 0
      total_path_length = 0
      
      for seed in range(ntrials):
        start = time.time()
        path = main(dim = 25, p = p, agent_type=agent, seed = seed*2)
        end = time.time() - start
        if path != None:
          total_time += end
          success_count += 1
          total_path_length += len(path)
      
      try: avg_time = total_time/success_count
      except ZeroDivisionError: avg_time = None

      try: avg_path_length = total_path_length/success_count
      except ZeroDivisionError: avg_path_length = None

      solvability = success_count/ntrials

      time_data[agent - 1].append(avg_time)
      path_length_data[agent - 1].append(avg_path_length)      
      solvability_data[agent - 1].append(solvability)

#   fig1, ax1 = plt.subplots(2, 2)
#   fig2, ax2 = plt.subplots(2, 2)
#   for agent in agents:
#     ax1[int(np.floor((agent-1)/2)), int((agent-1)%2)].plot(densities, time_data[agent-1])
#     ax2[int(np.floor((agent-1)/2)), int((agent-1)%2)].plot(densities, path_length_data[agent-1])

#   plt.show()

  fig1, ax1 = plt.subplots(1, 3, figsize=(15, 5))
  fig2, ax2 = plt.subplots(1, 3, figsize=(15, 5))
  
  for agent in agents:

    ax1[agent-1].plot(densities, time_data[agent-1])
    ax1[agent-1].set_title('Agent {}'.format(agent))
    ax1[agent-1].set_xlabel('Density')
    ax1[agent-1].set_ylabel('Avg. Compute Time')
    ax1[agent-1].set_ylim([0,260])

    ax2[agent-1].plot(densities, path_length_data[agent-1])
    ax2[agent-1].set_title('Agent {}'.format(agent))
    ax2[agent-1].set_xlabel('Density')
    ax2[agent-1].set_ylabel('Avg. Path Length')
    ax2[agent-1].set_ylim([180,650])

    
  plt.tight_layout()  
  plt.show()
  fig1.savefig('comp_time.jpg')
  fig2.savefig('path_len.jpg')

  print (np.array(time_data))
  print (np.array(path_length_data))
#   print (np.array(solvability_data))


plot(5)
