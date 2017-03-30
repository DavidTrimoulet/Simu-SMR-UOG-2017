import morse.core.robot
from morse.builder import *
from morse.core.services import service
import logging 

logger = logging.getLogger("morse." + __name__)

class CESIBot(Robot):

	_name = 'CESI Bot for test and fun'

	def __init__(self,name = None):
		Robot.__init__(self, "/usr/share/morse/data/robots/b21.blend", name)
		self.isInMission = False
		logger.warning("je viens d'être créé")

	def default_action(self):
		logger.warning("Default Action")

	@service
	def act(self):
		print("coucou")

	@service
	def moveTo(self, location):
		this = self.bge_object