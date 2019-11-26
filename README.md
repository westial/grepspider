```
$ grepspider --help
usage: grepspider [-h] [-e REGEX] [-o OUTPUT] [-r] [-i] [-a] [-l] [-m] [-d]
                  [-H HEADERS [HEADERS ...]]
                  urls [urls ...]

Recursive web crawler with regular expression content filter.

positional arguments:
  urls                  Page url to crawl.

optional arguments:
  -h, --help            show this help message and exit
  -e REGEX, --regex REGEX
                        User with permission on server
  -o OUTPUT, --output OUTPUT
                        Writes output to this file
  -r, --recursive       Follow links
  -i, --ignorecase      Regular expression flag IGNORECASE
  -a, --ascii           Regular expression flag ASCII
  -l, --locale          Regular expression flag LOCALE
  -m, --multiline       Regular expression flag MULTILINE
  -d, --dotall          Regular expression flag DOTALL
  -H HEADERS [HEADERS ...], --headers HEADERS [HEADERS ...]
                        CURL-like header parameter headers list, for example
                        "Accept: application/json"

```
