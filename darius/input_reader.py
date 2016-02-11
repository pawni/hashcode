import json


class InputReader:
    files = ['../busy_day.in.json', '../mother_of_all_warehouses.in.json', '../redundancy.in.json']

    def __init__(self):
        pass

    def read(self, file_num=0):
        with open(self.files[file_num]) as data_file:
            state = json.load(data_file)

        return state
