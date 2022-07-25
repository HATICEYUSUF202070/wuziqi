import numpy as np
import pygame, sys
from pygame import QUIT, font, MOUSEBUTTONDOWN
from pygame.time import Clock

from color import Colors


class Go:
    def __int__(self):
        self.size = (960, 960)
        self.font = pygame.font.SysFont('arial', 20)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = Clock()
        self.space = 60
        self.pieces_size = 40
        self.line = 15
        self.is_white = False
        self.board_piece_pos = []
        self.white_piece_pos = {}
        self.black_piece_pos = {}
        background_img = pygame.image.load("imags/tahta.jpg")
        self.background = pygame.transform.scale(background_img, (1000, 1000))
        # white_piece
        white_piece_img = pygame.image.load("imags/Go_w_no_bg.svg.png").convert_alpha()
        self.white_piece = pygame.transform.scale(white_piece_img, (self.pieces_size, self.pieces_size))
        # black_piece
        black_piece_img = pygame.image.load("imags/Go_b_no_bg.svg.png").convert_alpha()
        self.black_piece = pygame.transform.scale(black_piece_img, (self.pieces_size, self.pieces_size))
        self.screen.blit(self.background, (0, 0))

    def draw_board(self):
        x, y = self.size[0], self.size[1]
        number_space = 30
        # sayi+dik çizgi
        for i in range(self.line):

            if i < 9:
                line_number = self.font.render(str(i + 1), True, Colors.black)
                self.screen.blit(line_number, (number_space, y - 10))
            else:
                line_number = self.font.render(str(i + 1), True, Colors.black)
                self.screen.blit(line_number, (number_space - 5, y - 10))

            pygame.draw.line(self.screen, Colors.black, (self.space, y), (x - self.space, y), 1)
            y += self.space
        x, y = self.size[0], self.size[1]
        # harf+düz çizgi
        for i in range(self.line):
            # MERKEZ NOKTA
            if i == 7:
                pygame.draw.circle(self.screen, Colors.black, (x, 8 * self.space), 6)
            # 4 YIZDIZ NOKTA
            if i == 3:
                pygame.draw.circle(self.screen, Colors.black, (x, 4 * self.space), 5)
                pygame.draw.circle(self.screen, Colors.black, (x + (8 * self.space), 4 * self.space), 5)
                pygame.draw.circle(self.screen, Colors.black, (x, 12 * self.space), 5)
                pygame.draw.circle(self.screen, Colors.black, (x + (8 * self.space), 12 * self.space), 5)

            line_number = self.font.render(chr(i + 65), True, Colors.black)
            self.screen.blit(line_number, (x - 5, y - self.space + 10))
            pygame.draw.line(self.screen, Colors.black, (x, self.space), (x, y - self.space), 1)
            x += self.space

    def draw_piece(self, positions):

        if self.is_white:
            self.background.blit(self.white_piece, positions)
            self.black_piece_pos[positions] = "white"
        else:
            self.background.blit(self.black_piece, positions)
            self.white_piece_pos[positions] = "black"

    def find_can_move_pos(self, x, y):
        # kesişim noktalari
        # j sağdan sola doğru sayar
        # i üstten aşağa doğru sayar
        for i in range(self.space, self.size[0], self.space):
            for j in range(self.space, self.size[0], self.space):
                if (x < (i + 3)) and (x > (i - 3)) and (y < (j + 3)) and (y > (j - 3)):
                    return True
        return False

    def is_valid(self, x, y):
        if self.find_can_move_pos(x, y):
            for i in range(len(self.board_piece_pos)):
                if (x < (self.board_piece_pos[i][0] + 5)) and (x > (self.board_piece_pos[i][0] - 5)) and (
                        y < (self.board_piece_pos[i][1] + 5)) and (y > (self.board_piece_pos[i][1] - 5)):
                    return False
        return True

    def find_color(self, pos):
        white = "white"
        black = "black"
        for i in self.black_piece_pos.keys():
            if pos == i:
                return white

        for i in self.white_piece_pos.keys():
            if pos == i:
                return black

    def is_win(self):
        a = np.zeros([15, 15], dtype=int)
        for p in self.board_piece_pos:
            x = int((p[0] - 44) / 60)
            y = int((p[1] - 44) / 60)
            if self.find_color(p) == "white":
                a[y][x] = 1
            else:
                a[y][x] = 2
        # düz 5    a[x][y]
        for i in range(15):
            white_5 = []
            black_5 = []
            for j in range(15):
                if a[i][j] == 1:
                    white_5.append((i, j))
                else:
                    white_5 = []
                if a[i][j] == 2:
                    black_5.append((i, j))
                else:
                    black_5 = []
                if len(white_5) >= 5:
                    return [1, white_5]
                if len(black_5) >= 5:
                    return [2, black_5]
        # dik 5  a[y][x]
        for j in range(15):
            white_5 = []
            black_5 = []
            for i in range(15):
                if a[i][j] == 1:
                    white_5.append([i, j])
                else:
                    white_5 = []
                if a[i][j] == 2:
                    black_5.append([i, j])
                else:
                    black_5 = []
                if len(white_5) >= 5:
                    return [1, white_5]
                if len(black_5) >= 5:
                    return [2, black_5]
        # sağdan sola çapraz 5  a[x+1][y-1]
        for i in range(15):
            for j in range(15):
                white_5 = []
                black_5 = []
                for k in range(15):
                    if i + k >= 15 or j + k >= 15:
                        break
                    if a[i + k][j + k] == 1:
                        white_5.append([i + k, j + k])
                    else:
                        white_5 = []
                    if a[i + k][j + k] == 2:
                        black_5.append([i + k, j + k])
                    else:
                        black_5 = []
                    if len(white_5) >= 5:
                        return [1, white_5]
                    if len(black_5) >= 5:
                        return [2, black_5]
        # yukardan sağa çapraz 5 a[x-1][y+1]
        for i in range(15):
            for j in range(15):
                white_5 = []
                black_5 = []
                for k in range(15):
                    if i + k >= 15 or j - k < 0:
                        break
                    if a[i + k][j - k] == 1:
                        white_5.append([i + k, j - k])
                    else:
                        white_5 = []
                    if a[i + k][j - k] == 2:
                        black_5.append([i + k, j - k])
                    else:
                        black_5 = []
                    if len(white_5) >= 5:
                        return [1, white_5]
                    if len(black_5) >= 5:
                        return [2, black_5]

    def run(self):
        run = True
        while run:
            self.draw_board()
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    x, y = pos = event.pos
                    print(self.find_can_move_pos(x, y))
                    if self.is_win() == None:
                        if self.find_can_move_pos(x, y):
                            if self.is_valid(x, y):
                                self.draw_piece((x - 19, y - 15))
                                self.board_piece_pos.append(pos)
                                self.find_color(pos)
                                print(self.black_piece_pos)
                                print(self.white_piece_pos)

                                self.is_white = not self.is_white
                    else:
                        win_piece = self.is_win()
                        if win_piece[0] == 1:
                            print("white piece win !!", win_piece[1])
                        else:
                            print("black piece win !!", win_piece[1])

            pygame.display.flip()
