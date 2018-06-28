from buffer import buffer

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
					elif self.receivers[i].name == "register_bank" or self.receivers[i].name == "reorder_buffer":
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