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
			if info[0] == "SW":
				return
			else:
				if int(info[1]) != 0:
					self.registers[int(info[1])].Qi = info[0]
		elif info[0] == "SW":
			return
		else:
			if info[1] != 0 and info[0] == self.registers[int(info[1])].Qi:
				self.registers[int(info[1])].Vi = int(info[-1])
				self.registers[int(info[1])].Qi = ""