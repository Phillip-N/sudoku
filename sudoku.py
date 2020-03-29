grid = [[0, 1, 0, 0, 0, 0, 6, 5, 0],
		[0, 9, 0, 6, 0, 3, 1, 0, 7],
		[0, 0, 0, 0, 0, 7, 2, 8, 9],
		[0, 4, 0, 0, 1, 2, 3, 0, 0],
		[0, 8, 0, 0, 7, 0, 0, 2, 0],
		[0, 0, 3, 9, 8, 0, 0, 6, 0],
		[4, 5, 6, 7, 0, 0, 0, 0, 0],
		[9, 0, 2, 4, 0, 8, 0, 1, 0],
		[0, 7, 1, 0, 0, 0, 0, 9, 0]]
		
		
# define box coords
'''
if x in [0,2] and y in [0,2]
for x in range(3) ...
	for y in range(3)...
		check

we just need to check end points and add three to both x and y ranges
box_ends = [0, 3, 6, 9]

arb [x,y]
x_constr = []
y_constr = []

for endpoint in box_ends:
	if x > endpoint:
		continue
	else:
		for i in range(box_ends[endpoint-1], box_ends[endpoint-1]+3]:
			x_constr.append(i)
		break

for endpoint in box_ends:
	if y > endpoint:
		continue
	else:
		i in range(box_ends[endpoint-1], box_ends[endpoint-1]+3]:
			y_constr.append(i)
		break

'''

		
# helper function to find boxes that coordinate pertains to
def box(puzzle, x, y):
	x_constr = []
	y_constr = []
	
	for endpoint in box_ends:
		if x > endpoint:
			continue
		else:
			for i in range(box_ends[endpoint-1], box_ends[endpoint-1]+3]:
				x_constr.append(i)
			break

	for endpoint in box_ends:
		if y > endpoint:
			continue
		else:
			i in range(box_ends[endpoint-1], box_ends[endpoint-1]+3]:
				y_constr.append(i)
			break
			
	return [x_constr, y_constr]


def is_valid(puzzle, x, y, n):
	# check vertically
	for x in range(9):
		if grid[x][y] == n:
			return False
	
	# check horizontally
	for y in range(9):
		if grid[x][y] == n:
			return False
	
	# check square
	box = box(puzzle, x, y)
	for x in box[0]:
		for y in box[1]:
			if grid[x][y] == n:
				return False
				
	return True

def solve():
