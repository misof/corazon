import math
import random
import time

from src.constants import *
from src.helper_functions import *

class Worker:
    def __init__(self):
        self.position = (random.randint(CITYX1,CITYX2), random.randint(CITYY1,CITYY2))

        self.pending_houses = []
        self.has_cargo = False
        self.time_of_next_house = 5 + time.time()

        self.moving = False
        self.moving_start_pos = None
        self.moving_start_time = None
        self.moving_target = None

        self.last_movement_was_left = False

        self.basic_payment = 1
        self.basic_speed = 70
        self.can_automove = True

    def get_picture(self):
        return None

    def get_payment(self, state):
        return self.basic_payment

    def get_speed_multiplier(self, state):
        return 1

    def get_delay(self, state):
        return (1 + random.random()) / 2 ** state.item_counts[STAGE_ADS]

    def get_houses_per_run(self, state):
        return 1

    def move(self, state):
        if not self.moving:
            return
        
        current_time = time.time()
        time_elapsed = current_time - self.moving_start_time
        dx = self.moving_target[0] - self.moving_start_pos[0]
        dy = self.moving_target[1] - self.moving_start_pos[1]
        if dx != 0 or dy != 0:
            self.last_movement_was_left = (dx < 0)

            d = math.sqrt( dx*dx + dy*dy )

            multiplier = self.get_speed_multiplier(state)
            speed = self.basic_speed * multiplier

            time_needed = d / speed
            if time_needed <= time_elapsed:
                self.position = self.moving_target
            else:
                dx /= d
                dy /= d
                x = self.moving_start_pos[0] + dx * speed * time_elapsed
                y = self.moving_start_pos[1] + dy * speed * time_elapsed
                self.position = ( int(x+.5), int(y+.5) )

    def start_automove(self):
        if not self.can_automove:
            return

        if self.pending_houses == []:
            self.moving = False
            return

        self.moving = True
        self.moving_start_pos = self.position
        self.moving_start_time = time.time()

        if self.has_cargo == False:
            self.moving_target = WAREHOUSE_POS
        else:
            self.moving_target = self.pending_houses[-1]

    def new_order_if_needed(self, state, current_time):
        if self.pending_houses == [] and current_time >= self.time_of_next_house:
            banxlo, banxhi, banylo, banyhi = SCREENX//2 - 60, SCREENX//2 + 60, SCREENY//2 - 50, SCREENY//2 + 50
            while len(self.pending_houses) < self.get_houses_per_run(state):
                x = random.randint(CITYX1,CITYX2)
                y = random.randint(CITYY1,CITYY2)
                if not (banxlo <= x <= banxhi and banylo <= y <= banyhi):
                    self.pending_houses.append( (x,y) )
            if state.item_counts[STAGE_LOGISTICS]:
                self.pending_houses = optimize_order(self.pending_houses)
            self.start_automove()

    def pick_up_goods(self, state, current_time):
        if self.pending_houses != [] and self.has_cargo == False:
            if square_distance( WAREHOUSE_POS, self.position ) <= 400:
                self.has_cargo = True
                self.start_automove()

    def deliver_goods(self, state, current_time):
        if self.pending_houses != [] and self.has_cargo == True:
            if square_distance( self.pending_houses[-1], self.position ) <= 300:
                payment = self.get_payment(state)
                if state.item_counts[STAGE_MASSIVE_ADS]: payment *= 10
                if state.item_counts[STAGE_HUMUNGOUS_ADS]: payment *= 10
                if state.money < STAGES[STAGE_STERILE].cost and state.money + payment >= STAGES[STAGE_STERILE].cost and state.is_player_active() and not state.already_had_enough:
                    state.should_win_pro = True
                state.money += payment

                self.pending_houses.pop()
                if self.pending_houses == []:
                    self.has_cargo = False
                    self.time_of_next_house = current_time + self.get_delay(state)
                self.start_automove()

    def process_all_events(self, state, current_time):
        self.new_order_if_needed(state, current_time)
        self.pick_up_goods(state, current_time)
        self.deliver_goods(state, current_time)

