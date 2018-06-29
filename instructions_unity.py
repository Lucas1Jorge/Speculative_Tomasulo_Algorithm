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
			if instruction[0] == "SW":
				instruction[0] = "S" + load_store.ID[load_store.end][1:]
			elif instruction[0] == "LW":
				instruction[0] = load_store.ID[load_store.end]

		self.Tomasulo.ROB.push(instruction)

	def clock(self, register_bank):
		if not self.empty() and self.all_data_bus_available():
			if self.top() and self.top()[0] == "JMP":
				self.Tomasulo.PC = int(self.top()[3])
				self.pop()

			if self.top() and ((self.top()[0] == "BEQ") or (self.top()[0] == "BNE") or (self.top()[0] == "BLE")):
				if not self.Tomasulo.ROB.busy[int(self.top()[1])]:
					if len(register_bank.registers[int(self.top()[1])].Qi) == 0:
						self.Vj[self.start] = register_bank.registers[int(self.top()[1])].Vi
						self.Qj[self.start] = ""
					else:
						self.Qj[self.start] = register_bank.registers[int(self.top()[1])].Qi
				else:
					h = self.Tomasulo.ROB.RS_reorder[int(self.top()[1])]
					if self.Tomasulo.ROB.ready[h]:
						self.Vj[self.start] = self.Tomasulo.ROB.value[h]
						self.Qj[self.start] = ""
					else:
						self.Qj[self.start] = h

				if not self.Tomasulo.ROB.busy[int(self.top()[2])]:
					if len(register_bank.registers[int(self.top()[2])].Qi) == 0:
						self.Vk[self.start] = register_bank.registers[int(self.top()[2])].Vi
						self.Qk[self.start] = ""
					else:
						self.Qk[self.start] = register_bank.registers[int(self.top()[2])].Qi
				else:
					h = self.Tomasulo.ROB.RS_reorder[int(self.top()[2])]
					if self.Tomasulo.ROB.ready[h]:
						self.Vj[self.start] = self.Tomasulo.ROB.value[h]
						self.Qj[self.start] = ""
					else:
						self.Qj[self.start] = h

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
				else:
					pass
					# self.Tomasulo.ROB.push(copy_list(self.top()))

			elif self.top() and (self.top()[0] == "ADD" or self.top()[0] == "ADDI" or self.top()[0] == "SUB" or self.top()[0] == "MUL"):
				if not self.Tomasulo.ROB.busy[int(self.top()[2])]:
					if len(register_bank.registers[int(self.top()[2])].Qi) == 0:
						self.Vj[self.start] = int(register_bank.registers[int(self.top()[2])].Vi)
						self.Qj[self.start] = ""
					elif len(self.Qj[self.start]) == 0 and register_bank.registers[int(self.top()[2])].Qi != self.top()[0]:
						self.Qj[self.start] = register_bank.registers[int(self.top()[2])].Qi
				else:
					h = self.Tomasulo.ROB.RS_reorder[int(self.top()[2])]
					if self.Tomasulo.ROB.ready[h]:
						self.Vj[self.start] = self.Tomasulo.ROB.value[h]
						self.Qj[self.start] = ""
					else:
						self.Qj[self.start] = h

				if self.top()[0] == "ADD" or self.top()[0] == "SUB" or self.top()[0] == "MUL" or self.top()[0] == "LW" or self.top()[0] == "SW":
					if not self.Tomasulo.ROB.busy[int(self.top()[3])]:
						if len(register_bank.registers[int(self.top()[3])].Qi) == 0:
							self.Vk[self.start] = int(register_bank.registers[int(self.top()[3])].Vi)
							self.Qk[self.start] = ""
						elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[3])].Qi != self.top()[0]:
							self.Qk[self.start] = register_bank.registers[int(self.top()[3])].Qi
					else:
						h = self.Tomasulo.ROB.RS_reorder[int(self.top()[3])]
						if self.Tomasulo.ROB.ready[h]:
							self.Vk[self.start] = self.Tomasulo.ROB.value[h]
							self.Qk[self.start] = ""
						else:
							self.Qk[self.start] = h

				elif self.top()[0] == "ADDI":
					self.Vk[self.start] = int(self.top()[3])
					self.Qk[self.start] = ""

				if len(self.Qj[self.start]) == 0: self.top()[2] = str(self.Vj[self.start])
				else: self.top()[2] = str(self.Qj[self.start])
				if len(self.Qk[self.start]) == 0: self.top()[3] = str(self.Vk[self.start])
				else: self.top()[3] = str(self.Qk[self.start])
				for i in range(len(self.list_data_bus)):
					info = copy_list(self.top())
					self.list_data_bus[i].send(info)
				self.issue(self.Tomasulo.register_bank, self.Tomasulo.add_sub, self.Tomasulo.mult, self.Tomasulo.load_store)
				self.pop()

			elif self.top() and (self.top()[0] == "SW" or self.top()[0] == "LW"):
				if not self.Tomasulo.ROB.busy[int(self.top()[3])]:
					if len(register_bank.registers[int(self.top()[3])].Qi) == 0:
						self.Vk[self.start] = int(register_bank.registers[int(self.top()[3])].Vi)
						self.Qk[self.start] = ""
					elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[3])].Qi != self.top()[0]:
						self.Qk[self.start] = register_bank.registers[int(self.top()[3])].Qi
				else:
					h = self.Tomasulo.ROB.RS_reorder[int(self.top()[3])]
					if self.Tomasulo.ROB.ready[h]:
						self.Vk[self.start] = self.Tomasulo.ROB.value[h]
						self.Qk[self.start] = ""
					else:
						self.Qk[self.start] = h

				if self.top()[0] == "SW":
					if not self.Tomasulo.ROB.busy[int(self.top()[1])]:
						if len(register_bank.registers[int(self.top()[1])].Qi) == 0:
							self.Vj[self.start] = int(register_bank.registers[int(self.top()[1])].Vi)
							self.Qj[self.start] = ""
						elif len(self.Qk[self.start]) == 0 and register_bank.registers[int(self.top()[1])].Qi != self.top()[0]:
							self.Qj[self.start] = register_bank.registers[int(self.top()[1])].Qi
					else:
						h = self.Tomasulo.ROB.RS_reorder[int(self.top()[1])]
						if self.Tomasulo.ROB.ready[h]:
							self.Vk[self.start] = self.Tomasulo.ROB.value[h]
							self.Qk[self.start] = ""
						else:
							self.Qk[self.start] = h

				if self.top()[0] == "SW":
					if len(self.Qj[self.start]) == 0: self.top()[1] = str(self.Vj[self.start])
					else: self.top()[1] = str(self.Qj[self.start])

				if len(self.Qk[self.start]) == 0: self.top()[3] = str(self.Vk[self.start])
				else: self.top()[3] = str(self.Qk[self.start])
				for i in range(len(self.list_data_bus)):
					info = copy_list(self.top())
					self.list_data_bus[i].send(info)

				self.issue(self.Tomasulo.register_bank, self.Tomasulo.add_sub, self.Tomasulo.mult, self.Tomasulo.load_store)
				self.pop()

			elif self.top() and self.top()[0] == "NOP":
				self.pop()
