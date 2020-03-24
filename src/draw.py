import time

from src.easygame import *

from src.constants import *
from src.helper_functions import *
from src.resources import *

def draw_status_message(msg):
    draw_polygon( (0, 0), (SCREENX-1, 0), (SCREENX-1,24), (0,24), color=COLOR_LIGHTGRAY )
    draw_text( msg, 'Arial', 16, position=(20, 4), color=COLOR_BLACK )

def draw_money_textbox(state):
    peniaze_message = 'Peniaze: €{}'.format(state.money)
    if state.money >= 10**6: peniaze_message += ' (€{})'.format(scientific_format(state.money, force=True))

    draw_polygon( (200, SCREENY-34), (SCREENX-200, SCREENY-34), (SCREENX-200,SCREENY-10), (200,SCREENY-10), color=COLOR_LIGHTGRAY )
    draw_text( peniaze_message, 'Arial', 16, position=(204, SCREENY-30), color=COLOR_BLACK )

def draw_disinfection_button(urgent = False):
    draw_polygon( (SCREENX-180, SCREENY-34), (SCREENX-10, SCREENY-34), (SCREENX-10,SCREENY-10), (SCREENX-180,SCREENY-10), color=COLOR_BLACK )
    draw_polygon( (SCREENX-179, SCREENY-33), (SCREENX-11, SCREENY-33), (SCREENX-11,SCREENY-11), (SCREENX-179,SCREENY-11), color=COLOR_URGENT_BG if urgent else COLOR_LIGHTGRAY )
    draw_text('Dezinfikuj si ruky', 'Arial', 16, position=(SCREENX-176, SCREENY-30), color=COLOR_URGENT_FG if urgent else COLOR_BLACK )

def draw_button(label, offx, offy, enabled, width=24, font_size=16):
    draw_polygon( (offx,offy), (offx+width,offy), (offx+width,offy-24), (offx,offy-24), color=COLOR_BLACK if enabled else COLOR_DISABLED )
    draw_polygon( (offx+1,offy+1), (offx+width-1,offy+1), (offx+width-1,offy-23), (offx+1,offy-23), color=COLOR_LIGHTGRAY )
    draw_text( label, 'Arial', font_size, position=(offx+6, offy-20), color=COLOR_BLACK if enabled else COLOR_DISABLED )

def get_opacities(state):
    intern_opacity = 1
    van_opacity = 1
    airplane_opacity = 1
    teleport_opacity = 1
    replicator_opacity = 1

    if state.vans != []: intern_opacity = 0.2
    if state.airplanes != []: intern_opacity, van_opacity = 0.15, 0.07
    if state.teleports != []: intern_opacity, van_opacity, airplane_opacity = 0.15, 0.07, 0.15
    if state.replicators != []: intern_opacity, van_opacity, airplane_opacity, teleport_opacity = 0.15, 0.07, 0.15, 0.5

    return list([ intern_opacity, van_opacity, airplane_opacity, teleport_opacity, replicator_opacity ])

def draw_houses(state):
    worker_groups = [ state.interns, state.vans, state.airplanes, state.teleports, state.replicators ]
    house_pics = [ pic_dom, pic_veziak, pic_mesto, pic_mesto, pic_mesto ]
    opacities = get_opacities(state)
    if opacities[3] != 1: opacities[3] = 0.15 # adjustment for teleport houses

    for group, pic, opacity in zip(worker_groups, house_pics, opacities):
        for worker in group:
            for house in worker.pending_houses:
                draw_image( pic, position=house, opacity=opacity )

def draw_workers(state):
    intern_opacity, van_opacity, airplane_opacity, teleport_opacity, replicator_opacity = get_opacities(state)

    for worker in state.interns:
        draw_image(worker.get_picture(), position=worker.position, opacity=intern_opacity, scale_x=-1 if worker.last_movement_was_left else 1)

    for worker in state.vans:
        draw_image(worker.get_picture(), position=worker.position, opacity=van_opacity, scale_x=-1 if worker.last_movement_was_left else 1)

    for worker in state.airplanes:
        draw_image(worker.get_picture(), position=worker.position, opacity=airplane_opacity, scale_x=-1 if worker.last_movement_was_left else 1)

    for worker in state.teleports:
        if worker.has_cargo:
            draw_circle( WAREHOUSE_POS, radius=32, color=(1, 1, 0.5, 0.9*teleport_opacity) )
            draw_circle( worker.pending_houses[-1], radius=32, color=(1, 1, 0.5, 0.9*teleport_opacity) )
            draw_line( WAREHOUSE_POS, worker.pending_houses[-1], thickness=47, color=(1, 1, 0.5, 0.7*teleport_opacity) )
        
    for worker in state.replicators:
        if worker.has_cargo:
            dfull = math.sqrt( square_distance( WAREHOUSE_POS, worker.pending_houses[-1] ) )
            dpart = math.sqrt( square_distance( worker.position, worker.pending_houses[-1] ) )
            radius = int( 0.5 + 60 * dpart / dfull )
            draw_circle( worker.pending_houses[-1], radius=radius, color=(1, 0.3, 1, 0.7*replicator_opacity) )

def draw_stage_menu(state):
    menu = stages_in_menu(state)

    for sid in range(len(menu)):
        offset_y = SCREENY - 10 - 60*sid
        stage_id = menu[sid]

        stage_full_name = '{} (€{})'.format( STAGES[stage_id].name, scientific_format(STAGES[stage_id].cost) )

        draw_polygon( (10,offset_y), (189,offset_y), (189,offset_y-24), (10,offset_y-24), color=COLOR_LIGHTGRAY )
        draw_text( stage_full_name, 'Arial', 12, position=(14,offset_y-17), color=COLOR_BLACK )

        can_minus = (state.item_counts[stage_id] > STAGES[stage_id].lower_bound and STAGES[stage_id].can_sell)
        can_plus = (state.item_counts[stage_id] < STAGES[stage_id].upper_bound and state.money >= STAGES[stage_id].cost)

        draw_button( '–', 10, offset_y-26, can_minus )
        draw_button( '+', 165, offset_y-26, can_plus )

        draw_polygon( (36,offset_y-26), (163,offset_y-26), (163,offset_y-50), (36,offset_y-50), color=COLOR_LIGHTGRAY )
        draw_text( str(state.item_counts[stage_id]), 'Arial', 12, position=(40,offset_y-44), color=COLOR_BLACK )

def draw_current_screen(state):
    # draw_image(pic_background, position=(0, 0), anchor=(0, 0), scale_x=1.01, scale_y=1.01)
    draw_image(pic_background, position=(0, 0), anchor=(0, 0) )
    draw_image(pic_sklad, position=WAREHOUSE_POS)
    
    if state.is_player_active():
        for house in state.player.pending_houses: draw_image(pic_dom, position=house)
        draw_image(state.player.get_picture(), position=state.player.position, scale_x=-1 if state.player.last_movement_was_left else 1)
    else:
        draw_houses(state)
        draw_workers(state)

    draw_stage_menu(state)
    draw_status_message(state.current_status_message)
    draw_money_textbox(state)

    current_time = time.time()
    if current_time > state.last_disinfection + DISINF_APPEAR:
        draw_disinfection_button(current_time > state.last_disinfection + DISINF_URGENT)

    if state.item_counts[STAGE_CLONE] == 1:
        if state.saved_clone is None:
            draw_button('naklonuj sa (€10M)', 10, 60, state.money >= 10**7, 179, 12)
        else:
            draw_button('prepíš klon (€10M)', 10, 60, state.money >= 10**7, 179, 12)

