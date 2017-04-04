import math

class PotentialField():
	def __init__(self, Map, Obstacles, RobotSize, Start, Goal):
		self.map = Map
		self.obstacles = Obstacles
		self.robotSize = RobotSize
		self.start = Start
		self.goal = Goal
		self.ur = []
		self.ua = []
		self.u = []
		self.attractionConst = 1
		self.repulseConst = 10

	def printMap(self,map):
		for line in map:
			line = [round(x) for x in line]
			print(line)

	def generateRepulse(self):
		for i in range(self.map[0]):
			line = []
			for j in range(self.map[1]):
				line.append(0)
			self.ur.append(line)
		#print(self.ur)
		for obstacle in self.obstacles:
			closests = self.getClosestStates(obstacle, self.map[0], self.map[1], self.robotSize)
			for neighbour in closests :
				self.ur[neighbour[0]][neighbour[1]] = self.repulseConst - self.getDistance(neighbour, obstacle)

	def generateAttraction(self):
		for y in range( self.map[1] ):
			line = []
			for x in range( self.map[0] ):
				line.append( (self.getDistance( [x,y] , self.goal ) / (self.map[0] * self.map[1]) ) ) 
			self.ua.append(line)

	def generateU(self):
		self.generateAttraction()
		self.generateRepulse()
		for y in range(self.map[1]):
			line = []
			for x in range(self.map[0]):
				line.append( self.ua[y][x] + self.ur[y][x] )
			self.u.append(line)

	def getPath(self):
		self.generateU()
		#self.printMap(self.u)
		path = []
		path.append(self.start)
		curState = self.start
		stuck = 0
		while(curState != self.goal) :
			#on recupere la liste des noeuds adjacents
			nextStates = self.getClosestStates(curState, self.map[0], self.map[1], 1)
			#on stock le noeud courant
			nextstate = nextStates[0]
			for state in nextStates:
				if state == self.goal:
					nextstate = state
					break
				#print(state, curState)
				#si state est plus petit que le prochain noeud
				if self.u[ state[1] ][ state[0] ] < self.u[ nextstate[1] ][ nextstate[0] ] :
					nextstate = state
			path.append(nextstate)
			if stuck > 100:
				stuck = 0
				path = []
				#print("stuck")
				break;
			curState = nextstate
			stuck += 1
		#print("path", path)
		return path

	def getDistance(self, a, b):
		return math.sqrt( math.pow (a[0] - b[0] ,2) + math.pow (a[1] - b[1] , 2) )

	def getClosestStates(self, curState, xMax, yMax, d ):
		states = []
		minX = curState[0] - d if curState[0] - d > 0  else 0
		minY = curState[1] - d if curState[1] - d > 0  else 0
		maxX = curState[0] + d if curState[0] + d < xMax  else xMax-1
		maxY = curState[1] + d if curState[1] + d < yMax  else yMax-1
		#print("CurrentState:", curState)
		#print("bornes", minX, maxX, minY, maxY)
		for x in range(minX, maxX+1):
			for y in range(minY, maxY+1):
				states.append([x, y])
		
		#print("states = ", states)
		#print("closest states:", states)
		return states
