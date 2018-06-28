import threading
import sys
import time
import queue
import tomasuloui
from PyQt5 import QtCore, QtGui, QtWidgets


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


def copy_list(list):
	ans = []
	for el in list:
		ans.append(el)
	return ans

class data_bus:
	def __init__(self, name):
		self.receivers = []
		self.name = name
		self.queue = []
		self.sending = False
		self.i = 0

	def print(self):
		print(self.queue)

	def add_receivers(self, list):
		for i in range(len(list)):
			self.receivers.append(list[i])

	def send(self, info):
		if len(info) == 4: info.append("")
		self.queue.append(info)

	def available(self):
		flag = 1
		for receiver in self.receivers:
			if isinstance(receiver, buffer) and receiver.full() and self.name != "common_data_bus":
				flag = 0
		return flag == 1

	def clock(self):
		if not self.sending:
			self.sending = True
			self.i = 0

		# for i in range(len(self.queue)):
		i = self.i
		if i < len(self.queue):
			info = self.queue[i]
			
			if info:
				for i in range(len(self.receivers)):
					if len(info[-1]) == 0:
						if (self.receivers[i].name == "mult" and info and info[0] == "MUL") \
							or (self.receivers[i].name == "div" and info and info[0] == "DIV") \
							or (self.receivers[i].name == "add_sub" and info and info[0] == "ADD") \
							or (self.receivers[i].name == "add_sub" and info and info[0] == "ADDI") \
							or (self.receivers[i].name == "add_sub" and info and info[0] == "SUB") \
							or (self.receivers[i].name == "load_store" and info and info[0] == "LW") \
							or (self.receivers[i].name == "load_store" and info and info[0] == "SW") \
							or (self.receivers[i].name == "register_bank"):
							self.receivers[i].push(info)
					elif self.receivers[i].name == "register_bank":
						self.receivers[i].push(info)
					elif isinstance(self.receivers[i], buffer):
						for pos in range(self.receivers[i].max_size):
							if self.receivers[i].Qj[pos] == info[0]:
								self.receivers[i].Qj[pos] = ""
								self.receivers[i].Vj[pos] = info[-1]
								if self.receivers[i].list[pos][0] == "SW":
									self.receivers[i].list[pos][1] = info[-1]
								else:
									self.receivers[i].list[pos][2] = info[-1]
							if self.receivers[i].Qk[pos] == info[0]:
								self.receivers[i].Qk[pos] = ""
								self.receivers[i].Vk[pos] = info[-1]
								self.receivers[i].list[pos][3] = info[-1]

				self.i += 1

		else:
			self.sending = False
			self.queue.clear()
			self.i = 0


class executer:
	def __init__(self, list_data_bus):
		self.cycles = 0
		self.instruction = []
		self.list_data_bus = list_data_bus
		self.n1 = None
		self.n2 = None

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

	def mark_destiny(self, source=None, destiny=None):
		if not self.instruction:
			instruction = []
			instruction.append(source)
			instruction.append(destiny)
			instruction.append("")
			instruction.append("")
			instruction.append("")

		else: instruction = copy_list(self.instruction)

		instruction[-1] = "mark"
		for i in range(len(self.list_data_bus)):
			self.list_data_bus[i].send(instruction)

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
					Tomasulo.concluded_instructions += 1


class loader(executer):
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

	def get_result(self, register_bank):
		if self.instruction[0] == "LW":
			address = int(self.instruction[2]) + int(self.instruction[3])
			Tomasulo.recently_used_memory.push([address, Tomasulo.memory[address]])
			return Tomasulo.memory[address]
		elif self.instruction[0] == "SW":
			address = int(self.instruction[2]) + int(self.instruction[3])
			Tomasulo.memory[address] = self.instruction[1]
			Tomasulo.recently_used_memory.push([address, Tomasulo.memory[address]])

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
					Tomasulo.concluded_instructions += 1


class adder(executer):
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

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
	def __init__(self, list_data_bus):
		super().__init__(list_data_bus)

	def get_result(self, register_bank):
		return int(self.instruction[2]) * int(self.instruction[3])

	def execute(self, instruction, ID):
		self.instruction = instruction
		if instruction[0] == "MUL": self.cycles = 3
		elif instruction[0] == "DIV": self.cycles = 5
		self.ID = ID


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

			if obj[1] == "SW" or obj[1] == "LW":
				if str.isnumeric(obj[1]): self.Vj[self.end] = obj[1]
				else: self.Qj[self.end] = obj[1]
			else:
				if str.isnumeric(obj[2]): self.Vj[self.end] = obj[2]
				else: self.Qj[self.end] = obj[2]
			
			# if str.isnumeric(obj[2]): self.Vj[self.end] = obj[2]
			# else: self.Qj[self.end] = obj[2]
			
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


