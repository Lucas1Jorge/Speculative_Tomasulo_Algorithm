import threading
import sys
import time
import queue
import tomasuloui_v2
from PyQt5 import QtCore, QtGui, QtWidgets
from buffer import *
from executer import *
from functions import *
from memory import *
from data_bus import *
from register import *
from instructions_unity import *
from ROB import *


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
		self.ui = tomasuloui_v2.Ui_MainWindow()
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
		self.ROB_bus = data_bus("ROB_bus")
		self.ROB = ROB("reorder_buffer", 10, [self.ROB_bus], self)


		self.common_data_bus = data_bus("common_data_bus")
		# self.common_data_bus.add_receivers([self.register_bank, self.ROB])
		self.common_data_bus.add_receivers([self.ROB])

		self.loader = loader([self.common_data_bus], self)
		self.load_store = load_store("load_store", 5, [self.common_data_bus], self.loader)

		self.multiplier = multiplier([self.common_data_bus], self)
		self.mult = reservation_station("mult", 3, [self.common_data_bus], self.multiplier)

		self.adder = adder([self.common_data_bus], self)
		self.add_sub = reservation_station("add_sub", 3, [self.common_data_bus], self.adder)

		self.common_data_bus.add_receivers([self.load_store, self.mult, self.add_sub])
		self.ROB_bus.add_receivers([self.load_store, self.add_sub, self.mult, self.register_bank])

		self.load_store_bus = data_bus("load_store_bus")
		self.load_store_bus.add_receivers([self.load_store])

		self.operations_bus = data_bus("operations_bus")
		self.operations_bus.add_receivers([self.mult, self.add_sub])

		self.instructions_unity = instructions_unity("instructions_unity", 6, [self.load_store_bus, self.operations_bus], self)

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
		self.ROB.print()
		print()

		self.instructions_unity.clock(self.register_bank)
		self.load_store.clock(self.register_bank)
		self.mult.clock(self.register_bank)
		self.add_sub.clock(self.register_bank)
		# self.ROB.clock(self.register_bank)

		self.load_store_bus.clock()
		self.operations_bus.clock()
		self.common_data_bus.clock()
		# self.ROB_bus.clock()
		self.ROB.clock(self.register_bank)


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

		self.ui.update_ROB_Buffer_Table(self.ROB)
		self.ui.update_ROB_Registers_Table(self.ROB)

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

	input()