
import numpy as np
import random
import pygame
import sys
import math

BLUE = pygame.Color("#3E5AAA")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
YELLOW = pygame.Color("#FFF36D")

ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def boardCreate():
    board = np.zeros((6,7))
    return board

def is_valid_location(board, col):
    #ROW-COUNT-1 IS THE TOP MOST ROW, IF IT IS EMPTY (=0) THE ROW IS STILL VALID
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def print_board(board):
    print(np.flip(board, 0))

board = boardCreate()
print_board(board)
game_over = False
turn = 0 

pygame.init()


while not game_over:
    #Player 1
    if turn == 0:
        col = int(input("Player 1 enter number from 0-6: "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

    
    #Player 2
    else:
        col = int(input("Player 2 enter number from 0-6: "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

    print_board(board)
    turn += 1
    turn = turn % 2
   
