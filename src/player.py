import random

from src.constants import *
from src.interns import Intern

class Player(Intern):
    def __init__(self):
        super().__init__()
        self.can_automove = False

    def get_delay(self, state):
        if state.stage == 0: return 2 + 5*random.random()
        if state.stage == 1: return 1 + 4*random.random()
        if state.stage == 2: return 3*random.random()
        if state.stage >= 3: return random.random()

