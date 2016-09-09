import requests
from lxml import html

#storing response
response = requests.get('http://finance.yahoo.com/quote/MSFT')

#print response.text.split('\n')

formatted_string = response.text.encode('utf8')

with open("../test_data/msft_list.htm", "w") as text_file:
    text_file.write(formatted_string)
