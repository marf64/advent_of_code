with open('day8.txt', 'r') as f:
	raw_data = f.read()
	f.close()

width = 25
height = 6
size = width*height

layers = [raw_data[i:i+size] for i in range(0, len(raw_data), size)]

def count_zeros(layer):
	return len([p for p in layer if p == '0'])

layer = min(layers, key=count_zeros)
print(len([p for p in layer if p == '2']) * len([p for p in layer if p == '1']))

layers = reversed(layers)
image = [2]*size

for layer in layers:
	for i in range(size):
		p = layer[i]
		if p != '2':
			image[i] = '⬜'  if p == '1' else '⬛'

for i in range(height):
	print(str(''.join(image[i*width:(i+1)*width])))
