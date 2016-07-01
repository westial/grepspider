from http.client import HTTPException


class BrokenLink(HTTPException):

    def __init__(self, origin_exc, link):
        self._error = str(origin_exc)
        self._link = link

    @property
    def error(self):
        return self._error

    @property
    def link(self):
        return self._link
