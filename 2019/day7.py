from computer import Computer as C

ins = [3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99]

# ins = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
# -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
# 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
# Again with the doing everything myself even if its ugly and not optimal
def permute_phases():
	p = 1234
	while p <= 43210:
		flags = [0,0,0,0,0]
		for d in [int(d) for d in str(p)]:
			if d in [0,1,2,3,4]:
				if not flags[d]:
					flags[d] = 1
				else:
					break
			else:
				break
		str_p = str(p)
		if all(flags[1:]) and (flags[0] or len(str_p) == 4):
			yield [0]*(5-len(str_p)) + [int(d) for d in str(p)]
		p += 1

# Part 1

# signals = []
# for p in permute_phases():
# 	i1 = p[0:1]
# 	i2 = p[1:2]
# 	i3 = p[2:3]
# 	i4 = p[3:4]
# 	i5 = p[4:5]

# 	inputs = [i1,i2,i3,i4,i5]

# 	output = inputs[0] + [0]
# 	c = C(ins, output)
# 	c.do_work()
# 	for i in range(1, 5):
# 		output = inputs[i] + c.output
# 		c = C(ins, output)
# 		c.do_work()
# 	signals += c.output

# print(max(signals))

# Part 2

def permute_phases_2():
	p = 56789
	while p <= 98765:
		flags = [0,0,0,0,0]
		for d in [int(d) for d in str(p)]:
			if d in [5,6,7,8,9]:
				if not flags[d % 5]:
					flags[d % 5] = 1
				else:
					break
			else:
				break
		str_p = str(p)
		if all(flags):
			yield [int(d) for d in str(p)]
		p += 1

signals = []
# for p in permute_phases_2():
for p in permute_phases_2():
	i1 = p[0:1]
	i2 = p[1:2]
	i3 = p[2:3]
	i4 = p[3:4]
	i5 = p[4:5]

	inputs = [i1 + [0] ,i2,i3,i4,i5]
	computers = [C(ins, inputs[i]) for i in range(5)]

	# for i in range(5):
	# 	def on_output(output):
	# 		print(i, output)
	# 		computers[(i+1)%5].add_input([output[len(output)-1]])
	# 		computers[i].clear_output()

	# 	c = computers[i]
	# 	c.on_output(on_output)

	for c in computers:
		c.do_work()

	i = 0
	while computers[4].running:
		c1 = computers[i]
		c2 = computers[(i+1) % 5]
		# print(i, c1.running, c2.running, c1.output, c2.wait4input)
		c2.set_input(c1.output)
		c1.clear_output()
		# print(i, c1.running, c2.running)
		i = (i+1) % 5
	signals.append(computers[4].output[0])

print(max(signals))



		

