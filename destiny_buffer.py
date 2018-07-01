class destiny_buffer:
	def __init__(self):
		self.list = []

	def push(self, item):
		if len(self.list) == 4:
			self.list.pop(0)
		self.list.append(item)

	def pop(PC):
		for i in range(len(self.list)):
			if int(item[0]) == int(PC):
				self.pop(i)

	def print(self):
		for item in self.list:
			print("PC:", item[0], "destiny:", item[1], "prediction:", item[2])