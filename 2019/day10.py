ass_in = """
...###.#########.####
.######.###.###.##...
####.########.#####.#
########.####.##.###.
####..#.####.#.#.##..
#.################.##
..######.##.##.#####.
#.####.#####.###.#.##
#####.#########.#####
#####.##..##..#.#####
##.######....########
.#######.#.#########.
.#.##.#.#.#.##.###.##
######...####.#.#.###
###############.#.###
#.#####.##..###.##.#.
##..##..###.#.#######
#..#..########.#.##..
#.#.######.##.##...##
.#.##.#####.#..#####.
#.#.##########..#.##.
"""


rows = ass_in.split('\n')[1:-1]

ass = set()

for i, r in enumerate(rows):
	for j, a in enumerate(r):
		if a == '#':
			ass.add((j, i))

# Part 1

# visible = dict()

# for a in ass:
# 	slopes = set()
# 	for b in ass:
# 		x = a[0] - b[0]
# 		y = a[1] - b[1]
# 		sign = 1 if x > 0 else -1 if x < 0 else 1 if y > 0 else -1 
# 		s = y/x if x != 0 else 'v' 
# 		slopes.add((sign, s))
# 	visible[a] = len(slopes)

# print(max(visible.items(), key=lambda v: v[1]))

# Part 2

station = (11, 13)

by_slopes = dict()

offset = len(rows)

for a in ass:
	if a == station:
		continue

	x = station[0] - a[0]
	y = station[1] - a[1]
	
	if x <= 0 and y >= 0:
		if x == 0:
			slope = -offset*2
		elif y == 0:
			slope = -offset
		else:
			slope = y/x - offset
	elif y < 0:
		slope = -x/y
	elif x > 0 and y >= 0:
		if y == 0:
			slope = offset
		else:
			slope = y/x + offset

	asses = by_slopes.get(slope, [])
	asses.append(a)
	by_slopes[slope] = sorted(asses, key=lambda x: (station[0] -x[0])**2 + (station[1] - x[1])**2 )

i = 0
while len(ass) != 1:
	for slope, asses in sorted(by_slopes.items(), key=lambda x: x[0]):
		if len(asses):
			a = asses.pop(0)
			ass.remove(a)
			i += 1
			if i == 200:
				print(a)
