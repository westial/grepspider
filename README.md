grepspider
==========

Commandline spider script to crawl a full website and find the spoils you are 
looking for.

## Requirements ##

* python 3.6+

## Install ##

```
git clone https://github.com/westial/grepspider.git
cd grepspider/
pip3 install ./
```

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

## Combine with grep ##

Doing grep against the grepspider output it's the most powerful feature this
program can provide. Following, an example of use:

First, recursively crawl a website and all of its known subdomains:

```
grepspider --recursive \
    --output largewebsite-grepspider.log \
    https://www.largewebsite.dot \
    https://largewebsite.dot \
    https://sub.largewebsite.dot
```

If you want to monitor the session use `tail -f largewebsite-grepspider.log`, 
and also you can pipe the following commands to this tail command to instantly 
get the output as the program crawls the pages.

Grep command examples to use with the output:

* Broken links: `grep "## Broken Link " largewebsite-grepspider.log`
* HTTP 5XX errors: `grep "\- Status 5\-" largewebsite-grepspider.log`
* HTTP 4XX errors: `grep "\- Status 4\-" largewebsite-grepspider.log`
