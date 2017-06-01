from framework import Model as std
from helpers import dictionary

class Transaction(std.Model):
	attributes = ['wallet_from', 'wallet_to', 'value', 'operation']

	def perform(self):
		if self.model('Wallet').transfer(self.value, self.wallet_from, self.wallet_to):
			self.save().close()
			return True
		else:
			return False #It happens when value is not authorized to be transferred