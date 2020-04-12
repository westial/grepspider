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
usage: grepspider [-h] [-e REGEX] [-C CONTEXT] [-o OUTPUT] [-r] [-i] [-a] [-l]
                  [-m] [-d] [-H HEADERS [HEADERS ...]]
                  urls [urls ...]

Recursive web crawler with regular expression content filter.

positional arguments:
  urls                  Page url to crawl.

optional arguments:
  -h, --help            show this help message and exit
  -e REGEX, --regex REGEX
                        Regular expression to capture spoils
  -C CONTEXT, --context CONTEXT
                        Capture the number of characters before and after the
                        spoil so you can see the context of every spoil in the
                        output
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
grepspider --context 50 \
    --regex "lorem ipsum" \
    --ignorecase \
    --recursive \
    --output largewebsite-gs.log \
    https://www.largewebsite.dot \
    https://largewebsite.dot \
    https://sub.largewebsite.dot
```

If you want to monitor the session use `tail -f largewebsite-gs.log`, 
and also you can pipe the following commands to this tail command to instantly 
get the output as the program crawls the pages.

Grep command examples to use from the output to check HTTP issues:

* Broken links: `grep "## Broken Link " largewebsite-gs.log`
* HTTP 5XX errors: `grep "\- Status 5\-" largewebsite-gs.log`
* HTTP 4XX errors: `grep "\- Status 4\-" largewebsite-gs.log`

Grep command examples to get count and enumerate spoil and link results by page:

* Spoil count and first 3: `grep -A4 "## Found Spoils" largewebsite-gs.log`
* External links and first 4: `grep -A5 "## External Links" largewebsite-gs.log`
* Total links and first 6: `grep -A7 "## Found Links" largewebsite-gs.log`
