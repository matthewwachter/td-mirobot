"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

class MirobotPositions:
	"""
	MirobotPositions description
	"""

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.delayCMD = ownerComp.op('delayCMD')
		self.itemer = ownerComp.op('itemer')

	def GoToPosAxis(self, pos, delayMilliSeconds=0):
		if delayMilliSeconds == 0:
			self._GoToPosAxis(pos)
		else:
			self.delayCMD.run('_GoToPosAxis', pos, delayMilliSeconds=delayMilliSeconds)

	def _GoToPosAxis(self, pos):
		items = self.itemer.Items
		p = items[self.itemer.GetItemIndex(pos)]

		mirobot = self.ownerComp.par.Mirobot.eval()

		mirobot.GoToAxis(
			p['a1'],
			p['a2'],
			p['a3'],
			p['a4'],
			p['a5'],
			p['a6'],
			2000
		)

	def SayHello(self):
		print('hello')