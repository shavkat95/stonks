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
  
# print(data.keys())

slugs = ['bitcoin', 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba-inu', 'avalanche', 'tron', 'polkadot-new', 'bitcoin-cash', 'chainlink', 'near-protocol']



def get_ids(ids=[]):
  for slug in slugs:
    for dat in data['data']:
      if dat['slug']==slug:
        ids.append(dat['id'])
        break
  print('ids:')
  print(ids)
  print('slugs:')
  print(slugs)
  return slugs


    
ids = get_ids()

# print(data['data'][0])


  
  


# print(data['data'][1])



