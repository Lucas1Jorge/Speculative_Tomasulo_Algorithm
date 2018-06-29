from buffer import *

class ROB(buffer):
	def __init__(self, name, max_size, list_data_bus, Tomasulo):
		super().__init__(name, max_size, list_data_bus)
		self.destiny = [""] * max_size
		self.value = [""] * max_size
		self.ready = [False] * max_size
		self.RS_Busy = ["False"] * 32
		self.RS_reorder = [""] * 32
		self.Tomasulo = Tomasulo

	def print(self):
		for i in range(self.max_size):
			print(self.ID[i], self.name, self.busy[i], self.list[i], self.state[i], self.destiny[i], self.value[i], self.size, "empty:", self.empty())

	def push(self, info):
		if not self.full():
			if len(info[-1]) > 0 and info[-1] != "mark":
				for i in range(self.max_size):
					if len(self.list[i]) > 0:
						for j in range(1, len(self.list[i])):
							if self.list[i][j] == info[0]:
								self.list[i][j] = info[-1]
					# if self.list[i][0] == "BEQ" or self.list[i][0] == "BNE" or self.list[i][0] == "BLE":
					# 	if self.list[i][1] == info[0]:
					# 		self.list[i][1] = info[-1]
					# 	if self.list[i][2] == info[0]:
					# 		self.list[i][2] = info[-1]

					# elif self.list[i][0] == "SW":

					# if self.receivers[i].Qj[pos] == info[0]:
					# 	self.receivers[i].Qj[pos] = ""
					# 	self.receivers[i].Vj[pos] = info[-1]
					# 	if self.receivers[i].list[pos][0] == "SW":
					# 		self.receivers[i].list[pos][1] = info[-1]
					# 	else:
					# 		self.receivers[i].list[pos][2] = info[-1]
					# if self.receivers[i].Qk[pos] == info[0]:
					# 	self.receivers[i].Qk[pos] = ""
					# 	self.receivers[i].Vk[pos] = info[-1]
					# 	self.receivers[i].list[pos][3] = info[-1]


			while len(self.list[self.end]) > 0: self.end = (self.end + 1) % self.max_size
			self.list[self.end] = info

			if not self.empty() and (self.top()[0] == "BEQ" or self.top()[0] == "BNE" or self.top()[0] == "BLE") and info[-1] == "mark":
				self.state[self.end] = "Writing"
			else:
				self.state[self.end] = "Consolidating"

			if len(info) > 0 and info[0][0] != "S":
				self.destiny[self.end] = info[1]
				self.RS_Busy[int(self.destiny[self.end])] = True
				self.value[self.end] = info[-1]
			
			self.end = (self.end + 1) % self.max_size
			self.size += 1

	def pop(self):
		if self.size > 0:
			ans = copy_list(self.list[self.start])
			self.busy[self.start] = False
			self.list[self.start].clear()
			self.state[self.start] = ""
			self.value[self.start] = ""
			self.ready[self.start] = False
			if self.destiny[self.start]:
				self.RS_Busy[int(self.destiny[self.start])] = False
				self.RS_reorder[int(self.destiny[self.start])] = ""
			self.destiny[self.start] = ""
			self.start = (self.start + 1) % self.max_size
			self.size -= 1
			return ans

	def clock(self, register_bank):
		if self.top() and len(self.top()) > 0 and self.top()[-1] == "mark":
			self.Tomasulo.register_bank.push(copy_list(self.top()))
			self.pop()

		if self.top() and ((self.top()[0] == "BEQ") or (self.top()[0] == "BNE") or (self.top()[0] == "BLE")):
			if str.isnumeric(self.top()[1]) and str.isnumeric(self.top()[2]):
				prediction = True
				if self.top()[0] == "BEQ":
					if self.top()[1] == self.top()[2]:
						self.Tomasulo.PC += int(self.top()[3])
					# else:
						prediction = False
				if self.top()[0] == "BNE":
					if self.top()[1] != self.top()[2]:
						self.Tomasulo.PC += int(self.top()[3])
					# else:
						prediction = False
				if self.top()[0] == "BLE":
					if self.top()[1] <= self.top()[2]:
						self.Tomasulo.PC = int(self.top()[3])
					# else:
						prediction = False

				if prediction == False:
					for i in range(self.max_size):
						if self.state[i] != "Consolidating":
							self.busy[i] = False
							self.list[i].clear()
							self.state[i] = ""
							self.destiny[i] = ""
							self.value[i] = ""
							self.start = 0
							self.size = 0
					for i in range(32):
						self.RS_Busy[i] = False
						self.RS_reorder[i] = ""

				self.pop()

		else:
			if not self.empty():
				instruction = copy_list(self.top())

				if instruction[0][0] == "S":
					address = int(instruction[2]) + int(instruction[3])
					self.Tomasulo.memory[address] = instruction[1]
					self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])
					self.pop()
				else:
					register_bank.push(instruction)
					# register_bank.registers[int(self.destiny[self.start])].Vi = self.value[self.start]
					# register_bank.registers[int(self.destiny[self.start])].Qi = ""
					self.pop()

				if instruction[0][0] == "L":
					address = int(instruction[2]) + int(instruction[3])
					self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])

				# for i in range(len(self.list_data_bus)):
				# 	self.list_data_bus[i].send(instruction)

				# self.pop()

				# global concluded_instructions
				# Tomasulo.concluded_instructions += 1