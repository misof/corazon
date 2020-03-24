import pickle
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

def play():
    state = State()
    while True:
        next_frame()
        current_time = time.time()

        # win
        if state.item_counts[STAGE_STERILE] > 0:
            state.pause()
            win(state)
            report(state)
            return

        # fake win
        if not state.saw_fake_easter_egg and state.money >= 21 and sum(state.item_counts) == 0:
            state.pause()
            win_fake(state)
            state.unpause()
            state.saw_fake_easter_egg = True

        # level up
        for idx, stage in enumerate(STAGES):
            if state.money >= stage.reveal_at and state.stage < idx:
                state.stage = idx

        # potreba dezinfekcie a mozna smrt
        if current_time > state.last_disinfection + DISINF_DEAD:
            state.pause()
            loss(state)
            if state.saved_clone is None:
                report(state)
                return
            else:
                saved_state = pickle.loads(state.saved_clone)
                
                current_time = time.time()
                
                saved_state.game_start_timestamp = current_time
                saved_state.game_duration = state.game_duration
                saved_state.paused = True
                saved_state.pause_timestamp = state.pause_timestamp
                saved_state.disinfections = state.disinfections
                saved_state.clonings += 1

                state = saved_state
                state.last_disinfection = current_time
                state.unpause()

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
            if type(event) is KeyDownEvent:
                if event.key != 'ESCAPE':
                    state.pause()
                    pause_screen(state)
                    state.unpause()

if __name__ == '__main__':
    open_window('Corazón', SCREENX, SCREENY)
    while True:
        menu_choice = main_menu()
        if menu_choice == MENU_NEW_GAME: play()
        if menu_choice == MENU_INSTRUCTIONS: instructions()

