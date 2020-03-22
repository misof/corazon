import hashlib, math, pickle, random, sys, time
from easygame import *
from constants import *
from helper_functions import *
from resources import *
from state import State
from interns import Intern
from vans import Van
from airplanes import Airplane
from teleports import Teleport
from replicators import Replicator
from player import Player

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

def status_message(msg):
    draw_polygon( (0, 0), (SCREENX-1, 0), (SCREENX-1,24), (0,24), color=(0.9, 0.9, 0.9, 1) )
    draw_text(msg, 'Arial', 16, position=(20, 4), color=(0, 0, 0, 1) )

def add_money_textbox(state):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    draw_polygon( (200, SCREENY-34), (SCREENX-200, SCREENY-34), (SCREENX-200,SCREENY-10), (200,SCREENY-10), color=bgcolor )
    peniaze_message = 'Peniaze: €{}'.format(state.money)
    if state.money >= 10**6: peniaze_message += ' (€{})'.format(formatuj_cislo(state.money, force=True))
    draw_text(peniaze_message, 'Arial', 16, position=(204, SCREENY-30), color=txcolor )

def add_disinfection_button(urgent=False):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    if urgent:
        bgcolor = (0.9, 0.8, 0.8, 1)
        txcolor = (1, 0.1, 0.1, 1)

    draw_polygon( (SCREENX-180, SCREENY-34), (SCREENX-10, SCREENY-34), (SCREENX-10,SCREENY-10), (SCREENX-180,SCREENY-10), color=(0,0,0,1) )
    draw_polygon( (SCREENX-179, SCREENY-33), (SCREENX-11, SCREENY-33), (SCREENX-11,SCREENY-11), (SCREENX-179,SCREENY-11), color=bgcolor )
    draw_text('Dezinfikuj si ruky', 'Arial', 16, position=(SCREENX-176, SCREENY-30), color=txcolor )

def draw_button(label, offx, offy, enabled, width=24, font_size=16):
    bgcolor = (0.9, 0.9, 0.9, 1)
    txcolor = (0, 0, 0, 1)
    if not enabled: txcolor = (0.7, 0.7, 0.7, 1)
    draw_polygon( (offx,offy), (offx+width,offy), (offx+width,offy-24), (offx,offy-24), color = txcolor )
    draw_polygon( (offx+1,offy+1), (offx+width-1,offy+1), (offx+width-1,offy-23), (offx+1,offy-23), color = bgcolor )
    draw_text(label, 'Arial', font_size, position=(offx+6, offy-20), color=txcolor )

def draw_current_screen(state):
    draw_image(pic_background, position=(0, 0), anchor=(0, 0), scale_x=1.01, scale_y=1.01)
    draw_image(pic_sklad, position=WAREHOUSE_POS)

    if state.is_player_active():
        # draw player
        for house in state.player.pending_houses:
            draw_image(pic_dom, position=house)
        draw_image(state.player.get_picture(), position=state.player.position, scale_x=-1 if state.player.last_movement_was_left else 1)
    else:
        # draw workers' houses
        intern_opacity = van_opacity = airplane_opacity = teleport_opacity = replicator_opacity = 1
        if state.vans != []:
            intern_opacity = 0.2
        if state.airplanes != []:
            van_opacity = 0.07
            intern_opacity = 0.15
        if state.teleports != []:
            van_opacity = 0.07
            intern_opacity = 0.15
            airplane_opacity = 0.15
        if state.replicators != []:
            van_opacity = 0.07
            intern_opacity = 0.15
            airplane_opacity = 0.15
            teleport_opacity = 0.5

        for worker in state.interns:
            for house in worker.pending_houses:
                draw_image( pic_dom, position=house, opacity=intern_opacity )
        for worker in state.vans:
            for house in worker.pending_houses:
                draw_image( pic_veziak, position=house, opacity=van_opacity )
        for worker in state.airplanes:
            for house in worker.pending_houses:
                draw_image( pic_mesto, position=house, opacity=airplane_opacity )
        for worker in state.teleports:
            for house in worker.pending_houses:
                draw_image( pic_mesto, position=house, opacity=1 if teleport_opacity==1 else 0.15 )
        for worker in state.replicators:
            for house in worker.pending_houses:
                draw_image( pic_mesto, position=house, opacity=replicator_opacity )

        # draw interns, vans, airplanes
        for worker in state.interns:
            draw_image(worker.get_picture(), position=worker.position, opacity=intern_opacity, scale_x=-1 if worker.last_movement_was_left else 1)
        for worker in state.vans:
            draw_image(worker.get_picture(), position=worker.position, opacity=van_opacity, scale_x=-1 if worker.last_movement_was_left else 1)
        for worker in state.airplanes:
            draw_image(worker.get_picture(), position=worker.position, opacity=airplane_opacity, scale_x=-1 if worker.last_movement_was_left else 1)

        # draw teleports
        for worker in state.teleports:
            if worker.has_cargo:
                draw_circle( WAREHOUSE_POS, radius=32, color=(1, 1, 0.5, 0.9*teleport_opacity) )
                draw_circle( worker.pending_houses[-1], radius=32, color=(1, 1, 0.5, 0.9*teleport_opacity) )
                draw_line( WAREHOUSE_POS, worker.pending_houses[-1], thickness=47, color=(1, 1, 0.5, 0.7*teleport_opacity) )

        # draw replicators
        for worker in state.replicators:
            if worker.has_cargo:
                dfull = math.sqrt( square_distance( WAREHOUSE_POS, worker.pending_houses[-1] ) )
                dpart = math.sqrt( square_distance( worker.position, worker.pending_houses[-1] ) )
                radius = int( 0.5 + 60 * dpart / dfull )
                draw_circle( worker.pending_houses[-1], radius=radius, color=(1, 0.3, 1, 0.7*replicator_opacity) )

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

    if state.item_counts[STAGE_CLONE] == 1:
        if state.saved_clone is None:
            draw_button('naklonuj sa (€10M)', 10, 60, state.money >= 10**7, 179, 12)
        else:
            draw_button('prepíš klon (€10M)', 10, 60, state.money >= 10**7, 179, 12)

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

def game_over(state):
    while True:
        next_frame()
        state.current_status_message = ''
        draw_current_screen(state)
        if state.saved_clone is None:
            draw_image(pic_loss, position=(0, 0), anchor=(0, 0) )
        else:
            draw_image(pic_loss_clone, position=(0, 0), anchor=(0, 0) )
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
            game_over(state)
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
        if menu_choice == MENU_NEW_GAME:
            play()
        if menu_choice == MENU_INSTRUCTIONS:
            instructions()


