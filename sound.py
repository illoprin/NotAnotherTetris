from settings import *
from game_logic import *
from view import *
import pygame as pg


class SoundController():

	def __init__(self):
		# Load all sounds and music
		pg.mixer.music.load('sounds/main_theme.ogg')
		pg.mixer.music.play(50)

		self.all_sounds = {
			"selection": pg.mixer.Sound('sounds/menu_select.ogg'),
			"place": pg.mixer.Sound('sounds/place.ogg'),
			"rotate": pg.mixer.Sound('sounds/rotate.ogg'),
			"tetris": pg.mixer.Sound('sounds/tetris.ogg'),
			"line": pg.mixer.Sound('sounds/clear_line.ogg'),
			"next_level": pg.mixer.Sound('sounds/next_level.ogg'),
			"victory": pg.mixer.Sound('sounds/victory.ogg'),
		}

		self.music = {
			"stats": pg.mixer.Sound('sounds/stats.ogg'),
		}

	def stop_all(self):
		pg.mixer.music.pause()
		self.music["stats"].stop()

	def play_music(self, music_name):
		pg.mixer.music.pause()
		self.music[music_name].play()

	def play_main_theme(self, unpause):
		if unpause:
			pg.mixer.music.unpause()
		else:
			pg.mixer.music.play(50)

	def play(self, sound_name):
		self.stop_all()
		self.all_sounds[sound_name].play()

	def play_overlay(self, sound_name):
		self.all_sounds[sound_name].play()