class instructions_unity(buffer):
	def __init__(self, name, max_size, list_data_bus):
		super().__init__(name, max_size, list_data_bus)
		self.max_size = max_size

	def issue(self, register_bank, add_sub, mult, load_store):
		if not self.top(): return

		instruction = copy_list(self.top())

		instruction[-1] = "mark"

		if instruction[0] == "ADD" or instruction[0] == "ADDI" or instruction[0] == "SUB":
			instruction[0] = add_sub.ID[add_sub.end]

		elif instruction[0] == "MUL":
			instruction[0] = mult.ID[mult.end]

		elif instruction[0] == "SW" or instruction[0] == "LW":
			instruction[0] = load_store.ID[load_store.end]

		register_bank.push(instruction)

	def clock(self, register_bank):
		if not self.empty() and self.all_data_bus_available():
			if self.top() and self.top()[0] == "JMP":
				Tomasulo.PC = int(self.top()[3])
				self.pop()
				
			if self.top() and ((self.top()[0] == "BEQ") or (self.top()[0] == "BNE") or (self.top()[0] == "BLE")):
				if len(register_bank.registers[int(self.top()[1])].Qi) == 0:
					self.Vj[self.start] = register_bank.registers[int(self.top()[1])].Vi
					self.Qj[self.start] = ""
				else:
					self.Qj[self.start] = register_bank.registers[int(self.top()[1])].Qi

				if len(register_bank.registers[int(self.top()[2])].Qi) == 0:
					self.Vk[self.start] = register_bank.registers[int(self.top()[2])].Vi
					self.Qk[self.start] = ""
				else:
					self.Qk[self.start] = register_bank.registers[int(self.top()[2])].Qi

				if len(self.Qj[self.start]) == 0 and len(self.Qk[self.start]) == 0:
					# global PC
					global labels
					if self.top()[0] == "BEQ":
						if self.Vj[self.start] == self.Vk[self.start]:
							Tomasulo.PC += int(self.top()[3])
							# PC = labels[self.top()[3]]
					if self.top()[0] == "BNE":
						if self.Vj[self.start] != self.Vk[self.start]:
							Tomasulo.PC += int(self.top()[3])
							# PC = labels[self.top()[3]]
					if self.top()[0] == "BLE":
						if int(self.Vj[self.start]) <= int(self.Vk[self.start]):
							Tomasulo.PC = int(self.top()[3])
							# PC = labels[self.top()[3]]
					self.pop()

			elif self.top() and (self.top()[0] == "ADD" or self.top()[0] == "ADDI" or self.top()[0] == "SUB" or self.top()[0] == "MUL"):
				if len(register_bank.registers[int(self.top()[2])].Qi) == 0:
					self.Vj[self.start] = int(register_bank.registers[int(self.top()[2])].Vi)
					self.Qj[self.start] = ""
				elif len(self.Qj[self.start]) == 0 and register_bank.registers[int(self.top()[2])].Qi != self.top()[0]:
					self.Qj[self.start] = register_bank.registers[int(self.top()[2])].Qi

				if self.top()[0] == "ADD" or self.top()[0] == "SUB" or self.top()[0] == "MUL" or self.top()[0] == "LW" or self.top()[0] == "SW":
					if len(register_bank.registers[int(self.top()[3])].Qi) == 0:
						self.Vk[self.start] = int(register_bank.registers[int(self.top()[3])].Vi)
						self.Qk[self.start] = ""
					elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[3])].Qi != self.top()[0]:
						self.Qk[self.start] = register_bank.registers[int(self.top()[3])].Qi

				elif self.top()[0] == "ADDI":
					self.Vk[self.start] = int(self.top()[3])
					self.Qk[self.start] = ""
				for i in range(len(self.list_data_bus)):
					info = copy_list(self.top())
					if len(self.Qj[self.start]) == 0: info[2] = str(self.Vj[self.start])
					else: info[2] = str(self.Qj[self.start])
					if len(self.Qk[self.start]) == 0: info[3] = str(self.Vk[self.start])
					else: info[3] = str(self.Qk[self.start])
					self.list_data_bus[i].send(info)
				self.issue(Tomasulo.register_bank, Tomasulo.add_sub, Tomasulo.mult, Tomasulo.load_store)
				self.pop()

			elif self.top() and (self.top()[0] == "SW" or self.top()[0] == "LW"):
				if len(register_bank.registers[int(self.top()[3])].Qi) == 0:
					self.Vk[self.start] = int(register_bank.registers[int(self.top()[3])].Vi)
					self.Qk[self.start] = ""
				elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[3])].Qi != self.top()[0]:
					self.Qk[self.start] = register_bank.registers[int(self.top()[3])].Qi

				if self.top()[0] == "SW":
					if len(register_bank.registers[int(self.top()[1])].Qi) == 0:
						self.Vj[self.start] = int(register_bank.registers[int(self.top()[1])].Vi)
						self.Qj[self.start] = ""
					elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[1])].Qi != self.top()[0]:
						self.Qj[self.start] = register_bank.registers[int(self.top()[1])].Qi

				for i in range(len(self.list_data_bus)):
					info = copy_list(self.top())

					if self.top()[0] == "SW":
						if len(self.Qj[self.start]) == 0: info[1] = str(self.Vj[self.start])
						else: info[1] = str(self.Qj[self.start])

					if len(self.Qk[self.start]) == 0: info[3] = str(self.Vk[self.start])
					else: info[3] = str(self.Qk[self.start])

					self.list_data_bus[i].send(info)
				if self.top()[0] == "LW":
					self.issue(Tomasulo.register_bank, Tomasulo.add_sub, Tomasulo.mult, Tomasulo.load_store)
				self.pop()

			elif self.top() and self.top()[0] == "NOP":
				self.pop()


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


