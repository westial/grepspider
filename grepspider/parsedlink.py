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

    def absolute_link(self, relative):
        absolute = ParsedLink(relative)
        if absolute.netloc:
            return absolute
        absolute.scheme = self.scheme
        absolute.netloc = self.netloc
        if not relative.startswith('/'):
            base_path = self.base_path(self.path)
            absolute.path = self.join_paths([base_path, absolute.path])
        absolute.query = self.query
        absolute._original = '{!s}{!s}'.format(
            absolute.domain_url,
            absolute.after_domain
        )
        return absolute

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
