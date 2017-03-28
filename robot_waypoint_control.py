from pymorse import Morse
import math
from pprint import pprint
import random
from simuBot import *

def generateObstacles(obstaclesSeed):
	obstacles = []
	for seed in obstaclesSeed:
		for i in range(seed[0], seed[2]+1):
			for j in range(seed[1], seed[3]+1):
				obstacles.append([i,j])
	return obstacles

def getRandomCoordinate(XmaxVal, YmaxVal):
	return [ random.randint(1, XmaxVal) , random.randint(1, YmaxVal) ] 

def generateMission(missionQuantity, width, height, obstacles):
	missions = []
	for i in range(missionQuantity):
		mission = []
		while True :
			coor = getRandomCoordinate(width, height)  
			if coor not in obstacles:
				mission.append(coor)
				break

		while True :
			coor = getRandomCoordinate(width, height)  
			if coor not in obstacles:
				mission.append(coor)
				break
		missions.append(mission)

	return missions


def getSimuBot(currentMap, morse):
	bots = []
	bots.append(simuBot(morse.robot1.robot1Pose, morse.robot1.robot1Waypoint, currentMap))
	bots.append(simuBot(morse.robot2.robot2Pose, morse.robot2.robot2Waypoint, currentMap))
	bots.append(simuBot(morse.robot3.robot3Pose, morse.robot3.robot3Waypoint, currentMap))
	bots.append(simuBot(morse.robot4.robot4Pose, morse.robot4.robot4Waypoint, currentMap))
	return bots

def run(currentMap, missions, robots):
	while missions:
		for bot in robots:
			if not bot.mission :
				bot.mission = missions.pop()
		for bot in robots:
			print("bot action")
			bot.act()

def main():
	morse = Morse()
	maxX = 100
	maxY = 100
	missionNumber = 100
	obstaclesSeed = [	[50, 0, 50, 50],
						[80, 50,100,50],
						[75,75,75,100],
						[25,50,25,100]	]
	obstacles = generateObstacles(obstaclesSeed)
	pprint(obstacles)
	missions = generateMission(missionNumber, maxX, maxY, obstacles)
	pprint(missions)
	currentMap = { 'x':maxX , 'y':maxY, 'obstacles':obstacles }
	robots = getSimuBot(currentMap, morse)
	pprint(robots)
	run(currentMap, missions, robots)
	#goToNextPoint()

if __name__ == "__main__":
	main()