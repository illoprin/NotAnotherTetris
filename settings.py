import pygame

GAME_FIELD_W = 10
GAME_FIELD_H = 20

AVALIABLE_FIGURES = ("Z", "S", "L", "J", "T", "O", "I")
FIGURES = {
	"Z": (1, 2, 3, 4), # Z
	"S": (0, 2, 3, 5), # S
	"L": (0, 2, 4, 5), # L
	"J": (1, 3, 4, 5), # J
	"T": (0, 2, 3, 4), # T
	"O": (0, 1, 2, 3), # O
	"I": (0, 2, 4, 6), # I
}

FIGURES_COLOR = (49, 48, 77)


WIN_W = 1024
WIN_H = 768
BLOCK_SIZE = int(((WIN_W + WIN_H)*.04) / 2)
TILESET_BLOCK_SIZE = 9
FIELD_MARGIN = int(((WIN_W + WIN_H)*.025) / 2)
FPS = 60
BACKGOUND_COLOR = (20, 20, 20)

# Keys for tetramino handle
K_F_LEFT = pygame.K_LEFT
K_F_RIGHT = pygame.K_RIGHT
K_F_DOWN = pygame.K_DOWN
K_F_ROTATE = pygame.K_UP
K_F_MIRROR = pygame.K_t

K_START = pygame.K_SPACE
K_RESTART = pygame.K_r