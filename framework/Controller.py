from framework.Response import Response
from framework.Database import Database
from helpers import dictionary, general
import importlib
import os

class Controller:

	def __init__(self, request):
		self.response = Response()
		self.request = request

	def get_module_nome(self):
		"""
		get_module_name(): It gets the module name where controller is located into
		"""
		pass

	def build_query(self):
		return QueryBuilder()

	def action(self, action_name):
		"""
		action(): It tries to call a method called 'action_name' from the current Controller object. Then it returns the output of that method.
		If that method is not found, it returns a warning.
		"""
		if hasattr(self, action_name) and callable(getattr(self, action_name)):
			self.response.body = getattr(self, action_name)()
			return self.response
		else:
			return Response(code = 'Not Found', body = "Action '{}' unavailable".format(action_name))

	def get_db_connection(self):
		"""
		get_db_connection(): It returns the database connection
		"""
		return Database(getattr(importlib.import_module("modules.{}.db.config".format(self.request.module)), "config")())


	def model(self, data = None):
		"""
		get_model(): It returns a instance a of a correspondent model
		"""
		return self.model_class(self.__class__.__name__)(self.get_db_connection(), data)

	def model_class(self, model_name):
		"""
		model_class(): It returns a instance a of a correspondent model
		"""
		try:
			return getattr(importlib.import_module("modules.{}.models.{}".format(self.request.module, model_name)), model_name)
		except Exception as e:
			raise Exception("Error invoking model '{}': {}".format(model_name, str(e)))

	def get_request_parameters(self):
		"""
		get_request_parameters(): It returns the request parameters
		"""
		return self.request.get_inputs_from_method()

	def get_input(self, field):
		"""
		get_input(): It gets a request paramenter
		"""
		return self.request.get_input(field)

	def get_html(self, html_file_name):
		"""
		get_html(): It reads and returns the content of some html file placed on modules/{current_module}/html
		"""
		self.response_body_directly()
		return self.get_file("html/{}.html".format(html_file_name))

	def get_file(self, file_path, mode = 'r'):
		"""
		get_file(): Get the file content
		"""
		pack = general.get_package_from_module(self.request.module, "modules")
		with open("{}/{}".format(os.path.dirname(pack.__file__), file_path), mode) as file:
			return file.read()

	def response_body_directly(self):
		"""
		response_body_directly(): It sets response.raw as True
		"""
		self.response.raw = True

	def forbid(self, message = None, code = 'Bad Request'):
		"""
		forbid(): It sets the code as 400 by default
		"""
		self.response.code = code
		if message:
			return message 

	def make_conditions(self, dict, conditional_sign = '='):
		return dictionary.tuplefy(dict, conditional_sign)

	def register(self):
		db_id = self.model(self.get_request_parameters()).save().last_id()
		return "Done: {} {} created".format(__class__.__name__, db_id)

	def update(self):
		return "Done: {} rows affected".format(self.model().update(fields = self.get_request_parameters()).count_rows())

	def delete(self):
		return "Done: {} rows affected".format(self.model().destroy(list({'id': item} for item in self.get_request_parameters()['ids'])).count_rows())

	def fetch(self):
		return self.model().find(start_from = self.get_input('start'), limit = self.get_input('limit')).fetch(fields_to_ignore = ['password'])



