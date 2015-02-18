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
      raise Exception("U cannot equal V")
    return self.m * u + (v - self.n)

  def get_verticies_from_edge_index(self, index):
    u = index / self.m
    v = (index % self.m) + self.n
    return (u, v)


  def __init__(self, people, sites):
    self.people = people
    self.sites = sites
    self.n = len(self.people)
    self.m = len(self.sites)

    # edges between people and sites
    self.capacity = [x[1] for x in self.people for _ in range(self.m)]
    # edges between start and people
    self.capacity += [x[1] for x in self.people]
    # edges between sites and end
    self.capacity += [x[1] for x in self.sites]
    self.g = Graph.Full_Bipartite(self.n, self.m)

  def pretty_print(self):
    for i, edge in enumerate(self.flow.flow):
      if edge > 0 and i < self.m * self.n:
        u, v = self.get_verticies_from_edge_index(i)
        print self.people[u][0], "->", self.sites[v - self.n][0]

  def match(self):
    # adds start and finish
    self.g.add_vertices(2)
    # adds edges from start and finish
    start_index = self.n + self.m
    end_index = start_index + 1

    start_edges = [(start_index, i) for i in range(self.n)]
    end_edges = [(i + self.n, end_index) for i in range(self.m)]
    self.g.add_edges(start_edges + end_edges)

    #insert logic for removing edges in graph here

    self.flow = self.g.maxflow(start_index, end_index, self.capacity)
    return self.flow

if __name__ == '__main__':
  # for testing
  temp = matcher([("david", 1), ("max", 1), ("mary", 4)], [("school1", 4), ("school2", 3)])
  print temp.match().flow
  temp.pretty_print()
  #print temp.get_verticies_from_edge_index(7)
