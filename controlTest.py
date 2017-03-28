import pymorse
import math
import pprint


with pymorse.Morse("localhost", 4000) as simu :

	try:
		pprint.pprint(simu.__dict__)
		for robot in robots:

			robot.act()
	except Exception as e:
		raise e
	else:
		pass