from pymorse import Morse
import math
from pprint import pprint
import random
from simuBot import *
from ImprovedSimuBot import *
import sys
import logging
import matplotlib.pyplot as plt
from enum import Enum

class robotType(Enum):
	NORMAL = 0
	IMPROVED = 1

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

def getBot(botType, currentMap, number):
	bots = []
	global isMorse
	for i in range(0, number):
		if botType == robotType.NORMAL:
			bots.append(simuBot( {'x':int(i), 'y':int(i)}, {} , currentMap, isMorse ))
		else :
			bots.append(ImprovedSimuBot( {'x':int(i), 'y':int(i)}, {} , currentMap, isMorse ))
	return bots

def run(currentMap, missions, robots):
	curTime = 0
	while missions or [ x for x in robots if x.mission ] :
		print([ x for x in robots if x.mission ])
		global collision
		for bot in robots:
			if not bot.mission and missions :
				bot.mission = missions.pop()
		for bot in robots:
			print(bot.mission)
			bot.act(curTime)
		curTime += 1
		collision += checkCollision(robots)
		print("nombre de mission restante :", len(missions))

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
	ImSuccesses = []
	collisions = []
	ImCollisions = []
	fails = []
	ImFails = []
	noPaths = []
	ImNoPaths = []
	robotsQuantities = []
	ImRobotsQuantities = []


	for i in range(10,100):
		maxX = i
		maxY = i
		missionNumber = i*2
		robotNumber = int(i/5)
		global isMorse
		global morse
		global collision
		

		obstaclesSeed = [	[5, 5, 5, 5],
							[10, 10, 10, 10],	
							[50, 50, 50, 50],
							[50, 25, 50, 50],
							[80, 50, 90, 50],
							[200, 10, 200, 50],
							[400, 150, 400, 450],
							]
		obstacles = generateObstacles(obstaclesSeed)
		#obstacles = []
		print("obstacles:", obstacles)
		missions = generateMission(missionNumber, maxX, maxY, obstacles)
		print(missions)
		currentMap = { 'x':maxX , 'y':maxY, 'obstacles':obstacles }
		robots = []
		ImRobots = []
		if len(sys.argv) > 1 :
			morse = Morse()
			isMorse = True
			robots = getMorseBot(currentMap, morse)
		else:
			isMorse = False
			robots = getBot(robotType.NORMAL, currentMap, robotNumber)
			ImRobots = getBot(robotType.IMPROVED, currentMap, robotNumber)
		
		print(robots)
		print(ImRobots)
		NormalMissions = list(missions)
		ImprovedMissions = list(missions)

		run(currentMap, NormalMissions, robots)

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

		collision = 0
		
		run(currentMap, ImprovedMissions, ImRobots)

		print("Map Size: x:", maxX, "y:", maxY, "robot number:", len(robots), "Nombre de mission:", missionNumber )
		print("sucess:", sum([x.success for x in ImRobots]),
			  "/fail:", sum([x.fail for x in ImRobots]) ,
			  "/No path:", sum([x.noPath for x in ImRobots]),
			  "/Collision", collision , "\n")
		ImSuccesses.append(sum([x.success for x in ImRobots]))
		ImFails.append(sum([x.fail for x in ImRobots]))
		ImNoPaths.append(sum([x.noPath for x in ImRobots]))
		ImCollisions.append(collision)
		ImRobotsQuantities.append(len(ImRobots))

		
	plt.plot(maps, sucesses)
	plt.figure()
	plt.plot(maps, fails)
	plt.figure()
	plt.plot(maps, noPaths)
	plt.figure()
	plt.plot(maps, collisions)
	plt.figure()
	plt.plot(maps, robotsQuantities)
	plt.show()


		


	#goToNextPoint()

if __name__ == "__main__":
	main()



