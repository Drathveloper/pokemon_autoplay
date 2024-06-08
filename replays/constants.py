REPLAY_BATTLE_LOG_FIELD = "log"
REPLAY_INPUT_LOG_FIELD = "inputlog"
REPLAY_PLAYERS_LOG_FIELD = "players"
REPLAY_RATING_FIELD = "rating"
REPLAY_BATTLE_ID_FIELD = "id"

BATTLE_LOG_P1_SWITCH = "|switch|p1a"
BATTLE_LOG_P1_POKE_FAINT = "|faint|p1a"
BATTLE_LOG_P1_MOVE = "|move|p1a"
BATTLE_LOG_P2_MOVE = "|move|p2a"
BATTLE_LOG_BADGE_MESSAGE = "|badge|"
BATTLE_LOG_INACTIVE_OFF = "|inactiveoff|"
BATTLE_LOG_HIDE_LINES = "|hidelines|"

INPUT_LOG_P1_ACTION = ">p1"
INPUT_LOG_P1_SWITCH = INPUT_LOG_P1_ACTION + " switch"

P1_FORCE_SWITCH_MOVES = [
    'Baton Pass',
    'Chilly Reception',
    'Flip Turn',
    'Parting Shot',
    'Shed Tail',
    'Teleport',
    'U-turn',
    'Volt Switch'
]

P2_FORCE_SWITCH_MOVES = [
    'Circle Throw',
    'Dragon Tail',
    'Roar',
    'Whirlwind'
]

FORCE_SWITCH_LOG = '|request|{\"forceSwitch\": \"true\", \"side\":{\"pokemon\":[]}, \"noCancel\":true, \"rqid\":1}'
