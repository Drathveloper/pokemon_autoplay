from typing import List, Dict


class Replay:
    def __init__(
            self,
            battle_id: str,
            poke_moves: Dict[str, List[str]],
            battle_log: List[str],
            input_log: List[str],
            raw_input_log: List[str],
            battle_rating: int,
            player_name: str,
            opponent_name: str = None):
        self.id = battle_id
        self.input_log = input_log
        self.raw_input_log = raw_input_log
        self.battle_log = battle_log
        self.player_name = player_name
        self.opponent_name = opponent_name
        self.battle_rating = battle_rating
        self.poke_moves = poke_moves
