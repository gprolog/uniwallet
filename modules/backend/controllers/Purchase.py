from . import Controller as std

class Purchase(std.Controller):

	def create(self):
		consumer_id = self.model(name = 'Session').get_user()['id']
		total_price = 0
		i = 0
		products = []
		quantity = []
		for item in self.get_request_parameters()["products"]:
			if not self.model('Product').check_product_available(item["id"], item["quantity"]):
				return "Quantidade Indisponivel"
			total_price = total_price + self.model('Product').get_price(item["id"], item["quantity"])
			
			products.append(item["id"])
			quantity.append(item["quantity"])
			
			





		company_id = self.get_input('company_id')

		wallet_from = self.model('Wallet').find(conditions = [('user_id', '=', self.model('Consumer').load(consumer_id).user_id)]).fetchone()['id']
		wallet_to = self.model('Wallet').find(conditions = [('user_id', '=', self.model('Company').load(company_id).user_id)]).fetchone()['id']

		transaction_id = self.model(name = 'Transaction', data = {'wallet_from': wallet_from, 'wallet_to': wallet_to, 'value': total_price, 'operation': 'purchase'}).perform()
		if transaction_id is not None:
			self.model(data = {'transaction_id': transaction_id, 'consumer_id': consumer_id, 'company_id': company_id}).save().close()
			purchase_id = self.model().find(conditions = [('transaction_id', '=', transaction_id)]).fetchone()['id']
			
			for i in range(len(products)):
				#Salva na tabela "Purchase_Product" os produtos e quantidades
 					self.model(name = 'Purchase_Product', data = {'purchase_id': purchase_id, 'product_id': products[i], 'quantity': quantity[i]}).save().close()
 					i += 1
 				
			return "Purchase completed"
		else:
			return "Purchase not authorized"

	def showall(self):
		lista = []
		purchase_showall = self.model().find().fetch()
		transaction_showall = self.model(name = 'Transaction').find().fetch()
		for purchase in purchase_showall:
			lista.append({'Purchase':purchase,'Transaction':self.model(name = 'Transaction').find([('user_id','=',user['id'])]).fetch()})
		return (lista)
							

	def fetch(self):
		return self.model(name = 'Sale_Product').find(join = [('Product', 'product_id'), ('Company', 'Products.company_id'), ('Sale', 'sale_id'), ('Consumer', 'Sales.consumer_id')]).fetch()

	def fetchadmin(self):
		mask = self.metadata([('id', ':::hide'), ('consumer_fullname', ':Comprador::noneditable'), ('company_name', ':Empresa::noneditable'), ('transaction_value', ':Valor::noneditable')])
		return (self.model().find(join=[('Transaction', 'transaction_id'), ('Consumer', 'consumer_id'), ('Company', 'company_id')], start_from = self.get_input('start'), limit = self.get_input('limit'))
			.fetch(fields_mask = mask))

