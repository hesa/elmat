# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from elmat import Elmat

__elmat = None

def __init():
    global __elmat
    if not __elmat:
        __elmat = Elmat()

def is_compatible(outbound, inbound):
    __init()
    return __elmat.is_compatible(outbound, inbound)

def get_compatibility(outbound, inbound):
    __init()
    return __elmat.get_compatibility(outbound, inbound)

def supported_licenses():
    __init()
    return __elmat.supported_licenses()

def elmat_licenses():
    __init()
    return __elmat.elmat_licenses()
