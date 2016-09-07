import requests
from lxml import html

#storing response
response = requests.get('http://finance.yahoo.com/quote/MMM')

#print response.text.split('\n')

formatted_string = response.text.encode('utf8')

with open("../test_data/mmm_list.html", "w") as text_file:
    text_file.write(formatted_string)
