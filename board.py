import pygame
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 3 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, BLACK))
                elif row > 4 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, WHITE))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        if (row + col) % 2 == 0:
            return

        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        piece.move(row, col)

        if (piece.color == WHITE and row == 0) or (piece.color == BLACK and row == ROWS - 1):
            if not piece.king:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.black_kings += 1

    def get_piece(self, row, col):
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return None
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return "Чорні"
        elif self.black_left <= 0:
            return "Білі"
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0 or (r + left) % 2 == 0:
                break  # світла клітинка, туди ходити не можна

            current = self.get_piece(r, left)
            if current == 0:
                if (r + left) % 2 == 0:
                    break

                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    moves.update(self._traverse_left(r + step, stop, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, stop, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS or (r + right) % 2 == 0:
                break  # світла клітинка, туди ходити не можна

            current = self.get_piece(r, right)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    moves.update(self._traverse_left(r + step, stop, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, stop, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves
