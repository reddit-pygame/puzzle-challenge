import os
import pygame as pg
import tools


SCREEN_SIZE = (1000, 600)
ORIGINAL_CAPTION = "Puzzler"

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()
PIECE_RECT_SIZE = (80, 60)
CONTINENTS = ("Africa", "North America", "South America", "Europe", "Asia", "Oceania")

GFX = tools.load_all_gfx(os.path.join("resources", "graphics"))
