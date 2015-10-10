import pygame as pg
from state_engine import GameState


class DraggingPiece(GameState):
    def __init__(self):
        super(DraggingPiece, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.puzzle = self.persist["puzzle"]
        self.sections = self.puzzle.sections
        self.pieces = self.puzzle.pieces.values()
        self.grabbed = self.persist["grabbed_piece"]
        
    def check_pieces(self):
        """
        Checks whether self.grabbed (the piece controlled by the
        player) can be joined with any of the other unjoined
        pieces. If so, the pieces are joined and True is returned.
        Returns False if the piece cannot be joined with any others.
        """
        for piece in self.pieces:
            if self.grabbed.is_joinable(piece):
                self.puzzle.join_pieces(self.grabbed, piece)
                return True
        return False
        
    def check_sections(self): 
        """
        Similar to check_pieces but checks whether self.grabbed can be
        joined with any of the existing puzzle sections. If it can be joined
        it is added to the section and True is returned. Returns False if
        the piece cannot be added to any of the sections.
        """
        for section in self.sections:
            if section.can_add(self.grabbed):
                section.add_piece(self.grabbed, self.puzzle.pieces)
                return True
        return False
                    
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            if not self.check_pieces():
                self.check_sections()
            self.grabbed.grabbed = False
            self.done = True
            self.next_state = "IDLE"
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.grabbed.set_pos(mouse_pos)
        
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.puzzle.draw(surface)