def bin_to_int(b):
	ans = 0
	for i in range(len(b)-1, -1, -1):
		ans += int(b[i]) * 2**(len(b) - 1 - i)
	return str(ans)


def read_binary(Dict, instruction):
	ans = []
	if Dict[instruction[:6]] == "R":
		ans.append(Dict["R" + instruction[26:32]])
		ans.append(bin_to_int(instruction[16:21]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[11:16]))
		ans.append("")

	else:
		ans.append(Dict[instruction[:6]])
		ans.append(bin_to_int(instruction[11:16]))
		ans.append(bin_to_int(instruction[6:11]))
		ans.append(bin_to_int(instruction[16:32]))
		ans.append("")

	if ans[0] == "BEQ" or ans[0] == "BNE" or ans[0] == "BLE":
		ans[1], ans[2] = ans[2], ans[1]
	if ans[0] == "LW" or ans[0] == "SW":
		ans[2], ans[3] = ans[3], ans[2]

	return ans


def read_assembly(Dict, instruction):
	ans = []
	instruction = instruction[:-1]

	if instruction[0] == 'P':
		ans.append("P")
		ans.append(instruction[1:-1])
		return ans

	I_R = instruction.split(" ")
	ans.append(I_R[0])
	R = I_R[1].split(",")
	ans.append(R[0][1:])

	if ans[0] == "LW" or ans[0] == "SW":
		R = R[-1].split("(")
		ans.append(R[0])
		ans.append(R[1][1:-1])
	else:
		ans.append(R[1][1:])
		if R[2][0] == 'R' or R[2][0] == 'P':
			R[2] = R[2][1:]
		ans.append(R[2])

	return ans



