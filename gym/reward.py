class RewardValues:
    def __init__(
            self,
            fainted_value: float = 0.0,
            hp_value: float = 0.0,
            status_value: float = 0.0,
            invalid_action_value: float = 0.0,
            victory_value: float = 1.0):
        self.fainted_value = fainted_value
        self.hp_value = hp_value
        self.status_value = status_value
        self.invalid_action_value = invalid_action_value
        self.victory_value = victory_value

