from pymorse import Morse
import math
from pprint import pprint
import random
from simuBot import *
import sys

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
		#print([ x for x in robots if x.mission ])
		global collision
		for bot in robots:
			if not bot.mission and missions :
				bot.mission = missions.pop()
		for bot in robots:
			#print(bot.mission)
			bot.act()
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
	maxX = 100
	maxY = 100
	missionNumber = 100
	global isMorse
	global morse
	global collision
	obstaclesSeed = [	[5, 5, 5, 5],
						[10, 10, 10, 10],	
						[50, 50, 50, 50],
						#[50, 0, 50, 50],
						#[80, 50,100,50],
						#[75,75,75,100],
						#[25,50,25,100]	
						]
	obstacles = generateObstacles(obstaclesSeed)
	#obstacles = []
	print("obstacles:", obstacles)
	missions = generateMission(missionNumber, maxX, maxY, obstacles)
	pprint(missions)
	currentMap = { 'x':maxX , 'y':maxY, 'obstacles':obstacles }
	robots = []
	if len(sys.argv) > 1 :
		morse = Morse()
		isMorse = True
		robots = getMorseBot(currentMap, morse)
	else:
		isMorse = False
		robots = getBot(currentMap, 50)
	pprint(robots)
	run(currentMap, missions, robots)
	print("sucess:", sum([x.success for x in robots]) )
	print("fail:", sum([x.fail for x in robots]) )
	print("No  path:", sum([x.noPath for x in robots]) )
	print("collision", collision)
	
	#goToNextPoint()

if __name__ == "__main__":
	main()