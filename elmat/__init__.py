#!/bin/env python3

import osadl_matrix
from enum import Enum

class LicenseMatrix(Enum):
    YES = 'Yes'
    NO = 'No'
    UNKNOWN = 'Unknown'
    CHECKDEP = 'Check dependency'
    UNDEF = 'Undefined license'
                    
EXTENDED_LICENSES={
    'Proprietary-linked': {
        '0BSD': LicenseMatrix.YES,
        'AFL-2.0': LicenseMatrix.YES,
        'AFL-2.1': LicenseMatrix.YES,
        'AFL-3.0': LicenseMatrix.YES,
        'AGPL-3.0-only': LicenseMatrix.NO,
        'AGPL-3.0-or-later': LicenseMatrix.NO,
        'Apache-1.0': LicenseMatrix.YES,
        'Apache-1.1': LicenseMatrix.YES,
        'Apache-2.0': LicenseMatrix.YES,
        'Artistic-1.0': LicenseMatrix.YES,
        'Artistic-1.0-Perl': LicenseMatrix.YES,
        'Artistic-2.0': LicenseMatrix.YES,
        'blessing': LicenseMatrix.YES,
        'BSD-1-Clause': LicenseMatrix.YES,
        'BSD-2-Clause': LicenseMatrix.YES,
        'BSD-2-Clause-Patent': LicenseMatrix.YES,
        'BSD-3-Clause': LicenseMatrix.YES,
        'BSD-4-Clause': LicenseMatrix.YES,
        'BSD-4-Clause-UC': LicenseMatrix.YES,
        'BSD-Source-Code': LicenseMatrix.YES,
        'BSL-1.0': LicenseMatrix.YES,
        'bzip2-1.0.5': LicenseMatrix.YES,
        'bzip2-1.0.6': LicenseMatrix.YES,
        'CC0-1.0': LicenseMatrix.YES,
        'CDDL-1.0': LicenseMatrix.YES,
        'CDDL-1.1': LicenseMatrix.YES,
        'CPL-1.0': LicenseMatrix.NO,
        'curl': LicenseMatrix.YES,
        'EFL-2.0': LicenseMatrix.YES,
        'EPL-1.0': LicenseMatrix.NO,
        'EPL-2.0': LicenseMatrix.YES,
        'EUPL-1.1': LicenseMatrix.NO,
        'EUPL-1.2': LicenseMatrix.YES,
        'FSFAP': LicenseMatrix.YES,
        'FSFULLR': LicenseMatrix.YES,
        'FTL': LicenseMatrix.YES,
        'GPL-1.0-only': LicenseMatrix.NO,
        'GPL-1.0-or-later': LicenseMatrix.NO,
        'GPL-2.0-only': LicenseMatrix.NO,
        'GPL-2.0-only WITH Classpath-exception-2.0': LicenseMatrix.YES,
        'GPL-2.0-or-later': LicenseMatrix.NO,
        'GPL-3.0-only': LicenseMatrix.NO,
        'GPL-3.0-or-later': 'NO',
        'HPND': LicenseMatrix.YES,
        'IBM-pibs': LicenseMatrix.YES,
        'ICU': LicenseMatrix.YES,
        'IJG': LicenseMatrix.YES,
        'Info-ZIP': LicenseMatrix.YES,
        'IPL-1.0': LicenseMatrix.NO,
        'ISC': LicenseMatrix.YES,
        'LGPL-2.1-only': LicenseMatrix.YES,
        'LGPL-2.1-or-later': LicenseMatrix.YES,
        'LGPL-3.0-only': LicenseMatrix.YES,
        'LGPL-3.0-or-later': LicenseMatrix.YES,
        'Libpng': LicenseMatrix.YES,
        'libtiff': LicenseMatrix.YES,
        'MirOS': LicenseMatrix.YES,
        'MIT': LicenseMatrix.YES,
        'MIT-CMU': LicenseMatrix.YES,
        'MPL-1.1': LicenseMatrix.YES,
        'MPL-2.0': LicenseMatrix.YES,
        'MPL-2.0-no-copyleft-exception': LicenseMatrix.YES,
        'MS-PL': 'Unknown',
        'MS-RL': LicenseMatrix.NO,
        'NBPL-1.0': LicenseMatrix.YES,
        'NTP': LicenseMatrix.YES,
        'OpenSSL': LicenseMatrix.UNKNOWN,
        'OSL-3.0': LicenseMatrix.NO,
        'PHP-3.01': LicenseMatrix.YES,
        'PostgreSQL': LicenseMatrix.YES,
        'Python-2.0': LicenseMatrix.YES,
        'Qhull': LicenseMatrix.YES,
        'RSA-MD': LicenseMatrix.YES,
        'Sleepycat': LicenseMatrix.NO,
        'SunPro': LicenseMatrix.YES,
        'Unicode-DFS-2015': LicenseMatrix.YES,
        'Unicode-DFS-2016': LicenseMatrix.YES,
        'Unlicense': LicenseMatrix.YES,
        'UPL-1.0': LicenseMatrix.YES,
        'W3C': LicenseMatrix.YES,
        'W3C-19980720': LicenseMatrix.YES,
        'W3C-20150513': LicenseMatrix.YES,
        'WTFPL': LicenseMatrix.YES,
        'X11': LicenseMatrix.YES,
        'XFree86-1.1': LicenseMatrix.YES,
        'Zlib': LicenseMatrix.YES,
        'zlib-acknowledgement': LicenseMatrix.YES,
        'ZPL-2.0': LicenseMatrix.YES
    }
}

def is_compatible(outbound, inbound):
    compat=get_compatibility(outbound, inbound)
    return compat==LicenseMatrix.YES or compat==osadl_matrix.OSADLCompatibility.YES 

def get_compatibility(outbound, inbound):
    if outbound in EXTENDED_LICENSES:
        if outbound in osadl_matrix.supported_licenses():
            raise Exception(f'{outbound} found in both osadl_matrix as well as internally.')
        return EXTENDED_LICENSES[outbound].get(inbound, LicenseMatrix.UNDEF)
    
    return osadl_matrix.get_compatibility(outbound, inbound)

def supported_licenses():
    return osadl_matrix.supported_licenses() | EXTENDED_LICENSES.keys()

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
