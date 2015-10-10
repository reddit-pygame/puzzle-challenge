import sys
import pygame as pg

from state_engine import Game, GameState
import prepare
import menu, idle, dragging_piece, dragging_section

states = {"MENU": menu.Menu(),
               "IDLE": idle.Idle(),
               "DRAGGING_PIECE": dragging_piece.DraggingPiece(),
               "DRAGGING_SECTION": dragging_section.DraggingSection()}
game = Game(prepare.SCREEN, states, "MENU")
game.run()
pg.quit()
sys.exit()