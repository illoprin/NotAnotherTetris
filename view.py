from settings import *
import pygame
from pygame.locals import *
from math import fabs

class View():
	def __init__ (self, display, game_logic, debug):
		self.game = game_logic
		self.game_metrics = {}
		self.pygame_display = display
		self.is_debug = debug
		self.load_fonts()
		self.load_sprites()

		self.playing_effect = False

	def load_fonts(self):
		# Loading font
		self.h1 = pygame.font.Font('assets/press_start.ttf', 30)
		self.h2 = pygame.font.Font('assets/press_start.ttf', 20)
		self.h3 = pygame.font.Font('assets/press_start.ttf', 15)
		

	def load_sprites(self):
		# Load blocks tileset
		self.tileset = pygame.image.load("assets/blocks.png").convert()
		# Divide tileset into separate blocks
		# Scale each block to BLOCK_SIZE value
		# Add each block image to blocks array
		self.sprites = [[pygame.transform.scale(self.tileset.subsurface([(x * TILESET_BLOCK_SIZE)-x, (y * TILESET_BLOCK_SIZE)-y, TILESET_BLOCK_SIZE, TILESET_BLOCK_SIZE]), (BLOCK_SIZE, BLOCK_SIZE)) for x in range(3)] for y in range(10)]

	def render(self, game_metrics: dict):
		self.game_metrics = game_metrics

		#self.pygame_display.fill((240, 236, 229))
		if not self.playing_effect:
			self.pygame_display.fill((20, 20, 20))

		# GAME FIELD DRAW
		self.draw_field()

		# ACTIVE TETRAMINO DRAW
		self.draw_active_tetromino()

		self.draw_ui()
		# DEBUG
		# DRAW ACTIVE TETRAMINO BOUNDS
		if self.is_debug:
			pygame.draw.rect(self.pygame_display, "red", (self.game.active_tetramino["x"]*BLOCK_SIZE+FIELD_MARGIN, self.game.active_tetramino["y"]*BLOCK_SIZE+FIELD_MARGIN, BLOCK_SIZE * self.game.tetramino_bounding_box_size["width"], BLOCK_SIZE * self.game.tetramino_bounding_box_size["height"]), 2)
			pygame.draw.rect(self.pygame_display, "green", (self.game.next_tetramino["x"]*BLOCK_SIZE+FIELD_MARGIN, self.game.next_tetramino["y"]*BLOCK_SIZE+FIELD_MARGIN, BLOCK_SIZE * self.game.tetramino_bounding_box_size["width"], BLOCK_SIZE * self.game.tetramino_bounding_box_size["height"]), 2)


	def draw_active_tetromino(self):
		for j in range(self.game.tetramino_bounding_box_size['height']):
			for i in range(self.game.tetramino_bounding_box_size['width']):
				real_tetramino_pos = self.game.get_tetramino_cell_field_position(i, j)
				if real_tetramino_pos['y'] >= 0:
					self.draw_block(real_tetramino_pos['x'], real_tetramino_pos['y'], self.game.active_tetramino['tetramino'][j][i])

	def draw_field(self):
		# RENDER FIELD BACKGROUND
		pygame.draw.rect(self.pygame_display, "black", (FIELD_MARGIN, FIELD_MARGIN, BLOCK_SIZE*GAME_FIELD_W, BLOCK_SIZE*GAME_FIELD_H))
		# DRAW CELLS
		for y in range(len(self.game.field)):
			for x in range(len(self.game.field[y])):
				self.draw_block(x, y, self.game.field[y][x])
				# GRAY GRID
				pygame.draw.rect(self.pygame_display, (15,15,15), (x*BLOCK_SIZE+FIELD_MARGIN, y*BLOCK_SIZE+FIELD_MARGIN, BLOCK_SIZE, BLOCK_SIZE), 1)
		# RENDER FIELD BOUNDS
		pygame.draw.rect(self.pygame_display, "white", (FIELD_MARGIN-1, FIELD_MARGIN-1, BLOCK_SIZE*GAME_FIELD_W+1, BLOCK_SIZE*GAME_FIELD_H+1), 1)


	def draw_block(self, x, y, block_type):
		current_x = x * BLOCK_SIZE + FIELD_MARGIN
		current_y = y * BLOCK_SIZE + FIELD_MARGIN
		current_block_coloring_y = int(fabs(self.game_metrics["level"]%10-1))

		# CHECK CURRENT BLOCK TYPE
		if not block_type == ".":
			tileset_position = [0, current_block_coloring_y]
			if block_type == "J" or block_type == "S":
				tileset_position = [2, current_block_coloring_y]
			elif block_type == "Z" or block_type == "L":
				if self.game_metrics["level"] > 1:
					tileset_position = [1, current_block_coloring_y]
				else:
					tileset_position = [2, 9]
			# DRAW BLOCK
			self.pygame_display.blit(self.sprites[tileset_position[1]][tileset_position[0]], (current_x, current_y, BLOCK_SIZE, BLOCK_SIZE))

	def draw_ui(self):
		# DRAW SCORE AND etc
		game_metrics = self.game_metrics
		pos_x = FIELD_MARGIN*2+GAME_FIELD_W*BLOCK_SIZE+100
		self.render_text('SCORE: ' + str(game_metrics["score"]), "white", (pos_x, FIELD_MARGIN, 300, 30), self.h2)
		self.render_text('LEVEL: ' + str(game_metrics["level"]), "white", (pos_x, FIELD_MARGIN*2+5, 300, 30), self.h2)
		self.render_text('LINES: ' + str(game_metrics["cleared_lines"]), "white", (pos_x, FIELD_MARGIN*3+5*2, 300, 30), self.h2)
		self.render_text('NEXT', "white", (pos_x, FIELD_MARGIN*7, 300, 30), self.h2)
		# DRAW ACTIVE TETRAMINO
		for j in range(self.game.tetramino_bounding_box_size['height']):
			for i in range(self.game.tetramino_bounding_box_size['width']):
				self.draw_block(GAME_FIELD_W+3+i, 5+j, self.game.next_tetramino['tetramino'][j][i])
		# DRAW TETRIS RATE
		self.render_text('TETRIS RATE: ' + str(game_metrics["tetris_rate"]) + "%", "white", (pos_x+100, WIN_H-(FIELD_MARGIN+15), 300, 30), self.h2)


	def show_end_screen(self):
		self.pygame_display.fill('black')
		self.render_text('GAME OVER', "white", (WIN_W/2, WIN_H/2, 200, 30), self.h1)
		self.render_text('SCORE: ' + str(self.game_metrics["score"]), "cyan", (WIN_W/2, WIN_H/2+50, 200, 30), self.h2)

	def show_main_menu(self):
		self.pygame_display.fill((20, 20, 20))
		self.render_text('ORIGINAL CONCEPT AND DESIGN BY', "yellow", (WIN_W/2-5, 30, WIN_W-WIN_W*.05, WIN_H/10), self.h2)
		self.render_text('ALEXEY PAJITNOV', "cyan", (WIN_W/2-5, 70, WIN_W-WIN_W*.05, WIN_H/10), self.h2)
		self.render_text('PRESS SPACE TO START', (255,255,255), (WIN_W/2-5, WIN_H/2, WIN_W-WIN_W*.05, WIN_H/7), self.h1)

		self.render_text('666 Lines of code', "red", (FIELD_MARGIN+150, WIN_H-WIN_H*.05, 200, 50), self.h3)
		self.render_text('Not Another Tetris 0.1 beta', "white", (FIELD_MARGIN+225, WIN_H-WIN_H*.1, 200, 50), self.h3)
		self.render_text('Loprin Branding Design', "magenta", (WIN_W-FIELD_MARGIN-175, WIN_H-WIN_H*.05, 200, 50), self.h3)

	def show_pause_screen(self):
		self.pygame_display.fill((30, 30, 30))
		self.render_text('PAUSE', (49, 48, 77), (WIN_W/2, WIN_H/2, 200, 30), self.h1)
		

	def render_text(self, text, color, placement, font):
		text = font.render(text, True, color)
		rect = text.get_rect()
		rect.center = (placement[0], placement[1])
		rect.size = (placement[2], placement[3])
		self.pygame_display.blit(text, rect)

	def play_full_line_effect(self, tetris=False):
		print("View: Full line effect call")
		self.render(self.game_metrics)
		self.playing_effect = True
		white_bg = False
		for i in range(int(GAME_FIELD_W/2)):
			if tetris:
				if not white_bg:
					self.pygame_display.fill("white")
					white_bg = True
				else:
					self.pygame_display.fill(BACKGOUND_COLOR)
					white_bg = False
				self.render(self.game_metrics)
			x_left = (int(GAME_FIELD_W/2) - i - 1)*BLOCK_SIZE+FIELD_MARGIN
			x_right = (int(GAME_FIELD_W/2) + i)*BLOCK_SIZE+FIELD_MARGIN
			for j in self.game.full_lines_indices:
				y = j*BLOCK_SIZE+FIELD_MARGIN
				pygame.draw.rect(self.pygame_display, "black", (x_left, y, BLOCK_SIZE, BLOCK_SIZE-1))
				pygame.draw.rect(self.pygame_display, "black", (x_right, y, BLOCK_SIZE, BLOCK_SIZE-1))
				if tetris:
					for x in range(i+1):
						x_previous_left = x_left + (x*BLOCK_SIZE + FIELD_MARGIN)
						x_previous_right = x_right - (x*BLOCK_SIZE + FIELD_MARGIN)
						pygame.draw.rect(self.pygame_display, "black", (x_previous_left, y, BLOCK_SIZE, BLOCK_SIZE-1))
						pygame.draw.rect(self.pygame_display, "black", (x_previous_right, y, BLOCK_SIZE, BLOCK_SIZE-1))
					pygame.display.flip()
				else:
					pygame.display.flip()
			pygame.time.delay(100)
		pygame.event.pump()
		self.pygame_display.fill(BACKGOUND_COLOR)
		self.playing_effect = False