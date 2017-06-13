#!/usr/bin/env python


"""

Guards Listener Module
Authors: Oliver Ceccopieri, Sydney Pratt, Thomas Beard, Brenton Sundlie

Copy into MAVProxy source tree under "MAVProxy/modules"
Recompile MAVProxy with "python setup.py build install --user"

In MavProxy command line, load with "module load guards"
Run with "guards"

"""


from MAVProxy.modules.lib import mp_module

from time import time
from os import system


class GuardsModule(mp_module.MPModule):
	
	PING_COMMAND = 'ping -c 1 -W %d %s > /dev/null 2>&1'
	PING_DELAY = 1
	
	
	def __init__(self, mpstate):
		super(GuardsModule, self).__init__(mpstate, 'guards', 'GUARDS alert system')
		self.add_command('guards', self.cmd_guards, 'Begin GUARDS listen and alert sequence', ['arm', 'disarm'])
		self.armed = False
		self.motheraddr = ''
		self.lastping = 0
		
		
	""" Handle a mavlink packet """
	def mavlink_packet(self, packet):
		if self.armed and (time() - self.lastping) > GuardsModule.PING_DELAY:
			self.lastping = time()
			
			# Perform network ping
			response = system(GuardsModule.PING_COMMAND % (GuardsModule.PING_DELAY, self.motheraddr))
			if response != 0:
				# Launch drone
				self.say('GUARDS: No ping response. Launching!')
				self.armed = False
				self.master.arducopter_arm()
				
				
	""" Begin listen and alert sequence """
	def cmd_guards(self, args):
		helptext = 'usage: guards <arm|disarm>'
		if len(args) < 1:
			print(helptext)
			return
			
		# Arm the GUARDS system
		if args[0] == 'arm':
			if len(args) < 2:
				print('usage: guards arm <ip address>')
				return
				
			if self.armed:
				self.say('GUARDS: Already armed, listening for ' + self.motheraddr)
				return
				
			# Get initial ping response
			self.motheraddr = args[1]
			response = system(GuardsModule.PING_COMMAND % (GuardsModule.PING_DELAY, self.motheraddr))
			if response != 0:
				self.say('GUARDS: ERROR: Host is not up')
				return
				
			self.armed = True
			self.say('GUARDS: Armed, listening for ' + self.motheraddr)
			return
			
		# Disarm the GUARDS system
		if args[0] == 'disarm':
			self.armed = False
			self.say('GUARDS: Disarmed')
			return
			
		print(helptext)
		
		
""" Initialize module """
def init(mpstate):
	return GuardsModule(mpstate)
	