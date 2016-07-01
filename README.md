```
Recursive web crawler with regular expression search engine. Python 3 only.

usage: grepspider [-h] [-e REGEX] [-r] [-i] [-a] [-l] [-m] [-d]
                  urls [urls ...]

positional arguments:
  urls                  Page urls list to crawl.

optional arguments:
  -h, --help            show this help message and exit
  -e REGEX, --regex REGEX
                        User with permission on server
  -r, --recursive       Follow links
  -i, --ignorecase      Regular expression flag IGNORECASE
  -a, --ascii           Regular expression flag ASCII
  -l, --locale          Regular expression flag LOCALE
  -m, --multiline       Regular expression flag MULTILINE
  -d, --dotall          Regular expression flag DOTALL
```
