import numpy
import pygame
import sys

class Box():
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.can_change = False
		self.outline = (0,0,0)

	def draw(self, win):
		pygame.draw.rect(win, self.outline, (self.x,self.y,self.width+2,self.height+2),0)
		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
		
		if self.text != '':
			font = pygame.font.SysFont('comicsans', 60)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            
	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
            
		return False


class Sudoku():
	def __init__(self):
		pygame.init()
		
		self.screen = pygame.display.set_mode((900,900))
		pygame.display.set_caption('Sudoku')
		
		self.grid = [[0, 0, 0, 0, 8, 0, 0, 0, 0],
					[8, 0, 9, 0, 7, 1, 0, 2, 0],
					[4, 0, 3, 5, 0, 0, 0, 0, 1],
					[0, 0, 0, 1, 0, 0, 0, 0, 7],
					[0, 0, 2, 0, 3, 4, 0, 8, 0],
					[7, 3, 0, 0, 0, 9, 0, 0, 4],
					[9, 0, 0, 0, 0, 0, 7, 0, 2],
					[0, 0, 8, 2, 0, 5, 0, 9, 0],
					[1, 0, 0, 0, 4, 0, 3, 0, 0]]
					
		self.boxes = list()
					
		for x in range(9):
			for y in range (9):
				if self.grid[x][y] == 0:
					box = Box((255, 255, 255), y*100, x*100, 98, 98, '')
					box.can_change = True
				else:
					box = Box((0, 255, 255), y*100, x*100, 98, 98, str(self.grid[x][y]))
				
				box.draw(self.screen)
				self.boxes.append(box)
	
	def run_game(self):
		while True:
			self.check_events()
			self.update_screen()

				
	def check_events(self):
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()
				
			if event.type == pygame.QUIT:
				sys.exit()
			
			for box in self.boxes:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if box.can_change == True:
						box.color = (255, 255, 255)
					if box.isOver(pos) and box.can_change == True:
						box.color = (200,200,200)
			
			for box in self.boxes:
				if (event.type == pygame.KEYDOWN and box.color == (200,200,200)
				and box.can_change == True):
					key = event.unicode
					try:
						if int(key) in range(1, 10): 
							box.text = key
					except:
						pass
					

	def update_screen(self):
		
		for box in self.boxes:
			box.draw(self.screen)

		
		pygame.draw.rect(self.screen, (0,0,0), (300, 0, 3, 900), 0)
		pygame.draw.rect(self.screen, (0,0,0), (600, 0, 3, 900), 0)
		pygame.draw.rect(self.screen, (0,0,0), (0, 300, 900, 3), 0)
		pygame.draw.rect(self.screen, (0,0,0), (0, 600, 900, 3), 0)
		
		pygame.display.flip()


if __name__== '__main__':
	sud = Sudoku()
	sud.run_game()
	



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

def solve(grid):
	for x in range(9):
		for y in range(9):
			if grid[x][y] == 0:
				for n in range(1, 10):
					if is_valid(grid, x, y, n):
						grid[x][y] = n
						solve(grid)
						grid[x][y] = 0
				return None

	print(numpy.matrix(grid))
	
