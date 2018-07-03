def copy_list(list):
	ans = []
	for el in list:
		ans.append(el)
	return ans


def bin_to_int(b):
	ans = 0
	for i in range(len(b)-1, -1, -1):
		ans += int(b[i]) * 2**(len(b) - 1 - i)
	return str(ans)


def read_binary(Dict, instruction):
	mips = []
	if Dict[instruction[:6]] == "R":
		mips.append(Dict["R" + instruction[26:32]])
		mips.append(bin_to_int(instruction[16:21]))
		mips.append(bin_to_int(instruction[6:11]))
		mips.append(bin_to_int(instruction[11:16]))
		mips.append("")

	else:
		mips.append(Dict[instruction[:6]])
		mips.append(bin_to_int(instruction[11:16]))
		mips.append(bin_to_int(instruction[6:11]))
		mips.append(bin_to_int(instruction[16:32]))
		mips.append("")

	if mips[0] == "BEQ" or mips[0] == "BNE" or mips[0] == "BLE":
		mips[1], mips[2] = mips[2], mips[1]
	if mips[0] == "LW" or mips[0] == "SW":
		mips[2], mips[3] = mips[3], mips[2]

	return mips


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

def not_over(PC):
	# return True
	return int(PC) < 140

def update_buffer(buffer, info):
	for i in range(buffer.max_size):
		for j in range(1, len(buffer.list[i])):
			if buffer.list[i] == info[0]:
				buffer.list[i] = info[-1]


def search_ROB(ROB, register):
	for i in range(ROB.max_size):
		if len(ROB.list[i] > 0):
			if ROB.destiny[ROB.end + i] == register and ROB.list[ROB.end + i][0] != "SW":
				if len(ROB.value[i]) > 0:
					return ROB.value[i]
	return None