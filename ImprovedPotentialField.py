from PotentialField import PotentialField
import logging

logger = logging.getLogger("improvedTest")

class ImprovedPotentialField(PotentialField):

	def __init__(self, Map, Obstacles, RobotSize, Start, Goal, curTime, robotsPath):
		PotentialField.__init__(self, Map, Obstacles, RobotSize, Start, Goal)
		self.uRobots = []
		self.timeToStart = 3
		self.curTime = curTime
		self.timeConst = 5
		self.robotsPath = robotsPath

	def getPath(self):
		self.generateU()
		self.printMap(self.u)
		self.generateUrobots()
		path = []
		print("time:", self.curTime, "timeToStart:", self.timeToStart)
		stateTime = self.curTime + self.timeToStart
		path.append( [ self.start[0], self.start[1], stateTime ] )
		curState = self.start
		stuck = 0
		while(curState != self.goal) and stuck < 1000:
			stateTime += 1
			#on recupere la liste des noeuds adjacents
			nextStates = self.getClosestStates(curState, self.map[0], self.map[1], 1)
			#on stock le noeud courant
			nextstate = nextStates[0]
			for state in nextStates:
				if state == self.goal:
					nextstate = state
					break
				print(state, curState)
				#si state est plus petit que le prochain noeud
				if ( self.u[ state[1] ][ state[0] ] + self.getTimeValue(state, stateTime) )  < self.u[ nextstate[1] ][ nextstate[0] ] :
					nextstate = state
			path.append( [ nextstate[1], nextstate[0] , stateTime ] )
			if stuck > 100:
				stuck = 0
				path = []
				print("stuck")
				break;
			curState = nextstate
			stuck += 1
		print("Improved path", path)
		return path

	def generateUrobots(self) :
		for i in range(self.map[0]):
			line = []
			for j in range(self.map[1]):
				line.append(0)
			self.uRobots.append(line)
		print("Other Robot Path",self.robotsPath)
		for coorAtTime in self.robotsPath :
			self.uRobots[ coorAtTime[1] ][ coorAtTime[0] ] = coorAtTime[2]

	def getTimeValue(self, state, time) :
		timeval = ( - pow(self.uRobots[ state[1] ][ state[0] ] - time , 2) + self.timeConst )
		timeval = 0 if timeval < 0 else timeval 
		return timeval
