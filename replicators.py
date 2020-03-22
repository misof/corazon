import random
from constants import *
from worker import Worker

class Replicator(Worker):
    def __init__(self):
        super().__init__()
        self.basic_payment = 10**10
        self.basic_speed = 70

    def get_speed_multiplier(self, state):
        multiplier = 1 + state.item_counts[STAGE_FASTER_REPLICATOR]
        return multiplier

    def get_payment(self, state):
        return self.basic_payment * (1 + state.item_counts[STAGE_BIGGER_REPLICATOR])

