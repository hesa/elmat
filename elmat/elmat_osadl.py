# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from elmat import Elmat

__elmat = None

def __init():
    global __elmat
    if not __elmat:
        __elmat = Elmat()


def is_compatible(outbound, inbound, customdb=None):
    __init()
    return __elmat.is_compatible(outbound, inbound)

def get_compatibility(outbound, inbound, customdb=None):
    __init()
    return __elmat.get_compatibility(outbound, inbound)

def supported_licenses(customdb=None):
    __init()
    return __elmat.supported_licenses()