class Tomasulo:
	# Setting up Graphic Interface:
	def __init__(self, file):
		# Global variables
		self.memory = []
		self.clocks = 0	
		self.PC = 0
		self.concluded_instructions = 0
		self.recently_used_memory = recently_used_memory()
		self.labels = {}

		self.app = QtWidgets.QApplication(sys.argv)
		self.MainWindow = QtWidgets.QMainWindow()
		self.ui = tomasuloui.Ui_MainWindow()
		self.ui.setupUi(self.MainWindow)
		self.ui.set_Tomasulo(self)
		self.MainWindow.show()
		# sys.exit(app.exec_())


		Dict = {
			"000000": "R",
			"R100000": "ADD",
			"R011000": "MUL",
			"R000000": "NOP",
			"R100010": "SUB",
			"001000": "ADDI",
			"000101": "BEQ",
			"000111": "BLE",
			"000100": "BNE",
			"000010": "JMP",
			"100011": "LW",
			"101011": "SW"
		}	
		

		self.instructions = []

		# with open('benchmark.txt') as file_in:
		# with open('input.txt') as file_in:
		with open(file) as file_in:
			for line in file_in:
				if line[0] == '\n':
					print()
					break
				if line[0] == ';': continue
				self.instructions.append(read_binary(Dict, line))
				# instructions.append(read_assembly(Dict, line))
				print(self.instructions[-1])


		self.register_bank = register_bank("register_bank")


		self.common_data_bus = data_bus("common_data_bus")
		self.common_data_bus.add_receivers([self.register_bank])

		self.loader = loader([self.common_data_bus])
		self.load_store = load_store("load_store", 5, [self.common_data_bus], self.loader)

		self.multiplier = multiplier([self.common_data_bus])
		self.mult = reservation_station("mult", 3, [self.common_data_bus], self.multiplier)

		self.adder = adder([self.common_data_bus])
		self.add_sub = reservation_station("add_sub", 3, [self.common_data_bus], self.adder)

		self.common_data_bus.add_receivers([self.load_store, self.mult, self.add_sub])	

		self.load_store_bus = data_bus("load_store_bus")
		self.load_store_bus.add_receivers([self.load_store])

		self.operations_bus = data_bus("operations_bus")
		self.operations_bus.add_receivers([self.mult, self.add_sub])

		self.instructions_unity = instructions_unity("instructions_unity", 6, [self.load_store_bus, self.operations_bus])

		self.memory = [0] * 4000
		self.clocks = 0
		self.PC = 0
		self.concluded_instructions = 0
		self.recently_used_memory = recently_used_memory()
		
	def play(self):
		print("RUM:")
		self.recently_used_memory.print()
		print()
		print("CLOCKS:", self.clocks)
		print("PC:", self.PC)
		print("# of concluded instructions:", self.concluded_instructions)
		self.CPI = 0
		if self.concluded_instructions != 0:
			self.CPI = round(self.clocks/self.concluded_instructions, 3)
			print("CPI:", self.CPI)
		self.clocks += 1

		if (not self.instructions_unity.full()) and (int(self.PC / 4) < len(self.instructions)):
			# if instructions[int(PC / 4)][0] == "P":
			# 	labels[instructions[int(PC / 4)][1]] = PC
			# else:
			# 	instructions_unity.push(copy_list(instructions[int(PC / 4)]))
			if self.instructions_unity.empty() or (self.instructions_unity.top()[0] != "BEQ" and self.instructions_unity.top()[0] != "BLE" and self.instructions_unity.top()[0] != "BNE"):
				self.instructions_unity.push(copy_list(self.instructions[int(self.PC / 4)]))
				self.PC += 4

		# self.common_data_bus.print()

		print()
		self.instructions_unity.print()
		self.load_store.print()
		self.mult.print()
		self.add_sub.print()
		self.register_bank.print()

		self.instructions_unity.clock(self.register_bank)
		self.load_store.clock(self.register_bank)
		self.mult.clock(self.register_bank)
		self.add_sub.clock(self.register_bank)

		self.load_store_bus.clock()
		self.operations_bus.clock()
		self.common_data_bus.clock()


		# Updating Graphic Interface:
		self.ui.update_register_bank(self.register_bank)
		self.ui.update_RUM(self.recently_used_memory)
		self.ui.update_Clock_Table([self.clocks, self.PC, self.concluded_instructions, self.CPI])


		pos = 0
		self.ui.update_Stations_Table(self.load_store, pos)
		pos += self.load_store.max_size

		self.ui.update_Stations_Table(self.add_sub, pos)
		pos += self.add_sub.max_size

		self.ui.update_Stations_Table(self.mult, pos)
		pos += self.mult.max_size


		return self.is_active()
	
	def is_active(self):
		if (self.PC / 4) >= len(self.instructions):
			active = False

			for i in range(self.instructions_unity.max_size):
				# print(self.instructions_unity.list[i])
				if self.instructions_unity.list[i] or self.instructions_unity.busy[i] or self.instructions_unity.state[i] == "Executing":
					active = True
			for i in range(self.load_store.max_size):
				# print(self.load_store.list[i])
				if self.load_store.size > 0 or self.load_store.executer.busy():
					active = True
			for i in range(self.mult.max_size):
				# print(self.mult.list[i])
				if self.mult.size > 0 or self.mult.executer.busy():
					active = True
			for i in range(self.add_sub.max_size):
				# print(self.add_sub.list[i])
				# if self.add_sub.list[i] or self.add_sub.busy[i] or self.add_sub.state[i] == "Executing":
				if self.add_sub.size > 0 or self.add_sub.executer.busy():
					active = True

			if not active: return False


		return True



if __name__ == "__main__":
	Tomasulo = Tomasulo(sys.argv[1])
	# thread_tomasulo = threading.Thread(target = Tomasulo.play)
	# thread_ui = threading.Thread(target = Tomasulo.MainWindow.show)

	# thread_tomasulo = QtCore.QThread()
	# thread_tomasulo.started.connect(Tomasulo.play)
	# thread_tomasulo.start()

	# thread_ui = QtCore.QThread()
	# thread_ui.started.connect(Tomasulo.MainWindow.show)
	# thread_ui.start()
	# thread_ui = QtCore.QThread(target = Tomasulo.MainWindow.show)

	# thread_tomasulo.join()
	# thread_ui.join()

	input()