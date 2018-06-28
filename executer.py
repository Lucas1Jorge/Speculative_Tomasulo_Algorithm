from functions import *

class executer:
	def __init__(self, list_data_bus, Tomasulo):
		self.cycles = 0
		self.instruction = []
		self.list_data_bus = list_data_bus
		self.n1 = None
		self.n2 = None
		self.Tomasulo = Tomasulo

	def execute(self, instruction, ID):
		if not instruction: return

		self.instruction = instruction

		if instruction[0] == "LW" or instruction[0] == "SW": self.cycles = 4
		elif instructions[0] == "MUL": self.cycles = 3
		elif instruction[0] == "DIV": self.cycles = 5
		else: self.cycles = 1

		self.ID = ID

	def busy(self):
		return len(self.instruction) > 0

	def get_result(self, register_bank):
		return 0

	def pop(self):
		if len(self.instruction) > 0:
			ans = copy_list(self.instruction)
			self.instruction.clear()
			return ans

	def all_data_bus_available(self):
		flag = 1
		for data_bus in self.list_data_bus:
			if not data_bus.available():
				flag = 0
		return flag == 1

	def clock(self, register_bank):
		if len(self.instruction) > 0:
			instruction = copy_list(self.instruction)

			if self.cycles > 0:
				self.cycles -= 1

			if self.cycles == 0:
				if self.all_data_bus_available():
					for i in range(len(self.list_data_bus)):
						instruction[-1] = str(self.get_result(register_bank))
						instruction[0] = self.ID
						self.list_data_bus[i].send(instruction)
					
					self.pop()

					# global concluded_instructions
					self.Tomasulo.concluded_instructions += 1


class loader(executer):
	def __init__(self, list_data_bus, Tomasulo):
		super().__init__(list_data_bus, Tomasulo)

	def get_result(self, register_bank):
		if self.instruction[0] == "LW":
			address = int(self.instruction[2]) + int(self.instruction[3])
			self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])
			return self.Tomasulo.memory[address]
		elif self.instruction[0] == "SW":
			address = int(self.instruction[2]) + int(self.instruction[3])
			self.Tomasulo.memory[address] = self.instruction[1]
			self.Tomasulo.recently_used_memory.push([address, self.Tomasulo.memory[address]])

	def execute(self, instruction, ID):
		self.instruction = instruction
		self.cycles = 4
		self.ID = ID

	def clock(self, register_bank):
		if len(self.instruction) > 0:

			if self.cycles > 0:
				self.cycles -= 1

			if self.cycles == 0:
				if self.all_data_bus_available():
					instruction = copy_list(self.instruction)

					if instruction[0] == "LW":
						for i in range(len(self.list_data_bus)):
							instruction[-1] = str(self.get_result(register_bank))
							instruction[0] = self.ID
							self.list_data_bus[i].send(instruction)
					elif instruction[0] == "SW":
						self.get_result(register_bank)

					self.pop()

					# global concluded_instructions
					self.Tomasulo.concluded_instructions += 1


class adder(executer):
	def __init__(self, list_data_bus, Tomasulo):
		super().__init__(list_data_bus, Tomasulo)

	def get_result(self, register_bank):
		if self.instruction[0] == "ADD" or self.instruction[0] == "ADDI":
			return int(self.instruction[2]) + int(self.instruction[3])
		elif self.instruction[0] == "SUB":
			return int(self.instruction[2]) - int(self.instruction[3])

	def execute(self, instruction, ID):
		self.instruction = instruction
		self.cycles = 1
		self.ID = ID


class multiplier(executer):
	def __init__(self, list_data_bus, Tomasulo):
		super().__init__(list_data_bus, Tomasulo)

	def get_result(self, register_bank):
		return int(self.instruction[2]) * int(self.instruction[3])

	def execute(self, instruction, ID):
		self.instruction = instruction
		if instruction[0] == "MUL": self.cycles = 3
		elif instruction[0] == "DIV": self.cycles = 5
		self.ID = ID