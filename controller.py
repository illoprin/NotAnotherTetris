from settings import *
from game_logic import *
from view import *
from sound import *
from event_handler import *

import pygame
from pygame.locals import * 
import sys
import math
from copy import deepcopy


class Controller():

	def __init__(self, display, debug):
		self.pygame_display = display
		self.is_debug = debug
		self.tick = 0
		self.is_playing = False
		self.end_game = False
		self.main_menu = False

		self.sounds = SoundController()
		self.game_logic = GameLogic()
		self.view = View(self.pygame_display, self.game_logic, self.is_debug)

		self.goto_main_menu()
		
	def get_game_metrics(self):
		return {
			"score": self.game_logic.score,
			"level": self.game_logic.level,
			"cleared_lines": self.game_logic.cleared_lines,
			"tetris_rate": 0 if self.game_logic.cleared_lines == 0 else math.floor((self.game_logic.tetrises*4/self.game_logic.cleared_lines)*100)
		}
			


	def update(self):
		self.tick += 1
		self.handle_input()
		if not self.main_menu:
			#GAME LOGIC UPDATE
			if self.is_playing:
				game_speed = math.fabs(math.floor(FPS/(self.game_logic.level*.5)-10))
				self.view.render(self.get_game_metrics())
				self.handle_events()
				if self.game_logic.game_over:
					self.game_end()
				elif self.tick % game_speed == 0 and not self.view.playing_effect:
					# GAME UPDATE
					self.game_logic.move_vertical(1)
				
			elif not self.is_playing and not self.end_game:
				self.view.show_pause_screen()
			elif self.end_game:
				self.view.show_end_screen()

		else:
			self.view.show_main_menu()

	def handle_input(self):
		# LONE INPUT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.is_playing and not self.end_game:
					if event.key == K_F_ROTATE:
						self.game_logic.rotate_figure(True)
					if event.key == K_F_MIRROR and self.is_debug:
						self.game_logic.mirror_figure()
					if event.key == K_F_LEFT:
						self.game_logic.move_horizontal(-1)
					if event.key == K_F_RIGHT:
						self.game_logic.move_horizontal(1)
						
					# SLOW FALL ACCELERATION
					# if event.key == K_F_DOWN:
					# 	self.game_logic.move_vertical(1)
			
				if event.key == K_START and (not self.main_menu) and (not self.end_game):
					self.pause_and_resume()
				elif event.key == K_START and self.main_menu:
					self.start_game()
				elif event.key == K_START and self.end_game:
					self.restart_game()
				elif event.key == pygame.K_ESCAPE and (not self.main_menu):
					self.goto_main_menu()

		# FASTER INPUT
		if self.tick % int(FPS/10) == 0 and not self.end_game and self.is_playing:
			keys = pygame.key.get_pressed()
			# FAST FALL ACCELERATION
			if keys[K_F_DOWN]:
				self.game_logic.move_vertical(1)

	def handle_events(self):
		for event in self.game_logic.event_listener.events:
			if event == "PLACE_FIGURE":
				self.sounds.play_overlay("place")
			elif event == "LEVEL_UP":
				self.sounds.play_overlay("next_level")
			elif event == "MOVE":
				continue
			elif event == "FULL_LINE":
				self.sounds.play_overlay("line")
				self.view.play_full_line_effect()
				self.game_logic.update_field_state()
			elif event == "ROTATE":
				self.sounds.play_overlay("rotate")
			elif event == "FOUR_FULL_LINES":
				self.sounds.play_overlay("tetris")
				self.view.play_full_line_effect(True)
				self.game_logic.update_field_state()
		self.game_logic.event_listener.clear_event_stack()

	def pause_and_resume(self):
		self.sounds.stop_all()
		self.is_playing = not self.is_playing
		if self.is_playing:
			self.sounds.play_main_theme(True)
		self.sounds.all_sounds["selection"].play()
		print("Controller: Game paused")

	def start_game(self):
		self.game_logic.start_game()
		if self.is_debug:
			for j in range(5):
				for i in range(GAME_FIELD_W-1):
					self.game_logic.field[GAME_FIELD_H-j-1][i] = "S"
		self.sounds.play("selection")
		self.main_menu = False
		self.is_playing = True
		self.end_game = False
		self.sounds.play_main_theme(False)

	def restart_game(self):
		self.sounds.stop_all()
		self.end_game = False
		self.is_playing = True
		self.game_logic.start_game()
		self.sounds.play_main_theme(False)
		

	def goto_main_menu(self):
		self.sounds.play("selection")
		print("Controller: Goto main_menu")
		self.is_playing = False
		self.game_logic.exit_game()
		self.main_menu = True

	def game_end(self):
		self.sounds.play_overlay("place")
		self.sounds.play_music("stats")
		self.end_game = True
		self.is_playing = False
		self.game_logic.exit_game()
		print("Controller: Game ended")