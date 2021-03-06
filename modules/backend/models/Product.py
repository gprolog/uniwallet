from framework import Model as std

class Product(std.Model):
	attributes = ['name', 'description', 'company_id', 'price', 'quantity']

	def check_product_available(self, id, quantity):

		if quantity <= self.find([('id', '=', id)]).fetchone()['quantity']:
			return True
		else:
			return False

	def get_price(self, id, quantity):
		price = self.find([('id', '=', id)]).fetchone()['price']
		return price * quantity

	def decrement(self, quantity):
		if (quantity <= self.quantity):
			self.quantity -= quantity
			self.save().close()

