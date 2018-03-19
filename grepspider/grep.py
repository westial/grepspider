import re
import socket
import http.client

from grepspider.config import REQUEST_HEADERS
from grepspider.exceptions import BrokenLink
from grepspider.parsedlink import ParsedLink


class Grep(object):

    _LINK_PATTERN = '''(?:href=|src=|Location:)(?: +|["'])([^"'\r\n]+)'''

    def __init__(
            self,
            parsed_link: ParsedLink,
            *regex_flags,
            spoil_pattern=None,
            headers=None
    ):
        self._parsed_link = parsed_link
        self._spoil_pattern = spoil_pattern
        self._found_links = None
        self._found_spoils = None
        self._headers = REQUEST_HEADERS
        if headers:
            self._headers.update(headers)
        if regex_flags:
            self._regex_flags = self._merge_regex_flags(list(regex_flags))
        else:
            self._regex_flags = None

    def run(self):
        """
        Open page for the given link and find all links and all spoils if
        required. Store into the context variables.

        Return False on error of True on success.

        :return: bool
        """
        try:
            content = self._get_content()
        except (
                socket.gaierror,
                http.client.InvalidURL,
                http.client.HTTPException,
                Exception
        ) as exc:
            raise BrokenLink(exc, self._parsed_link.original)

        self._found_links = self._find_links(content)
        self._found_spoils = self._find_spoils(
            content,
            self._spoil_pattern,
            self._regex_flags
        )
        return True

    @property
    def links(self):
        """
        Return the found links.
        :return: None|list
        """
        return self._found_links

    @property
    def spoils(self):
        """
        Return the found spoils.
        :return: None|list
        """
        return self._found_spoils

    @classmethod
    def _merge_regex_flags(cls, regex_flags=None):
        if not regex_flags:
            return None
        result = regex_flags.pop(0)
        while regex_flags:
            result |= regex_flags.pop(0)
        return result

    def _get_content(self):
        if self._parsed_link.scheme == 'https':
            connector = http.client.HTTPSConnection
        else:
            connector = http.client.HTTPConnection
        connection = connector(self._parsed_link.netloc)
        connection.request(
            'GET',
            self._parsed_link.after_domain,
            headers=self._headers
        )
        response = connection.getresponse()
        status = int(response.status)
        if status >= 400:
            raise http.client.HTTPException('Status {:d}'.format(status))
        content = '{!s}\n{!s}'.format(response.msg, response.read())
        return content

    @classmethod
    def _find_links(cls, content):
        return re.findall(cls._LINK_PATTERN, content, re.I)

    @classmethod
    def _find_spoils(cls, content, spoil_pattern, regex_flags):
        if not spoil_pattern:
            return None
        if regex_flags:
            return re.findall(spoil_pattern, content, regex_flags)
        else:
            return re.findall(spoil_pattern, content)
