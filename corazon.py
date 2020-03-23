import hashlib
import math
import pickle
import random
import sys
import time

from src.easygame import *

from src.constants import *
from src.helper_functions import *
from src.resources import *
from src.screens import *

from src.click import handle_left_click, handle_drag
from src.draw import draw_current_screen

from src.state import State
from src.player import Player

from src.interns import Intern
from src.vans import Van
from src.airplanes import Airplane
from src.teleports import Teleport
from src.replicators import Replicator

def handle_left_click(state, event, current_time):
    # dezinfekcia ruk
    if current_time > state.last_disinfection + DISINF_APPEAR:
        if SCREENX-180 <= event.x <= SCREENX-10 and SCREENY-34 <= event.y <= SCREENY-10:
            state.last_disinfection = current_time
            state.seen_disinfection_button = True
            return

    # zaciatok pohybu
    if 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.player.moving = True
        state.player.moving_start_pos = state.player.position
        state.player.moving_start_time = current_time
        state.player.moving_target = (event.x, event.y)
        return

    # save game
    if state.item_counts[STAGE_CLONE] == 1 and state.money >= 10**7:
        if 10 <= event.x <= 179 and 36 <= event.y <= 60:
            state.money -= 10**7
            state.saved_clone = None
            state.player.cargo_type = None
            for worker in state.interns: worker.cargo_type = None
            tmp = pickle.dumps(state)
            state.saved_clone = tmp
    
    menu = stages_in_menu(state)
    for sid in range(len(menu)):
        offy = SCREENY - 36 - 60*sid
        s = menu[sid]
        if 10 <= event.x <= 34 and offy-24 <= event.y <= offy:
            if state.item_counts[s] > STAGES[s].lower_bound and STAGES[s].can_sell:
                state.item_counts[s] -= 1
                state.money += STAGES[s].cost // 2
                if state.money >= STAGES[STAGE_STERILE].cost: state.already_had_enough = True
                if s == STAGE_INTERN:
                    if len(state.interns) == 1:
                        state.player.position = state.interns[0].position
                        state.player.pending_houses = state.interns[0].pending_houses
                        state.player.has_cargo = state.interns[0].has_cargo
                        state.player.cargo_type = state.interns[0].cargo_type
                        state.player.time_of_next_house = state.interns[0].time_of_next_house
                    state.interns.pop()
                if s == STAGE_VAN:
                    state.vans.pop()
                if s == STAGE_AIRDROP:
                    state.airplanes.pop()
                if s == STAGE_TELEPORT:
                    state.teleports.pop()
                if s == STAGE_REPLICATOR:
                    state.replicators.pop()
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
                        state.interns[0].cargo_type = state.player.cargo_type
                        state.interns[0].time_of_next_house = state.player.time_of_next_house
                        state.interns[0].start_automove()
                if s == STAGE_VAN:
                    state.vans.append( Van() )
                if s == STAGE_AIRDROP:
                    state.airplanes.append( Airplane() )
                if s == STAGE_TELEPORT:
                    state.teleports.append( Teleport() )
                if s == STAGE_REPLICATOR:
                    state.replicators.append( Replicator() )

def handle_drag(state, event, current_time):
    if state.player.moving and 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.player.moving_start_pos = state.player.position
        state.player.moving_start_time = current_time
        state.player.moving_target = (event.x, event.y)

def play():
    state = State()
    while True:
        next_frame()
        current_time = time.time()

        # win
        if state.item_counts[STAGE_STERILE] > 0:
            win(state)
            return

        # fake win
        if not state.saw_fake_easter_egg and state.money >= 47 and sum(state.item_counts) == 0:
            win_fake(state)
            state.saw_fake_easter_egg = True

        # level up
        for idx, stage in enumerate(STAGES):
            if state.money >= stage.reveal_at and state.stage < idx:
                state.stage = idx

        # potreba dezinfekcie a mozna smrt
        if current_time > state.last_disinfection + DISINF_DEAD:
            loss(state)
            if state.saved_clone is None:
                return
            else:
                saved_state = pickle.loads(state.saved_clone)
                state = saved_state
                current_time = time.time()
                state.last_disinfection = current_time

        # automaticky pohyb internov a vanov
        for worker in state.get_all_workers():
            worker.process_all_events(state, current_time)
            worker.move(state)
            
        # pohyb rikse
        if state.is_player_active():
            state.player.process_all_events(state, current_time)
            state.player.move(state)

        # update status_message
        state.update_status_message()
            
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
        if menu_choice == MENU_NEW_GAME: play()
        if menu_choice == MENU_INSTRUCTIONS: instructions()

