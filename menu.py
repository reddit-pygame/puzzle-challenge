import pygame as pg
import prepare
from state_engine import GameState
from labels import Button, ButtonGroup
from puzzle import Puzzle


class Menu(GameState):
    def __init__(self):
        super(Menu, self).__init__()
        self.screen_rect = prepare.SCREEN_RECT
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        style = {"fill_color": pg.Color("gray10"),
                    "hover_fill_color": pg.Color("gray20"),
                    "text_color": pg.Color("gray80"),
                    "hover_text_color": pg.Color("gray90")}
        continents = sorted(prepare.CONTINENTS)
        w, h = 250, 80
        left = self.screen_rect.centerx - (w // 2)
        top = 50
        vert_space = 100 
        for continent in continents:
            Button((left, top, w, h), self.buttons, text=continent, 
                      hover_text=continent, call=self.choose_map,
                      args=continent, **style)
            top += vert_space
            
    def choose_map(self, continent):
        name = continent.replace(" ", "-")
        img = pg.transform.smoothscale(prepare.GFX[name], (640, 480))
        self.persist["puzzle"] = Puzzle(img)
        self.next_state = "IDLE"
        self.done = True
            
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self, event):
        self.buttons.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.buttons.draw(surface)