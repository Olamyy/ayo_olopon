def generate_name():
    import names
    return names.get_full_name()


def save_to_file(data_map):
    import csv
    filename = "data/{}vs{}.csv".format(str(list(data_map.keys())[0]), str(list(data_map.keys())[1]))
    print(filename)
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data_map.items():
            writer.writerow([key, value])
