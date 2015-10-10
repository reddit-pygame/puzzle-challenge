import pygame as pg
import prepare
from state_engine import GameState
from puzzle import Puzzle


class Idle(GameState):
    def __init__(self):
        super(Idle, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.puzzle = self.persist["puzzle"]
        self.sections = self.puzzle.sections
        self.pieces = self.puzzle.pieces.values()
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            for section in self.puzzle.sections:
                if section.grab(event.pos):
                    self.persist["grabbed_piece"] = section
                    self.next_state = "DRAGGING_SECTION"
                    self.done = True
                    return
            for piece in self.pieces:
                if piece.rect.collidepoint(event.pos):
                    piece.grabbed = True
                    self.persist["grabbed_piece"] = piece
                    self.next_state = "DRAGGING_PIECE"
                    self.done = True
                    return
    
    def update(self, dt):
        pass
        
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.puzzle.draw(surface)
    