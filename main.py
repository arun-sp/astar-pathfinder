from heapq import *
import time
from gridworld import GridWorld
from agent import Agent

def AstarSearch(start, end, gridworld):

  print ('AstarSearch begins... Start: {} & end: {}'.format(start, end))
  
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
  print ('AstarSearch initialization done...')
  while len(fringe) != 0:
      
      current_node = heappop(fringe)

      closed.append(current_node)

      if current_node == goal_node:
        print ('Goal node found...')
        # return ['Success', pathFinder(current_node)]
        return ['Success', current_node.pathFinder()]

      children = current_node.generateChildren()    
      # children = generateChildren(current_node)

      for i in children:

          i_new_g = current_node.g + 1          
          # i.g = current_node.g + 1
          # i.fofn()

          # if i.position in [j.position for j in closed]:
          if i in closed:
              continue
          # if i.position in [j.position for j in fringe]:
          if i in fringe:
              # k = [k for k in fringe if k.position == i.position][0]
              k = [j for j in fringe if j == i][0]
              if k.g < i_new_g:
                continue
              else:
                k.parent = current_node
                k.g = i_new_g
                k.fofn()
                heapify(fringe)

          else:      
            i.parent = current_node
            i.g = i_new_g
            i.fofn()
            heappush(fringe, i)

  print ('Path not available...')
  return ['Failed', None]

def startVoyage(gridworld_real, agent_type):

  print ('startVoyage begins...')

  [status, path] = AstarSearch(gridworld_real.start, gridworld_real.goal, gridworld_real)

  if status == 'Failed':
    print ('No actual path for the given gridworld. Try a new gridworld.')
    return 'Failed', None
  else:
    print ('Path available for the given gridworld. Path: {}'.format(path))

  gridworld_explore = GridWorld(gridworld_real.dim, gridworld_goal=gridworld_real)
  print ('Gridworld copy created')

  agent = Agent(gridworld_explore, agent_type)

  while agent.position != agent.goal:

    print ('Agent AstarSearch begins')
    [status, path] = AstarSearch(agent.position, agent.goal, agent.gridworld)

    status = gridworld_real.tryPath(path, agent)
    if status:
      return 'Success', agent.path


def main(dim=50, p=0.25, agent_type=1):
  
  print ('Program starts...')
  print ('Grid Dimension: {}x{} and p: {}'.format(dim, dim, p))

  gridworld_real = GridWorld(dim, p)
  gridworld_real.printGrid()

  status, path = startVoyage(gridworld_real, agent_type)
  print (len(path))
  print (path)

start = time.time()
# for i in range(5):
main(agent_type=3)
print (time.time()-start)

# time1 = time.time()
# main(agent_type=1)
# time2 = time.time()
# main(agent_type=3)
# time3 = time.time()