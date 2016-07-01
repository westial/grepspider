from grepspider.config import REPORT_TYPE
from grepspider.exceptions import BrokenLink
from grepspider.grep import Grep
from grepspider.parsedlink import ParsedLink


class Spider(REPORT_TYPE):

    def crawl(self, *flags, spoil_pattern=None):
        """
        Recursively crawl all links, store links and spoils if required.
        :param flags: args
        :param spoil_pattern: str
        :return: None|function
        """
        if not self._links:
            self.statistics()
            return
        link = self._pop_link()
        self._parsed_link = ParsedLink(link)
        crawler = Grep(self._parsed_link, *flags, spoil_pattern=spoil_pattern)
        try:
            crawler.run()
            self._update_links(crawler.links)
            self._update_spoils(crawler.spoils)
        except BrokenLink as exc:
            self._push_broken(exc)
        self.link_report()
        return self.crawl(
            *flags,
            spoil_pattern=spoil_pattern
        )
