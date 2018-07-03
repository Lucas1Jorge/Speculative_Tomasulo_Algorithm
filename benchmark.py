def printM(memo, r1):
	for i in range(1, r1 + 1):
		for j in range(1, r1 + 1):
			print(memo[i * r1 + j], end=" ")
		print()

memo = [0] * 4000
r1 = 3
r2 = 1

for i in range(1, r1 + 1):
	for j in range(1, r1 +1):
		memo[i * r1 + j] = r2
		r2 += 1

r2 = 0
printM(memo, r1)

for i in range(1, r1 + 1):
	
	r2 += memo[i * r1 + i]

	for j in range(i + 1, r1 + 1):
		aux = memo[i * r1 + j]

		memo[i * r1 + j] = memo[j * r1 + i]

		r2 += memo[j * r1 + i]

		memo[j * r1 + i] = aux

		r2 += memo[j * r1 + i]

# r6 = 0
print()
printM(memo, r1)

print()
print(r2)

# ADDI R1,R0,6
# ADDI R2,R0,1
# ADDI R4,R0,1
# P1:
# ADDI R5,R0,1
# P2:
# MUL R6,R1,R4
# ADD R6,R6,R5
# SW R2,0(R6)
# ADDI R2,R2,1
# ADDI R5,R5,1
# BLE R5,R1,P2
# ADDI R4,R4,1
# BLE R4,R1,P1
# ADDI R2,R0,0
# ADDI R4,R0,1
# P3:
# MUL R6,R4,R1
# ADD R6,R6,R4
# LW R6,0(R6)
# ADD R2,R2,R6
# ADDI R5,R4,1
# ADDI R9,R1,1
# BEQ R5,R9,P5
# P4:
# MUL R6,R4,R1
# ADD R6,R6,R5
# LW R3,0(R6)
# MUL R7,R5,R1
# ADD R7,R7,R4
# LW R8,0(R7)
# SW R8,0(R6)
# ADD R2,R2,R8
# SW R3,0(R7)
# ADD R2,R2,R3
# ADDI R5,R5,1
# BLE R5,R1,P4
# ADDI R4,R4,1
# BLE R4,R1,P3
# P5:
# ADDI R6,R0,0