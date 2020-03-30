import pygame
import sys
import ctypes
import copy
from solver import box, is_valid, find_empty

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
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
            
		return False

class Timer():
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.counter = 0
	
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
	
		if self.text != '':
			font = pygame.font.SysFont('comicsans', 60)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

class Sudoku():
	def __init__(self):
		pygame.init()
		pygame.time.set_timer(pygame.USEREVENT, 1000)
		
		self.screen = pygame.display.set_mode((675,725))
		pygame.display.set_caption('Sudoku')
		
		# Complex Puzzle
		# self.grid = [[0, 0, 0, 0, 8, 0, 0, 0, 0],
					# [8, 0, 9, 0, 7, 1, 0, 2, 0],
					# [4, 0, 3, 5, 0, 0, 0, 0, 1],
					# [0, 0, 0, 1, 0, 0, 0, 0, 7],
					# [0, 0, 2, 0, 3, 4, 0, 8, 0],
					# [7, 3, 0, 0, 0, 9, 0, 0, 4],
					# [9, 0, 0, 0, 0, 0, 7, 0, 2],
					# [0, 0, 8, 2, 0, 5, 0, 9, 0],
					# [1, 0, 0, 0, 4, 0, 3, 0, 0]]

		# Easy Puzzle
		self.grid = [[8, 1, 7, 0, 0, 0, 0, 4, 5],
					[0, 0, 0, 0, 5, 1, 7, 0, 6],
					[2, 6, 5, 0, 0, 3, 0, 0, 1],
					[4, 7, 0, 5, 6, 8, 0, 0, 0],
					[9, 5, 1, 0, 0, 0, 0, 8, 0],
					[0, 3, 0, 0, 9, 0, 2, 0, 0],
					[0, 4, 0, 2, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 5, 0, 7, 9],
					[5, 8, 9, 7, 3, 0, 1, 6, 0]]
		
		# creating a deep copy of the original puzzle for the purpose of the solver
		self.default = copy.deepcopy(self.grid)
		self.cur_grid = self.grid
					
		self.boxes = list()
		

					
		for x in range(9):
			for y in range (9):
				if self.grid[x][y] == 0:
					box = Box((255, 255, 255), y*75, x*75, 73, 73, '')
					box.can_change = True
				else:
					box = Box((0, 255, 255), y*75, x*75, 73, 73, str(self.grid[x][y]))
				
				box.draw(self.screen)
				self.boxes.append(box)
		
		self.timer = Timer((255,255,255), 525, 675, 150, 50, '00:00')
		self.timer.draw(self.screen)
		
		pygame.draw.rect(self.screen, (255,255,255), (0, 675, 525, 50), 0)
		font = pygame.font.SysFont('comicsans', 32)
		text = font.render('Press Space to Auto-Solve or Enter to Submit', 1, (0,0,0))
		self.screen.blit(text, (6, 686))
	
	def run_game(self):
		while True:
			self.check_events()
			self.update_screen(self.cur_grid)

				
	def check_events(self):
		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()
			
			if event.type == pygame.USEREVENT:
				self.timer.counter += 1
				if len(str(self.timer.counter//60)) == 1:
					mins = '0' + str(self.timer.counter//60)
				else:
					mins = str(self.timer.counter//60)
				
				if len(str(self.timer.counter%60)) == 1:
					secs = '0' + str(self.timer.counter%60)
				else:
					secs = str(self.timer.counter%60)
				self.timer.text = mins + ':' + secs
				self.timer.draw(self.screen)
			
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
							self.grid[int(box.y/75)][int(box.x/75)] = key
					except ValueError:
						pass
						
						
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				def check_win():
					for box in self.boxes:
						if is_valid(self.grid, int(box.y/75), int(box.x/75), int(box.text)) == False:
							box.color = (255, 0, 0)
							return False
							break
						else:
							continue
						
						return True
						
				try:
					if check_win() == False:
						ctypes.windll.user32.MessageBoxW(0, "You made a mistake somewhere", "Sorry!", 1)
					else:
						ctypes.windll.user32.MessageBoxW(0, "You Win!", "CONGRATULATIONS!", 1)
				except ValueError:
					ctypes.windll.user32.MessageBoxW(0, "Please make sure you fill in all the squares", "Error!", 1)

			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				# Nesting the solver function directly as a event response
				# in order to draw solver visualization
				def solve(grid):
					next_ = find_empty(grid)
					if not next_:
						return True
					else:
						x, y = next_
						for n in range(1, 10):
							if is_valid(grid, x, y, n):
								grid[x][y] = n
								# calling update_screen to show solver algo steps
								# and backtracking
								self.update_screen(grid)
								if solve(grid):
									return True
								grid[x][y] = 0
						return None
				self.cur_grid = self.default
				solve(self.cur_grid)

	def update_screen(self, grid):
		
		# Redefining the box parameters and drawing to screen
		for box in self.boxes:
			if str(grid[int(box.y/75)][int(box.x/75)]) == '0':
				box.text = ''
			else:
				box.text = str(grid[int(box.y/75)][int(box.x/75)])
			box.draw(self.screen)
		
		# Drawing solid lines to seperate internal sudoku boxes
		pygame.draw.rect(self.screen, (0,0,0), (225, 0, 3, 675), 0)
		pygame.draw.rect(self.screen, (0,0,0), (450, 0, 3, 675), 0)
		pygame.draw.rect(self.screen, (0,0,0), (0, 225, 675, 3), 0)
		pygame.draw.rect(self.screen, (0,0,0), (0, 450, 675, 3), 0)
		

		pygame.display.flip()


if __name__== '__main__':
	sud = Sudoku()
	sud.run_game()

