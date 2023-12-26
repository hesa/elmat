#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import RawTextHelpFormatter
import argparse
import json
import logging
import sys
from elmat import Elmat
from elmat.format import Formatter

def get_parser():

    parser = argparse.ArgumentParser(
        description="",
        epilog="",
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument('-of', '--output-format',
                        type=str,
                        help='Format for outoput',
                        default="JSON")

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='output verbose information',
                        default=False)

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='output debug information to stderr',
                        default=False)

    subparsers = parser.add_subparsers(help='Sub commands')


    # merge
    parser_m = subparsers.add_parser(
        'merge', help='Merge license with other')
    parser_m.set_defaults(which='merge', func=merge_licenses)
    parser_m.add_argument('--license-files', type=str, nargs='+', help='license files to merge')
    parser_m.add_argument('--exclude-osadl', action='store_true', dest='exclude_osadl', help='', default=False)
    parser_m.add_argument('--exclude-elmat', action='store_true', dest='exclude_elmat', help='', default=False)

    return parser

def merge_licenses(args, formatter):

    include_osadl = not args.exclude_osadl
    include_elmat = not args.exclude_elmat
    license_files = args.license_files
    
    elmat = Elmat()
    matrix = elmat.merge_licenses(license_files, include_osadl, include_elmat)
    formatted = formatter.format_matrix(matrix)
    return formatted
    


def main():

    args = get_parser().parse_args()
    formatter = Formatter.formatter(args.output_format)
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.func:
        try:
            ret = args.func(args, formatter)
            print(ret)
        except Exception as e:
            if args.verbose:
                import traceback
                print(traceback.format_exc())
        
if __name__ == '__main__':
    main()
