import json
import csv
import os

class DataPersistence:
    @staticmethod
    def save_to_json(data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)

    @staticmethod
    def load_from_json(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                return json.load(json_file)
        return None

    @staticmethod
    def save_to_csv(data, filename):
        keys = data[0].keys() if data else []
        with open(filename, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def load_from_csv(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as csv_file:
                return list(csv.DictReader(csv_file))
        return None
