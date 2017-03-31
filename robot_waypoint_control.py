from pymorse import Morse
import math
from pprint import pprint
import random
from simuBot import *
import sys
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger("SimuCESI")

isMorse = True
morse = []
collision  = 0

def generateObstacles(obstaclesSeed):
	obstacles = []
	for seed in obstaclesSeed:
		for i in range(seed[0], seed[2]+1):
			for j in range(seed[1], seed[3]+1):
				obstacles.append([i,j])
	return obstacles

def getRandomCoordinate(XmaxVal, YmaxVal):
	return [ random.randint(0, XmaxVal-1) , random.randint(0, YmaxVal-1) ] 

def generateMission(missionQuantity, width, height, obstacles):
	missions = []
	for i in range(missionQuantity):
		mission = []
		while len(mission) < 2 :
			coor = getRandomCoordinate(width, height)  
			if coor not in obstacles:
				mission.append(coor)

		missions.append(mission)

	return missions

def getMorseBot(currentMap, morse):
	bots = []
	global isMorse
	bots.append(simuBot(morse.robot1.robot1Pose, morse.robot1.robot1Waypoint, currentMap, isMorse))
	bots.append(simuBot(morse.robot2.robot2Pose, morse.robot2.robot2Waypoint, currentMap, isMorse))
	bots.append(simuBot(morse.robot3.robot3Pose, morse.robot3.robot3Waypoint, currentMap, isMorse))
	bots.append(simuBot(morse.robot4.robot4Pose, morse.robot4.robot4Waypoint, currentMap, isMorse))
	return bots

def getBot(currentMap, number):
	bots = []
	global isMorse
	for i in range(0, number):
		bots.append(simuBot( {'x':int(i), 'y':int(i)}, {} , currentMap, isMorse ))
	return bots

def run(currentMap, missions, robots):
	while missions or [ x for x in robots if x.mission ] :
		logger.debug([ x for x in robots if x.mission ])
		global collision
		for bot in robots:
			if not bot.mission and missions :
				bot.mission = missions.pop()
		for bot in robots:
			logger.debug(bot.mission)
			bot.act()
		collision += checkCollision(robots)
		logger.debug("nombre de mission restante :", len(missions))

def checkCollision(robots):
	val = 0
	for i in range(0, len(robots)):
		for j in range(0, len(robots)):
			if i != j :
				if robots[i].position == robots[j].position :
					val += 1
	return val

def main():

	maps = []
	sucesses = []
	collisions = []
	fails = []
	noPaths = []
	robotsQuantities = []

	for i in range(10,100):
		maxX = i
		maxY = i
		missionNumber = i*2
		robotNumber = int(i/5)
		global isMorse
		global morse
		global collision
		

		obstaclesSeed = [	[5, 5, 5, 10],
							[10, 10, 10, 10],	
							[50, 50, 50, 50],
							[50, 25, 50, 50],
							[80, 50, 90, 50],
							[200, 10, 200, 50],
							[400, 150, 400, 450],
							]
		obstacles = generateObstacles(obstaclesSeed)
		#obstacles = []
		logger.debug("obstacles:", obstacles)
		missions = generateMission(missionNumber, maxX, maxY, obstacles)
		logger.debug(missions)
		currentMap = { 'x':maxX , 'y':maxY, 'obstacles':obstacles }
		robots = []
		if len(sys.argv) > 1 :
			morse = Morse()
			isMorse = True
			robots = getMorseBot(currentMap, morse)
		else:
			isMorse = False
			robots = getBot(currentMap, robotNumber)
		logger.debug(robots)
		run(currentMap, missions, robots)

		print("Map Size: x:", maxX, "y:", maxY, "robot number:", len(robots), "Nombre de mission:", missionNumber )
		print("sucess:", sum([x.success for x in robots]),
			  "/fail:", sum([x.fail for x in robots]) ,
			  "/No path:", sum([x.noPath for x in robots]),
			  "/Collision", collision , "\n")
		maps.append(maxX*maxY)
		sucesses.append(sum([x.success for x in robots]))
		fails.append(sum([x.fail for x in robots]))
		noPaths.append(sum([x.noPath for x in robots]))
		collisions.append(collision)
		robotsQuantities.append(len(robots))
		
	p1 = plt.plot(maps, sucesses)
	p2 = plt.plot(maps, fails)
	p3 = plt.plot(maps, noPaths)
	p4 = plt.plot(maps, collisions)
	p5 = plt.plot(maps, robotsQuantities)
	plt.legend([p1,p2,p3,p4,p5], ["Suces","Echec","Pas de chemin","collisions", "nombre de robots"] )
	plt.show()
		#plt.plot(robotsQuantities, collisions)

		


	#goToNextPoint()

if __name__ == "__main__":
	main()