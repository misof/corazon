from src.easygame import *

from src.constants import *
from src.helper_functions import *
from src.resources import *

def instructions():
    while True:
        next_frame()
        draw_image(pic_instructions, position=(0, 0), anchor=(0, 0))
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is MouseDownEvent:
                return
            if type(event) is KeyDownEvent:
                return

def main_menu():
    while True:
        next_frame()
        draw_image(pic_init_screen, position=(0, 0), anchor=(0, 0))
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is MouseDownEvent:
                if event.button == 'LEFT':
                    if 204 <= event.x <= 598:
                        y = 599 - event.y
                        if 343 <= y <= 430:
                            return MENU_NEW_GAME
                        if 463 <= y <= 549:
                            return MENU_INSTRUCTIONS

def loss(state):
    while True:
        next_frame()
        if state.saved_clone is None:
            draw_image(pic_loss, position=(0, 0), anchor=(0, 0) )
        else:
            draw_image(pic_loss_clone, position=(0, 0), anchor=(0, 0) )
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is KeyDownEvent:
                return

def win(state):
    while True:
        next_frame()
        draw_image(pic_win, position=(0, 0), anchor=(0, 0) )
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is KeyDownEvent:
                win_pro(state)
                return

def win_fake(state):
    while True:
        next_frame()
        draw_image(pic_win_fake, position=(0, 0), anchor=(0, 0) )
        for event in poll_events():
            if type(event) is CloseEvent:
                terminate()
            if type(event) is KeyDownEvent:
                return

def win_pro(state):
    if state.should_win_pro:
        verification_string = '_'.join( str(state.item_counts[s]) for s in FINGERPRINT)
        verification_string = hashlib.sha256(verification_string.encode()).hexdigest()
        while True:
            next_frame()
            draw_image(pic_win_pro, position=(0, 0), anchor=(0, 0) )
            draw_text('verifikačný reťazec:', 'Arial', 16, position=(10,30), color=(0,0,0,1) )
            draw_text(verification_string, 'Arial', 12, position=(10,10), color=(0,0,0,1) )
            for event in poll_events():
                if type(event) is CloseEvent:
                    terminate()
                if type(event) is KeyDownEvent:
                    return


