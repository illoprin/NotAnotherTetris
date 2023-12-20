from settings import *
from event_handler import EventListener
import random
import math
from os import system
from copy import deepcopy

# BLOCK - \u2588
class GameLogic():
	def __init__(self):
		
		self.tetramino_bounding_box_size = {
			"width": 4,
			"height": 4
		}

		self.cleared_lines = 0
		self.full_lines_indices = []

		self.game_over = False
		self.event_listener = EventListener()

		self.points = (
			40, 100, 300, 1200
		)
		self.level = 20

	def start_game(self):
		# METRICS CLEAN
		self.level = 1
		self.score = 0
		self.tetrises = 0
		self.cleared_lines = 0

		# CLEAR FIELD
		self.field = [["." for i in range(GAME_FIELD_W)] for j in range(GAME_FIELD_H)]
		
		# CREATE NEW TETRAMINO
		self.active_tetramino = self.generate_new_tetramino()
		self.next_tetramino = self.generate_new_tetramino()

		# DEBUG
		print ("Game Logic: Start game, field created, tetraminoes generated")

	def exit_game(self):
		self.field = [["." for i in range(GAME_FIELD_W)] for j in range(GAME_FIELD_H)]
		self.next_tetramino = {}
		self.active_tetramino = {}
		self.game_over = False
		print ("Game Logic: field cleared, next_tetramino cleared")

	def update_game_metrics(self, full_lines):
		if full_lines > 0 and full_lines < 5:
			if full_lines == 4:
				print ("Game Logic: It's tetris. Great!")
				self.tetrises += 1
			self.cleared_lines += full_lines
			last_level = self.level
			self.level = math.floor(self.cleared_lines*0.1)+1
			if last_level < self.level:
				self.event_listener.receive_event("LEVEL_UP")
			self.score += self.level * self.points[full_lines-1]
			print ("Game Logic: Filled lines: ", full_lines)
			print ("Game Logic: Total number of cleared lines is: ", self.cleared_lines)
			return self.level


	def update_field_state(self):
		self.clear_full_lines()
	
	def generate_new_tetramino(self):
		tetramino = [["." for i in range(self.tetramino_bounding_box_size["height"])] for j in range(self.tetramino_bounding_box_size["width"])]
		tetramino_pos_matrix = [int(GAME_FIELD_W/2-2), -4]

		current_figure = AVALIABLE_FIGURES[random.randint(0,6)]
		current_figure_indices = FIGURES[current_figure];
		
		for num in current_figure_indices:
			x = (num%2)+1
			y = int(num/2)
			tetramino[y][x] = current_figure
		print ("Game Logic: New tetramino generated " + current_figure)

		return {
				"tetramino": tetramino,
				"x": tetramino_pos_matrix[0],
				"y": tetramino_pos_matrix[1]
		}

	def get_tetramino_cell_field_position(self, x, y):
		real_pos = {
			"x": (x + self.active_tetramino["x"]),
			"y": (y + self.active_tetramino["y"]),
		}
		return real_pos

	def update_tetraminoes(self):
		self.active_tetramino = self.next_tetramino
		self.next_tetramino = self.generate_new_tetramino()
		

	def draw_array(self, array):
		# system('cls||clear')
		for y, row in enumerate(array):
			print(" <| ", end='')
			for x, elem in enumerate(row):
				print(elem, end=' ')
			print("|>\n", end='')

	def move_horizontal(self, dx):
		self.active_tetramino["x"] += dx
		if self.check_collision():
			self.active_tetramino["x"] -= dx
		else:
			self.event_listener.receive_event("MOVE")

	def move_vertical(self, dy):
		self.active_tetramino["y"] += dy
		if self.check_collision() and (self.active_tetramino["y"]<=0):
			self.active_tetramino["y"] -= dy
			self.game_over = True
			print("Game Logic: Game over")
		elif self.check_collision() and (self.active_tetramino["y"]>0):
			self.active_tetramino["y"] -= dy
			self.place_figure()


	def rotate_figure(self, clockwise):
		tetramino_buffer = [["." for i in range(4)] for j in range(4)]
		last_state = deepcopy(self.active_tetramino["tetramino"])
		for j in range(4):
			for i in range(4):
				if clockwise:
					# Все строки тетрамино записываются в стобцы буффера
					# Движение записи начинается с нижнего левого края
					# Движение по буфферу идёт с левого верхнего
					tetramino_buffer[i][j] = self.active_tetramino["tetramino"][3 - j][i]
				else:
					# Движение по буфферу идёт с левого нижнего
					tetramino_buffer[3 - i][j] = self.active_tetramino["tetramino"][3 - j][i]

		self.active_tetramino["tetramino"] = deepcopy(tetramino_buffer)
		if self.check_collision():
			self.active_tetramino["tetramino"] = deepcopy(last_state)
		else:
			self.event_listener.receive_event("ROTATE")

	def mirror_figure(self):
		tetramino_buffer = [["." for i in range(4)] for j in range(4)]
		last_state = deepcopy(self.active_tetramino["tetramino"])

		for j in range(4):
			for i in range(4):
				# TETRAMINO MIRRORING
				tetramino_buffer[j][3 - i] = self.active_tetramino["tetramino"][j][i]

		self.active_tetramino["tetramino"] = deepcopy(tetramino_buffer)
		if self.check_collision():
			self.active_tetramino["tetramino"] = deepcopy(last_state)

	def check_collision(self):
		for y in range(len(self.active_tetramino["tetramino"])):
			for x in range(len(self.active_tetramino["tetramino"][y])):
				real_pos = self.get_tetramino_cell_field_position(x, y)
				if not self.active_tetramino["tetramino"][y][x] == ".":
					if not (real_pos["x"] < 0 or real_pos["x"] >= GAME_FIELD_W or real_pos["y"] >= GAME_FIELD_H):
						if real_pos["y"] >= 0:
							if not self.field[real_pos["y"]][real_pos["x"]] == ".":
								print("Game Logic: Collision in field bounds")
								return True
					else:
						print("Game Logic: Collision out of field bounds")
						return True
		return False


	def place_figure(self):
		# PLACE PIECES
		# FROM BUFFER TO MAP
		print("Place figure call")
		for y in range(len(self.active_tetramino["tetramino"])):
			for x in range(len(self.active_tetramino["tetramino"][y])):
				if not self.active_tetramino["tetramino"][y][x] == ".":
					real_pos_array = self.get_tetramino_cell_field_position(x, y)
					print("Game Logic: Cell placed in:\nx: ",real_pos_array["x"],"\ny: ",real_pos_array["y"])
					self.field[real_pos_array["y"]][real_pos_array["x"]] = self.active_tetramino["tetramino"][y][x]
		# DEBUG
		self.draw_array(self.field)

		self.event_listener.receive_event("PLACE_FIGURE")
		
		self.check_full_lines()

		self.update_tetraminoes()

	def check_full_lines(self):
		# CHECK FULL LINES
		full_lines = 0
		self.full_lines_indices = []
		for y, row in enumerate(self.field):
			filled_cells = 0
			for i in row:
				if not i == ".":
					filled_cells += 1
			if filled_cells == GAME_FIELD_W:
				full_lines += 1
				self.full_lines_indices.append(y)
				print("Game Logic: Full line: ", y)

		if len(self.full_lines_indices) > 0 and len(self.full_lines_indices) < 4:
			self.event_listener.receive_event("FULL_LINE")
		elif len(self.full_lines_indices) >= 4:
			self.event_listener.receive_event("FOUR_FULL_LINES")

	def clear_full_lines(self):
		if self.full_lines_indices:
			for index in self.full_lines_indices:
				del self.field[index]
				self.field.insert(0, ["." for i in range(GAME_FIELD_W)])
			self.update_game_metrics(len(self.full_lines_indices))