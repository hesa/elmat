#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from elmat import elmat_osadl
import osadl_matrix

class TestNrLicenses(unittest.TestCase):
    
    def test_supported_licenses(self):
        el = set(elmat_osadl.supported_licenses())
        ol = set(osadl_matrix.supported_licenses())

        # Proprietary linked is available in ELMAT only, so diff is 1
        self.assertEqual(len(elmat_osadl.supported_licenses()) - len(osadl_matrix.supported_licenses()),1)
        self.assertTrue(len([x for x in el if x not in ol]) == 1)
        
        # All OSAL should exist in elmat
        self.assertTrue(len([x for x in ol if x not in el]) == 0)

