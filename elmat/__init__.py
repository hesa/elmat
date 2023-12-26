#!/bin/env python3

import osadl_matrix
from  osadl_matrix import OSADLCompatibility

from enum import Enum
import json
import os


elmat_version = "0.0.1"
emlat_name = "emlat"


TOP_DIR=os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")
VAR_DIR=os.path.join(TOP_DIR, "var")
LICENSES_FILE=os.path.join(VAR_DIR, "elmat.json")

class Elmat:

    def __init__(self):
        self.license_data=None
        self.extended_licenses=None
        if not self.license_data:
            self.__read_license_file()
        
    
    def is_compatible(self, outbound, inbound):
        compat=self.get_compatibility(outbound, inbound)
        return compat==osadl_matrix.OSADLCompatibility.YES or compat=="Yes"

    def get_compatibility(self, outbound, inbound):
        if outbound in self.extended_licenses:
            if outbound in osadl_matrix.supported_licenses():
                raise Exception(f'{outbound} found in both osadl_matrix as well as internally.')

            try:
                value = self.__text_to_enum(self.extended_licenses[outbound].get(inbound))
                return value
            except:
                pass

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
            #OSADLCompatibility.YES: 'Same'
        }
        return _map.get(value)

    def merge_licenses(self, license_files=[], include_osadl=True, include_elmat=True):

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
        for license_file in license_files:
            with open(license_file) as fp:
                license_data=json.load(fp)
                license_matrix = license_matrix | license_data['extended_licenses']

        # check if each outer license has all values, if not: add Unknown
        for outer_lic in license_matrix.keys():
            for inner_lic in license_matrix.keys():
                if inner_lic not in license_matrix[outer_lic]:
                    #print(f'{outer_lic} {inner_lic} ==> undef')
                    if inner_lic == outer_lic:
                        license_matrix[outer_lic][inner_lic] = 'Same'
                    else:
                        license_matrix[outer_lic][inner_lic] = 'Unknown'

        #print(json.dumps(license_matrix, indent=4))
        return license_matrix

    def __read_license_file(self):
        with open(LICENSES_FILE) as fp:
            all_license_data=json.load(fp)
            self.extended_licenses=all_license_data['extended_licenses']

    def __text_to_enum(self, value_str):
        return osadl_matrix.OSADLCompatibility.from_text(value_str)

    def __fix_value(self, value):
        if value != None:
            return value
        return 'Unknown'
    
    
def __test_me_sub(inbound, outbound):
    elmat = Elmat()
    print(f'{inbound} ---> {outbound} ===> {elmat.get_compatibility(inbound, outbound)}')
    print(f'    ===> {elmat.is_compatible(inbound, outbound)}')
    print(f'{outbound} ---> {inbound} ===> {elmat.get_compatibility(outbound, inbound)}')
    print(f'    ===> {elmat.is_compatible(outbound, inbound)}')
    print('')
    
def __test_me():
#    __test_me_sub('MIT', 'X11')
#    __test_me_sub('MIT', 'GPL-2.0-or-later')
    __test_me_sub('Proprietary-linked', 'MIT')
#    __test_me_sub('Proprietary-linked', 'GPL-2.0-or-later')
#    __test_me_sub('Proprietary-linked', 'LGPL-3.0-or-later')
#    __test_me_sub('Proprietary-linked', 'GPL-3.0-or-later')
#    __test_me_sub('Proprietary-linked', 'OpenSSL')
#    __test_me_sub('Proprietary-linked', 'GPL-2.0-only WITH Classpath-exception-2.0')
#    __test_me_sub('Proprietary-linked', 'GPL-2.0-or-later WITH Classpath-exception-2.0')

    print(f'supported: {Elmat().supported_licenses()}')
#__test_me()
