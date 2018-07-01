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


class register:
	def __init__(self, name):
		self.name = name
		self.Vi = 0
		self.Qi = ""


class register_bank:
	def __init__(self, name):
		self.name = name
		self.registers = []	
		for i in range(32):
			self.registers.append(register(str(i)))

	def print(self):
		for register in self.registers:
			print(register.name, " - Vi:", register.Vi, " - Qi:", register.Qi)

	def push(self, info):
		if info[-1] == "mark":
			if info[0][0] == "S":
				return
			else:
				if int(info[1]) != 0:
					self.registers[int(info[1])].Qi = info[0]
		elif info[0][0] == "S":
			return
		else:
			# if info[1] != 0 and info[0] == self.registers[int(info[1])].Qi:
			# 	self.registers[int(info[1])].Vi = int(info[-1])
			# 	self.registers[int(info[1])].Qi = ""
			if info[1] != "0":
				self.registers[int(info[1])].Vi = int(info[-1])
				self.registers[int(info[1])].Qi = ""


class destiny_buffer():
	def __init__(self, name, max_size):
		# self.list = [[]] * max_size
		self.name = name
		# self.start = 0
		# self.end = 0
		# self.size = 0
		# self.max_size = max_size
		# self.ID = []
		# for i in range(max_size):
		# 	self.ID.append(str.upper(name[0]) + str(i))
		self.list = {}

	def print(self):
		# for key, value in self.list:
		# 	print("PC:", key, "destiny", value)
		for key in self.list.keys():
			print("PC:", key, "destiny:", self.list[key][0], "prediction:", self.list[key][1])

	def push(PC, destiny, prediction):
		self.list[str(PC)] = [destiny, prediction]

	def pop(PC):
		del self.list[str(PC)]