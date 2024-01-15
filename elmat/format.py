# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import yaml

class Formatter():

    def format_matrix(self, matrix):
        return None

    def format_licenses(self, license_list):
        return None

    def format_verification(self, verification):
        return None

    def format_exception(self, exception):
        return None

    def format_compatiblity(self, compatibility):
        return None

    def _exception_to_dict(self, exception):
        return {
            'message': exception.error_message(),
            'code': exception.error_code(),
        }

    @staticmethod
    def formatter(_format):
        if _format.lower() == "json":
            return JsonFormatter()
        elif _format.lower() == "yaml" or _format.lower() == "yml":
            return YamlFormatter()
        elif _format.lower() == "csv":
            return CsvFormatter()
        elif _format.lower() == "text" or _format.lower() == "txt":
            return TxtFormatter()

class JsonFormatter(Formatter):

    def format_matrix(self, matrix):
        return json.dumps(matrix, indent=4)

    def format_licenses(self, license_list):
        return json.dumps(list(license_list), indent=4)

    def format_verification(self, verification):
        return json.dumps(verification)

    def format_exception(self, exception):
        return json.dumps(self._exception_to_dict(exception))

    def format_compatiblity(self, compatibility):
        return json.dumps(compatibility)

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

    def format_licenses(self, license_list):
        return {",".join(license_list)}

    def format_verification(self, verification):
        return f'{verification}'

    def format_exception(self, exception):
        return exception.error_message()

    def format_compatiblity(self, compatibility):
        return compatibility

class TxtFormatter(Formatter):

    def format_matrix(self, matrix):
        return CsvFormatter().format_matrix(matrix)

    def format_licenses(self, license_list):
        return '\n'.join(license_list)

    def format_verification(self, verification):
        return f'{verification}'

    def format_exception(self, exception):
        return exception.error_message()

    def format_compatiblity(self, compatibility):
        return compatibility

class YamlFormatter(Formatter):

    def format_matrix(self, matrix):
        return yaml.safe_dump(matrix)

    def format_licenses(self, license_list):
        return yaml.safe_dump(list(license_list))

    def format_verification(self, verification):
        return yaml.safe_dump(verification)

    def format_exception(self, exception):
        return yaml.safe_dump(self._exception_to_dict(exception))

    def format_compatiblity(self, compatibility):
        return yaml.safe_dump(compatibility)
