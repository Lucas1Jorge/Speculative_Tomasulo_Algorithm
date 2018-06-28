class recently_used_memory:
	def __init__(self):
		self.list = []

	def push(self, item):
		if len(self.list) == 4:
			self.list.pop(0)
		self.list.append(item)

	def print(self):
		for item in self.list:
			print("adress:", item[0], "val:", item[1])