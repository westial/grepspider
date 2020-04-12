from grepspider.config import REPORT_TYPE
from grepspider.exceptions import BrokenLink
from grepspider.grep import Grep
from grepspider.parsedlink import ParsedLink


class Spider(REPORT_TYPE):

    def crawl(self, *flags, spoil_pattern=None, spoil_context=0):
        """
        Recursively crawl all links, store links and spoils if required.
        :param flags: args
        :param spoil_context: int
        :param spoil_pattern: str
        :return: None|function
        """
        if not self._links:
            self.statistics()
            return
        link = self._pop_link()
        self._parsed_link = ParsedLink(link)
        crawler = Grep(
            self._parsed_link,
            *flags,
            spoil_pattern=self._build_spoil(spoil_pattern, spoil_context),
            headers=self._headers
        )
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

    @classmethod
    def _build_spoil(cls, spoil_pattern, spoil_context):
        if not spoil_context:
            return spoil_pattern
        else:
            context_fix = ".{{,{:d}}}".format(int(spoil_context / 2))
            return context_fix + spoil_pattern + context_fix
