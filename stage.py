
class Stage:
    def __init__(self, cost, reveal_at, name, lower_bound, upper_bound, can_sell, message):
        self.cost = cost
        self.reveal_at = reveal_at
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.can_sell = can_sell
        self.message = message

