from PotentialField import PotentialField


xSize = 20
ySize = 10

map = [xSize, ySize]
print(map[1])
obstacles = [ [4,4] , [18,8] ]

potentialField = PotentialField(map, obstacles, 1, [1,1], [9, 9])
potentialField.generateU()

print("Attraction Map")
for line in potentialField.ua:
	print( [round(x) for x in line ] )

print("Repulsive Map")
for line in potentialField.ur:
	print( [round(x) for x in line ] )

print("Path Map")
for line in potentialField.u:
	print( [round(x) for x in line ] )

print("Path")
print(potentialField.getPath())