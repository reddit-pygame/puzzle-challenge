from random import randint, shuffle
import pygame as pg
import prepare
from puzzle_piece import PuzzlePiece, PuzzleSection


class Puzzle(object):
    def __init__(self, puzzle_image):
        self.make_pieces(puzzle_image)
        self.piece_total = len(self.pieces)
        self.spread_pieces()
        self.sections = []
        
    def get_event(self, event):
        self.state.get_event(event)

    def update(self, dt):
        pass
        
    def draw(self, surface):
        for section in reversed(self.sections):
            section.draw(surface)
        for piece in reversed(self.pieces.values()):
            piece.draw(surface)
        
    def make_pieces(self, puzzle_image):
        self.pieces = {}
        img = puzzle_image
        img_rect = img.get_rect()
        for column, x in enumerate(range(0, 640, 80)):
            for row, y in enumerate(range(0, 480, 60)):
                rect = pg.Rect(x - 20, y - 16, 120, 92)
                clipped= rect.clip(img_rect)
                offset = clipped.x - rect.x, clipped.y - rect.y
                surf = pg.Surface((120, 92))
                surf.blit(img.subsurface(clipped), offset)
                cover = prepare.GFX["piece{}-{}".format(column, row)]
                surf.blit(cover, (0, 0))
                surf.set_colorkey(pg.Color("black"))
                self.pieces[(column, row)] = PuzzlePiece((column, row), surf, (x, y))
        for piece in self.pieces.values():
            piece.get_neighbors(self.pieces)
        
    def spread_pieces(self):
        screen_w, screen_h  = prepare.SCREEN_SIZE
        w = screen_w // 8
        h = screen_h // 8
        rects = [pg.Rect(x, y, w, h)
                for y in range(0, screen_h, h)
                for x in range(0, screen_w, w)]
        pieces = self.pieces.values()
        shuffle(pieces)
        for p, rect in zip(pieces, rects):
            p.rect.center = rect.center
            
    def join_pieces(self, piece1, piece2):
        p1 = pg.Rect((0, 0), prepare.PIECE_RECT_SIZE)
        p2 = p1.copy()
        p1.center = piece1.rect.center
        for side in piece2.neighbors:
            if piece1 is piece2.neighbors[side]:
                if side == "left":
                    p2.left = p1.right
                    p2.top = p1.top
                elif side == "right":
                    p2.right = p1.left
                    p2.top = p1.top
                elif side == "top":
                    p2.top = p1.bottom
                    p2.left = p1.left
                elif side == "bottom":
                    p2.bottom = p1.top
                    p2.left = p1.left
        piece2.rect.center = p2.center
        section = PuzzleSection((piece1, piece2))
        indices = (piece1.index, piece2.index)
        for ind in indices:
            try:
                del self.pieces[ind]
            except KeyError:
                pass
        self.sections.append(section)
        
        





            
            
