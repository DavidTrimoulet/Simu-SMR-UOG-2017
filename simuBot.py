from PotentialField import *
from pymorse import Morse
import time

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
		self.position = self.pose.get()
	#si la mission est terminée on la supprime et on retire le chemin
		if ( round( self.position['x']) == self.mission[1][0] ) and ( round(self.position['y']) == self.mission[1][1] ):
			print("mission done")
			self.mission = []
			self.path = []
	#si on est a atteint le point de départ de la mission
		if ( round( self.position['x']) == self.mission[0][0] ) and ( round(self.position['y']) == self.mission[0][1] ) :
			print("mission start")
			self.computePath( self.mission[1] )
			self.motion.publish( { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 } )
	#si on a une mission mais pas encore de chemin
		if self.mission and not self.path:
			print("new mission, going to start point")
			self.computePath( self.mission[0]  )
			self.motion.publish( { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 } )
	#si on a un chemin
		if self.path :
			print("i'm at:",round(self.position['x']),round(self.position['y']) )
			print("going to:", self.path[self.pathStep][0] , self.path[self.pathStep][0] )
			print("Mission Goal:", self.mission )
			time.sleep(1)
			self.motion.publish( { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 } )
			if (round(self.position['x']) == self.path[self.pathStep][0] ) and (round(self.position['y']) == self.path[self.pathStep][1]  ) :
				self.pathStep+=1

	def computePath(self, Goal):
		pot =  PotentialField( [ self.map['x'], self.map['y'] ] , self.map['obstacles'], 1, [round(self.position['x']),round(self.position['y'])], Goal)
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
