from settings import *
from game_logic import *
import sys
import math

class EventListener():
	def __init__(self):
		self.events = []
		# существует словарь events
		# он хранит информацию об обработке событий
		# ключи словря - название события
		# значения словаря - состояние события
		# 0 - событие не произошло
		# 1 - событие произошло и ожидает обработки
		# 2 - событие обработано

	def receive_event(self, event_name):
		self.events.append(event_name)
		print ("Event Listener: event " + event_name + " received")
		print ("Event Listener: Current event listener list is ", self.events)

	def clear_event_stack(self):
		self.events = []