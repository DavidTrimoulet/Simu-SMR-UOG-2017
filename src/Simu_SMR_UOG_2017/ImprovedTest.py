from ImprovedPotentialField import ImprovedPotentialField
from ImprovedSimuBot import ImprovedSimuBot
import pprint
import logging


def main():
	logging.basicConfig(filename='test.log', level=logging.DEBUG)
	maxX = 10
	maxY = 10
	logging.debug("test")
	obstacles = [ [5,5] ]
	currentMap = { 'x':maxX , 'y':maxY, 'obstacles':obstacles }
	time = 0
	robots = [ ImprovedSimuBot( {'x':int(i), 'y':int(i)}, {} , currentMap, False )  for i in range(0,2) ]
	
	for bot in robots :
		bot.setOthersBots( [x for x in robots if bot != x] )
	missions = [ [ [8,8], [2,1] ] , [ [8,8], [2,1] ] ]
	print(currentMap)
	print(robots)
	print(missions)
	time = 0
	collision = 0	
	while missions or [ x for x in robots if x.mission ] :
		time += 1
		print("time:", time)
		for bot in robots:
			if not bot.mission and missions :
				bot.mission = missions.pop()
		for bot in robots:
			bot.act(time)
		collision += checkCollision(robots)
	print(collision)

def checkCollision(robots):
	val = 0
	for i in range(0, len(robots)):
		for j in range(0, len(robots)):
			if i != j :
				if robots[i].position == robots[j].position :
					val += 1
	return val

if __name__ == "__main__":
	main()