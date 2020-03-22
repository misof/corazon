from constants import *
from worker import Worker

class Airplane(Worker):
    def __init__(self):
        super().__init__()
        self.basic_payment = 5000
        self.basic_speed = 9*70

    def get_houses_per_run(self, state):
        return 1 + state.item_counts[STAGE_FUELTANK]

    def get_payment(self, state):
        return self.basic_payment * (1 + 9 * state.item_counts[STAGE_SHRINK])

