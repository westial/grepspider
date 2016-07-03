#!/usr/bin/env python3
"""
grepspider entry point
"""
import argparse

import re

import signal

import sys

from grepspider.spider import Spider

sys.setrecursionlimit(1000000)


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

arg_config = parser.parse_args()

links = arg_config.urls
spoil_pattern = arg_config.regex
recursive = arg_config.recursive
output_file = arg_config.output

regex_flags = list()

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

signal.signal(signal.SIGTERM, signal_term)
signal.signal(signal.SIGINT , signal_term)

spider = Spider(*links, recursive=recursive, output_file=output_file)
spider.crawl(*regex_flags, spoil_pattern=spoil_pattern)

# if __name__ == '__main__':
#     from grepspider.__main__ import run
#     run()