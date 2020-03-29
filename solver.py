import numpy

grid = [[0, 0, 0, 0, 8, 0, 0, 0, 0],
		[8, 0, 9, 0, 7, 1, 0, 2, 0],
		[4, 0, 3, 5, 0, 0, 0, 0, 1],
		[0, 0, 0, 1, 0, 0, 0, 0, 7],
		[0, 0, 2, 0, 3, 4, 0, 8, 0],
		[7, 3, 0, 0, 0, 9, 0, 0, 4],
		[9, 0, 0, 0, 0, 0, 7, 0, 2],
		[0, 0, 8, 2, 0, 5, 0, 9, 0],
		[1, 0, 0, 0, 4, 0, 3, 0, 0]]
		

# helper function to find boxes that coordinate pertains to
def box(x, y):
	box_ends = [0, 3, 6, 9]
	x_constr = []
	y_constr = []
	
	for endpoint in range(len(box_ends)):
		if x >= box_ends[endpoint]:
			continue
		else:
			start = None
			if x == 0:
				start = 0
			else:
				start = endpoint-1
			for i in range(box_ends[start], box_ends[start]+3):
				x_constr.append(i)
			break

	for endpoint in range(len(box_ends)):
		if y >= box_ends[endpoint]:
			continue
		else:
			start = None
			if y == 0:
				start = 0
			else:
				start = endpoint-1
			for i in range(box_ends[start], box_ends[start]+3):
				y_constr.append(i)
			break
	
	return [x_constr, y_constr]


def is_valid(grid, x, y, n):
	# check vertically
	for i in range(9):
		if grid[i][y] == n:
			return False
	
	# check horizontally
	for i in range(9):
		if grid[x][i] == n:
			return False
	
	# check box
	box_ = box(x, y)
	for i in box_[0]:
		for z in box_[1]:
			if grid[i][z] == n:
				return False
				
	return True

def find_empty(grid):
	for y in range(9):
		for x in range(9):
			if grid[y][x] == 0:
				return (y, x)
				
	return False


def solve(grid):
	next_ = find_empty(grid)
	if not next_:
		return True
	else:
		x, y = next_
		for n in range(1, 10):
			if is_valid(grid, x, y, n):
				grid[x][y] = n
				if solve(grid):
					return True
				grid[x][y] = 0
		return None
		


