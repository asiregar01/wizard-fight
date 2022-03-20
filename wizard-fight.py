import random, time, pygame, sys
from random import seed
from random import randint
from pygame.locals import *
import pygbutton

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
UP_KEY = False
DOWN_KEY = False
BACK_KEY = False
START_KEY = False
MAIN_MENU = False
HELP_MENU = False
INFO_MENU = False
FIRST_TURN = True
PLAYER_TURN = True
PLAYER_HEALTH = 100
COMPUTER_HEALTH = 100
ATTACK = ""
DEFEND = ""
COMPUTER_ATTACK = ""
COMPUTER_DEFEND = ""
SCREEN = ("TITLE", "HELP", "INFO", "INITIAL", "ATTACK", "DEFEND", "SIMULATION", "RESULT")
CURRENT_SCREEN = SCREEN[0]

# global button variables
START_BUTTON = pygbutton.PygButton((200, 425, 60, 30), 'START')
INFO_BUTTON = pygbutton.PygButton((200 + 60 + 10, 425, 60, 30), 'INFO')
HELP_BUTTON = pygbutton.PygButton((200 + (60 * 2) + (10 * 2), 425, 60, 30), 'HELP')
QUIT_BUTTON = pygbutton.PygButton((200 + (60 * 3) + (10 * 3), 425, 60, 30), 'QUIT')
TITLE_BUTTONS = (START_BUTTON, INFO_BUTTON, HELP_BUTTON, QUIT_BUTTON)

MAIN_BUTTON = pygbutton.PygButton((200, 325, 60, 30), 'MAIN')
QUIT_I_BUTTON = pygbutton.PygButton((200 + (60 * 3) + (10 * 3), 325, 60, 30), 'QUIT')
INFO_BUTTONS = (MAIN_BUTTON, QUIT_I_BUTTON)

FIGHT_BUTTON = pygbutton.PygButton((200 + 60 + 10, 375, 60, 30), 'FIGHT')
QUIT_F_BUTTON = pygbutton.PygButton((200 + (60 * 2) + (10 * 2), 375, 60, 30), 'QUIT')
INITIAL_BUTTONS = (FIGHT_BUTTON, QUIT_F_BUTTON)

FIRE_BUTTON = pygbutton.PygButton((50, 100, 100, 30), 'FIRE')
LIGHTNING_BUTTON = pygbutton.PygButton((50, 200, 100, 30), 'LIGHTNING')
WATER_BUTTON = pygbutton.PygButton((50, 300, 100, 30), 'WATER')
ATTACK_BUTTON = pygbutton.PygButton((450, 200, 100, 30), 'ATTACK')
ATTACK_BUTTONS = (FIRE_BUTTON, LIGHTNING_BUTTON, WATER_BUTTON, ATTACK_BUTTON)

FIRE_SHIELD_BUTTON = pygbutton.PygButton((150, 150, 150, 30), 'FIRE SHIELD')
LIGHTNING_SHIELD_BUTTON = pygbutton.PygButton((150, 250, 150, 30), 'LIGHTNING SHIELD')
WATER_SHIELD_BUTTON = pygbutton.PygButton((150, 350, 150, 30), 'WATER SHIELD')
DEFEND_BUTTON = pygbutton.PygButton((400, 250, 100, 30), 'DEFEND')
DEFEND_BUTTONS = (FIRE_SHIELD_BUTTON, LIGHTNING_SHIELD_BUTTON, WATER_SHIELD_BUTTON, DEFEND_BUTTON)

OK_BUTTON = pygbutton.PygButton((75, 150, 60, 30), 'OK')

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

