from framework import Treater as std

class Wallet(std.Treater):
	def register(self):
		return self.rules({
				"fields": {
					"balance": 	["required"],
					"user_id":	["required", "exists:id:User"]
				},
				"method": "get",
				#"auth": ["manager", "client"]
			})

	def update(self):
		return self.rules({
				"fields": {
					"id": 			["required", "exists:id:Wallet"],
					"balance":		["required", "float"]
				},
				"method": "post",
				"auth": ["god"]
			})

	def check(self):
		return self.rules({
				"fields": {
					"value": 	["required"],
					
				},
				"method": "get",
				#"auth": ["manager", "client"]
			})