#!/bin/env python3

import osadl_matrix
from enum import Enum
import json
import os


elmat_version = "0.0.1"
emlat_name = "emlat"


TOP_DIR=os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")
VAR_DIR=os.path.join(TOP_DIR, "var")
LICENSES_FILE=os.path.join(VAR_DIR, "elmat.json")

license_data=None
EXTENDED_LICENSES=None

def is_compatible(outbound, inbound):
    compat=get_compatibility(outbound, inbound)
    print("compat: " + str(compat))
    return compat==osadl_matrix.OSADLCompatibility.YES or compat=="Yes"

def get_compatibility(outbound, inbound):
    global EXTENDED_LICENSES
    if not license_data:
        __read_license_file()
    if outbound in EXTENDED_LICENSES:
        if outbound in osadl_matrix.supported_licenses():
            raise Exception(f'{outbound} found in both osadl_matrix as well as internally.')

        try:
            value = __text_to_enum(EXTENDED_LICENSES[outbound].get(inbound))
            return value
        except:
            pass
    
    return osadl_matrix.get_compatibility(outbound, inbound)

def supported_licenses():
    return osadl_matrix.supported_licenses() | EXTENDED_LICENSES.keys()

def __read_license_file():
    global EXTENDED_LICENSES
    with open(LICENSES_FILE) as fp:
        all_license_data=json.load(fp)
        EXTENDED_LICENSES=all_license_data['extended_licenses']

def __text_to_enum(value_str):
    return osadl_matrix.OSADLCompatibility.from_text(value_str)

def __test_me_sub(inbound, outbound):
    print(f'{inbound} ---> {outbound} ===> {get_compatibility(inbound, outbound)}')
    print(f'    ===> {is_compatible(inbound, outbound)}')
    print(f'{outbound} ---> {inbound} ===> {get_compatibility(outbound, inbound)}')
    print(f'    ===> {is_compatible(outbound, inbound)}')
    print('')
    
def __test_me():
    __test_me_sub('MIT', 'X11')
    __test_me_sub('MIT', 'GPL-2.0-or-later')
    __test_me_sub('Proprietary-linked', 'MIT')
    __test_me_sub('Proprietary-linked', 'GPL-2.0-or-later')
    __test_me_sub('Proprietary-linked', 'LGPL-3.0-or-later')
    __test_me_sub('Proprietary-linked', 'GPL-3.0-or-later')
    __test_me_sub('Proprietary-linked', 'OpenSSL')

    print(f'supported: {supported_licenses()}')
__test_me()
