#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

import elmat
import osadl_matrix

class TestIsCompatible(unittest.TestCase):

    def test_mit_gpl2(self):
        self.assertFalse(elmat.is_compatible('MIT','GPL-2.0-or-later'))
        self.assertTrue(elmat.is_compatible('GPL-2.0-or-later', 'MIT'))

    def test_mit_prop(self):
        self.assertFalse(elmat.is_compatible('MIT','Proprietary-linked'))
        self.assertTrue(elmat.is_compatible('Proprietary-linked', 'MIT'))

class TestGetCompatibility(unittest.TestCase):

    def test_mit_gpl2(self):
        self.assertEqual(elmat.get_compatibility('MIT','GPL-2.0-or-later'), osadl_matrix.OSADLCompatibility.NO)
        self.assertEqual(elmat.get_compatibility('GPL-2.0-or-later', 'MIT'), osadl_matrix.OSADLCompatibility.YES)

    def test_mit_prop(self):
        self.assertEqual(elmat.get_compatibility('MIT','Proprietary-linked'), osadl_matrix.OSADLCompatibility.UNDEF)
        self.assertEqual(elmat.get_compatibility('Proprietary-linked', 'MIT'), osadl_matrix.OSADLCompatibility.YES)

class TestSupportedLicenses(unittest.TestCase):
    
    def test_supported_licenses(self):
        self.assertEqual(len(elmat.supported_licenses()) - len(osadl_matrix.supported_licenses()),1)

    def test_proprietary_linked(self):
        self.assertTrue('Proprietary-linked' in elmat.supported_licenses())
        self.assertFalse('Proprietary-linked' in osadl_matrix.supported_licenses())

    def test_proprietary_supports_osadl(self):
        for lic in osadl_matrix.supported_licenses():
            compat = elmat.get_compatibility('Proprietary-linked','GPL-2.0-or-later')
            self.assertTrue(compat == osadl_matrix.OSADLCompatibility.YES or compat == osadl_matrix.OSADLCompatibility.NO)


