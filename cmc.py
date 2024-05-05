 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import csv

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
#   'start':'1',
#   'limit':'5000',
#   'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'df851e8c-fbea-49ce-85ab-7b022c0b1cd1',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  # print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  
print(data.keys())

coins = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'XRP', 'Dogecoin', 'Toncoin', 'Cardano', 'Shiba Inu']

for dat in data['data']:
  print(dat['name'])


# print(data['data'][1])



