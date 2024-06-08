import common
import json
import os
import requests

base_url = "https://replay.pokemonshowdown.com"
replay_list_url = base_url + "/api/replays/search?username=&format={}&page={}&sort={}"
default_workspace = os.environ['WORKSPACE_ENV']
battle_format = 'gen9randombattle'
replay_pages = 100
replays_per_page = 50
json_extension = ".json"
separator = "/"


def store_replay(replay_id, ws):
    if not os.path.isfile(ws + separator + replay_id + json_extension):
        json_replay = requests.get(base_url + separator + replay_id + json_extension)
        file = open(ws + separator + replay_id + json_extension, "w")
        file.write(json_replay.content.decode("utf-8"))
        file.close()
        print("downloaded replay " + replay_id + " successfully")
    else:
        print("skipped replay " + replay_id + " because already downloaded")


def download_replays(ws, fmt):
    sort_types = ["rating", ""]
    for t in sort_types:
        for i in range(1, replay_pages):
            response = requests.get(replay_list_url.format(fmt, i, t))
            doc = json.loads(response.content[1:])
            for j in range(0, replays_per_page):
                store_replay(doc[j]["id"], ws)


if __name__ == "__main__":
    workspace = common.get_workspace_dir()
    workspace = workspace + '/replays/' + battle_format
    if not os.path.isdir(workspace):
        os.makedirs(workspace)
    download_replays(workspace, battle_format)
