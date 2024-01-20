#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import RawTextHelpFormatter
import argparse
import logging
import sys
import traceback

import elmat.config
from elmat import Elmat
from elmat import ElmatException
from elmat import ElmatReturnCodes
from elmat.format import Formatter

def get_parser():

    parser = argparse.ArgumentParser(
        description="",
        epilog="",
        formatter_class=RawTextHelpFormatter,
    )
    parser.set_defaults(func=None)

    parser.add_argument('-of', '--output-format',
                        type=str,
                        help='Format for outoput',
                        default="JSON")

    parser.add_argument('--exclude-osadl', '-eo', action='store_true', dest='exclude_osadl', help='Exclude the licenses as found in the OSADL license matrix.', default=False)

    parser.add_argument('--exclude-elmat', '-ee', action='store_true', dest='exclude_elmat', help='Exclude the licenses as found in the Elmat license file.', default=False)

    parser.add_argument('--license-file', '-lf', dest='license_files', type=str, nargs='+', help='license files to merge')

    parser.add_argument('-V', '--version',
                        action='version',
                        version=elmat.config.SW_VERSION)

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='output verbose information',
                        default=False)

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='output debug information to stderr',
                        default=False)

    subparsers = parser.add_subparsers(help='Sub commands')

    # list
    parser_l = subparsers.add_parser(
        'list', help='List licenses')
    parser_l.set_defaults(which='list', func=list_licenses)

    # merge
    parser_m = subparsers.add_parser(
        'merge', help='Merge license and output result')
    parser_m.set_defaults(which='merge', func=merge_licenses)

    # verify
    parser_v = subparsers.add_parser(
        'verify', help='Verify if inbound license and an outbound license are compatible (true/false)')
    parser_v.set_defaults(which='merge', func=verify)
    parser_v.add_argument('--inbound-license', '-il', type=str, dest='inbound_license', help='', default=False)
    parser_v.add_argument('--outbound-license', '-ol', type=str, dest='outbound_license', help='', default=False)

    # compatibility
    parser_c = subparsers.add_parser(
        'compatibility', help='Get the compatiblity status between an inbound license and an outbound license')
    parser_c.set_defaults(which='compatiblity', func=compatibility)
    parser_c.add_argument('--inbound-license', '-il', type=str, dest='inbound_license', help='', default=False)
    parser_c.add_argument('--outbound-license', '-ol', type=str, dest='outbound_license', help='', default=False)

    return parser

def __get_elmat(args):
    include_osadl = not args.exclude_osadl
    include_elmat = not args.exclude_elmat
    license_files = args.license_files

    elmat = Elmat(license_files, include_osadl, include_elmat)
    return elmat

def compatibility(args, formatter):
    elmat = __get_elmat(args)

    inbound = args.inbound_license
    outbound = args.outbound_license
    if outbound not in elmat.supported_licenses():
        raise ElmatException(ElmatReturnCodes.ELMAT_LICENSE_UNKNOWN, f'Outbound license "{outbound}" not supported.')
    if inbound not in elmat.supported_licenses():
        raise ElmatException(ElmatReturnCodes.ELMAT_LICENSE_UNKNOWN, f'Inbound license "{inbound}" not supported.')

    ret = elmat.get_compatibility(outbound, inbound)
    formatted = formatter.format_compatiblity(ret)
    return formatted

def verify(args, formatter):
    elmat = __get_elmat(args)

    inbound = args.inbound_license
    outbound = args.outbound_license
    if outbound not in elmat.supported_licenses():
        raise ElmatException(ElmatReturnCodes.ELMAT_LICENSE_UNKNOWN, f'Outbound license "{outbound}" not supported.')
    if inbound not in elmat.supported_licenses():
        raise ElmatException(ElmatReturnCodes.ELMAT_LICENSE_UNKNOWN, f'Inbound license "{inbound}" not supported.')

    ret = elmat.is_compatible(outbound, inbound)
    formatted = formatter.format_verification(ret)
    return formatted


def list_licenses(args, formatter):
    elmat = __get_elmat(args)
    matrix = elmat.supported_licenses()
    formatted = formatter.format_licenses(matrix)
    return formatted

def merge_licenses(args, formatter):
    elmat = __get_elmat(args)
    matrix = elmat.matrix()
    formatted = formatter.format_matrix(matrix)
    return formatted

def main():

    parser = get_parser()
    args = parser.parse_args()
    formatter = Formatter.formatter(args.output_format)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.func:
        try:
            ret = args.func(args, formatter)
            print(ret)
        except ElmatException as e:
            print(formatter.format_exception(e))
            sys.exit(e.error_code())
        except Exception as e:
            logging.debug(f'exception caught: {e}')
            if args.verbose:
                print(traceback.format_exc())
    else:
        parser.print_help(sys.stderr)


if __name__ == '__main__':
    main()
