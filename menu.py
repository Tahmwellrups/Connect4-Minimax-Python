import pygame
import sys
from button import Button

BG = pygame.Color("#203972")
BLUE = pygame.Color("#3E5AAA")
DARK_BLUE = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
YELLOW = pygame.Color("#FFF36D")
WHITE = pygame.Color("#FFFFFF")

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.init()

background_image = pygame.image.load("Connect4 BG.png")
pygame.display.set_caption('Connecc 4')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('montserrat', size)

def player_vs_player():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

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

def player_vs_ai():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

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
        
        PVP_BUTTON = Button(image=pygame.image.load("Button BG.png"), pos=(640, 250), 
                            text_input="PLAYER VS PLAYER", font=get_font(53), base_color="#ffffff", hovering_color="#101B3B")
        PVAI_BUTTON = Button(image=pygame.image.load("Button BG.png"), pos=(640, 400), 
                            text_input="PLAYER VS AI", font=get_font(53), base_color="#ffffff", hovering_color="#101B3B")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Button BG.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(53), base_color="#ffffff", hovering_color="#101B3B")
        
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
    
    


