def generate_name():
    import names
    return names.get_full_name()


def generate_game_id():
    import uuid
    return "AYO-{}".format(str(uuid.uuid4())[:5])


def save_to_file_json(data):
    north, south = str(list(data.keys())[0]), str(list(data.keys())[1])
    import json
    filename = "data/{}VS{}.json".format(north, south)
    with open(filename, 'w+') as dict_:
        json.dump(data, dict_)

    process_file(filename, [north, south])


def process_file(file, name):
    import pandas
    import json

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
    final.to_csv('data/cleaned/{}vs{}.csv'.format(name[0], name[1]))
