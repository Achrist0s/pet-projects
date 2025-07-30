import pygame
from game import Game
from constants import *
import random

WIN = pygame.display.set_mode((COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE))
pygame.display.set_caption("Шашки")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def show_winner(winner_name):
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render(f"Переможець: {winner_name}", True, HIGHLIGHT)
    WIN.blit(text, (200, 300))

    button_font = pygame.font.SysFont("comicsans", 40)
    btn_text = button_font.render("Грати ще", True, WHITE)
    btn_rect = pygame.Rect(300, 400, 200, 60)
    pygame.draw.rect(WIN, BLACK, btn_rect)
    WIN.blit(btn_text, (btn_rect.x + 25, btn_rect.y + 10))
    pygame.display.update()
    return btn_rect

def main():
    run = True
    clock = pygame.time.Clock()

    player_color = random.choice([WHITE, BLACK])
    print("Гравець грає за", "білих" if player_color == WHITE else "чорних")

    game = Game(WIN, player_color)

    while run:
        clock.tick(60)

        winner = game.winner()
        if winner:
            btn_rect = show_winner(winner)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        waiting = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_rect.collidepoint(event.pos):
                            player_color = random.choice([WHITE, BLACK])
                            game = Game(WIN, player_color)
                            waiting = False

        if game.turn != game.player_color:
            pygame.time.delay(500)
            game.ai_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == game.player_color:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()
