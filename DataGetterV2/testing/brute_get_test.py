import urllib2

i = 1
while True:
    urllib2.urlopen('http://finance.yahoo.com/quote/MSFT')
    print i
    i += 1
