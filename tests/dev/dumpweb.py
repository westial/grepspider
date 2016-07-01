import http.client

conn = http.client.HTTPSConnection("donate.wikimedia.org")
conn.request('GET', '/w/index.php?title=Special:FundraiserLandingPage&country=XX&uselang=en&utm_medium=spontaneous&utm_source=fr-redir&utm_campaign=spontaneous')
r = conn.getresponse()
print(r.msg)
print(r.read())
