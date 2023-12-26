#!/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import osadl_matrix
from osadl_matrix import OSADLCompatibility

import json
import logging
import os

elmat_version = " 0.0.1"
emlat_name = "emlat"
TOP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
VAR_DIR = os.path.join(TOP_DIR, "var")
LICENSES_FILE = os.path.join(VAR_DIR, "elmat.json")

class Elmat:

    def __init__(self):
        self.license_data = None
        self.extended_licenses = None
        if not self.license_data:
            self.__read_license_file()

    def is_compatible(self, outbound, inbound):
        compat = self.get_compatibility(outbound, inbound)
        return compat == osadl_matrix.OSADLCompatibility.YES or compat == "Yes"

    def get_compatibility(self, outbound, inbound):
        if outbound in self.extended_licenses:
            if outbound in osadl_matrix.supported_licenses():
                raise Exception(f'{outbound} found in both osadl_matrix as well as internally.')

            try:
                value = self.__text_to_enum(self.extended_licenses[outbound].get(inbound))
                return value
            except Exception:
                logging.debug('Could not get the enum for "{outbound}" and "{inbound}"')

        return osadl_matrix.get_compatibility(outbound, inbound)

    def supported_licenses(self):
        return osadl_matrix.supported_licenses() | self.extended_licenses.keys()

    def elmat_licenses(self):
        return self.extended_licenses.keys()

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

    def merge_licenses(self, license_files=None, include_osadl=True, include_elmat=True):

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
                compat = self.enum_to_text(self.get_compatibility(outer_lic, inner_lic))
                license_matrix[outer_lic][inner_lic] = self.__fix_value(compat)

        # if user has supplied any license files, add them to the matrix
        if license_files:
            for license_file in license_files:
                with open(license_file) as fp:
                    license_data = json.load(fp)
                    license_matrix = license_matrix | license_data['extended_licenses']

        # check if each outer license has all values, if not: add Unknown
        for outer_lic in license_matrix.keys():
            for inner_lic in license_matrix.keys():
                if inner_lic not in license_matrix[outer_lic]:
                    if inner_lic == outer_lic:
                        license_matrix[outer_lic][inner_lic] = 'Same'
                    else:
                        license_matrix[outer_lic][inner_lic] = 'Unknown'

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
