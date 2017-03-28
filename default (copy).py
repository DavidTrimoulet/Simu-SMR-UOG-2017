
from morse.builder import *
from math import pi
from CESIBot import CESIBot

robot = CESIBot()
waypoint = Waypoint()
robot.append(waypoint)
waypoint.add_stream('socket')
robotPose = Pose()
robot.append(robotPose)
robotPose.add_stream('socket')
semanticC = SemanticCamera()
semanticC.translate(x=0.3, z=-0.05)
semanticC.rotate(x=+0.2)
robot.append(semanticC)
semanticC.properties(Vertical_Flip=True)
robot.add_service('socket')
robot.translate(x=1, y=1,z=0)
#	myrobots.append(robot)

env = Environment('Models/Models.blend')
env.set_camera_location([0.0, 0.0, 20.0])
env.set_camera_rotation([45, 0, 0])
#env.select_display_camera(semanticC1)
#env.select_display_camera(semanticC2)
