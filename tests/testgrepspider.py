#!/usr/bin/env python
"""Unit test for Controller methods

Run a docker nginx server from the samples folder:
```
cd tests/samples
docker run -p 8000:80 -v $(pwd):/usr/share/nginx/html nginx
```
"""
import sys
import unittest

import re

from grepspider.spider import Spider

sys.path.append('..')


class TestGrepSpider(unittest.TestCase):

    PAGES_ROOT_URL = 'http://localhost:8000/pages'

    def setUp(self):
        self.links = None
        self.spider = None
        pass

    def _crawl(self, provider, *flags, recursive=False):
        self._crawl_by_spoil(
            provider,
            'title[^(?: is not a spoil)]',
            *flags,
            recursive=recursive
        )

    def _crawl_by_spoil(
            self,
            provider,
            spoil_pattern,
            *flags,
            recursive=False,
            spoil_context=0
    ):
        links = tuple(provider())
        regex_flags = flags
        self.spider = Spider(*links, recursive=recursive)
        self.spider.crawl(
            *regex_flags,
            spoil_pattern=spoil_pattern,
            spoil_context=spoil_context
        )

    def test_recursive(self):
        self._crawl(self.provide_1_link_recursive, re.IGNORECASE, recursive=True)
        unique = 13
        broken = 1
        stored = 30
        spoil = 37
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_recursive_no_flags(self):
        self._crawl(self.provide_1_link_recursive, recursive=True)
        unique = 13
        broken = 1
        stored = 30
        spoil = 25
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_mailto_link_issue(self):
        """
        @see https://github.com/westial/grepspider/issues/1
        """
        self._crawl(self.provide_mailto_link, recursive=True)
        unique = 1
        broken = 0
        stored = 0
        spoil = 2
        external = 0
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_clear_spoil(self):
        self._crawl_by_spoil(
            self.provide_clear_spoil_link,
            "lorem ipsum",
            re.IGNORECASE,
            recursive=False,
            spoil_context=100
        )
        unique = 29
        broken = 0
        stored = 94
        spoil = 23
        external = 61
        self._assert_counters(unique, broken, stored, spoil, external)

    def test_no_recursive_multiple(self):
        self._crawl(self.provide_2_links, re.IGNORECASE)
        unique = 8
        broken = 0
        stored = 9
        spoil = 7
        external = 2
        self._assert_counters(unique, broken, stored, spoil, external)

    def _assert_counters(self, unique, broken, stored, spoil, external):
        self.assertEqual(
            unique, len(self.spider._unique_links), 'Local unique links'
        )
        self.assertEqual(
            broken, self.spider._total_count_broken, 'Local broken links'
        )
        self.assertEqual(
            stored, self.spider._total_count_stored, 'Links found'
        )
        self.assertEqual(
            spoil, self.spider._total_count_spoil, 'Spoils found'
        )
        self.assertEqual(
            external, self.spider._total_count_external, 'External links'
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

    @classmethod
    def provide_mailto_link(cls):
        return ['{!s}/page_mailto.html'.format(cls.PAGES_ROOT_URL)]

    @classmethod
    def provide_clear_spoil_link(cls):
        return ['{!s}/loremipsum.html'.format(cls.PAGES_ROOT_URL)]
