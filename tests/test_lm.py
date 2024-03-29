#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from elmat import elmat_osadl
import osadl_matrix

class TestIsCompatible(unittest.TestCase):

    def test_same(self):
        self.assertTrue(elmat_osadl.is_compatible('MIT','MIT'))
        self.assertTrue(elmat_osadl.is_compatible('GPL-2.0-or-later', 'GPL-2.0-or-later'))

    def test_mit_gpl2(self):
        self.assertFalse(elmat_osadl.is_compatible('MIT','GPL-2.0-or-later'))
        self.assertTrue(elmat_osadl.is_compatible('GPL-2.0-or-later', 'MIT'))

    def test_mit_prop(self):
        self.assertFalse(elmat_osadl.is_compatible('MIT','Proprietary-linked'))
        self.assertTrue(elmat_osadl.is_compatible('Proprietary-linked', 'MIT'))

    def test_prop_prop(self):
        self.assertTrue(elmat_osadl.is_compatible('Proprietary-linked','Proprietary-linked'))

class TestGetCompatibility(unittest.TestCase):

    def test_mit_gpl(self):
        self.assertEqual(elmat_osadl.get_compatibility('MIT','GPL-2.0-or-later'), 'No')
        self.assertEqual(elmat_osadl.get_compatibility('GPL-2.0-or-later', 'MIT'), 'Yes')
        self.assertEqual(elmat_osadl.get_compatibility('MIT','GPL-3.0-or-later'), 'No')
        self.assertEqual(elmat_osadl.get_compatibility('GPL-3.0-or-later', 'MIT'), 'Yes')
        self.assertEqual(elmat_osadl.get_compatibility('MIT','AGPL-3.0-or-later'), 'No')
        self.assertEqual(elmat_osadl.get_compatibility('AGPL-3.0-or-later', 'MIT'), 'Yes')

    def test_mit_lgpl(self):
        # The below might seem confusing (anyone can link to LGPL) but
        # the use case for OSADL's matrix is source code "mix"
        self.assertEqual(elmat_osadl.get_compatibility('MIT','LGPL-2.1-or-later'), 'No')
        self.assertEqual(elmat_osadl.get_compatibility('LGPL-2.1-or-later', 'MIT'), 'Yes')

    def test_mit_prop(self):
        self.assertEqual(elmat_osadl.get_compatibility('MIT','Proprietary-linked'), "Unknown")
        self.assertEqual(elmat_osadl.get_compatibility('Proprietary-linked', 'MIT'), 'Yes')

    def test_gpl_prop(self):
        self.assertEqual(elmat_osadl.get_compatibility('GPL-2.0-or-later','Proprietary-linked'), 'Unknown')
        self.assertEqual(elmat_osadl.get_compatibility('Proprietary-linked', 'GPL-2.0-or-later'), 'No')

        self.assertEqual(elmat_osadl.get_compatibility('GPL-3.0-or-later','Proprietary-linked'), 'Unknown')
        self.assertEqual(elmat_osadl.get_compatibility('Proprietary-linked', 'GPL-3.0-or-later'), 'No')

        self.assertEqual(elmat_osadl.get_compatibility('AGPL-3.0-or-later','Proprietary-linked'), 'Unknown')
        self.assertEqual(elmat_osadl.get_compatibility('Proprietary-linked', 'AGPL-3.0-or-later'), 'No')

class TestSupportedLicenses(unittest.TestCase):
    
    def test_supported_licenses(self):
        self.assertEqual(len(elmat_osadl.supported_licenses()) - len(osadl_matrix.supported_licenses()),1)

    def test_proprietary_linked(self):
        self.assertTrue('Proprietary-linked' in elmat_osadl.supported_licenses())
        self.assertFalse('Proprietary-linked' in osadl_matrix.supported_licenses())

    def test_proprietary_supports_osadl(self):
        for lic in osadl_matrix.supported_licenses():
            compat = elmat_osadl.get_compatibility('Proprietary-linked','GPL-2.0-or-later')
            self.assertTrue(compat == 'Yes' or compat == 'No')
