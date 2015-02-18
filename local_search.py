#!/usr/bin/env python

import random

class Person(object):
  def __init__(self, name, available_times, is_driver=False):
    self.name = name
    self.available_times = available_times
    self.is_driver = is_driver
  
  def __repr__(self):
    return self.name

class Site(object):
  def __init__(self, name, meeting_time, capacity):
    self.name = name
    self.meeting_time = meeting_time
    self.capacity = capacity

  def __repr__(self):
    return self.name

class StateSpace(object):
  def __init__(self, people, sites):
    self.people = people
    self.sites = sites
    self.inial_state = Node(self, [random.randint(0, len(self.sites)-1) for x in self.people])
  
  def search(self):
    '''searches the state space until a valid solution is found'''
    state = self.inial_state
    visited = set()
    while state.conflicts() > 0:
      if tuple(state.partial_solution) in visited:
        print "RESTARTING"
        state = Node(self, [random.randint(0, len(self.sites)-1) for x in self.people])
      else:
        visited.add(tuple(state.partial_solution))
        valid_neighbors = [x for x in state.neighbors() if tuple(x.partial_solution) not in visited]
        state = min(valid_neighbors, key= lambda x: x.conflicts())

    for index, assignment in enumerate(state.partial_solution):
      print self.people[index].name + "->" + self.sites[assignment].name


class Node(StateSpace):
  def __init__(self, parent, partial_solution):
    # partial solution takes the form [site_index, site_index ...] with one entry for ever person
    self.parent = parent
    self.partial_solution = partial_solution

  def __repr__(self):
    return str(self.partial_solution)

  def is_complete(self):
    return (None not in self.partial_solution)

  def neighbors(self):
    ret = []
    for index, assignment in enumerate(self.partial_solution):
      for site_index, _ in enumerate(self.parent.sites):
        if assignment != site_index:
          new_state = self.partial_solution[:]
          new_state[index] = site_index
          new_state = Node(self.parent, new_state)
          ret.append(new_state)
    return ret

  def conflicts(self):
    '''calculates the total number of conflicts given in the partial solution'''
    total = 0
    site_population = {}
    for index, assignment in enumerate(self.partial_solution):
      if assignment is not None:
        # counts number of people per site
        if assignment in site_population:
          site_population[assignment] += 1
        else:
          site_population[assignment] = 1

        # checks if site is available to the person
        if self.parent.sites[assignment].meeting_time not in self.parent.people[index].available_times:
          total += 1

    for site_index, population in site_population.iteritems():
      if population > self.parent.sites[site_index].capacity:
        total += 1
    return total

if __name__ == '__main__':
  people = [Person("person1", [1, 2, 3], True),
            Person("person2", [1]),
            Person("person3", [1, 2, 3], True),
            Person("person4", [2]),
            Person("person5", [1, 3]),
            Person("person6", [1, 2]),
            Person("person7", [3], True),
            Person("person8", [1, 2, 3]),
            Person("person9", [1]),
            Person("person10", [3])]
  
  sites = [Site("site1", 1, 3), Site("site2", 2, 3), Site("site3", 3, 4)]

  temp = StateSpace(people, sites)
  temp.search()
  