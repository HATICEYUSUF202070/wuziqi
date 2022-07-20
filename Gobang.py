import numpy as np
import pygame, sys
from pygame import QUIT, font, MOUSEBUTTONDOWN
pygame.init()

width, height = 960, 960

screen = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
space = 60

##img
background = pygame.image.load("imags/tahta.jpg")
background = pygame.transform.scale(background, (1000, 1000))
# white_piece
white_piece = pygame.image.load("imags/Go_w_no_bg.svg.png").convert_alpha()
white_piece = pygame.transform.scale(white_piece, (40, 40))
# black_piece
black_piece = pygame.image.load("imags/Go_b_no_bg.svg.png").convert_alpha()
black_piece = pygame.transform.scale(black_piece, (40, 40))

###font
font = pygame.font.SysFont('arial', 20)

first_intersection = (40, 40)

step = 60
line = 15
is_white = False
board_piece_pos = []
white_piece_pos = {}
black_piece_pos = {}
MZ=[



]

def finde_can_move_pos(x, y):
    # kesişim noktalari
    # j sağdan sola doğru sayar
    # i üstten aşağa doğru sayar
    for i in range(60, height, space):
        for j in range(60, height, space):
            if (x < (i + 3)) and (x > (i - 3)) and (y < (j + 3)) and (y > (j - 3)):
                return True
    return False


pos_index = {}


def find_intersection():
    index = 0
    for i in range(60, height, space):
        for j in range(60, height, space):
            pos_index[(i, j)] = index
            index += 1
    print(pos_index)


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
    if finde_can_move_pos(x, y):
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

    for i in board_piece_pos:
        x=int(i[0]+60)
        y=int(i[1])


    # sol düz 5


# üst dik 5
# alt dik 5
# üst sag çapraz 5
# alt sag çapraz 5
# üst sol çapraz 5
# alt sol çapraz 5


pos = (0, 0)
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
            print(finde_can_move_pos(x, y))

            if finde_can_move_pos(x, y):
                if is_valid(x, y):
                    draw_piece((x - 19, y - 15))
                    count += 1
                    board_piece_pos.append(pos)
                    color(pos)
                    print(black_piece_pos)
                    print(white_piece_pos)

                    is_white = not is_white

    pygame.display.update()
