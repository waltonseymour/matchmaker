from constraint import *
import bipartite

def invert(dict_):
  inv_map = {}
  for k, v in dict_.iteritems():
    inv_map[v] = inv_map.get(v, [])
    inv_map[v].append(k)
  return inv_map

def valid(sol):
  inv_map = invert(sol)
  if all(any(members in driver_set for members in inv_map[group]) for group in inv_map.keys()):
    return True
  else:
    return False

if __name__ == '__main__':
  people = ["person" + str(x) for x in range(100)]
  drivers = ["person" + str(x) for x in range(50)]
  driver_set = set(drivers)
  locations = ["school" + str(x) for x in range(50)]