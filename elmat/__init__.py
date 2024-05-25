# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import osadl_matrix
from osadl_matrix import OSADLCompatibility

import json
import logging
import os
from enum import Enum

TOP_DIR = os.path.dirname(os.path.realpath(__file__))
VAR_DIR = os.path.join(TOP_DIR, 'var')
LICENSES_FILE = os.path.join(VAR_DIR, "elmat.json")

class Elmat:

    def __init__(self, license_files=None, include_osadl=True, include_elmat=True):
        self.license_matrix = None
        self.__read_license_file()
        self.__merge_licenses(license_files, include_osadl, include_elmat)

    def is_compatible(self, outbound, inbound):
        compat = self.get_compatibility(outbound, inbound)
        return compat == osadl_matrix.OSADLCompatibility.YES or compat == "Yes"

    def get_compatibility(self, outbound, inbound):
        return self.license_matrix.get(outbound).get(inbound)

    def __internal_get_compatibility(self, outbound, inbound):
        if self.license_matrix:
            return self.license_matrix.get(outbound).get(inbound)
        if outbound in self.extended_licenses:
            if outbound in osadl_matrix.supported_licenses():
                raise ElmatException(ElmatReturnCodes.ELMAT_LICENSE_DEFINED_TWICE, f'{outbound} found in both osadl_matrix as well as internally.')

            try:
                value = self.__text_to_enum(self.extended_licenses[outbound].get(inbound))
                return value
            except Exception:
                logging.debug('Could not get the enum for "{outbound}" and "{inbound}"')

        return osadl_matrix.get_compatibility(outbound, inbound)

    def supported_licenses(self):
        return self.license_matrix.keys()

    def elmat_licenses(self):
        return self.extended_licenses

    def osadl_licenses(self):
        return osadl_matrix.supported_licenses()

    def enum_to_text(self, value):
        _map = {
            OSADLCompatibility.YES: 'Yes',
            OSADLCompatibility.NO: 'No',
            OSADLCompatibility.UNKNOWN: 'Unknown',
            OSADLCompatibility.CHECKDEP: 'Check dependency',
        }
        return _map.get(value)

    def matrix(self):
        return self.license_matrix

    def __merge_licenses(self, license_files=None, include_osadl=True, include_elmat=True):

        license_matrix = {}
        licenses = []

        # Include OSADL's licenses if requested
        if include_osadl:
            licenses += self.osadl_licenses()
        # Include Elmat's licenses if requested
        if include_elmat:
            licenses += self.elmat_licenses()

        # go through each license, and for each such go through them again
        for outer_lic in licenses:
            # this entry dies not exist, so create a map in place
            license_matrix[outer_lic] = {}
            for inner_lic in licenses:
                # fill the map with license compatibility, from OSADL,
                # per each license
                compat = self.enum_to_text(self.__internal_get_compatibility(outer_lic, inner_lic))
                license_matrix[outer_lic][inner_lic] = self.__fix_value(compat)

        # if user has supplied any license files, add them to the matrix
        if license_files:
            try:
                for license_file in license_files:
                    with open(license_file) as fp:
                        license_data = json.load(fp)
                        license_matrix = license_matrix | license_data['extended_licenses']
            except FileNotFoundError as e:
                raise ElmatException(ElmatReturnCodes.ELMAT_FILE_ERROR, f'Could not read file "{license_file}". Message: "{e}"')

        # check if each outer license has all values, if not: add Unknown or Yes
        for outer_lic in license_matrix.keys():
            for inner_lic in license_matrix.keys():
                if inner_lic == outer_lic:
                    license_matrix[outer_lic][inner_lic] = 'Yes'
                elif inner_lic not in license_matrix[outer_lic]:
                    license_matrix[outer_lic][inner_lic] = 'Unknown'

        self.license_matrix = license_matrix
        return license_matrix

    def __read_license_file(self):
        with open(LICENSES_FILE) as fp:
            all_license_data = json.load(fp)
            self.extended_licenses = all_license_data['extended_licenses']

    def __text_to_enum(self, value_str):
        return osadl_matrix.OSADLCompatibility.from_text(value_str)

    def __fix_value(self, value):
        if value is not None:
            return value
        return 'Unknown'

class ElmatReturnCodes(Enum):
    ELMAT_OK = 0
    ELMAT_INCOMPATIBLE = 1
    ELMAT_FILE_ERROR = 10
    ELMAT_LICENSE_UNKNOWN = 11
    ELMAT_LICENSE_DEFINED_TWICE = 12

class ElmatException(Exception):

    def __init__(self, error_code, error_message=None):
        self._error_code = int(error_code.value)
        if error_message is None:
            self._error_message = self._error_code.value[1]
        else:
            self._error_message = error_message

    def error_message(self):
        return self._error_message

    def error_code(self):
        return self._error_code
