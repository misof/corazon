import random

from src.constants import *
from src.worker import Worker

class Teleport(Worker):
    def __init__(self):
        super().__init__()
        self.basic_payment = 10**7
        self.basic_speed = 6*70

    def get_speed_multiplier(self, state):
        multiplier = 1 + state.item_counts[STAGE_FASTER_TELEPORT]
        return multiplier

    def get_payment(self, state):
        return self.basic_payment * (1 + state.item_counts[STAGE_BIGGER_TELEPORT])

