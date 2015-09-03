# Pseudo-code from https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
# Left side of river: boat, # missionaries, # cannibals
BOAT = 0
MISSIONARIES = 1
CANNIBALS = 2

start = [1, 3, 3]
goal = [0, 0, 0]

configurations = [
  [1, 0, 1],
  [1, 0, 2],
  [1, 1, 0],
  [1, 1, 1],
  [1, 2, 0]]

def isValid(node):
  m = node[MISSIONARIES]
  c = node[CANNIBALS]
  return c >= 0 and c <= 3 and m <= 3 and m >= 0 and (m == c or m == 0 or m == 3)

def getChildren(node):
  children = []
  op = -1 if node[BOAT] else 1

  for config in configurations:
    diff = [x * op for x in config]
    child = [sum(x) for x in zip(node, diff)]
    if isValid(child):
      children.append(child)
    
  return children

def DLS(node, depth):
  if depth == 0 and node == goal:
    return [node]
  elif depth > 0:
    for child in getChildren(node):
      result = DLS(child, depth - 1)
      if result:
        path = [node]
        path.extend(result)
        return path
  return None

def IDDFS(root):
  depth = 0
  while True:
    result = DLS(root, depth)
    if result:
      return result
    depth += 1

print(IDDFS(start))
