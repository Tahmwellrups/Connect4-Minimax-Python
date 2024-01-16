import numpy as np
import pygame
import sys
import math
import random
from button import Button

BG = pygame.Color("#203972")
BLUE = pygame.Color("#3E5AAA")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
YELLOW = pygame.Color("#FFF36D")
WHITE = pygame.Color("#FFFFFF")

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.init()

background_image = pygame.image.load("resources/Connect 4 BG.png")
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
			pygame.draw.rect(screen, BLUE, ((c*SQUARESIZE)+344, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, ((int(c*SQUARESIZE+SQUARESIZE/2))+344, int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, ((int(c*SQUARESIZE+SQUARESIZE/2))+344, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, ((int(c*SQUARESIZE+SQUARESIZE/2))+344, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('lilita one', size)

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def game_over_options(board, label, mode):
	
    pvp_bg = pygame.image.load("resources/PVP_BG.png")
    screen.blit(pvp_bg, (0,0))
    draw_board(board)
    screen.blit(label, (442,7))
	
    # Your loop for checking events
    while True:
        PVP_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=None, pos=(460, 650), text_input="PLAY AGAIN", font=get_font(40), base_color="#ffffff", hovering_color="#D32735")
        MENU_BUTTON = Button(image=None, pos=(830, 650), text_input="MAIN MENU", font=get_font(40), base_color="#ffffff", hovering_color="#D32735")


        for button in [PLAY_BUTTON, MENU_BUTTON]:
            button.changeColor(PVP_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(PVP_MOUSE_POS):
                    if mode == 1:
                        player_vs_player()
                    else:
                        player_vs_ai()
                elif MENU_BUTTON.checkForInput(PVP_MOUSE_POS):
                    main_menu()
		
        pygame.display.flip()		
        
        

def player_vs_player():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pvp_bg = pygame.image.load("resources/PVP_BG.png")
    screen.blit(pvp_bg, (0,0))
    draw_board(board)
    pygame.display.update()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (344,0, width, SQUARESIZE))

                posx = event.pos[0]
                if posx <= 384:
                    posx = 384
                elif posx >= 899:
                    posx = 899
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (344,0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    if posx <= 384:
                        posx = 384
                    elif posx >= 899:
                        posx = 899
                    col = int(math.floor((posx-344)/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = get_font(60).render("PLAYER 1 WINS!", 1, RED)                          
                            game_over_options(board, label, 1)
                            

                # Ask for Player 2 Input
                else:				
                    posx = event.pos[0]
                    if posx <= 384:
                        posx = 384
                    elif posx >= 899:
                        posx = 899
                    col = int(math.floor((posx-344)/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = get_font(60).render("PLAYER 2 WINS!", 1, YELLOW)
                            game_over_options(board, label, 1)
                            
                            

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2
                
                if game_over:
                    pygame.time.wait(3000) 
                    
                    
					
def player_vs_ai():
    board = create_board()
    print_board(board)
    game_over = False

    pvp_bg = pygame.image.load("resources/PVP_BG.png")
    screen.blit(pvp_bg, (0,0))
    draw_board(board)
    pygame.display.update()

    turn = random.randint(PLAYER, AI)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (344,0, width, SQUARESIZE))
                posx = event.pos[0]
                if posx <= 384:
                        posx = 384
                elif posx >= 899:
                    posx = 899
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (344,0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    if posx <= 384:
                        posx = 384
                    elif posx >= 899:
                        posx = 899
                    col = int(math.floor((posx-344)/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = get_font(60).render("PLAYER 1 WINS!", 1, RED)                          
                            game_over_options(board, label, 2)

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)


        # # Ask for Player 2 Input
        if turn == AI and not game_over:				

            #col = random.randint(0, COLUMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                #pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = get_font(60).render("PLAYER 2 WINS!", 1, YELLOW)                          
                    game_over_options(board, label, 2)

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

def main_menu():

    running = True 
    while running:
        screen.blit(background_image, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        PVP_BUTTON = Button(image=None, pos=(960, 300), 
                            text_input="PLAYER VS PLAYER", font=get_font(64), base_color="#ffffff", hovering_color="#D32735")
        PVAI_BUTTON = Button(image=None, pos=(960, 450), 
                            text_input="PLAYER VS AI", font=get_font(64), base_color="#ffffff", hovering_color="#D32735")
        QUIT_BUTTON = Button(image=None, pos=(960, 600), 
                            text_input="QUIT", font=get_font(64), base_color="#ffffff", hovering_color="#D32735")
        
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
    
    


