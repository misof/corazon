import math, random, sys, time
from easygame import *
from constants import *
from helper_functions import *
from interns import Intern
from vans import Van
from airplanes import Airplane
from player import Player

pic_init_screen = load_image('resources/init_screen.png')
pic_init_screen_nocont = load_image('resources/init_screen_nocont.png')
pic_instr_screen = load_image('resources/instructions.png')
pic_background = load_image('resources/background.png')
pic_sklad = load_image('resources/sklad.png')
pic_riksarempty = load_image('resources/riksarempty.png')
pic_riksarorange = load_image('resources/riksarorange.png')
pic_dom = load_image('resources/dom.png')
pic_van = load_image('resources/van.png')
pic_veziak = load_image('resources/veziak.png')
pic_lietadlo = load_image('resources/lietadlo.png')
pic_mesto = load_image('resources/mesto.png')

def formatuj_cislo(cislo):
    sufixy = [ '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ]
    exponent = 0
    while exponent+1 < len(sufixy) and cislo % 1000 == 0:
        cislo //= 1000
        exponent += 1
    return str(cislo) + sufixy[exponent]

class GameState:
    def __init__(self):
        self.stage = 0
        self.money = 244990
        self.item_counts = [ 0 for _ in range(len(STAGES)) ]

        self.current_status_message = 'Vitaj!'
        self.player = Player()

        self.last_disinfection = 25 + time.time()
        self.seen_disinfection_button = False

        self.interns = []
        self.vans = []
        self.airplanes = []

    def get_all_workers(self):
        return self.interns + self.vans + self.airplanes

    def is_player_active(self):
        return len(self.get_all_workers()) == 0

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
                            return MENU_NEW_GAME
                        if 343 <= y <= 430:
                            pass
                        if 463 <= y <= 549:
                            return MENU_INSTRUCTIONS

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

def draw_button(label, offx, offy, enabled):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    if not enabled: txcolor = (0.7, 0.7, 0.7, 1)
    draw_polygon( (offx,offy), (offx+24,offy), (offx+24,offy-24), (offx,offy-24), color = txcolor )
    draw_polygon( (offx+1,offy+1), (offx+23,offy+1), (offx+23,offy-23), (offx+1,offy-23), color = bgcolor )
    draw_text(label, 'Arial', 16, position=(offx+6, offy-20), color=txcolor )

def draw_current_screen(state):
    draw_image(pic_background, position=(0, 0), anchor=(0, 0))
    draw_image(pic_sklad, position=WAREHOUSE_POS)

    if state.is_player_active():
        # draw player
        for house in state.player.pending_houses:
            draw_image(pic_dom, position=house)
        if state.player.has_cargo:
            draw_image(pic_riksarorange, position=state.player.position)
        else:
            draw_image(pic_riksarempty, position=state.player.position)
    else:
        # draw interns' and vans' houses
        intern_opacity = van_opacity = airplane_opacity = 1
        if state.vans != []: intern_opacity = 0.2
        if state.airplanes != []: van_opacity = intern_opacity = 0.1

        for worker in state.interns:
            for house in worker.pending_houses:
                draw_image( pic_dom, position=house, opacity=intern_opacity )
        for worker in state.vans:
            for house in worker.pending_houses:
                draw_image( pic_veziak, position=house, opacity=van_opacity )
        for worker in state.airplanes:
            for house in worker.pending_houses:
                draw_image( pic_mesto, position=house, opacity=airplane_opacity )

        # draw interns and vans
        for worker in state.interns:
            if worker.has_cargo:
                draw_image(pic_riksarorange, position=worker.position, opacity=intern_opacity)
            else:
                draw_image(pic_riksarempty, position=worker.position, opacity=intern_opacity)
        for worker in state.vans:
            draw_image(pic_van, position=worker.position, opacity=van_opacity)
        for worker in state.airplanes:
            draw_image(pic_lietadlo, position=worker.position, opacity=airplane_opacity)

    status_message(state.current_status_message)
    current_time = time.time()
    # draw_polygon( (200, 25), (SCREENX-1, 25), (SCREENX-1, SCREENY-35), (200, SCREENY-35), color=(0,0,0,0.2) )
    if current_time > state.last_disinfection + DISINF_APPEAR:
        add_disinfection_button(current_time > state.last_disinfection + DISINF_URGENT)
    add_money_textbox(state)

    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    menu = stages_in_menu(state)
    for sid in range(len(menu)):
        offy = SCREENY - 10 - 60*sid
        s = menu[sid]
        draw_polygon( (10,offy), (189,offy), (189,offy-24), (10,offy-24), color=bgcolor )
        draw_text( STAGES[s].name + ' (€' + formatuj_cislo(STAGES[s].cost) + ')', 'Arial', 12, position=(14,offy-17), color=txcolor )
        draw_button( '–', 10, offy-26, state.item_counts[s] > STAGES[s].lower_bound and STAGES[s].can_sell )
        draw_button( '+', 165, offy-26, state.item_counts[s] < STAGES[s].upper_bound and state.money >= STAGES[s].cost )
        draw_polygon( (36,offy-26), (163,offy-26), (163,offy-50), (36,offy-50), color=bgcolor )
        draw_text( str(state.item_counts[s]), 'Arial', 12, position=(40,offy-44), color=txcolor )

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
    # dezinfekcia ruk
    if current_time > state.last_disinfection + DISINF_APPEAR:
        if SCREENX-180 <= event.x <= SCREENX-10 and SCREENY-34 <= event.y <= SCREENY-10:
            state.last_disinfection = current_time
            state.seen_disinfection_button = True
            state.current_status_message = ''
            return

    # zaciatok pohybu
    if 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.player.moving = True
        state.player.moving_start_pos = state.player.position
        state.player.moving_start_time = current_time
        state.player.moving_target = (event.x, event.y)
        return
    
    menu = stages_in_menu(state)
    for sid in range(len(menu)):
        offy = SCREENY - 36 - 60*sid
        s = menu[sid]
        if 10 <= event.x <= 34 and offy-24 <= event.y <= offy:
            if state.item_counts[s] > STAGES[s].lower_bound and STAGES[s].can_sell:
                state.item_counts[s] -= 1
                state.money += STAGES[s].cost // 2
                if s == STAGE_INTERN:
                    state.interns.pop()
                if s == STAGE_VAN:
                    state.vans.pop()
                if s == STAGE_AIRDROP:
                    state.airplanes.pop()
        if 165 <= event.x <= 189 and offy-24 <= event.y <= offy:
            if state.item_counts[s] < STAGES[s].upper_bound and state.money >= STAGES[s].cost:
                state.item_counts[s] += 1
                state.money -= STAGES[s].cost
                if s == STAGE_INTERN:
                    state.interns.append( Intern() )
                    if len(state.interns) == 1:
                        state.interns[0].position = state.player.position
                        state.interns[0].pending_houses = state.player.pending_houses
                        state.interns[0].has_cargo = state.player.has_cargo
                        state.interns[0].time_of_next_house = state.player.time_of_next_house
                        state.interns[0].start_automove()
                if s == STAGE_VAN:
                    state.vans.append( Van() )
                if s == STAGE_AIRDROP:
                    state.airplanes.append( Airplane() )

def handle_drag(state, event, current_time):
    if state.player.moving and 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.player.moving_start_pos = state.player.position
        state.player.moving_start_time = current_time
        state.player.moving_target = (event.x, event.y)

def play():
    state = GameState()
    while True:
        next_frame()
        current_time = time.time()

        # level up
        for idx, stage in enumerate(STAGES):
            if state.money >= stage.reveal_at and state.stage < idx:
                state.stage = idx
                if STAGES[idx].message is not None:
                    state.current_status_message = STAGES[idx].message

        # potreba dezinfekcie
        if current_time > state.last_disinfection + DISINF_APPEAR and not state.seen_disinfection_button:
            state.current_status_message = 'Kliknutím na button vpravo hore si dezinfikuj ruky.'
        if current_time > state.last_disinfection + DISINF_URGENT and not state.seen_disinfection_button:
            state.current_status_message = 'Kliknutím na button vpravo hore si dezinfikuj ruky. Rýchlo!'
        if current_time > state.last_disinfection + DISINF_DEAD:
            game_over(state, 'nakazil(a) si sa')
            return

        # automaticky pohyb internov a vanov
        for worker in state.get_all_workers():
            worker.process_all_events(state, current_time)
            worker.move(state)
            
        # pohyb rikse
        if state.is_player_active():
            state.player.process_all_events(state, current_time)
            state.player.move(state)
            
        # vykreslenie obrazovky
        draw_current_screen(state)
        
        # handlovanie eventov
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) == MouseDownEvent:
                if event.button == 'LEFT':
                    handle_left_click(state, event, current_time)
            if type(event) == MouseDragEvent:
                handle_drag(state, event, current_time)
            if type(event) == MouseUpEvent:
                state.player.moving = False

if __name__ == '__main__':
    open_window('Corazón', SCREENX, SCREENY)
    while True:
        menu_choice = main_menu()
        if menu_choice == MENU_NEW_GAME:
            play()
        if menu_choice == MENU_INSTRUCTIONS:
            instructions()


