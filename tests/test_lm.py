# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from elmat import elmat_osadl
import osadl_matrix

class TestIsCompatible(unittest.TestCase):

    def test_same(self):
        self.assertTrue(elmat_osadl.is_compatible('MIT', 'MIT'))
        self.assertTrue(elmat_osadl.is_compatible('GPL-2.0-or-later', 'GPL-2.0-or-later'))

    def test_mit_gpl2(self):
        self.assertFalse(elmat_osadl.is_compatible('MIT', 'GPL-2.0-or-later'))
        self.assertTrue(elmat_osadl.is_compatible('GPL-2.0-or-later', 'MIT'))

    def test_mit_prop(self):
        self.assertFalse(elmat_osadl.is_compatible('MIT', 'Proprietary-linked'))
        self.assertTrue(elmat_osadl.is_compatible('Proprietary-linked', 'MIT'))

    def test_infozip_prop(self):
        self.assertFalse(elmat_osadl.is_compatible('LicenseRef-scancode-info-zip-2003-05', 'Proprietary-linked'))
        self.assertTrue(elmat_osadl.is_compatible('Proprietary-linked', 'LicenseRef-scancode-info-zip-2003-05'))

    def test_ppp_prop(self):
        self.assertFalse(elmat_osadl.is_compatible('LicenseRef-scancode-ppp', 'Proprietary-linked'))
        self.assertTrue(elmat_osadl.is_compatible('Proprietary-linked', 'LicenseRef-scancode-ppp'))

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

    def test_nr_licenses(self):
        osadl_licenses = osadl_matrix.supported_licenses()
        elmat_licenses = elmat_osadl.elmat_licenses()
        # for each license in elmat
        for elmat_lic_key in elmat_licenses:
            elmat_license = elmat_licenses[elmat_lic_key]
            # and for for each license in osadl
            for osadl_lic in osadl_licenses:
                #print(f'Check {osadl_lic} in {elmat_license}')
                # make sure the osadl key is present in elmat 
                self.assertTrue(osadl_lic in elmat_license)
            self.assertEqual(len(elmat_license), len(osadl_matrix.supported_licenses()))

    def test_proprietary_linked(self):
        self.assertTrue('Proprietary-linked' in elmat_osadl.supported_licenses())
        self.assertFalse('Proprietary-linked' in osadl_matrix.supported_licenses())

    def test_proprietary_supports_osadl(self):
        for lic in osadl_matrix.supported_licenses():
            compat = elmat_osadl.get_compatibility('Proprietary-linked','GPL-2.0-or-later')
            self.assertTrue(compat == 'Yes' or compat == 'No')
