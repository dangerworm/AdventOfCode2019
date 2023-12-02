def getGridValues(wires):
  # a[min, max]
  x = [0, 0]
  y = [0, 0]

  for wire in wires:
    r = 0
    u = 0
    for step in wire:
      if step[0] == 'R': r += int(step[1:])
      if step[0] == 'L': r -= int(step[1:])
      if step[0] == 'U': u += int(step[1:])
      if step[0] == 'D': u -= int(step[1:])

      if (r < x[0]): x[0] = r
      if (r > x[1]): x[1] = r
      if (u < y[0]): y[0] = u
      if (u > y[1]): y[1] = u

  # print("x max/min/range: %d/%d/%d" % (x[0], x[1], x[1]-x[0]))
  # print("y max/min/range: %d/%d/%d" % (y[0], y[1], y[1]-y[0]))
  # print()

  return [x[1]-x[0]+1, y[1]-y[0]+1, [-x[0], -y[0]]]

def initGrid(width, height):
  for y in range(height):
    grid.append(['.'] * width)

def drawWire(origin, wire, canOverlap=False):
  x, y = origin[0], origin[1]
  lastChar = ''
  for step in wire:
    direction = step[0]
    distance = int(step[1:])

    if direction == 'R' or direction == 'L':
      char = '-'
      if lastChar == '|':
        draw([x,y], '+', canOverlap)

    if direction == 'U' or direction == 'D':
      char = '|'
      if lastChar == '-':
        draw([x,y], '+', canOverlap)

    if direction == 'R':
      for i in range(x+1, x+distance):
        draw([i,y], char, canOverlap)
      x += int(distance)

    if direction == 'L': 
      for i in range(x-1, x-distance, -1):
        draw([i,y], char, canOverlap)
      x -= int(distance)

    if direction == 'U':
      for j in range(y+1, y+distance):
        draw([x,j], char, canOverlap)
      y += int(distance)

    if direction == 'D': 
      for j in range(y-1, y-distance, -1):
        draw([x,j], char, canOverlap)
      y -= int(distance)

    lastChar = char
  
  draw([x, y], char)

def draw(point, character, canOverlap=False):
  x = point[0]
  y = height - point[1] - 1

  if grid[y][x] == 'O':
    return

  if not canOverlap or grid[y][x] == '.':
    grid[y][x] = character
  else:
    grid[y][x] = 'X'
    crossovers.append([x,height-y-1])

def countSteps(origin, wire):
  x, y = origin[0], origin[1]
  numSteps = 0
  intersections = {}
  for step in wire:
    direction = step[0]
    distance = int(step[1:])

    if direction == 'R':
      for i in range(x+1, x+distance+1):
        numSteps += 1
        if intersects([i,y]):
          intersections[str([i, height-y-1])] = numSteps
      x += int(distance)

    if direction == 'L': 
      for i in range(x-1, x-distance-1, -1):
        numSteps += 1
        if intersects([i,y]):
          intersections[str([i, height-y-1])] = numSteps
      x -= int(distance)

    if direction == 'U':
      for j in range(y+1, y+distance+1):
        numSteps += 1
        if intersects([x,j]):
          intersections[str([x, height-j-1])] = numSteps
      y += int(distance)

    if direction == 'D': 
      for j in range(y-1, y-distance-1, -1):
        numSteps += 1
        if intersects([x,j]):
          intersections[str([x, height-j-1])] = numSteps
      y -= int(distance)

  return intersections

def intersects(point):
  x = point[0]
  y = height - point[1] - 1

  return grid[y][x] == 'X'

file = open('3-1.txt', 'r')
wire1, wire2 = [line.split(',') for line in file]
grid = []
crossovers = []

width, height, origin = getGridValues([wire1, wire2])
# print("width/height/origin: %d/%d/%s" % (width, height, origin))
# print()

initGrid(width, height)
draw(origin, 'O')
drawWire(origin, wire1)
drawWire(origin, wire2, canOverlap=True)

# for row in grid:
#   print(''.join(row))

crossoverDistances = []
for cross in crossovers:
    distance = abs(origin[0] - cross[0]) + abs(origin[1] - cross[1])
    crossoverDistances.append(distance)

print("Minimum Manhattan distance to crossover: %d" % (min(crossoverDistances)))

wire1Crossovers = countSteps(origin, wire1)
wire2Crossovers = countSteps(origin, wire2)

signalDistances = []
for key in wire1Crossovers.keys():
    signalDistances.append(wire1Crossovers[key] + wire2Crossovers[key])

print("Minimum signal distance to crossover: %d" % (min(signalDistances)))
