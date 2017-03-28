import math
from pprint import pprint

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
		self.attractionConst = 0.01
		self.repulseConst = 10


	def generateRepulse(self):
		for i in range(self.map[1]):
			line = []
			for j in range(self.map[0]):
				line.append(0)
			self.ur.append(line)
		#print(self.ur)
		for obstacle in self.obstacles:
			closests = self.getClosestStates(obstacle, self.map[0], self.map[1], self.robotSize)
			for neighbour in closests :
				self.ur[neighbour[1]][neighbour[0]] = self.repulseConst - self.getDistance(neighbour, obstacle)


	def generateAttraction(self):
		for i in range( self.map[1] ):
			line = []
			for j in range( self.map[0] ):
				line.append(self.getDistance( [j,i] , self.goal ))
			self.ua.append(line)

	def generateU(self):
		self.generateAttraction()
		self.generateRepulse()
		for i in range(self.map[1]):
			line = []
			for j in range(self.map[0]):
				line.append( self.ua[i][j] + self.ur[i][j] )
			self.u.append(line)

	def getPath(self):
		#print(self.u)
		self.generateU()
		#print(self.u)
		path = []
		path.append(self.start)
		curState = self.start
		stuck = 1
		while(curState != self.goal) and stuck :
			nextStates = self.getClosestStates(curState, self.map[0], self.map[1], 1)
			nextstate = curState
			for state in nextStates:
				#print(state, curState)
				if self.u[ state[1] ][ state[0] ] < self.u[ curState[1] ][ curState[0] ] :
					nextstate = state
			path.append(state)
			if nextstate == curState:
				stuck = 0
				break;
			curState = nextstate
		return path


	def getDistance(self, a, b):
		return math.sqrt( math.pow (a[0] - b[0] ,2) + math.pow (a[1] - b[1] , 2) )

#
	def getClosestStates(self, obstacle, xMax, yMax, d ):
		states = []
		minX = obstacle[0] - d if obstacle[0] - d > 0  else 0
		minY = obstacle[1] - d if obstacle[1] - d > 0  else 0
		maxX = obstacle[0] + d if obstacle[0] + d < xMax  else xMax-1
		maxY = obstacle[1] + d if obstacle[1] + d < yMax  else yMax-1
		print(minX, maxX, minY, maxY)
		for i in range(minX, maxX+1):
			for j in range(minY, maxY+1):
				states.append([i, j])

		print("states = ", states)
		return states
