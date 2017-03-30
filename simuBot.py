from PotentialField import *
from pymorse import Morse
import time

class simuBot():
	"""docstring for simuBot"""
	def __init__(self, pose, motion, currentMap, isMorse ):
		self.pose = pose
		self.position = []
		self.motion = motion
		self.mission = []
		self.path = []
		self.pathStep = 0
		self.map = currentMap
		self.otherBotPath = []
		self.isMorse = isMorse
		self.success = 0
		self.fail = 0
		self.noPath = 0

	def act(self):
		self.position = self.getPose()
	#si la mission est terminée on la supprime et on retire le chemin
		if self.mission :
			print( "position :", self.position, "mission", self.mission)
		#si on a atteient l'objectif
			if ( round( self.position['x']) == self.mission[1][0] ) and ( round(self.position['y']) == self.mission[1][1] ):
				print("mission done")
				self.success+=1
				self.mission = []
				self.path = []
			#si on a pas atteint l'objectif
			else :
				#Si on a atteint le milieu de la mission
				if ( round( self.position['x']) == self.mission[0][0] ) and ( round(self.position['y']) == self.mission[0][1] ) :
					print("mission start : ", self.mission[1] )
					self.computePath( self.mission[1] )
					if self.path :
						self.move()
					else:
						self.fail += 1
						self.mission = []
				# si on a pas atteint le milieu
				else :
					#si on a pas de chemin
					if not self.path:
						print("new mission, going to start point")
						self.computePath( self.mission[0]  )
						if self.path :
							self.move()
						else:
							self.noPath += 1
							self.mission = []
					else :
						#si on a un chemin et qu'on est au bout
						if len(self.path) > 0 and (self.pathStep == len(self.path)):
							print("blocked at :", self.position, "mission", self.mission )
							self.mission = []
							self.path = []
							self.noPath +=1
						#si on est pas au bout du chemin
						else:
						#print("step is:", self.pathStep, "pathSize is:", len(self.path))
						#print("i'm at:",round(self.position['x']),round(self.position['y']) )
						#print("going to:", self.path[self.pathStep][0] , self.path[self.pathStep][0] )
						#print("Mission Goal:", self.mission )
						#time.sleep(1)
							#on avance jusqu'au point a atteindre
							self.move()
							#si on a atteint le point ou l'on souhaite aller
							if (round(self.position['x']) == self.path[self.pathStep][0] ) and (round(self.position['y']) == self.path[self.pathStep][1]  ) :
								self.pathStep+=1
							#si on a une mission mais pas encore de chemin			
							#si on est a atteint le point de départ de la mission				
				

	def getPose(self):
		if self.isMorse :
			return self.pose.get()
		else:
			return self.pose

	def move(self):
		if self.isMorse :
			self.motion.publish( { 'x':self.path[self.pathStep][0] , 'y':self.path[self.pathStep][0], 'z':0,  'speed':1, 'tolerance':0 } )
		else :
			self.pose = {'x': self.path[self.pathStep][0] , 'y': self.path[self.pathStep][1]}	

	def computePath(self, Goal):
		pot =  PotentialField( [ self.map['x'], self.map['y'] ] , self.map['obstacles'], 2, [round(self.position['x']),round(self.position['y'])], Goal)
		self.path = pot.getPath()
		self.pathStep = 1
		#on previens les autres du nouveau chemin
		#self.signify(self.path)
	
	def signify(self, Goal):
		for bot in self.map['robots'] :
			bot.notify(self.path)

	def notify(self, botPath):
		#to be continued
		print("newpath")
