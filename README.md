<!--
SPDX-FileCopyrightText: 2024 Henrik Sandklef <hesa@sandklef.com>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# elmat (El Mat) - Extension to License Matrix

This project provides:

* Compatibility for proprietary license called `Proprietary-linked`

* Python API

* Command line program

# Compatibility for proprietary license

This can be used in combination with Further information [OSADL's License Checklist](https://www.osadl.org/Access-to-raw-data.oss-compliance-raw-data-access.0.html) and more specifically to extend the license matrix with a propprietary license.

## Extending flict

[flict](https://github.com/vinland-technology/flict) can be extend with support for the proprietary license. This is done in two steps:

* create a new license matrix file (using elmat)

* use the new matrix file to flict

###  Create a new license matrix file

Assuming we want to call the new matrix file `extended-matrix.json`

```
$ elmat merge > extended-matrix.json
```

### Use the new matrix file to flict

use the new matrix file `extended-matrix.json` as input to flict  to verify if elmat's proprietary license, `Proprietary-linked`, can be used as outbound for the inbound license "MIT OR BSD-3-Clause".

```
$ flict --license-matrix-file extended-matrix.json -of text verify -il MIT OR BSD-3-Clause -ol Proprietary-linked
```

# Python API

See [Python API](PYTHON_API.md).

# Command line program

The command line program can do four things:

* merge licenses

* list supported licenses

* verify an outbound license with an inbound license

* get compatibility for an outbound #license with an inbound license

* extend elmat with your own licenses

# Merge licenses

To merge and output [osadl_matrix](https://github.com/priv-kweihmann/osadl-matrix) with elmat's license:

```
$ elmat merge 
```

# List supported licenses

```
$ elmat list
```

# Verify an outbound license with an inbound license

Elmat can verify a single outbound license with a single inbound license. As an example elmat can check if the inbound license "BSD-3-Clause" be used by the outbound license "Proprietary-linked" and vice versa.

Example:

```
$ elmat verify -il BSD-3-Clause -ol Proprietary-linked
true
$ elmat verify -il Proprietary-linked -ol BSD-3-Clause
false
```

*Note: If you need support for complex license expressions (e.g. `MIT OR BSD-3-Clause`), check out [flict](https://github.com/vinland-technology/flict)*

# Get compatibility for an outbound license with an inbound license

If you want a more detailed answer, then from `verify`, you can get the actual compatibility status with the `compatibility` command.

Example:

```
$ elmat/__main__.py compatibility -il BSD-3-Clause -ol Proprietary-linked
"Yes"
$ elmat/__main__.py compatibility -il Proprietary-linked -ol BSD-3-Clause
"Unknown"
```
*Note: If you need support for complex license expressions (e.g. `MIT OR BSD-3-Clause`), check out [flict](https://github.com/vinland-technology/flict)*

# Extend elmat with your own licenses

This can be done in combination with the commands above using the option `--license-file`. Let's assume you have a file, called `foobar-license.json`, defining the compatiblity for the license `FooBar` that you would like to extend elmat with.

Example without extending elmat with your license file:
```
$ elmat/__main__.py -of text compatibility -il BSD-3-Clause -ol FooBar
Outbound license "FooBar" not supported.
```

Example when extending elmat with your license file:

```
$ elmat --license-file foobar-license.json -of text compatibility -il BSD-3-Clause -ol FooBar
Yes
$ elmat --license-file foobar-license.json -of text compatibility -il Apache-2.0 -ol FooBar
No
$ elmat --license-file foobar-license.json -of text compatibility -il BSD-2-Clause -ol FooBar
Unknown
```
*Note: read more about the format for extending the elmat in [Extending Elmat](EXTENDING_ELMAT.md).

License definitions used in the example above (`foobar-license.json`):
```
{
    "extended_licenses": {
	"FooBar": {
	    "BSD-3-Clause": "Yes",
	    "Apache-2.0": "No"
	}
    }
}
```



# Related projects

* [flict](https://github.com/vinland-technology/flict) - License Compatibility Tool

* [FOSS Licenses](https://github.com/hesa/foss-licenses) - A database with meta data for FOSS licenses adding useful information to existing licenses aiming at simplifying compliance work.

* [Open Source License Checklists](https://www.osadl.org/OSADL-Open-Source-License-Checklists.oss-compliance-lists.0.html) - Open Source License Obligations Checklists

* [osadl_matrix](https://github.com/priv-kweihmann/osadl-matrix) - Python API on top of OSADL license compatibility matrix

* [ScanCode LicenseDB](https://scancode-licensedb.aboutcode.org/) - LicenseDB is likely the largest collection of software licenses available on earth and may be beyond.


