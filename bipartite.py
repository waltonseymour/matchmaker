from igraph import Graph

def assign_drivers(drivers, locations):
  '''returns a dictionary mapping drivers to locations using max bipartite matching'''
  g = Graph.Full_Bipartite(len(drivers), len(locations))

  # insert logic for deleting edges here

  matching = g.maximum_bipartite_matching()
  ret = {}
  for i, driver in enumerate(drivers):
    if matching.matching[i] != -1: 
      ret[driver] = matching.matching[i] - len(drivers)
  return ret


class matcher(object):
  def remove_edge(self, u, v):
    index = self.get_edge_index(u, v)
    self.capacity[index] = 0
      
  def get_edge_index(self, u, v):
    # needs to check if u and v are in the same partition
    if u > v:
      u, v = v, u
    elif u == v:
      # error
      raise Exception("U cannot equal V")
    return self.m * u + (v - self.n)

  def __init__(self, n, m):
    self.n = n
    self.m = m
    self.g = Graph.Full_Bipartite(n, m)

  def match(self):
    # adds start and finish
    self.g.add_vertices(2)
    # adds edges from start and finish
    start_index = self.n + self.m
    end_index = start_index + 1

    start_edges = [(start_index, i) for i in range(self.n)]
    end_edges = [(i + self.n, end_index) for i in range(self.m)]
    self.g.add_edges(start_edges + end_edges)
    
    
    # sets all edges to 1, arbitrarily sets group size to 2 for testing
    self.capacity = [1] * (self.n * self.m + self.n)
    self.capacity += [2] * self.m
    
    #insert logic for removing edges in graph here

    self.flow = self.g.maxflow(start_index, end_index, self.capacity)
    return self.flow

if __name__ == '__main__':
  # for testing
  temp = matcher(4, 2)
  print temp.match()