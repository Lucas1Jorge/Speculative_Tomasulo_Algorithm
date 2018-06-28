from functions import *

class buffer:
	def __init__(self, name, max_size, list_data_bus):
		self.busy = [False] * max_size
		self.list = [[]] * max_size
		self.state = [""] * max_size
		self.Qj = [""] * max_size
		self.Qk = [""] * max_size
		self.Vj = [""] * max_size
		self.Vk = [""] * max_size
		self.name = name
		self.start = 0
		self.end = 0
		self.size = 0
		self.max_size = max_size
		self.list_data_bus = list_data_bus
		self.ID = []
		for i in range(max_size):
			self.ID.append(str.upper(name[0]) + str(i))

	def push(self, obj):
		if not self.full():
			while len(self.list[self.end]) > 0: self.end = (self.end + 1) % self.max_size
			self.list[self.end] = obj
			if self.name != "instructions_unity":
				self.state[self.end] = "issued"
			
			if str.isnumeric(obj[3]): self.Vk[self.end] = obj[3]
			else: self.Qk[self.end] = obj[3]

			if obj[0] == "SW" or obj[1] == "LW":
				if str.isnumeric(obj[1]): self.Vj[self.end] = obj[1]
				else: self.Qj[self.end] = obj[1]
			else:
				if str.isnumeric(obj[2]): self.Vj[self.end] = obj[2]
				else: self.Qj[self.end] = obj[2]
			
			self.end = (self.end + 1) % self.max_size
			self.size += 1

	def pop(self):
		if self.size > 0:
			ans = copy_list(self.list[self.start])
			self.busy[self.start] = False
			self.list[self.start].clear()
			self.Qj[self.start] = ""
			self.Qk[self.start] = ""
			self.Vj[self.start] = ""
			self.Vk[self.start] = ""
			self.state[self.start] = ""
			self.start = (self.start + 1) % self.max_size
			self.size -= 1
			return ans

	def top(self):
		if self.size > 0:
			while not self.list[self.start]: self.start = (self.start + 1) % self.max_size
			return self.list[self.start]

	def empty(self):
		return self.size == 0

	def full(self):
		return self.size >= self.max_size

	def add_data_bus(self, data_bus):
		self.list_data_bus.append(data_bus)

	def print(self):
		for i in range(self.max_size):
			print(self.ID[i], self.name, self.list[i], self.state[i], self.Vj[i], self.Vk[i], self.Qj[i], self.Qk[i], self.size)

	def all_data_bus_available(self):
		flag = 1
		for data_bus in self.list_data_bus:
			if not data_bus.available():
				flag = 0
		return flag == 1


class reservation_station(buffer):
	def __init__(self, name, max_size, list_data_bus, executer):
		super().__init__(name, max_size, list_data_bus)
		self.executer = executer
		self.marked = 0

	def print(self):
		for i in range(self.max_size):
			print(self.ID[i], self.name, self.busy[i], self.list[i], self.state[i], self.Vj[i], self.Vk[i], self.Qj[i], self.Qk[i], self.executer.cycles, self.size)

	def clock(self, register_bank):
		if not self.executer.busy() and self.busy[self.start] == 1:
			self.busy[self.start] = False
			self.state[self.start] = ""
			self.size -= 1
			# self.pop()

		if not self.executer.busy() and self.top():
			# if self.instruction[0] == "SW":

			if len(self.Qj[self.start]) == 0 and len(self.Qk[self.start]) == 0:
				self.executer.execute(self.top(), self.ID[self.start])
				self.busy[self.start] = True
				self.state[self.start] = "Executing"

		self.executer.clock(register_bank)

		if len(self.list[self.start]) == 0:
			self.Vj[self.start] = ""
			self.Vk[self.start] = ""
			self.Qj[self.start] = ""
			self.Qk[self.start] = ""


class load_store(buffer):
	def __init__(self, name, max_size, list_data_bus, executer):
		super().__init__(name, max_size, list_data_bus)
		self.executer = executer
		self.marked = 0

	def print(self):
		for i in range(self.max_size):
			print(self.ID[i], self.name, self.busy[i], self.list[i], self.state[i], self.Vj[i], self.Vk[i], self.Qj[i], self.Qk[i], self.executer.cycles, self.size)

	def clock(self, register_bank):
		if not self.executer.busy() and self.busy[self.start] == 1:
			self.busy[self.start] = False
			self.state[self.start] = ""
			self.size -= 1
			# self.pop()

		if not self.executer.busy() and self.top():
			if len(self.Qj[self.start]) == 0 and len(self.Qk[self.start]) == 0:
				self.executer.execute(self.top(), self.ID[self.start])
				self.busy[self.start] = True
				self.state[self.start] = "Executing"

		self.executer.clock(register_bank)

		if len(self.list[self.start]) == 0:
			self.Vj[self.start] = ""
			self.Vk[self.start] = ""
			self.Qj[self.start] = ""
			self.Qk[self.start] = ""