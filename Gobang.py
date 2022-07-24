import numpy as np
import pygame, sys
from pygame import QUIT, font, MOUSEBUTTONDOWN

pygame.init()

width, height = 960, 960

screen = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
space = 60
pieces_size = 40

##img
background = pygame.image.load("imags/tahta.jpg")
background = pygame.transform.scale(background, (1000, 1000))
# white_piece
white_piece = pygame.image.load("imags/Go_w_no_bg.svg.png").convert_alpha()
white_piece = pygame.transform.scale(white_piece, (pieces_size, pieces_size))
# black_piece
black_piece = pygame.image.load("imags/Go_b_no_bg.svg.png").convert_alpha()
black_piece = pygame.transform.scale(black_piece, (pieces_size, pieces_size))

###font
font = pygame.font.SysFont('arial', 20)

step = 60
line = 15
is_white = False
board_piece_pos = []
white_piece_pos = {}
black_piece_pos = {}


def find_can_move_pos(x, y):
    # kesişim noktalari
    # j sağdan sola doğru sayar
    # i üstten aşağa doğru sayar
    for i in range(60, height, space):
        for j in range(60, height, space):
            if (x < (i + 3)) and (x > (i - 3)) and (y < (j + 3)) and (y > (j - 3)):
                return True
    return False


def draw_board():
    x, y = width, space
    number_space = 30
    # sayi+dik çizgi
    for i in range(line):

        if i < 9:
            line_number = font.render(str(i + 1), True, black)
            screen.blit(line_number, (number_space, y - 10))
        else:
            line_number = font.render(str(i + 1), True, black)
            screen.blit(line_number, (number_space - 5, y - 10))

        pygame.draw.line(screen, black, (space, y), (x - space, y), 1)
        y += space
    x, y = space, height
    # harf+düz çizgi
    for i in range(line):
        # MERKEZ NOKTA
        if i == 7:
            pygame.draw.circle(screen, black, (x, 8 * space), 6)
        # 4 YIZDIZ NOKTA
        if i == 3:
            pygame.draw.circle(screen, black, (x, 4 * space), 5)
            pygame.draw.circle(screen, black, (x + (8 * space), 4 * space), 5)
            pygame.draw.circle(screen, black, (x, 12 * space), 5)
            pygame.draw.circle(screen, black, (x + (8 * space), 12 * space), 5)

        line_number = font.render(chr(i + 65), True, black)
        screen.blit(line_number, (x - 5, y - space + 10))
        pygame.draw.line(screen, black, (x, space), (x, y - space), 1)
        x += space


def is_valid(x, y):
    if find_can_move_pos(x, y):
        for i in range(len(board_piece_pos)):
            if (x < (board_piece_pos[i][0] + 5)) and (x > (board_piece_pos[i][0] - 5)) and (
                    y < (board_piece_pos[i][1] + 5)) and (y > (board_piece_pos[i][1] - 5)):
                return False
    return True


def draw_piece(board_piece_pos):
    if is_white:
        background.blit(white_piece, board_piece_pos)
        black_piece_pos[pos] = "white"
        print("white")
    else:
        background.blit(black_piece, board_piece_pos)
        white_piece_pos[pos] = "black"
        print("black")


def color(pos):
    white = "white"
    black = "black"
    for i in black_piece_pos.keys():
        if pos == i:
            return white

    for i in white_piece_pos.keys():
        if pos == i:
            return black


def is_win(board_piece_pos):
    a = np.zeros([15, 15], dtype=int)
    for p in board_piece_pos:
        x = int((p[0] - 44) / 60)
        y = int((p[1] - 44) / 60)
        if color(p) == "white":
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


run = True
count = 0
while run:
    screen.blit(background, (0, 0))
    draw_board()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            x, y = pos = event.pos
            print(find_can_move_pos(x, y))
            if is_win(board_piece_pos) == None:
                if find_can_move_pos(x, y):
                    if is_valid(x, y):
                        draw_piece((x - 19, y - 15))
                        count += 1
                        board_piece_pos.append(pos)
                        color(pos)
                        print(black_piece_pos)
                        print(white_piece_pos)

                        is_white = not is_white
            else:
                win_piece = is_win(board_piece_pos)
                if win_piece[0] == 1:
                    print("white piece win !!", win_piece[1])
                else:
                    print("black piece win !!", win_piece[1])

    pygame.display.update()