def button(position, text, size, colors="white on blue"):
    global DISPLAYSURF
    fg, bg = colors.split(" on ")
    font = pygame.font.Font("fonts/8-bit-wonder.ttf", size)
    text_render = font.render(text, 1, fg)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(DISPLAYSURF, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(DISPLAYSURF, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(DISPLAYSURF, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(DISPLAYSURF, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(DISPLAYSURF, bg, (x, y, w , h))
    print(DISPLAYSURF.blit(text_render, (x, y)))
    
    return DISPLAYSURF.blit(text_render, (x, y)) 
 
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, PLAYER_TURN
    global START_BUTTON, INFO_BUTTON, HELP_BUTTON, QUIT_BUTTON, TITLE_BUTTONS
    global PLAYER_HEALTH, COMPUTER_HEALTH, SCREEN, CURRENT_SCREEN
    global PLAYTER_TURN, ATTACK, DEFEND
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Wizard Fight')
    
    pygame.mixer.init()
    pygame.mixer.music.load('assets/music/alex-productions-epic-cinematic-gaming-cyberpunk-reset.mp3')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)

    
    bg_image = pygame.image.load("assets/images/background.jpg")
    DISPLAYSURF.blit(bg_image,(0,0))    
    first_player = random_first_play()

    end_sound_played = False
    running = True
    while running: # start game loop
        if (CURRENT_SCREEN == SCREEN[0]):       # Title Screen
            draw_title_screen()
        elif (CURRENT_SCREEN == SCREEN[1]):     # Help Screen
            draw_help_screen()
        elif (CURRENT_SCREEN == SCREEN[2]):     # Info Screen
            draw_info_screen()
        elif (CURRENT_SCREEN == SCREEN[3]):     # Initial battle Screen
            draw_initial_screen()
        elif (CURRENT_SCREEN == SCREEN[4]):     # Attack Screen
            draw_attack_screen()
        elif (CURRENT_SCREEN == SCREEN[5]):     # Defend Screen
            draw_defend_screen()
        elif (CURRENT_SCREEN == SCREEN[6]):     # Simulation Screen
            draw_simulation_screen()
        elif (CURRENT_SCREEN == SCREEN[7]):     # Result Screen
            draw_result_screen()
            if (PLAYER_HEALTH <= 0):
                if end_sound_played == False:
                    pygame.time.delay(1000)
                    lose_sound = pygame.mixer.Sound("assets/sound/you-lose.mp3")
                    pygame.mixer.Sound.play(lose_sound)
                    end_sound_played = True
            elif (COMPUTER_HEALTH <= 0):
                if end_sound_played == False:
                    pygame.time.delay(1000)
                    win_sound = pygame.mixer.Sound("assets/sound/you-win.mp3")
                    pygame.mixer.Sound.play(win_sound)
                    end_sound_played = True
            
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if 'click' in INFO_BUTTON.handleEvent(event):
                CURRENT_SCREEN = SCREEN[2]
            if 'click' in HELP_BUTTON.handleEvent(event):
                CURRENT_SCREEN = SCREEN[1]
            if 'click' in MAIN_BUTTON.handleEvent(event):
                CURRENT_SCREEN = SCREEN[0]
                
            if 'click' in START_BUTTON.handleEvent(event):
                CURRENT_SCREEN = SCREEN[3]
                pygame.mixer.music.load('assets/music/BoxCat-Games-Battle-Boss.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

            if 'click' in QUIT_BUTTON.handleEvent(event):
                terminate()
            if 'click' in QUIT_I_BUTTON.handleEvent(event):
                terminate()
            if 'click' in QUIT_F_BUTTON.handleEvent(event):
                terminate()
            if 'click' in FIGHT_BUTTON.handleEvent(event):
                if (PLAYER_TURN):
                    CURRENT_SCREEN = SCREEN[4]
                else:
                    CURRENT_SCREEN = SCREEN[5]
            if 'click' in FIRE_BUTTON.handleEvent(event):
                ATTACK = "FIRE"
                fire_sound = pygame.mixer.Sound("assets/sound/fire-attack.mp3")
                pygame.mixer.Sound.play(fire_sound)
            if 'click' in WATER_BUTTON.handleEvent(event):
                ATTACK = "WATER"
                water_sound = pygame.mixer.Sound("assets/sound/water-attack.mp3")
                pygame.mixer.Sound.play(water_sound)                
            if 'click' in LIGHTNING_BUTTON.handleEvent(event):
                ATTACK = "LIGHTNING"
                lightning_sound = pygame.mixer.Sound("assets/sound/lightning-attack.wav")
                pygame.mixer.Sound.play(lightning_sound)  
            if 'click' in FIRE_SHIELD_BUTTON.handleEvent(event):
                DEFEND = "FIRE SHIELD"
            if 'click' in WATER_SHIELD_BUTTON.handleEvent(event):
                DEFEND = "WATER SHIELD"
            if 'click' in LIGHTNING_SHIELD_BUTTON.handleEvent(event):
                DEFEND = "LIGHTNING SHIELD"
            if 'click' in ATTACK_BUTTON.handleEvent(event):
                generate_computer_step()
                CURRENT_SCREEN = SCREEN[6]
            if 'click' in DEFEND_BUTTON.handleEvent(event):
                generate_computer_step()
                CURRENT_SCREEN = SCREEN[6]
            if 'click' in OK_BUTTON.handleEvent(event):
                if (PLAYER_TURN):
                    if not (ATTACK in COMPUTER_DEFEND):
                        COMPUTER_HEALTH = COMPUTER_HEALTH - 25
                else:
                    if not (COMPUTER_ATTACK in DEFEND):
                        PLAYER_HEALTH = PLAYER_HEALTH - 25
                PLAYER_TURN = not PLAYER_TURN
                if (PLAYER_HEALTH <= 0 or COMPUTER_HEALTH <= 0):
                    CURRENT_SCREEN = SCREEN[7]
                else:
                    CURRENT_SCREEN = SCREEN[3]
                        
        pygame.display.update()
        
    terminate()

def generate_computer_step():
    global PLAYER_TURN
    global COMPUTER_ATTACK, COMPUTER_DEFEND
    
    value = randint(0, 2)

    if (value == 0):
        if PLAYER_TURN:
            COMPUTER_DEFEND = "FIRE SHIELD"
        else:
            COMPUTER_ATTACK = "FIRE"
    elif (value == 1):
        if PLAYER_TURN:
            COMPUTER_DEFEND = "LIGHTNING SHIELD"
        else:
            COMPUTER_ATTACK = "LIGHTNING"
    elif (value == 2):
        if PLAYER_TURN:
            COMPUTER_DEFEND = "WATER SHIELD"
        else:
            COMPUTER_ATTACK = "WATER"

def draw_result_screen():
    global DISPLAYSURF
    global PLAYER_HEALTH, COMPUTER_HEALTH

    bg = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg,(0,0))

    y_pos = 40
    y_increment = 20
    
    if (PLAYER_HEALTH <= 0):    
        draw_normal_text('Player kalah', WHITE, 12, WINDOWWIDTH / 2, y_pos)
        y_pos += y_increment
        draw_normal_text('Anda belum menguasai element', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    elif (COMPUTER_HEALTH <= 0):
        draw_normal_text('Player menang', WHITE, 12, WINDOWWIDTH / 2, y_pos)
        y_pos += y_increment
        draw_normal_text('Anda telah menguasai element', WHITE, 12, WINDOWWIDTH / 2, y_pos)
        if (PLAYER_HEALTH == 100):
            y_pos += y_increment
            draw_normal_text('Anda telah menguasai element', WHITE, 12, WINDOWWIDTH / 2, y_pos)
            
    QUIT_BUTTON.draw(DISPLAYSURF)

def draw_simulation_screen():
    global DISPLAYSURF
    global PLAYER_TURN, PLAYER_HEALTH, COMPUTER_HEALTH
    global COMPUTER_ATTACK, COMPUTER_DEFEND, PLAYER_ATTACK, PLAYER_DEFEND

    bg = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg,(0,0))

    if (ATTACK == "FIRE" or COMPUTER_ATTACK == "FIRE"):      
        fire_sound = pygame.mixer.Sound("assets/sound/fire-attack.mp3")
        pygame.mixer.Sound.play(fire_sound)
    elif (ATTACK == "WATER" or COMPUTER_ATTACK == "WATER"):
        water_sound = pygame.mixer.Sound("assets/sound/water-attack.mp3")
        pygame.mixer.Sound.play(water_sound)
    elif (ATTACK == "LIGHTNING" or COMPUTER_ATTACK == "LIGHTNING"):
        lightning_sound = pygame.mixer.Sound("assets/sound/lightning-attack.wav")
        pygame.mixer.Sound.play(lightning_sound)
        
    if PLAYER_TURN:
        draw_normal_text('Player attack with ' + ATTACK, WHITE, 15, 250, 10)
        draw_normal_text('Computer defend with ' + COMPUTER_DEFEND, WHITE, 15, 250, 50)
        if ATTACK in COMPUTER_DEFEND:
            draw_normal_text("Player attack is blocked", WHITE, 15, 250, 90)
            blocked_sound = pygame.mixer.Sound("assets/sound/attack-blocked.mp3")
            pygame.mixer.Sound.play(blocked_sound)
        else:
            draw_normal_text("Player attack is successful", WHITE, 15, 250, 90)
            hit_sound = pygame.mixer.Sound("assets/sound/attack-hit.mp3")
            pygame.mixer.Sound.play(hit_sound)
    else:
        draw_normal_text('Computer attack with ' + COMPUTER_ATTACK, WHITE, 15, 250, 10)
        draw_normal_text('Player defend with ' + DEFEND, WHITE, 15, 250, 50)
        if COMPUTER_ATTACK in DEFEND:
            draw_normal_text("Computer attack is blocked", WHITE, 15, 250, 90)
            blocked_sound = pygame.mixer.Sound("assets/sound/attack-blocked.mp3")
            pygame.mixer.Sound.play(blocked_sound)
        else:
            draw_normal_text("Computer attack is successful", WHITE, 15, 250, 90)
            hit_sound = pygame.mixer.Sound("assets/sound/attack-hit.mp3")
            pygame.mixer.Sound.play(hit_sound)
            
    OK_BUTTON.draw(DISPLAYSURF)
    
def draw_title_screen():
    global DISPLAYSURF
    
    bg_wizard = pygame.image.load("assets/images/wizard.png")
    bg_image = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg_image,(0, 0))
    DISPLAYSURF.blit(bg_wizard,(225, 10))
    draw_big_text("WIZARD FIGHT", LIGHTBLUE, 90, WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    for button in TITLE_BUTTONS:
        button.draw(DISPLAYSURF)

def draw_help_screen():
    global DISPLAYSURF

    bg_image = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg_image,(0, 0))

    fire_image = pygame.image.load("assets/images/fire.png")
    water_image = pygame.image.load("assets/images/water.png")
    lightning_image = pygame.image.load("assets/images/lightning.png")

    DISPLAYSURF.blit(fire_image,(150, 100))
    DISPLAYSURF.blit(water_image,(250, 100))
    DISPLAYSURF.blit(lightning_image,(350, 100))
    
    y_pos = 40
    y_increment = 20
    
    draw_normal_text('Player bermain sebagai seorang wizard', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('yang harus melawan seorang witch', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment 
    draw_normal_text('Cara bermain', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment * 2
    draw_normal_text('Attack dilakukan secara bergantian', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Ada 3 macam attack yang bisa dipilih', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment * 2
    draw_normal_text('FIRE (Api) LIGHTNING (Petir) WATER(Air)', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Jika attack dan defend yang dipilih sama', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Maka attack gagal', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Jika berbeda maka attack berhasil', WHITE, 12, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Giliran attack pertama ditentukan secara random', WHITE, 12, WINDOWWIDTH / 2, y_pos)

    for button in INFO_BUTTONS:
        button.draw(DISPLAYSURF)

def draw_info_screen():
    global DISPLAYSURF

    bg_image = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg_image,(0, 0))
    
    y_pos = 40
    y_increment = 20
    
    draw_normal_text('Game Sederhana Wizard Fight', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Dibuat menggunakan python', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment 
    draw_normal_text('dan pygame library', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment * 2
    draw_normal_text('Untuk tugas mata kuliah Pengantar IoT', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('Dibuat oleh Kelompok 1', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment * 2
    draw_normal_text('1 Alexander Siregar 1002210031', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('2 Aji Sapto 1002210053', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('3 Ahmad Junaedi 1002210016', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('4 Alfando R Rorong 1002210068', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('5 Deri Riduifana 1002210045', WHITE, 18, WINDOWWIDTH / 2, y_pos)
    y_pos += y_increment
    draw_normal_text('6 Desi Triparwanti 1002210018', WHITE, 18, WINDOWWIDTH / 2, y_pos)

    for button in INFO_BUTTONS:
        button.draw(DISPLAYSURF)

def draw_defend_screen():
    global BASICFONT, DISPLAYSURF, DEFEND

    bg = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg,(0,0))

    fire_shield_image = pygame.image.load("assets/images/fire-shield.png")
    water_shield_image = pygame.image.load("assets/images/water-shield.png")
    lightning_shield_image = pygame.image.load("assets/images/lightning-shield.png")

    DISPLAYSURF.blit(fire_shield_image,(300, 125))
    DISPLAYSURF.blit(lightning_shield_image,(300, 225))
    DISPLAYSURF.blit(water_shield_image,(300, 325))
    
    draw_normal_text('Choose your defend', WHITE, 25, 250, 10)
    draw_normal_text('You choose ' + DEFEND, WHITE, 25, 300, 50)
    
    for button in DEFEND_BUTTONS:
        button.draw(DISPLAYSURF)
    
def draw_attack_screen():
    global BASICFONT, DISPLAYSURF, ATTACK

    bg = pygame.image.load("assets/images/background.jpg")
    
    DISPLAYSURF.blit(bg,(0,0))

    fire_image = pygame.image.load("assets/images/fire.png")
    water_image = pygame.image.load("assets/images/water.png")
    lightning_image = pygame.image.load("assets/images/lightning.png")

    DISPLAYSURF.blit(fire_image,(150, 5))
    DISPLAYSURF.blit(lightning_image,(150, 150))
    DISPLAYSURF.blit(water_image,(150, 175))
    
    draw_normal_text('Choose your attack', WHITE, 25, 250, 10)
    draw_normal_text('You choose ' + ATTACK, WHITE, 25, 250, 50)
    
    for button in ATTACK_BUTTONS:
        button.draw(DISPLAYSURF)

def random_first_play():
    global PLAYER_TURN
    
    value = randint(0, 1)

    if (value == 0):
        PLAYER_TURN = True
    else:
        PLAYER_TURN = False
        
    return value

def draw_attack_turn():
    global PLAYER_TURN

    if PLAYER_TURN:
        draw_normal_text('Attack is Player', WHITE, 15, 350, 200)
        draw_normal_text('Defend is Computer', WHITE, 15, 350, 225)
    else:
        draw_normal_text('Attack is Computer', WHITE, 15, 350, 200)
        draw_normal_text('Defend is Player', WHITE, 15, 350, 225)        

def draw_initial_screen():
    global BASICFONT, DISPLAYSURF

    bg = pygame.image.load("assets/images/background.jpg")
    DISPLAYSURF.blit(bg,(0,0))
    player_image = pygame.image.load("assets/images/player.png")
    computer_image = pygame.image.load("assets/images/computer.png")
    
    DISPLAYSURF.blit(player_image,(30,75))
    DISPLAYSURF.blit(computer_image,(420,75))
    draw_player_health()
    draw_computer_health()
    draw_attack_turn()

    for button in INITIAL_BUTTONS:
        button.draw(DISPLAYSURF)
    
def draw_player_health():
    global DISPLAYSURF
    global PLAYER_HEALTH

    draw_normal_text('Player ' + str(PLAYER_HEALTH), WHITE, 10, 50, 10)
    pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(30, 30, PLAYER_HEALTH * 2, 20))

def draw_computer_health():
    global DISPLAYSURF
    global COMPUTER_HEALTH

    draw_normal_text('Computer ' + str(COMPUTER_HEALTH), WHITE, 10, 580, 10)
    pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(410, 30, COMPUTER_HEALTH * 2, 20))

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            #continue
        #return event.key
            if event.key == pygame.K_i:
                show_about = True
                #DISPLAYSURF.fill(BLACK)
                bg = pygame.image.load("assets/images/background.jpg")
                bg = pygame.transform.scale(bg, (640, 480))
                DISPLAYSURF.blit(bg,(0,0))    

                y_pos = 40
                y_increment = 20
                draw_normal_text('Game Sederhana Wizard Fight', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('Dibuat menggunakan python', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment 
                draw_normal_text('dan pygame library', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment * 2
                draw_normal_text('Untuk tugas mata kuliah Pengantar IoT', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('Dibuat oleh Kelompok 1', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment * 2
                draw_normal_text('1 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('2 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('3 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('4 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('5 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                y_pos += y_increment
                draw_normal_text('6 ', WHITE, 18, WINDOWWIDTH / 2, y_pos)
                                
                pygame.display.update()
                while show_about:
                    checkForQuit()
                    for event in pygame.event.get([KEYDOWN, KEYUP, QUIT]):
                        if event.type == KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                show_about = False
                        if event.type == QUIT:
                            terminate()
                        
                                
            if event.key == pygame.K_h:
                print("Key h has been pressed")
                            
            if event.key == pygame.K_RETURN:
                return event.key
    return None

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, LIGHTBLUE)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Press ENTER to play, H for Help, I for Info', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def draw_normal_text(text, color, size, x, y ):
        global BASICFONT, DISPLAYSURF
        
        BASICFONT = pygame.font.Font('fonts/8-bit-wonder.ttf', size)
        text_surface = BASICFONT.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        DISPLAYSURF.blit(text_surface,text_rect)

def draw_big_text(text, color, size, x, y ):
        global BIGFONT, DISPLAYSURF
        
        BIGFONT = pygame.font.Font('fonts/space-mission.otf', size)
        text_surface = BIGFONT.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        DISPLAYSURF.blit(text_surface,text_rect)

if __name__ == '__main__':
    main()
