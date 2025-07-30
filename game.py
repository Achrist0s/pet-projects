import pygame
from board import Board
from constants import *
import random

class Game:
    def __init__(self, win, player_color):
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.player_color = player_color
        self.turn = WHITE

    def update(self):
        self.board.draw(self.win)
        if self.selected:
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.__init__(self.win, self.player_color)

    def select(self, row, col):
        if (row + col) % 2 == 0:
            return False

        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        self.turn = BLACK if self.turn == WHITE else WHITE

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, HIGHLIGHT, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def winner(self):
        return self.board.winner()

    def ai_move(self):
        best_score = -1
        best_move = None

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    valid = self.board.get_valid_moves(piece)
                    for move, skipped in valid.items():
                        score = len(skipped)
                        if piece.king:
                            score += 0.5
                        if (piece.color == BLACK and move[0] == ROWS - 1) or \
                           (piece.color == WHITE and move[0] == 0):
                            score += 1  # стати дамкою

                        if score > best_score:
                            best_score = score
                            best_move = (piece, move, skipped)

        if best_move:
            piece, move, skipped = best_move
            self.board.move(piece, move[0], move[1])
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
