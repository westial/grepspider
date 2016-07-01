#!/usr/bin/env python
"""Unit test for Controller methods
"""
import sys
import unittest

import re

from grepspider.spider import Spider

sys.path.append('..')


class TestGrepSpider(unittest.TestCase):

    PAGES_ROOT_URL = 'http://localhost/grepspider/pages'

    def setUp(self):
        self.links = None
        self.spider = None
        pass

    def _crawl(self, provider, *flags, recursive=False):
        links = tuple(provider())
        regex_flags = flags
        spoil_pattern = 'title[^(?: is not a spoil)]'
        self.spider = Spider(*links, recursive=recursive)
        self.spider.crawl(
            *regex_flags,
            spoil_pattern=spoil_pattern
        )

    def test_recursive(self):
        self._crawl(self.provide_1_link_recursive, re.IGNORECASE, recursive=True)
        unique = 11
        broken = 1
        stored = 36
        spoil = 31
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_recursive_no_flags(self):
        self._crawl(self.provide_1_link_recursive, recursive=True)
        unique = 11
        broken = 1
        stored = 36
        spoil = 21
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_no_recursive_multiple(self):
        self._crawl(self.provide_2_links, re.IGNORECASE)
        unique = 7
        broken = 0
        stored = 13
        spoil = 7
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def _assert_counters(self, unique, broken, stored, spoil, external):
        self.assertEqual(
            len(self.spider._unique_links), unique, 'Local unique links'
        )
        self.assertEqual(
            self.spider._total_count_broken, broken, 'Local broken links'
        )
        self.assertEqual(
            self.spider._total_count_stored, stored, 'Links found'
        )
        self.assertEqual(
            self.spider._total_count_spoil, spoil, 'Spoils found'
        )
        self.assertEqual(
            self.spider._total_count_external, external, 'External links'
        )

    @classmethod
    def provide_1_link_wikipedia(cls):
        return ['https://donate.wikimedia.org']

    @classmethod
    def provide_2_links(cls):
        return ['{!s}/page10.html'.format(cls.PAGES_ROOT_URL), '{!s}/page1.html'.format(cls.PAGES_ROOT_URL)]

    @classmethod
    def provide_1_link_recursive(cls):
        return ['{!s}/page1.html'.format(cls.PAGES_ROOT_URL)]
