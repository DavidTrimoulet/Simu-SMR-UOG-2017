from PotentialField import *
from pymorse import Morse

class simuBot():
	"""docstring for simuBot"""
	def __init__(self, pose, motion, currentMap ):
		self.pose = pose
		self.position = []
		self.motion = motion
		self.mission = []
		self.path = []
		self.pathStep = 0
		self.map = currentMap
		self.otherBotPath = []

	def act(self):
	
		print("getPose")
		self.position = self.pose.get()
		print("pose getted")
	#si la mission est terminée on la supprime et on retire le chemin
		if ( int(self.position['x']) == self.mission[1][0] ) and ( int(self.position['x']) == self.mission[1][1] ):
			print("mission done")
			self.mission = []
			self.path = []
	#si on est a atteint le point de départ de la mission
		if ( int(self.position['x']) == self.mission[0][0] ) and ( int(self.position['x']) == self.mission[0][1] ) :
			print("mission start")
			self.computePath( self.mission[0] )
	#si on a une mission mais pas encore de chemin
		if self.mission and not self.path:
			print("new mission, going to start point")
			self.computePath( self.mission[0]  )
	#si on a un chemin
		if self.path :
			print("going to", { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 })
			if ( int(self.position['x']) == self.path[self.pathStep][0] ) and ( int(self.position['x']) == self.path[self.pathStep][1]  ) :
				self.pathStep+=1
				self.motion.publish( { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 } )

	def computePath(self, Goal):
		pot =  PotentialField( [ self.map['x'], self.map['y'] ] , self.map['obstacles'], 1, [int(self.position['x']), int(self.position['y'])], Goal)
		self.path = pot.getPath()
		self.pathStep = 0
		#on previens les autres du nouveau chemin
		#self.signify(self.path)
	
	def signify(self, Goal):
		for bot in self.map['robots'] :
			bot.notify(self.path)

	def notify(self, botPath):
		#to be continued
		print("newpath")
