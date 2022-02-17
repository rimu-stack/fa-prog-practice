import os.path
import csv
import pickle
import re
from typing import Any


def set_typed_values(value: str) -> Any:

    if re.match(r'^(true|false)$', value, re.IGNORECASE):
        return bool(value)

    if re.match(r'^[0-9]+$', value, re.IGNORECASE):
        return int(value)

    if re.match(r'^[0-9]+\.[0-9]*$', value, re.IGNORECASE):
        return float(value)

    if not re.sub(r' +', '', value):
        return None

    return value


class Table:
    data: list

    def __init__(self) -> None:
        self.data = []

    # Module 1
    def load_table(self, *files, set_types: bool = False) -> None:
        files_data = {}

        for file_name in files:
            if not os.path.isfile(file_name):
                print(f'File not found ({file_name})')
                continue

            if file_name[-4:] == '.pkl':
                with open(file_name, 'rb') as file:
                    files_data[file_name] = pickle.load(file)

            if file_name[-4:] == '.csv':
                with open(file_name, 'r', encoding='utf-8-sig') as file:
                    files_data[file_name] = [
                        row for row in csv.DictReader(file)]

            if not files_data or not set_types:
                continue

            files_data[file_name] = self.set_auto_types(files_data[file_name])

        if not files_data.values():
            return print('Files are empty')

        ethalon_keys = list(files_data.values())[0][0].keys()
        for file_name, file_data in files_data.items():
            for table_row in file_data:
                row = {}

                for key in ethalon_keys:
                    if not key in table_row.keys():
                        self.data = []
                        return print('Tables structure is not the same!')

                    row[key] = table_row[key]

                self.data.append(row)

    def save_table(self, file_name: str, delimet: str = '\n', max_rows: bool = None) -> None:
        if len(self.data) == 0:
            return print('Data is empty is taken')

        slices = [self.data]
        if max_rows != None:
            copy = self.data
            slices = [copy[index:index+max_rows]
                      for index in range(0, len(copy), max_rows)]

        headers = self.data[0].keys()

        for index, slice in enumerate(slices):
            short_file_name = re.sub(r'\..*?$', '', file_name)
            extention = re.search(r'\.([^./]*?)$', file_name)
            extention = extention.group(0) if extention else None

            if not extention:
                return print('File has no extention!')

            temp_file_name = f'{short_file_name}{index}{extention}' if index != 0 else file_name

            if extention == '.csv':
                with open(temp_file_name, 'w', newline='', encoding='utf-8-sig') as new_csv:
                    file_writer = csv.DictWriter(
                        new_csv, fieldnames=headers)
                    file_writer.writeheader()
                    file_writer.writerows(slice)

            if extention == '.pkl':
                with open(temp_file_name, 'wb') as new_pickle:
                    pickle.dump(slice, new_pickle)

            if extention == '.txt':
                with open(temp_file_name, 'w', encoding='utf-8-sig') as new_txt:
                    new_txt.write(','.join(headers) + delimet)
                    string_rows = [','.join(row.values()) for row in slice]
                    data = delimet.join(string_rows)
                    new_txt.write(data)

    # Module 2
    def set_column_types(self, types: dict, by_number=True) -> None:
        last_type = None
        last_value = None

        if not self.data:
            return print('Table data is empty!')

        if by_number and len(types.values()) > len(self.data[0].values()):
            return print('Types are out of range')

        try:
            if by_number:
                row_keys = list(self.data[0].keys())

                for column, to_type in types.items():
                    last_type = to_type
                    key = row_keys[column]
                    for index in enumerate(self.data):
                        last_value = self.data[index][key]
                        self.data[index][key] = to_type(
                            self.data[index][key])

                return None

            for key, to_type in types.items():
                last_type = to_type
                for index, (value) in enumerate(self.data):
                    last_value = self.data[index][key]
                    self.data[index][key] = to_type(self.data[index][key])
        except ValueError:
            return print(f'Invalid type {last_type} for value {last_value}')

    def get_rows_by_number(self, start: int, stop: None = None, copy_table: bool = False) -> None:
        if not self.data:
            return print('Table data is empty!')

        if stop and type(stop) != int:
            return print('Stop must be integer!')

        if type(start) != int:
            return print('Start must be integer!')

        if start > len(self.data):
            return print('Start out of range!')

        if stop and stop > len(self.data):
            return print('Stop out of range!')

        if stop and start > stop:
            return print('Start can`t be bigger than start!')

        result = self.data[start:stop]

        if copy_table:
            return result

        self.data = result

    def get_rows_by_index(self, *indexes, copy_table: bool = False) -> list:
        if not self.data:
            return print('Table data is empty!')

        first_key = list(self.data[0].keys())[0]
        result = [row for row in self.data if row[first_key] in indexes]

        if copy_table:
            return result

        self.data = result

    def get_column_types(self, by_number: bool = True) -> dict:
        if not self.data:
            return print('Table data is empty!')

        first_values = self.data[0].items()

        if by_number:
            return {index: type(value) for index, (key, value) in enumerate(first_values)}

        return {key: type(value) for (key, value) in first_values}

    def get_values(self, column: int = 0) -> list:
        if not self.data:
            return print('Table data is empty!')

        if column > len(self.data[0]) - 1:
            return print('Column is out of range!')

        return [list(row.values())[column] for row in self.data]

    def set_values(self, values: list, column: int = 0) -> None:
        if column > len(self.data[0]) - 1:
            return print('Column is out of range!')

        value_types = [type(value) for value in values]

        if len(value_types) > len(self.data):
            return print('Values are out of range!')

        if not self.data:
            return print('Table data is empty!')

        column_type = type(list(self.data[0].values())[column])
        filtered = list(filter(lambda item: item != column_type, value_types))

        if filtered:
            return print('Values list contains wrong type for this column')

        key = list(self.data[0].keys())[column]
        for index, (value) in enumerate(values):
            self.data[index][key] = value

    def get_value(self, column: int = 0, row: int = 0) -> Any:
        if not self.data:
            return print('Table data is empty!')

        if column > len(self.data[0]) - 1:
            return print('Column is out of range!')

        if row > len(self.data) - 1:
            return print('Row is out of range!')

        return list(self.data[row].values())[column]

    def set_value(self, value: Any, column: int = 0, row: int = 0) -> None:
        if not self.data:
            return print('Table data is empty!')

        if column > len(self.data[0]) - 1:
            return print('Column is out of range!')

        if row > len(self.data) - 1:
            return print('Row is out of range!')

        key = list(self.data[0].keys())[column]
        column_type = type(self.data[row][key])

        if (column_type != type(value)):
            return print('Value has an incorrect type')

        self.data[row][key] = value

    def print_table(self):
        if not self.data:
            return print('Table is empty')

        print(self.data)

    def getData(self) -> list:
        return self.data

    # Advanced tasks
    def set_auto_types(self, table: list = None) -> None:
        temp = table

        if not temp:
            temp = self.data

        for row_index in range(len(temp)):
            for (key, value) in temp[row_index].items():
                temp[row_index][key] = set_typed_values(value)

        if table:
            return temp

        self.data = temp

    def split(self, row: int) -> list:
        if row > len(self.data) - 1:
            return print('Row is out of range!')

        return [
            self.data[row:],
            self.data[:row],
        ]

    def concat(self, *tables) -> list:
        temp = []
        for table in tables:
            temp = [
                *temp,
                *table
            ]
        return temp
