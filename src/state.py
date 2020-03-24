import time

from src.constants import *
from src.player import Player

class State:
    def __init__(self):
        self.stage = 0
        self.money = 0
        self.item_counts = [ 0 for _ in range(len(STAGES)) ]

        self.current_status_message = ''
        self.player = Player()

        self.last_disinfection = 25 + time.time()
        self.seen_disinfection_button = False

        self.interns = []
        self.vans = []
        self.airplanes = []
        self.teleports = []
        self.replicators = []

        self.already_had_enough = False
        self.saw_fake_easter_egg = False
        self.should_win_pro = False

        self.saved_clone = None

        self.game_start_timestamp = time.time()
        self.game_duration = 0
        self.paused = False
        self.pause_timestamp = None

        self.disinfections = 0
        self.clonings = 0

    def pause(self):
        current_time = time.time()
        self.game_duration += current_time - self.game_start_timestamp
        self.paused = True
        self.pause_timestamp = current_time

    def unpause(self):
        current_time = time.time()

        # shift stuff around in time
        self.last_disinfection += (current_time - self.pause_timestamp)
        for worker in self.get_all_workers() + [self.player]:
            if worker.moving_start_time is not None: worker.moving_start_time += (current_time - self.pause_timestamp)
            worker.time_of_next_house += (current_time - self.pause_timestamp)

        self.game_start_timestamp = current_time
        self.paused = False
        self.pause_timestamp = None

    def get_all_workers(self):
        return self.interns + self.vans + self.airplanes + self.teleports + self.replicators

    def is_player_active(self):
        return len(self.get_all_workers()) == 0

    def update_status_message(self):
        self.current_status_message = ''
        if self.stage == 0 and self.money == 0: self.current_status_message = MESSAGE_WELCOME

        if STAGES[self.stage].message is not None and self.item_counts[self.stage] == 0: self.current_status_message = STAGES[self.stage].message

        if self.is_player_active():
            if self.player.pending_houses == [] and self.stage == 0 and self.money == 1: self.current_status_message = MESSAGE_FIRST_BLOOD
            if self.player.pending_houses != [] and self.player.has_cargo == False and self.stage <= 1: self.current_status_message = MESSAGE_PICK_UP_GOODS
            if self.player.pending_houses != [] and self.player.has_cargo == True and self.stage <= 1: self.current_status_message = MESSAGE_DELIVER_GOODS
        
        current_time = time.time()
        if current_time >= self.last_disinfection + DISINF_APPEAR and not self.seen_disinfection_button: self.current_status_message = MESSAGE_DISINFECT
        if current_time >= self.last_disinfection + DISINF_URGENT and not self.seen_disinfection_button: self.current_status_message = MESSAGE_DISINFECT_URGENT

