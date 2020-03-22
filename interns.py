import random
from constants import *
from resources import *
from worker import Worker

class Intern(Worker):
    def __init__(self):
        super().__init__()
        self.cargo_type = None

    def get_speed_multiplier(self, state):
        multiplier = 1 + state.item_counts[STAGE_OIL] + state.item_counts[STAGE_GEARS]
        if state.item_counts[STAGE_MOTO]: multiplier = 7
        return multiplier

    def get_payment(self, state):
        return self.basic_payment + state.item_counts[STAGE_BIGGER]

    def get_picture(self):
        if self.has_cargo:
            if self.cargo_type is None:
                self.cargo_type = random.choice([ pic_riksa_jablko, pic_riksa_pomaranc, pic_riksa_kapusta ])
            return self.cargo_type
        else:
            self.cargo_type = None
            return pic_riksa_empty

