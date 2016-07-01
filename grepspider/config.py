"""General configuration parameters"""
from grepspider.reports import MarkDownReport

REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              '*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; '
                  '+http://www.google.com/bot.html)',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

# Report class type. Custom Report implementations are full supported.
# See the module reports.py for more information.
REPORT_TYPE = MarkDownReport
