import pygame as pg
import prepare
from state_engine import GameState


class DraggingSection(GameState):
    def __init__(self):
        super(DraggingSection, self).__init__()
        self.connect_sound = prepare.SFX["connect"]
        
    def startup(self, persistent):
        self.persist = persistent
        self.puzzle = self.persist["puzzle"]
        self.sections = self.puzzle.sections
        self.pieces = self.puzzle.pieces.values()
        self.grabbed = self.persist["grabbed_piece"]
   
    def leave_state(self, next_state):
        self.done = True
        self.next_state = next_state
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            for section in [x for x in self.sections if x is not self.grabbed]:
                if self.grabbed.can_add_section(section):
                    self.grabbed.add_section(section)
                    self.connect_sound.play()
                    self.sections.remove(section)
                    self.grabbed.release()
                    self.leave_state("IDLE")
                    return
            self.leave_state("IDLE")
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.grabbed.set_pos(mouse_pos)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.puzzle.draw(surface)