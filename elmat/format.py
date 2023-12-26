# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import yaml

class Formatter():

    def format_matrix(self, matrix):
        return None

    @staticmethod
    def formatter(_format):
        if _format.lower() == "json":
            return JsonFormatter()
        elif _format.lower() == "yaml":
            return YamlFormatter()
        elif _format.lower() == "csv":
            return CsvFormatter()

class JsonFormatter(Formatter):

    def format_matrix(self, matrix):
        return json.dumps(matrix, indent=4)

class CsvFormatter(Formatter):

    def __format_row_item(self, item):
        return f'"{item}"'

    def format_matrix(self, matrix):
        rows = []
        keys = list(matrix.keys())
        keys.remove('timeformat')
        keys.remove('timestamp')
        rows.append(f'"Compatiblity*", {", ".join([self.__format_row_item(x) for x in keys])}')

        for key in keys:
            row = []
            row.append(f'{key}')
            for inner_key in keys:
                row.append(f'{self.__format_row_item(matrix[key][inner_key])}')
            rows.append(', '.join(row))
        return '\n'.join(rows)

class YamlFormatter(Formatter):

    def format_matrix(self, matrix):
        return yaml.safe_dump(matrix)
