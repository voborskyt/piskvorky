import pygame
from my_dataclasses import data_game_class
from colors import *

class GameBoard:
    def __init__(self, x, y, screen: pygame.display):
        self.x = x
        self.y = y
        self.screen = screen
        self.size = 20
        self.cols = 6
        self.game_exist = False
        self.game = None
        self.player1name = "None"
        self.player2name = "None"
        self.player1score = None
        self.player2score = None
        self.font = pygame.font.Font(None, 18)
        self.active = False
        self.active_game_col = {"Lines": BLACK, "Player1": BLUE, "Player2": RED, "Font": BLACK}
        self.nonactive_game_col = {"Lines": GREY, "Player1": LIGHT_BLUE, "Player2": LIGHT_RED, "Font": GREY}
        self.current_game_col = self.active_game_col

    def draw_board(self):
        for i in range(self.cols):
            pygame.draw.line(self.screen, self.current_game_col["Lines"], (self.x, self.y+i*self.size),
                             (self.x+self.size*(self.cols-1), self.y+i*self.size), 2)
        for i in range(self.cols):
            pygame.draw.line(self.screen, self.current_game_col["Lines"], (self.x + i * self.size, self.y),
                             (self.x + i * self.size, self.y + self.size * (self.cols-1)), 2)

    def draw_game(self):
        for i in range(self.cols-1):
            for j in range(self.cols-1):
                if self.game[i,j] == 1:
                    pygame.draw.circle(self.screen, self.current_game_col["Player1"],
                                       (self.x + (i) * self.size+self.size / 2,
                                        self.y + (j) * self.size+self.size / 2), 5)
                if self.game[i,j] == -1:
                    pygame.draw.circle(self.screen, self.current_game_col["Player2"],
                                       (self.x + (i) * self.size + self.size / 2,
                                        self.y + (j) * self.size + self.size / 2), 5)

    def draw_text(self):
        self.textexpr = (self.player1name.ljust(9) + str(self.player1score) +" | " +
                         str(self.player2score) + self.player2name.rjust(9))
        self.text = self.font.render(self.textexpr, True, self.current_game_col["Font"])
        self.text_rect = self.text.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y - 20
        self.screen.blit(self.text, self.text_rect)

    def reset_game(self):
        self.game_exist = False
        self.game = None
        self.player1name = None
        self.player2name = None
        self.player1score = 0
        self.player2score = 0
        self.active = False

    def set_game(self, data_game: data_game_class):
        self.game = data_game.board
        self.player1name = data_game.player1name
        self.player2name = data_game.player2name
        self.player1score = data_game.player1score
        self.player2score = data_game.player2score
        self.active = data_game.active
        self.game_exist = True

    def draw(self):
        if(self.active):
            self.current_game_col = self.active_game_col
        else:
            self.current_game_col = self.nonactive_game_col

        self.draw_board()

        if(self.game_exist):
            self.draw_game()
            self.draw_text()
