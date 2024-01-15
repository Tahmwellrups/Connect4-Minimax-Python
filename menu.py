import numpy as np
import pygame
import sys
import math
from button import Button

BG = pygame.Color("#203972")
BLUE = pygame.Color("#3E5AAA")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
YELLOW = pygame.Color("#FFF36D")
WHITE = pygame.Color("#FFFFFF")

ROW_COUNT = 6
COLUMN_COUNT = 7

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.init()

background_image = pygame.image.load("resources/Connect4 BG.png")
pygame.display.set_caption('Connecc 4')

SQUARESIZE = 85

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, ((c*SQUARESIZE)+319, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, ((int(c*SQUARESIZE+SQUARESIZE/2))+319, int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, ((int(c*SQUARESIZE+SQUARESIZE/2))+319, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, ((int(c*SQUARESIZE+SQUARESIZE/2))+319, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('montserrat', size)

def player_vs_player():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    screen.fill(BLACK)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        PVP_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=None, pos=(370, 640), 
                            text_input="PLAY AGAIN", font=get_font(64), base_color="#ffffff", hovering_color="#3E5AAA")
        MENU_BUTTON = Button(image=None, pos=(960, 640), 
                            text_input="MAIN MENU", font=get_font(64), base_color="#ffffff", hovering_color="#3E5AAA")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (319,0, width, SQUARESIZE))

                posx = event.pos[0]
                if posx <= 359:
                    posx = 359
                elif posx >= 874:
                    posx = 874
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (319,0, width, SQUARESIZE))
                print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    if posx <= 359:
                        posx = 359
                    elif posx >= 874:
                        posx = 874
                    col = int(math.floor((posx-319)/SQUARESIZE))
                    print(col)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = pygame.font.SysFont('fugaz one', 50).render("PLAYER 1 WINS", 1, RED)
                            screen.blit(label, (445,5))                            
                            
                            for button in [PLAY_BUTTON, MENU_BUTTON]:
                                button.changeColor(PVP_MOUSE_POS)
                                label = pygame.font.SysFont('fugaz one', 50).render("PLAYER 1 WINS", 1, RED)
                                screen.blit(label, (445,5))       
                                button.update(screen)

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if PLAY_BUTTON.checkForInput(PVP_MOUSE_POS):
                                        player_vs_player()
                                    if MENU_BUTTON.checkForInput(PVP_MOUSE_POS):
                                        game_over = True

                            pygame.display.update()

                # # Ask for Player 2 Input
                else:				
                    posx = event.pos[0]
                    if posx <= 359:
                        posx = 359
                    elif posx >= 874:
                        posx = 874
                    col = int(math.floor((posx-319)/SQUARESIZE))
                    print(col)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = pygame.font.SysFont('fugaz one', 50).render("PLAYER 2 WINS", 1, YELLOW)
                            screen.blit(label, (445,5))

                            for button in [PLAY_BUTTON, MENU_BUTTON]:
                                button.changeColor(PVP_MOUSE_POS)
                                label = pygame.font.SysFont('fugaz one', 50).render("PLAYER 2 WINS", 1, YELLOW)
                                screen.blit(label, (445,5))
                                button.update(screen)

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if PLAY_BUTTON.checkForInput(PVP_MOUSE_POS):
                                        player_vs_player()
                                    if MENU_BUTTON.checkForInput(PVP_MOUSE_POS):
                                        game_over = True

                            pygame.display.update()

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2
                
                if game_over:
                    pygame.time.wait(3000)

def player_vs_ai():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill(BG)

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():

    running = True 
    while running:
        screen.blit(background_image, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        menu_text = pygame.font.SysFont('fugaz one', 100).render('CONNECC4', True, WHITE)
        menu_text_Rect = menu_text.get_rect()
        menu_text_Rect.center = (screen_width//2, 100)
        
        PVP_BUTTON = Button(image=pygame.image.load("resources/Button BG.png"), pos=(640, 250), 
                            text_input="PLAYER VS PLAYER", font=get_font(64), base_color="#ffffff", hovering_color="#101B3B")
        PVAI_BUTTON = Button(image=pygame.image.load("resources/Button BG.png"), pos=(640, 400), 
                            text_input="PLAYER VS AI", font=get_font(64), base_color="#ffffff", hovering_color="#101B3B")
        QUIT_BUTTON = Button(image=pygame.image.load("resources/Quit Button BG.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(64), base_color="#ffffff", hovering_color="#101B3B")
        
        screen.blit(menu_text, menu_text_Rect)
        
        for button in [PVP_BUTTON, PVAI_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs_player()
                if PVAI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs_ai()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            

        pygame.display.update()


main_menu()
    
    


