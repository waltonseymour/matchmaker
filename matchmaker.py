#!/usr/bin/env python

import random

class Person(object):
    '''Models an applicant'''
    def __init__(self, name, available_times, is_driver=False, size=1, is_site_leader=False):
        self.name = name
        self.available_times = available_times
        self.is_driver = is_driver
        self.size = size
        self.is_site_leader = is_site_leader

    def __repr__(self):
        return self.name

class Site(object):
    '''Models a group'''
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
        self.state = self.random_state()

    def search(self):
        '''searches the state space until a valid solution is found'''
        visited = set()
        min_conflict = self.state
        iter_count = 0
        while self.state.conflicts() > 0 and iter_count < 1000:
            iter_count += 1
            if tuple(self.state.assignments) in visited:
                #restarts if we are in an explored node
                self.state = self.random_state()
            else:
                visited.add(tuple(self.state.assignments))
                valid_neighbors = [x for x in self.state.neighbors() if tuple(x.assignments) not in visited]
                if valid_neighbors:
                    self.state = min(valid_neighbors, key= lambda x: x.conflicts())
                    min_conflict = min([self.state, min_conflict], key= lambda x: x.conflicts())

        if min_conflict.conflicts() > 0:
            print "No solution found. " +  str(min_conflict.conflicts()) + " conflicts"
        # returns a dictionary of people to site assignments
        return {self.people[index]: self.sites[assignment] for index, assignment
        in enumerate(self.state.assignments)}

    def random_state(self):
        return Node(self, [random.randint(0, len(self.sites)-1) for _ in self.people])

class Node(object):
    def __init__(self, state_space, assignments):
        # partial solution takes the form [site_index, site_index ...] with one entry for every person
        self.state_space = state_space
        self.assignments = assignments
    def __repr__(self):
        return str(self.assignments)

    def is_complete(self):
        return (None not in self.assignments)

    def neighbors(self):
        '''returns a list of all neighboring nodes'''
        ret = []
        for index, assignment in enumerate(self.assignments):
            for site_index, _ in enumerate(self.state_space.sites):
                if assignment != site_index:
                    new_state = self.assignments[:]
                    new_state[index] = site_index
                    new_state = Node(self.state_space, new_state)
                    ret.append(new_state)
        return ret

    def conflicts(self):
        '''calculates the total number of conflicts in the given solution'''
        total = 0
        site_population = [0] * len(self.state_space.sites)
        site_has_driver = [False] * len(self.state_space.sites)
        site_has_leader = [False] * len(self.state_space.sites)
        for index, assignment in enumerate(self.assignments):
            if assignment is not None:
                site_population[assignment] += self.state_space.people[index].size
                if self.state_space.people[index].is_driver and not site_has_driver[assignment]:
                    site_has_driver[assignment] = True
                if self.state_space.people[index].is_site_leader and not site_has_leader[assignment]:
                    site_has_leader[assignment] = True
                # checks if site is available to the person
                if self.state_space.sites[assignment].meeting_time not in \
                   self.state_space.people[index].available_times:
                    total += 1

        for site_index, population in enumerate(site_population):
            if population > self.state_space.sites[site_index].capacity:
                total += 1
        total += site_has_driver.count(False)
        total += site_has_leader.count(False)

        return total
