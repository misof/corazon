from src.constants import *
from src.resources import *
from src.worker import Worker

class Van(Worker):
    def __init__(self):
        super().__init__()
        self.basic_payment = 25
        self.basic_speed = 6*70

    def get_houses_per_run(self, state):
        return 3 + state.item_counts[STAGE_PACKING]

    def get_picture(self):
        return pic_van

