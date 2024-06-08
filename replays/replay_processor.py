import json
from typing import List, Dict
from replays import constants
from replays.replay import Replay


class ReplayProcessor:
    def __init__(self):
        self._processed = False
        self._input_log = []
        self._raw_input_log = []
        self._battle_log = []
        self._player_name = None
        self._opponent_name = None
        self._battle_rating = 0
        self._battle_id = ''
        self._poke_moves: Dict[str, List[str]] = {}

    def load_normalized_replay(self, replay_path: str):
        replay = open(replay_path, "r")
        json_replay = json.loads(replay.read())
        self._battle_log = json_replay[constants.REPLAY_BATTLE_LOG_FIELD]
        self._input_log = json_replay[constants.REPLAY_INPUT_LOG_FIELD]
        self._player_name = json_replay[constants.REPLAY_PLAYERS_LOG_FIELD][0]
        self._opponent_name = json_replay[constants.REPLAY_PLAYERS_LOG_FIELD][1]
        self._battle_rating = json_replay[constants.REPLAY_RATING_FIELD]
        self._processed = True

    def load_replay(self, replay_path: str):
        replay = open(replay_path, "r")
        json_replay = json.loads(replay.read())
        self._battle_id = json_replay[constants.REPLAY_BATTLE_ID_FIELD]
        self._battle_log = json_replay[constants.REPLAY_BATTLE_LOG_FIELD].split('\n')
        self._input_log = json_replay[constants.REPLAY_INPUT_LOG_FIELD].split('\n')
        self._player_name = json_replay[constants.REPLAY_PLAYERS_LOG_FIELD][0]
        self._opponent_name = json_replay[constants.REPLAY_PLAYERS_LOG_FIELD][1]
        self._battle_rating = json_replay[constants.REPLAY_RATING_FIELD]

    def process_replay(self):
        if not self._processed:
            self._discard_non_p1_input_log()
            self._add_force_switch_battle_logs()
            self._remove_unexpected_logs()
            self._get_pokemon_moves()
            self._processed = True

    def _get_pokemon_moves(self):
        poke_moves = {}
        for line in self._battle_log:
            if line.startswith('|move|p1a: '):
                line_parts = line.split('|')
                pokemon = line_parts[2][5:].replace(' ', '').replace('-', '').replace('.', '').lower()
                move = line_parts[3].replace(' ', '').replace('-', '').replace('.', '').lower()
                if poke_moves.get(pokemon, None):
                    if move not in poke_moves.get(pokemon):
                        poke_moves[pokemon].append(move)
                else:
                    poke_moves[pokemon] = [move]
        self._poke_moves = poke_moves

    def _discard_non_p1_input_log(self):
        switch_logs = []
        skip = True
        for line in self._battle_log:
            if line.startswith(constants.BATTLE_LOG_P1_SWITCH):
                if not skip:
                    switch_logs.append(line.split('|')[2][4:])
                skip = False
        switch_count = 0
        p1_input_log = []
        for line in self._input_log:
            if line.startswith(constants.INPUT_LOG_P1_ACTION):
                self._raw_input_log.append(line)
                if constants.INPUT_LOG_P1_SWITCH in line:
                    # need this trick to avoid errors later parsing pokemon names with a space like 'Iron Valiant'
                    pokemon_name = switch_logs[switch_count].strip().replace(' ', '#')
                    p1_input_log.append(constants.INPUT_LOG_P1_SWITCH + " " + pokemon_name)
                    switch_count += 1
                else:
                    p1_input_log.append(line)
        self._input_log = p1_input_log

    def _add_force_switch_battle_logs(self):
        add_indexes = []
        for i in range(0, len(self._battle_log) - 1):
            if constants.BATTLE_LOG_P1_POKE_FAINT in self._battle_log[i]:
                add_indexes.append(i)
            elif constants.BATTLE_LOG_P1_MOVE in self._battle_log[i]:
                command = self._battle_log[i].split('|')
                if len(command) >= 4 and command[3] in constants.P1_FORCE_SWITCH_MOVES:
                    add_indexes.append(i)
            elif constants.BATTLE_LOG_P2_MOVE in self._battle_log[i]:
                command = self._battle_log[i].split('|')
                if len(command) >= 4 and command[3] in constants.P2_FORCE_SWITCH_MOVES:
                    add_indexes.append(i)
        # remove the last faint pokemon because no switches available
        add_indexes = add_indexes[0:len(add_indexes) - 1]
        for i in add_indexes[::-1]:
            self._battle_log.insert(i, constants.FORCE_SWITCH_LOG)

    def _remove_unexpected_logs(self):
        battle_logs_filtered = []
        for line in self._battle_log:
            if (not line.startswith(constants.BATTLE_LOG_BADGE_MESSAGE) and
                    not line.startswith(constants.BATTLE_LOG_INACTIVE_OFF) and
                    not line.startswith(constants.BATTLE_LOG_HIDE_LINES)):
                battle_logs_filtered.append(line)
        self._battle_log = battle_logs_filtered

    def to_data(self):
        return Replay(
            battle_id=self._battle_id,
            battle_log=self._battle_log,
            input_log=self._input_log,
            raw_input_log=self._raw_input_log,
            battle_rating=self._battle_rating,
            player_name=self._player_name,
            opponent_name=self._opponent_name,
            poke_moves=self._poke_moves)

    def save_replay(self, out_path=None):
        with open(out_path, 'w') as file:
            json.dump({
                constants.REPLAY_BATTLE_LOG_FIELD: self._battle_log,
                constants.REPLAY_INPUT_LOG_FIELD: self._input_log,
                constants.REPLAY_RATING_FIELD: self._battle_rating,
                constants.REPLAY_PLAYERS_LOG_FIELD: [self._player_name, self._opponent_name],
            }, file)
