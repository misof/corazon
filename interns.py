from constants import *
from worker import Worker

class Intern(Worker):
    def get_speed_multiplier(self, state):
        multiplier = 1 + state.item_counts[STAGE_OIL] + state.item_counts[STAGE_GEARS]
        if state.item_counts[STAGE_MOTO]: multiplier = 7
        return multiplier

    def get_payment(self, state):
        return self.basic_payment + state.item_counts[STAGE_BIGGER]

