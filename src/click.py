import pickle

from src.constants import *
from src.helper_functions import *

from src.interns import Intern
from src.vans import Van
from src.airplanes import Airplane
from src.teleports import Teleport
from src.replicators import Replicator

def handler_disinfection_button(state, event, current_time):
    if current_time > state.last_disinfection + DISINF_APPEAR:
        state.last_disinfection = current_time
        state.seen_disinfection_button = True
        return True
    return False

def handler_movement_start(state, event, current_time):
    state.player.moving = True
    state.player.moving_start_pos = state.player.position
    state.player.moving_start_time = current_time
    state.player.moving_target = (event.x, event.y)
    return True

def handler_clone(state, event, current_time):
    if state.item_counts[STAGE_CLONE] == 1 and state.money >= 10**7:
        state.money -= 10**7
        state.saved_clone = None
        state.player.cargo_type = None
        for worker in state.interns: worker.cargo_type = None
        tmp = pickle.dumps(state)
        state.saved_clone = tmp
        return True
    return False

def handler_sell(state, event, current_time, stage_id):
    if state.item_counts[stage_id] <= STAGES[stage_id].lower_bound:
        return False
    if not STAGES[stage_id].can_sell:
        return False

    state.item_counts[stage_id] -= 1
    state.money += STAGES[stage_id].cost // 2
    if state.money >= STAGES[STAGE_STERILE].cost:
        state.already_had_enough = True

    if stage_id == STAGE_INTERN:
        if len(state.interns) == 1:
            state.player.position = state.interns[0].position
            state.player.pending_houses = state.interns[0].pending_houses
            state.player.has_cargo = state.interns[0].has_cargo
            state.player.cargo_type = state.interns[0].cargo_type
            state.player.time_of_next_house = state.interns[0].time_of_next_house
        state.interns.pop()

    if stage_id == STAGE_VAN: state.vans.pop()
    if stage_id == STAGE_AIRDROP: state.airplanes.pop()
    if stage_id == STAGE_TELEPORT: state.teleports.pop()
    if stage_id == STAGE_REPLICATOR: state.replicators.pop()
    return True

def handler_buy(state, event, current_time, stage_id):
    if state.item_counts[stage_id] >= STAGES[stage_id].upper_bound:
        return False
    if state.money < STAGES[stage_id].cost:
        return False

    state.item_counts[stage_id] += 1
    state.money -= STAGES[stage_id].cost

    if stage_id == STAGE_INTERN:
        state.interns.append( Intern() )
        if len(state.interns) == 1:
            state.interns[0].position = state.player.position
            state.interns[0].pending_houses = state.player.pending_houses
            state.interns[0].has_cargo = state.player.has_cargo
            state.interns[0].cargo_type = state.player.cargo_type
            state.interns[0].time_of_next_house = state.player.time_of_next_house
            state.interns[0].start_automove()

    if stage_id == STAGE_VAN: state.vans.append( Van() )
    if stage_id == STAGE_AIRDROP: state.airplanes.append( Airplane() )
    if stage_id == STAGE_TELEPORT: state.teleports.append( Teleport() )
    if stage_id == STAGE_REPLICATOR: state.replicators.append( Replicator() )
    return True

def handle_left_click(state, event, current_time):
    click_handlers = []
    click_handlers.append( (SCREENX-180, SCREENX-10, SCREENY-34, SCREENY-10, handler_disinfection_button) )
    click_handlers.append( (200, SCREENX-1, 25, SCREENY-35, handler_movement_start) )
    click_handlers.append( (10, 179, 36, 60, handler_clone) )

    menu = stages_in_menu(state)
    for sid in range(len(menu)):
        offset_y = SCREENY - 36 - 60*sid
        stage_id = menu[sid]
        click_handlers.append( (10, 34, offset_y-24, offset_y, lambda s,e,c,i=stage_id : handler_sell(s,e,c,i)) )
        click_handlers.append( (165, 189, offset_y-24, offset_y, lambda s,e,c,i=stage_id : handler_buy(s,e,c,i)) )

    for xlo, xhi, ylo, yhi, handler in click_handlers:
        if xlo <= event.x <= xhi and ylo <= event.y <= yhi:
            if handler(state, event, current_time):
                return

def handle_drag(state, event, current_time):
    if state.player.moving and 200 <= event.x <= SCREENX-1 and 25 <= event.y <= SCREENY-35:
        state.player.moving_start_pos = state.player.position
        state.player.moving_start_time = current_time
        state.player.moving_target = (event.x, event.y)

