import os
import io
import json
import time
import threading

dir_path = os.path.abspath("resources")


def cooldown(function, duration=int(5)):
    function.on_cooldown = False

    def sleeper():
        function.on_cooldown = True
        time.sleep(duration)
        function.on_cooldown = False

    async def wrapper(*args, **kwargs):
        if function.on_cooldown:
            print(f"Function {function.__name__} on cooldown")
        else:
            timer = threading.Thread(target=sleeper)
            await function(*args, **kwargs)
            timer.start()
    return wrapper


def get_channel():
    JSON_FILE = str(dir_path) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        global CHAN
        CHAN = data['CHANNEL']
    return CHAN


def update_channel(value):
    JSON_FILE = str(dir_path) + '/channels.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['CHANNEL'] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def get_drt(ac, channel):
    dorito = {'drt': ['ferro', 'iron', 'bronze', 'prata', 'silver', 'ouro',
                      'gold', 'plat', 'platinum', 'platina', 'esmeralda', 'emerald']}
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        cmd = data[f'elo{ac}'].lower()
        if cmd in dorito['drt']:
            drt = 'DoritosChip '
        else:
            drt = 'PdL'
        return drt


def get_elo(ac, channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'elo{ac}']


def get_conta(ac, channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'conta{ac}']


def get_div(ac, channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'div{ac}']


def get_pdl(ac, channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'pdl{ac}']


def update_value(key, value, channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data[key] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def file_check(channel):
    JSON_FILE = str(dir_path) + f'/channeldata/{channel}.json'
    if os.path.isfile(JSON_FILE) and os.access(JSON_FILE, os.R_OK):
        return True
    else:
        with io.open(os.path.join(JSON_FILE), 'w') as json_file:
            json_file.write(json.dumps({}))
