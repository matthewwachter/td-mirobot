from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

import re

from pprint import pprint

class Mirobot:
	"""
	Mirobot description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.serialDat = ownerComp.op('serial1')
		self.res_state = 0

	### UTILITY

	def delayCMD(self, method, args, delayMilliSeconds=0):
		self.ownerComp.op('delayCMD').run(method, args, delayMilliSeconds=delayMilliSeconds)

	### COMMUNICATION

	def _send_msg(self, msg, get_status=True):
		self.serialDat.send(msg,  terminator='\r\n')
		self.res_state += 1

		if get_status:
			self.delayCMD('GetStatus', None, 100)

	def _recv_msg(self, msg):
		self.res_state -= 1
		self.res_state = max(0, self.res_state)

		#print(msg, '\n')

		if msg.startswith('<'):
			self._recv_status(msg)

	def _recv_status(self, msg):
		pars = self.ownerComp.par

		msg = msg.strip('<').strip('>')

		state = msg.split(',')[0]
		if state is not None:
			pars.Status = state

		msg = ','.join(msg.split(',')[1:])

		angle = re.match(r'Angle\(ABCDXYZ\):(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),', msg)

		if angle is not None:
			a4, a5, a6, rail, a1, a2, a3 = angle.groups()
			axis_angles = [a1, a2, a3, a4, a5, a6]
			pars.A1 = a1
			pars.A2 = a2
			pars.A3 = a3
			pars.A4 = a4
			pars.A5 = a5
			pars.A6 = a6
			pars.Rail = rail
			# pprint(axis_angles)

		cart = re.match(r'.*Cartesian\scoordinate\(XYZ\sRxRyRz\):(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),(-*\d*.\d*),', msg)
		if cart is not None:
			x, y, z, rx, ry, rz = cart.groups()
			cart_coord = [x, y, z, rx, ry, rz]
			pars.Tx = x
			pars.Ty = y
			pars.Tz = z
			pars.Rx = rx
			pars.Ry = ry
			pars.Rz = rz
			# pprint(cart_coord)

		pump_pwm = re.match(r'.*Pump\sPWM:(\d+)', msg)
		if pump_pwm is not None:
			pars.Pumppwm = pump_pwm.groups(0)[0]

		valve_pwm = re.match(r'.*Valve\sPWM:(\d+)', msg)
		if valve_pwm is not None:
			pars.Valvepwm = valve_pwm.groups(0)[0]

		motion_mode = re.match(r'.*Motion_MODE:(\d+)', msg)
		if motion_mode is not None:
			pars.Motionmode = motion_mode.groups(0)[0]

		#print(pump_pwm, valve_pwm, motion_mode)


	### COMMANDS
	def GetStatus(self):
		msg = '?'
		self._send_msg(msg, get_status=False)

	def HomingIndividual(self):
		msg = '$HH'
		self._send_msg(msg, get_status=False)

	def HomingSimultaneous(self):
		msg = '$H'
		self._send_msg(msg, get_status=False)

	def SetHardLimit(self, state):
		msg = '$21=' + str(int(state))
		self._send_msg(msg, get_status=False)

	def SetSoftLimit(self, state):
		msg = '$21=' + str(int(state))
		self._send_msg(msg, get_status=False)

	def UnlockShaft(self):
		msg = 'M50'
		self._send_msg(msg)

	def GoToZero(self):
		self.GoToAxis(0, 0, 0, 0, 0, 0, 2000)

	def GoToAxis(self, a1, a2, a3, a4, a5, a6, speed):
		msg = 'M21 G90'
		msg += ' X' + str(a1)
		msg += ' Y' + str(a2)
		msg += ' Z' + str(a3)
		msg += ' A' + str(a4)
		msg += ' B' + str(a5)
		msg += ' C' + str(a6)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def IncrementAxis(self, a1, a2, a3, a4, a5, a6, speed):
		msg = 'M21 G91'
		msg += ' X' + str(a1)
		msg += ' Y' + str(a2)
		msg += ' Z' + str(a3)
		msg += ' A' + str(a4)
		msg += ' B' + str(a5)
		msg += ' C' + str(a6)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def GoToCartesianPTP(self, x, y, z, a, b, c, speed):
		msg = 'M20 G90 G0'
		msg += ' X' + str(x)
		msg += ' Y' + str(y)
		msg += ' Z' + str(z)
		msg += ' A' + str(a)
		msg += ' B' + str(b)
		msg += ' C' + str(c)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def GoToCartesianLin(self, x, y, z, a, b, c, speed):
		msg = 'M20 G90 G1'
		msg += ' X' + str(x)
		msg += ' Y' + str(y)
		msg += ' Z' + str(z)
		msg += ' A' + str(a)
		msg += ' B' + str(b)
		msg += ' C' + str(c)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def IncrementCartesianPTP(self, x, y, z, a, b, c, speed):
		msg = 'M20 G91 G0'
		msg += ' X' + str(x)
		msg += ' Y' + str(y)
		msg += ' Z' + str(z)
		msg += ' A' + str(a)
		msg += ' B' + str(b)
		msg += ' C' + str(c)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def IncrementCartesianLin(self, x, y, z, a, b, c, speed):
		msg = 'M20 G91 G1'
		msg += ' X' + str(x)
		msg += ' Y' + str(y)
		msg += ' Z' + str(z)
		msg += ' A' + str(a)
		msg += ' B' + str(b)
		msg += ' C' + str(c)
		msg += ' F' + str(speed)
		self._send_msg(msg)
		return

	def SetAirPump(self, pwm):
		msg = 'M3S' + str(pwm)
		self._send_msg(msg)

	def SetGripper(self, pwm):
		msg = 'M4E' + str(pwm)
		self._send_msg(msg)




	### PULSE PARAMETERS
	def pulse_Getstatus(self):
		self.GetStatus()

	def pulse_Homingindividual(self):
		self.HomingIndividual()

	def pulse_Homingsimultaneous(self):
		self.HomingSimultaneous()

	def pulse_Gotozero(self):
		self.GoToZero()

	def pulse_Unlockshaft(self):
		self.UnlockShaft()

	def pulse_Airon(self):
		self.SetAirPump(40)

	def pulse_Airoff(self):
		self.SetAirPump(0)

	def pulse_Gripperon(self):
		self.SetGripper(40)

	def pulse_Gripperoff(self):
		self.SetGripper(0)

	def pulse_A1i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(inc, 0, 0, 0, 0, 0, 2000)

	def pulse_A1d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(-inc, 0, 0, 0, 0, 0, 2000)

	def pulse_A2i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, inc, 0, 0, 0, 0, 2000)

	def pulse_A2d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, -inc, 0, 0, 0, 0, 2000)

	def pulse_A3i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, inc, 0, 0, 0, 2000)

	def pulse_A3d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, -inc, 0, 0, 0, 2000)

	def pulse_A4i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, inc, 0, 0, 2000)

	def pulse_A4d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, -inc, 0, 0, 2000)

	def pulse_A5i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, 0, inc, 0, 2000)

	def pulse_A5d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, 0, -inc, 0, 2000)

	def pulse_A6i(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, 0, 0, inc, 2000)

	def pulse_A6d(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementAxis(0, 0, 0, 0, 0, -inc, 2000)


	def pulse_Txi(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(inc, 0, 0, 0, 0, 0, 2000)

	def pulse_Txd(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(-inc, 0, 0, 0, 0, 0, 2000)

	def pulse_Tyi(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(0, inc, 0, 0, 0, 0, 2000)

	def pulse_Tyd(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(0, -inc, 0, 0, 0, 0, 2000)

	def pulse_Tzi(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(0, 0, inc, 0, 0, 0, 2000)

	def pulse_Tzd(self):
		inc = self.ownerComp.par.Jogincrementmm.eval()
		self.IncrementCartesianLin(0, 0, -inc, 0, 0, 0, 2000)

	def pulse_Rxi(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, inc, 0, 0, 2000)

	def pulse_Rxd(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, -inc, 0, 0, 2000)

	def pulse_Ryi(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, 0, inc, 0, 2000)

	def pulse_Ryd(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, 0, -inc, 0, 2000)

	def pulse_Rzi(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, 0, 0, inc, 2000)

	def pulse_Rzd(self):
		inc = self.ownerComp.par.Jogincrementdeg.eval()
		self.IncrementCartesianLin(0, 0, 0, 0, 0, -inc, 2000)


