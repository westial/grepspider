# -*- coding: utf-8 -*-
"""Super client class"""
from abc import ABCMeta, abstractmethod

from grepspider.exceptions import BrokenLink


class Report:

    __metaclass__ = ABCMeta

    def __init__(self, *link, recursive=False):
        self._recursive = recursive
        self._links = list(link)
        self._unique_links = set(self._links)
        self._parsed_link = None
        self._stored_links = list()
        self._stored_broken_links = list()
        self._stored_spoils = list()
        self._stored_ext_links = set()

        self._total_count_broken = 0

        self._total_count_stored = 0
        self._total_count_external = 0
        self._total_count_spoil = 0

        self._count_stored = 0
        self._count_external = 0
        self._count_spoil = 0

    def reset_statistics(self):
        """
        Add an individual link statistics to the total ones and reset the
        individual statistics for the next link.
        """
        self._total_count_stored += self._count_stored
        self._total_count_external += self._count_external
        self._total_count_spoil += self._count_spoil

        self._count_stored = 0
        self._count_external = 0
        self._count_spoil = 0

    def _update_links(self, found_links):
        if not found_links:
            return
        new_link = found_links.pop(0)
        self._push_found_link(new_link)
        parsed_new_link = self._parsed_link.absolute_link(new_link)
        new_link = parsed_new_link.original
        if not self._parsed_link.is_same_domain(new_link):
            self._push_external(new_link)
        elif new_link not in self._unique_links:
            self._push_link(new_link)
        return self._update_links(found_links)

    def _update_spoils(self, found_spoils):
        if not found_spoils:
            return
        self._count_spoil += len(found_spoils)
        self._stored_spoils += found_spoils

    def _push_found_link(self, found_link):
        self._count_stored += 1
        self._stored_links.append(found_link)

    def _push_link(self, link):
        self._count_stored += 1
        self._unique_links.add(link)
        if self._recursive:
            self._links.append(link)

    def _push_broken(self, exc: BrokenLink):
        self._total_count_broken += 1
        self._stored_broken_links.append((exc.error, exc.link))

    def _push_external(self, link):
        self._count_external += 1
        self._stored_ext_links.add(link)

    def _pop_link(self):
        link = self._links.pop(0)
        return link

    @abstractmethod
    def link_report(self):
        """
        Full report for the current link
        """
        pass

    @abstractmethod
    def statistics(self):
        """
        Statistics report
        """

    @abstractmethod
    def found_links_out(self):
        """
        Report for all active links found into link's page
        :return:
        """

    @abstractmethod
    def spoils_out(self):
        """
        Report for all spoils found into link's page
        """

    @abstractmethod
    def broken_links_out(self):
        """
        Report for all broken links found into link's page
        """

    @abstractmethod
    def ext_links_out(self):
        """
        Report for all external links found into link's page
        """


class MarkDownReport(Report):
    """
    MarkDown-like standard output report implementation.
    """

    def statistics(self):
        print('\n## Total Statistics ##\n')
        print('* Local unique links     {:d}'.format(len(self._unique_links)))
        print('* Local broken links     {:d}'.format(self._total_count_broken))
        print('* Links found            {:d}'.format(self._total_count_stored))
        print('* Spoils found           {:d}'.format(self._total_count_spoil))
        print('* External links         {:d}'.format(self._total_count_external))

    def link_report(self):
        if self._stored_broken_links:
            print(
                '\n## [!] Broken Link ({!s}) ##\n'.format(self._parsed_link.original)
            )
            self.broken_links_out()
            return

        print('## [v] Report for ({!s}) ##'.format(self._parsed_link.original))
        if self._stored_links:
            print(
                '\n### Found Links ({:d}) ###\n'.format(
                    self._count_stored
                )
            )
            self.found_links_out()
        if self._stored_spoils:
            print(
                '\n### Found Spoils ({:d}) ###\n'.format(self._count_spoil)
            )
            self.spoils_out()
        if self._stored_ext_links:
            print(
                '\n### External Links ({:d}) ###\n'.format(self._count_external)
            )
            self.ext_links_out()
        print()
        self.reset_statistics()

    def found_links_out(self):
        if not self._stored_links:
            return
        print('# {!s}'.format(self._stored_links.pop(0)))
        return self.found_links_out()

    def spoils_out(self):
        if not self._stored_spoils:
            return
        print('# {!s}'.format(self._stored_spoils.pop(0)))
        return self.spoils_out()

    def broken_links_out(self):
        if not self._stored_broken_links:
            return
        error, link = self._stored_broken_links.pop(0)
        print('# {!s} - {!s}'.format(error, link))
        return self.broken_links_out()

    def ext_links_out(self):
        if not self._stored_ext_links:
            return
        print('* {!s}'.format(self._stored_ext_links.pop()))
        return self.ext_links_out()
