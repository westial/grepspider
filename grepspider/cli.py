#!/usr/bin/env python3
"""
grepspider entry point
"""
import argparse
import json

import re

import signal

import sys

from grepspider.spider import Spider

sys.setrecursionlimit(1000000)


def parse_headers(raw_headers):
    parsed_headers = dict()
    while raw_headers:
        raw_header = raw_headers.pop(0)
        header_name, header_value = raw_header.split(":")
        header_value = header_value.strip()
        parsed_headers.update({header_name: header_value})
    return parsed_headers


def signal_term(signum, frame):
    global spider
    spider.print_out('\n--- Caught SIGTERM; Attempting to quit gracefully ---')
    spider.statistics()
    del spider
    exit(130)


parser = argparse.ArgumentParser(
    description='Recursive web crawler with regular expression content filter.'
)

parser.add_argument(
    'urls',
    nargs='+',
    type=str,
    help='Page url to crawl.'
)

parser.add_argument(
    '-e',
    '--regex',
    type=str,
    required=False,
    help='User with permission on server'
)

parser.add_argument(
    '-o',
    '--output',
    type=str,
    required=False,
    help='Writes output to this file'
)

parser.add_argument(
    '-r',
    '--recursive',
    action='store_true',
    help='Follow links'
)

parser.add_argument(
    '-i',
    '--ignorecase',
    action='store_true',
    help='Regular expression flag IGNORECASE'
)

parser.add_argument(
    '-a',
    '--ascii',
    action='store_true',
    help='Regular expression flag ASCII'
)

parser.add_argument(
    '-l',
    '--locale',
    action='store_true',
    help='Regular expression flag LOCALE'
)

parser.add_argument(
    '-m',
    '--multiline',
    action='store_true',
    help='Regular expression flag MULTILINE'
)

parser.add_argument(
    '-d',
    '--dotall',
    action='store_true',
    help='Regular expression flag DOTALL'
)

parser.add_argument(
    '-H',
    '--headers',
    nargs='+',
    type=str,
    help='CURL-like header parameter headers list, for example "Accept: application/json"'
)

arg_config = parser.parse_args()

links = arg_config.urls
spoil_pattern = arg_config.regex
recursive = arg_config.recursive
output_file = arg_config.output

regex_flags = list()
headers = None

if arg_config.ignorecase:
    regex_flags.append(re.IGNORECASE)

if arg_config.ascii:
    regex_flags.append(re.ASCII)

if arg_config.locale:
    regex_flags.append(re.LOCALE)

if arg_config.multiline:
    regex_flags.append(re.MULTILINE)

if arg_config.dotall:
    regex_flags.append(re.DOTALL)

if arg_config.headers:
    headers = parse_headers(arg_config.headers)

signal.signal(signal.SIGTERM, signal_term)
signal.signal(signal.SIGINT , signal_term)

spider = Spider(
    *links,
    recursive=recursive,
    output_file=output_file,
    headers=headers
)
spider.crawl(*regex_flags, spoil_pattern=spoil_pattern)