from buffer import *

class ROB(buffer):
	def __init__(self, name, max_size, list_data_bus, Tomasulo):
		super().__init__(name, max_size, list_data_bus)
		self.destiny = [""] * max_size
		self.value = [""] * max_size
		self.ready = [False] * max_size
		self.RS_Busy = [False] * 32
		self.RS_reorder = [""] * 32
		self.Tomasulo = Tomasulo
		self.PC = [""] * max_size
		self.jump = [""] * max_size

	def print(self):
		for i in range(self.max_size):
			print(self.ID[i], self.name, self.busy[i], self.list[i], self.state[i], self.destiny[i], self.value[i], self.size, "PC:", self.PC[i], "jump:", self.jump[i])

	def push(self, info):
		if not self.full():
			if info[0] == "BEQ" or info[0] == "BLE" or info[0] == "BNE":
				while len(self.list[self.end]) > 0: self.end = (self.end + 1) % self.max_size
				self.list[self.end] = info
				self.PC[self.end] = str(self.Tomasulo.PC)

				self.end = (self.end + 1) % self.max_size
				self.size += 1

			elif len(info) > 0 and info[-1] == "mark":
				while len(self.list[self.end]) > 0: self.end = (self.end + 1) % self.max_size
				self.list[self.end] = info
				self.state[self.end] = "Not Ready"

				self.ready[self.end] = False
				self.busy[self.end] = True
				if info[0][0] != "S":
					self.destiny[self.end] = info[1]
					self.RS_Busy[int(self.destiny[self.end])] = True
					self.RS_reorder[int(info[1])] = str(self.end)
				print("mark:", info)
				# self.Tomasulo.register_bank.push(info)

				self.end = (self.end + 1) % self.max_size
				self.size += 1

			elif len(info) > 0:
				found = False
				ID = ""
				for i in range(self.max_size):
					if len(self.list[i]) > 0:
						if self.list[i][0] == info[0] and self.list[i][-1] == "mark":
							self.list[i] = copy_list(info)
							found = True
							ID = self.ID[i]
							self.state[i] = "Consolidating"
							self.ready[i] = True
							break

				if found:
					for i in range(self.max_size):
						if len(self.list[i]) > 0:
							for j in range(1, len(self.list[i])):
								# if self.list[i][j] == info[0]:
								if self.list[i][j] == ID:
									self.list[i][j] = info[-1]
								self.ready[i] = True

	def Ready(self, pos):
		if len(self.list[pos]) == 0:
			return False
		for i in range(1, len(self.list[pos])):
			if not str.isnumeric(self.list[pos][i]):
				return False
		return True

	def Value(self, pos):
		if len(self.list[pos]) == 0:
			return None
		if not str.isnumeric(self.list[pos][-1]):
			return None
		return self.list[pos][-1]

	def pop(self):
		if self.size > 0:
			ans = copy_list(self.list[self.start])
			self.busy[self.start] = False
			self.list[self.start].clear()
			self.state[self.start] = ""
			self.value[self.start] = ""
			self.PC[self.start] = ""
			self.jump[self.start] = ""
			self.ready[self.start] = False
			if self.destiny[self.start]:
				if int(self.RS_reorder[int(self.destiny[self.start])]) == int(self.start):
					# print("a:", self.RS_reorder[int(self.destiny[self.start])], "b:", self.start)
					self.RS_Busy[int(self.destiny[self.start])] = False
					self.RS_reorder[int(self.destiny[self.start])] = ""
			self.destiny[self.start] = ""
			self.start = (self.start + 1) % self.max_size
			self.size -= 1
			return ans

	def clock(self, register_bank):
		if self.top() and ((self.top()[0] == "BEQ") or (self.top()[0] == "BNE") or (self.top()[0] == "BLE")):
			if str.isnumeric(self.top()[1]) and str.isnumeric(self.top()[2]):
				jumping = "not"
				PC = 0
				if self.top()[0] == "BEQ":
					if self.top()[1] == self.top()[2]:
						PC = int(self.PC[self.start]) + int(self.top()[3])
						jumping = "jump"
				if self.top()[0] == "BNE":
					if self.top()[1] != self.top()[2]:
						PC = int(self.PC[self.start]) + int(self.top()[3])
						jumping = "jump"
				if self.top()[0] == "BLE":
					if int(self.top()[1]) <= int(self.top()[2]):
						PC = int(self.top()[3])
						jumping = "jump"

				if jumping == "jump" and self.jump[self.start] != "jump" or \
					jumping == "not" and self.jump[self.start] == "jump":
					for i in range(self.max_size):
						self.busy[i] = False
						self.list[i].clear()
						self.state[i] = ""
						self.destiny[i] = ""
						self.value[i] = ""
						self.PC[i] = ""
						self.jump[i] = ""
						self.start = 0
						self.size = 0
					for i in range(32):
						self.RS_Busy[i] = False
						self.RS_reorder[i] = ""

					for i in range(self.Tomasulo.instructions_unity.max_size):
						if len(self.Tomasulo.instructions_unity.list[i]) > 0:
							self.Tomasulo.instructions_unity.clear(i)
					for i in range(self.Tomasulo.load_store.max_size):
						for j in range(1,4):
							if self.Tomasulo.load_store.list[i] and self.Tomasulo.load_store.list[i][j][0] == "R":
								self.Tomasulo.load_store.clear(i)
								print("Cleaned load_store")
					for i in range(self.Tomasulo.add_sub.max_size):
						for j in range(1,4):
							if self.Tomasulo.add_sub.list[i] and self.Tomasulo.add_sub.list[i][j][0] == "R":
								self.Tomasulo.add_sub.clear(i)
								print("Cleaned add_sub")
					for i in range(self.Tomasulo.mult.max_size):
						for j in range(1,4):
							if self.Tomasulo.mult.list[i] and self.Tomasulo.mult.list[i][j][0] == "R":
								self.Tomasulo.mult.clear(i)
								print("Cleaned mult")

				if jumping == "jump":
					# if not str(self.PC[self.start]) in self.Tomasulo.destiny_buffer.list or \
					# jumping != self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])][1] or \
					# int(self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])][0]) != PC:
					if self.jump[self.start] != "jump":
						self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])] = [str(PC), "jump"]
						self.Tomasulo.PC = PC

				elif jumping == "not":
					# if (str(self.PC[self.start]) in self.Tomasulo.destiny_buffer.list and \
					# jumping != self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])][1]):
					if self.jump[self.start] == "jump":
						# print(jumping)
						# print(self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])][1])
						self.Tomasulo.PC = int(self.PC[self.start])
						# del self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])]
						self.Tomasulo.destiny_buffer.list[str(self.PC[self.start])] = [str(self.PC[self.start]), "not"]

				self.pop()

		elif not self.empty() and not self.Ready(self.start):
			return

		else:
			if not self.empty():
				instruction = copy_list(self.top())

				if instruction[0][0] == "S":
					address = int(instruction[2]) + int(instruction[3])
					self.Tomasulo.memory[address] = instruction[1]
					self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])

				else:
					if instruction[0][0] == "L":
						address = int(instruction[2]) + int(instruction[3])
						instruction[-1] = self.Tomasulo.memory[address]
						self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])
					
					self.Tomasulo.register_bank.push(instruction)
					# register_bank.registers[int(self.destiny[self.start])].Vi = self.Value(self.start)
					# register_bank.registers[int(self.destiny[self.start])].Qi = ""
				
				for i in range(self.Tomasulo.load_store.max_size):
					for j in range(1,4):
						# if self.Tomasulo.load_store.list[i] and self.Tomasulo.load_store.list[i][j] == instruction[0]:
						if self.Tomasulo.load_store.list[i] and self.Tomasulo.load_store.list[i][j] == self.ID[self.start]:
							self.Tomasulo.load_store.list[i][j] = str(instruction[-1])
							if j == 1 or j == 2:
								self.Tomasulo.load_store.Vj[i] = instruction[-1]
								self.Tomasulo.load_store.Qj[i] = ""
							if j == 3:
								self.Tomasulo.load_store.Vk[i] = instruction[-1]
								self.Tomasulo.load_store.Qk[i] = ""
				for i in range(self.Tomasulo.add_sub.max_size):
					for j in range(1,4):
						# if self.Tomasulo.add_sub.list[i] and self.Tomasulo.add_sub.list[i][j] == instruction[0]:
						if self.Tomasulo.add_sub.list[i] and self.Tomasulo.add_sub.list[i][j] == self.ID[self.start]:
							self.Tomasulo.add_sub.list[i][j] = str(instruction[-1])
							if j == 1 or j == 2:
								self.Tomasulo.add_sub.Vj[i] = instruction[-1]
								self.Tomasulo.add_sub.Qj[i] = ""
							if j == 3:
								self.Tomasulo.add_sub.Vk[i] = instruction[-1]
								self.Tomasulo.add_sub.Qk[i] = ""
				for i in range(self.Tomasulo.mult.max_size):
					for j in range(1,4):
						# if self.Tomasulo.mult.list[i] and self.Tomasulo.mult.list[i][j] == instruction[0]:
						if self.Tomasulo.mult.list[i] and self.Tomasulo.mult.list[i][j] == self.ID[self.start]:
							self.Tomasulo.mult.list[i][j] = str(instruction[-1])
							if j == 1 or j == 2:
								self.Tomasulo.mult.Vj[i] = instruction[-1]
								self.Tomasulo.mult.Qj[i] = ""
							if j == 3:
								self.Tomasulo.mult.Vk[i] = instruction[-1]
								self.Tomasulo.mult.Qk[i] = ""

				self.pop()


				# global concluded_instructions
				# Tomasulo.concluded_instructions += 1