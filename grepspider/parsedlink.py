from urllib.parse import urlparse, ParseResult, urlunparse


class ParsedLink(object):

    def __init__(self, link: str):
        self._original = link
        self._scheme = None
        self._netloc = None
        self._path = None
        self._params = None
        self._query = None
        self._fragments = None
        self._parse(link)

    def is_same_domain(self, other_link: str):
        other = ParsedLink(other_link)
        return not bool(other.netloc) or self.domain_url == other.domain_url

    def format_link(self, in_link):
        out_parsed = ParsedLink(in_link)
        if out_parsed.netloc:
            if in_link.startswith('//'):
                out_parsed.scheme = self.scheme
                out_parsed.original = '{!s}:{!s}'.format(
                    self.scheme, out_parsed.original
                )
            return out_parsed
        out_parsed.scheme = self.scheme
        out_parsed.netloc = self.netloc
        if not in_link.startswith('/'):
            base_path = self.base_path(self.path)
            out_parsed.path = self.join_paths([base_path, out_parsed.path])
        out_parsed.query = self.query
        out_parsed._original = '{!s}{!s}'.format(
            out_parsed.domain_url,
            out_parsed.after_domain
        )
        return out_parsed

    @classmethod
    def base_path(cls, path):
        parts = path.split('/')
        return '/'.join(parts[:-1])

    @classmethod
    def join_paths(cls, parts):
        path = ''
        while parts:
            part = parts.pop(0)
            if part and part[0] != '/':
                part = '/{!s}'.format(part)
            path += part
        return path

    def _parse(self, url):
        parsed = urlparse(url)
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.path = parsed.path
        self.params = parsed.params
        self.query = parsed.query

    @property
    def domain_url(self):
        return '{!s}://{!s}'.format(self.scheme, self.netloc)

    @property
    def base_url(self):
        return '{!s}{!s}'.format(self.domain_url, self.path)

    @property
    def after_domain(self):
        if self.query:
            return '{!s}?{!s}'.format(self.path, self.query)
        return self.path

    @property
    def original(self):
        return self._original

    @property
    def scheme(self):
        return self._scheme

    @property
    def netloc(self):
        return self._netloc

    @property
    def path(self):
        return self._path

    @property
    def params(self):
        return self._params

    @property
    def query(self):
        return self._query

    @original.setter
    def original(self, value):
        self._original = value

    @scheme.setter
    def scheme(self, value):
        self._scheme = value

    @netloc.setter
    def netloc(self, value):
        self._netloc = value

    @path.setter
    def path(self, value):
        self._path = value

    @params.setter
    def params(self, value):
        self._params = value

    @query.setter
    def query(self, value):
        self._query = value
