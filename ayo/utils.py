import json
from datetime import datetime
from pathlib import Path

import pandas


def generate_name():
    import names
    return names.get_full_name()


def generate_game_id():
    import uuid
    return f"AYO-{str(uuid.uuid4())[:5]}"


def save_to_file_json(data):
    north, south = str(list(data.keys())[0]), str(list(data.keys())[1])
    today = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    ayo_dir = Path(f"{Path.home()}/ayo_data/records/raw/")
    if not ayo_dir.exists():
        ayo_dir.mkdir(exist_ok=True, parents=True)
    filename = f"{ayo_dir}/{north}VS{south}_{today}.json"
    with open(filename, 'w+') as dict_:
        json.dump(data, dict_)

    process_file(filename, [north, south])


def process_file(file, name):
    with open(file) as f:
        data = json.load(f)

    df = pandas.DataFrame(data)
    columns = list(df.columns[:2])

    game_id = generate_game_id()

    data[columns[0]]['player'] = ['north'] * len(data[columns[0]]['moves'])
    data[columns[1]]['player'] = ['south'] * len(data[columns[1]]['moves'])
    data[columns[0]]['game_id'] = [game_id] * len(data[columns[0]]['moves'])
    data[columns[1]]['game_id'] = [game_id] * len(data[columns[1]]['moves'])

    north_data = pandas.DataFrame.from_dict(data[columns[0]], orient='index')
    north_data = north_data.transpose()
    south_data = pandas.DataFrame.from_dict(data[columns[1]], orient='index')
    south_data = south_data.transpose()
    final = pandas.concat([north_data, south_data])
    data_dir = Path(f"{Path.home()}/ayo_data/records/cleaned")
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True, parents=True)
    final.to_csv(f'{data_dir}/{name[0]}vs{name[1]}.csv')
