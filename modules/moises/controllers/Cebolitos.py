from framework import Controller as std

class Cebolitos(std.Controller):
		
	def arca(self):
		self.response_body_directly()
		return self.get_html("index")

	def salvar(self):
		self.model(self.get_request_parameters()).save().close()
		return "sucesso"

	def get(self):
		connection = self.model().find(start_from = 0, limit = 3)
		data = connection.fetch(fields_to_ignore = ['senha'])
		connection.close()
		return data

