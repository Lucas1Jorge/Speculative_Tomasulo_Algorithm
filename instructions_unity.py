from buffer import *

class instructions_unity(buffer):
	def __init__(self, name, max_size, list_data_bus, Tomasulo):
		super().__init__(name, max_size, list_data_bus)
		self.max_size = max_size
		self.Tomasulo = Tomasulo

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

		if instruction[0] != "SW":
			self.Tomasulo.ROB.RS_Busy[int(instruction[1])] = True
			self.Tomasulo.ROB.RS_reorder[int(instruction[1])] = str(self.Tomasulo.ROB.end)

		register_bank.push(instruction)

	def clock(self, register_bank):
		if not self.empty() and self.all_data_bus_available():
			if self.top() and self.top()[0] == "JMP":
				self.Tomasulo.PC = int(self.top()[3])
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
					if self.top()[0] == "BEQ":
						if self.Vj[self.start] == self.Vk[self.start]:
							self.Tomasulo.PC += int(self.top()[3])
					if self.top()[0] == "BNE":
						if self.Vj[self.start] != self.Vk[self.start]:
							self.Tomasulo.PC += int(self.top()[3])
					if self.top()[0] == "BLE":
						if int(self.Vj[self.start]) <= int(self.Vk[self.start]):
							self.Tomasulo.PC = int(self.top()[3])
					self.pop()

			# if self.top() and ((self.top()[0] == "BEQ") or (self.top()[0] == "BNE") or (self.top()[0] == "BLE")):
			# 	if len(register_bank.registers[int(self.top()[1])].Qi) == 0:
			# 		self.top()[1] = str(register_bank.registers[int(self.top()[1])].Vi)
			# 	else:
			# 		self.top()[1] = register_bank.registers[int(self.top()[1])].Qi

			# 	if len(register_bank.registers[int(self.top()[2])].Qi) == 0:
			# 		self.top()[2] = str(register_bank.registers[int(self.top()[2])].Vi)
			# 	else:
			# 		self.top()[2] = register_bank.registers[int(self.top()[2])].Qi

			# 	if str.isnumeric(self.top()[1]) and str.isnumeric(self.top()[2]):
			# 		if self.top()[0] == "BEQ":
			# 			if self.top()[1] == self.Vtop()[2]:
			# 				self.Tomasulo.PC += int(self.top()[3])
			# 		if self.top()[0] == "BNE":
			# 			if self.top()[1] != self.top()[2]:
			# 				self.Tomasulo.PC += int(self.top()[3])
			# 		if self.top()[0] == "BLE":
			# 			if int(self.top()[1]) <= int(self.top()[2]):
			# 				self.Tomasulo.PC = int(self.top()[3])

			# 	else:
			# 		info = copy_list(self.top())
			# 		self.Tomasulo.ROB.push(info)
				
			# 	self.pop()

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
				self.issue(self.Tomasulo.register_bank, self.Tomasulo.add_sub, self.Tomasulo.mult, self.Tomasulo.load_store)
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
					self.issue(self.Tomasulo.register_bank, self.Tomasulo.add_sub, self.Tomasulo.mult, self.Tomasulo.load_store)
				self.pop()

			elif self.top() and self.top()[0] == "NOP":
				self.pop()