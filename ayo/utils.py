def generate_name():
    import names
    return names.get_full_name()


def save_to_file(data_map):
    import json
    filename = "data/{}vs{}.json".format(str(list(data_map.keys())[0]), str(list(data_map.keys())[1]))
    with open(filename, 'a') as json_file:
        json.dump(data_map, json_file)
