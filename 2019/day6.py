# While I'm not totally against using libraries like numpy and networkx
# I'm going to try to solve the problems using nothing but 'native' python
# ya know have fun with it and all

with open('day6.txt', 'r') as f:
	raw_data  = f.read().split('\n')
	f.close()

# raw_data = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L""".split('\n')

# raw_data = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN""".split('\n')

orbits = dict()
for orbit in raw_data:
	e1, e2 = orbit.split(')')
	buddies = orbits.get(e1, [])
	buddies.append(e2)
	orbits[e1] = buddies


def get_orbits(origin, something=0):
	o = orbits.get(origin, [])
	num = something
	for e in o:
		num += get_orbits(e, something+1)
	return num

# Part 1
# print(get_orbits('COM'))

# Part 2 - oh shit oh fuck I need to be able to move both ways
# To cricumvent this issue I'm going to get the path from COM for both start and end
# and then get the intersection of their paths


def pathfind(start, end):
	os = orbits.get(start, [])
	for e in os:
		if e == end:
			return [start]
		p = pathfind(e, end)
		if not p:
			continue
		return [start] + p

	return None

me = pathfind('COM', 'YOU') 
santa = pathfind('COM', 'SAN')

inter = 0
for i in range(len(me)):
	if me[i] == 'SAN' or santa[i] == 'YOU':
		print('yoyo')
		inter = i
		break
	if me[i] != santa[i]:
		inter = i-1
		break
print(inter, me[inter], santa[inter])
print(me[inter:], santa[inter:])
print(len(me[inter+1:]) + len(santa[inter+1:]))