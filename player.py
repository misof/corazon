import random
from constants import *
from interns import Intern

class Player(Intern):
    def __init__(self):
        super().__init__()
        self.can_automove = False

    def get_delay(self, state):
        if state.stage == 0: return 2 + 5*random.random()
        if state.stage == 1: return 1 + 4*random.random()
        if state.stage == 2: return 3*random.random()
        if state.stage >= 3: return random.random()

    def new_order_if_needed(self, state, current_time):
        super().new_order_if_needed(state, current_time)
        if state.stage <= 1:
            state.current_status_message = 'Choď do skladu po tovar!'

    def pick_up_goods(self, state, current_time):
        super().pick_up_goods(state, current_time)
        if state.stage <= 1:
            state.current_status_message = 'Doruč tovar zákazníkovi!'

    def deliver_goods(self, state, current_time):
        super().deliver_goods(state, current_time)
        if state.money == 1:
            state.current_status_message = 'Výborne, zarobil(a) si jedno euro.'
        else:
            if state.current_status_message == 'Doruč tovar zákazníkovi!':
                state.current_status_message = ''

