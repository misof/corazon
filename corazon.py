import math
import sys
import time
from easygame import *
from enum import Enum

SCREEN = (800, 600)
SCREENX, SCREENY = SCREEN

DISINF_APPEAR, DISINF_URGENT, DISINF_DEAD = 5, 8, 10

pic_init_screen = load_image('resources/init_screen.png')
pic_init_screen_nocont = load_image('resources/init_screen_nocont.png')
pic_instr_screen = load_image('resources/instructions.png')
pic_background = load_image('resources/background.png')
pic_sklad = load_image('resources/sklad.png')
pic_riksarempty = load_image('resources/riksarempty.png')
pic_riksarorange = load_image('resources/riksarorange.png')
pic_dom = load_image('resources/dom.png')

class MenuResult(Enum):
    new_game = 1
    cont_game = 2
    instructions = 3

class GameState:
    def __init__(self):
        self.stage = 0
        self.money = 0

        self.sklad_pos = (SCREENX//2, SCREENY//2)
        self.riksa_pos = (3*SCREENX//4, 2*SCREENY//3)
        self.current_status_message = 'Vitaj!'

        self.last_disinfection = time.time()
        self.seen_disinfection_button = False

        self.moving = False
        self.moving_start_pos = None
        self.moving_start_time = None
        self.moving_target = None
        self.riksa_speed = 70 # pixels/s

        self.house


def terminate():
    close_window()
    sys.exit()

def main_menu():
    while True:
        next_frame()
        draw_image(pic_init_screen_nocont, position=(0, 0), anchor=(0, 0))
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is MouseDownEvent:
                if event.button == 'LEFT':
                    if 204 <= event.x <= 598:
                        y = 599 - event.y
                        if 222 <= y <= 308:
                            return MenuResult.new_game
                        if 343 <= y <= 430:
                            pass
                        if 463 <= y <= 549:
                            return MenuResult.instructions

def instructions():
    while True:
        next_frame()
        draw_image(pic_instr_screen, position=(0, 0), anchor=(0, 0))
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is MouseDownEvent:
                return
            if type(event) is KeyDownEvent:
                return

def status_message(msg):
    draw_polygon( (0, 0), (SCREENX-1, 0), (SCREENX-1,24), (0,24), color=(0.9, 0.9, 0.9, 1) )
    draw_text(msg, 'Arial', 16, position=(20, 4), color=(0, 0, 0, 1) )

def add_money_textbox(state):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    draw_polygon( (200, SCREENY-34), (SCREENX-200, SCREENY-34), (SCREENX-200,SCREENY-10), (200,SCREENY-10), color=bgcolor )
    draw_text('Peniaze: €{}'.format(state.money), 'Arial', 16, position=(204, SCREENY-30), color=txcolor )

def add_disinfection_button(urgent=False):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    if urgent:
        bgcolor = (0.9, 0.8, 0.8, 1)
        txcolor = (1, 0.1, 0.1, 1)

    draw_polygon( (SCREENX-180, SCREENY-34), (SCREENX-10, SCREENY-34), (SCREENX-10,SCREENY-10), (SCREENX-180,SCREENY-10), color=(0,0,0,1) )
    draw_polygon( (SCREENX-179, SCREENY-33), (SCREENX-11, SCREENY-33), (SCREENX-11,SCREENY-11), (SCREENX-179,SCREENY-11), color=bgcolor )
    draw_text('Dezinfikuj si ruky', 'Arial', 16, position=(SCREENX-176, SCREENY-30), color=txcolor )

def draw_current_screen(state):
    draw_image(pic_background, position=(0, 0), anchor=(0, 0))
    draw_image(pic_sklad, position=state.sklad_pos)
    draw_image(pic_riksarempty, position=state.riksa_pos)
    status_message(state.current_status_message)
    current_time = time.time()
    # draw_polygon( (200, 25), (SCREENX-1, 25), (SCREENX-1, SCREENY-35), (200, SCREENY-35), color=(0,0,0,0.2) )
    if current_time > state.last_disinfection + DISINF_APPEAR:
        add_disinfection_button(current_time > state.last_disinfection + DISINF_URGENT)
    add_money_textbox(state)

def game_over(state, reason):
    while True:
        next_frame()
        draw_current_screen(state)
        draw_text('YOU LOSE', 'Arial', 100, position=(50, SCREENY//2), color=(1,0,0,1))
        draw_text(reason, 'Arial', 60, position=(50, SCREENY//2 - 90), color=(1,0,0,1))
        draw_text('press any key', 'Arial', 20, position=(50, 40), color=(1,0,0,1))
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is KeyDownEvent:
                return

def handle_left_click(state, event, current_time):
    if current_time > state.last_disinfection + DISINF_APPEAR:
        if SCREENX-180 <= event.x <= SCREENX-10 and SCREENY-34 <= event.y <= SCREENY-10:
            state.last_disinfection = current_time
            state.seen_disinfection_button = True
            state.current_status_message = ''
            return
    if 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.moving = True
        state.moving_start_pos = state.riksa_pos
        state.moving_start_time = current_time
        state.moving_target = (event.x, event.y)

def play():
    state = GameState()
    while True:
        next_frame()
        current_time = time.time()

        # potreba dezinfekcie
        if current_time > state.last_disinfection + DISINF_APPEAR and not state.seen_disinfection_button:
            state.current_status_message = 'Kliknutím na button vpravo hore si dezinfikuj ruky.'
        if current_time > state.last_disinfection + DISINF_URGENT and not state.seen_disinfection_button:
            state.current_status_message = 'Kliknutím na button vpravo hore si dezinfikuj ruky. Rýchlo!'
        if current_time > state.last_disinfection + DISINF_DEAD:
            game_over(state, 'nakazil(a) si sa')
            return

        # pohyb rikse
        if state.moving:
            time_elapsed = current_time - state.moving_start_time
            dx = state.moving_target[0] - state.moving_start_pos[0]
            dy = state.moving_target[1] - state.moving_start_pos[1]
            if dx != 0 or dy != 0:
                d = math.sqrt( dx*dx + dy*dy )
                time_needed = d / state.riksa_speed
                if time_needed <= time_elapsed:
                    state.riksa_pos = state.moving_target
                else:
                    dx /= d
                    dy /= d
                    x = state.moving_start_pos[0] + dx * state.riksa_speed * time_elapsed
                    y = state.moving_start_pos[1] + dy * state.riksa_speed * time_elapsed
                    state.riksa_pos = ( int(x+.5), int(y+.5) )

        draw_current_screen(state)
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) == MouseDownEvent:
                if event.button == 'LEFT':
                    handle_left_click(state, event, current_time)
            if type(event) == MouseUpEvent:
                state.moving = False

if __name__ == '__main__':
    open_window('Corazón', SCREENX, SCREENY)
    while True:
        menu_choice = main_menu()
        if menu_choice == MenuResult.new_game:
            play()
        if menu_choice == MenuResult.instructions:
            instructions()


