"""A very small subset of the requests API used in this project."""
import http.cookiejar
import urllib.error
import urllib.parse
import urllib.request
from types import SimpleNamespace


class _CookieStore(dict):
    def set(self, key, value):
        if value is None:
            self.pop(key, None)
        else:
            self[key] = value

    def clear(self):
        super().clear()


class Response:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


class Session:
    def __init__(self):
        self.headers = {}
        self.cookies = _CookieStore()
        self._cookie_jar = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self._cookie_jar)
        )

    def request(self, method, url, data=None, timeout=None, allow_redirects=False, **_):
        request_data = None
        if data is not None:
            if isinstance(data, (dict, list, tuple)):
                request_data = urllib.parse.urlencode(data).encode()
            elif isinstance(data, str):
                request_data = data.encode()
            else:
                request_data = data
        if self.cookies:
            cookie_header = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
            self.headers.setdefault("Cookie", cookie_header)
        req = urllib.request.Request(url=url, data=request_data, headers=self.headers)
        with self._opener.open(req, timeout=timeout) as resp:
            return Response(resp.getcode(), resp.read())

    def get(self, url, **kwargs):
        return self.request("get", url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request("post", url, data=data, **kwargs)


class _DummyUrllib3:
    @staticmethod
    def disable_warnings():
        return None


class exceptions:
    Timeout = urllib.error.URLError
    ReadTimeout = urllib.error.URLError
    ConnectionError = urllib.error.URLError


packages = SimpleNamespace(urllib3=_DummyUrllib3())


def post(url, data=None, **kwargs):
    return Session().post(url, data=data, **kwargs)


def get(url, **kwargs):
    return Session().get(url, **kwargs)
