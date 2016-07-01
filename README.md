```                                     _     _           
                                       (_)   | |          
          __ _ _ __ ___ _ __  ___ _ __  _  __| | ___ _ __ 
         / _` | '__/ _ \ '_ \/ __| '_ \| |/ _` |/ _ \ '__|
        | (_| | | |  __/ |_) \__ \ |_) | | (_| |  __/ |   
         \__, |_|  \___| .__/|___/ .__/|_|\__,_|\___|_|   
          __/ |        | |       | |                      
         |___/         |_|       |_|                      
 
usage: grepspider [-h] [-e REGEX] [-r] [-i] [-a] [-l] [-m] [-d]
                  urls [urls ...]

Recursive web crawler with regular expression search engine.

positional arguments:
  urls                  Page url to crawl.

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