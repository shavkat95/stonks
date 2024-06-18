 #This example uses Python 2.7 and the python-request library.

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
#   'start':'1',
#   'limit':'5000',
#   'convert':'USD' #,AUD,EUR,CHF,JPY,NOK,SEK,SGD,GBP,CAD
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'df851e8c-fbea-49ce-85ab-7b022c0b1cd1',
}

session = Session()
session.headers.update(headers)
  
# print(data.keys())

 # need get more
slugs = ['bitcoin', 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba-inu', 'avalanche', 'tron', 'polkadot-new', 'bitcoin-cash', 'chainlink', 'near-protocol'] # need get more

metrics = [
    "bitcoin_volume_24h",
    "bitcoin_percent_change_1h",
    "bitcoin_percent_change_24h",
    "bitcoin_percent_change_7d",
    "bitcoin_percent_change_30d",
    "ethereum_volume_24h",
    "ethereum_percent_change_1h",
    "ethereum_percent_change_24h",
    "ethereum_percent_change_7d",
    "ethereum_percent_change_30d",
    "bnb_volume_24h",
    "bnb_percent_change_1h",
    "bnb_percent_change_24h",
    "bnb_percent_change_7d",
    "bnb_percent_change_30d",
    "solana_volume_24h",
    "solana_percent_change_1h",
    "solana_percent_change_24h",
    "solana_percent_change_7d",
    "solana_percent_change_30d",
    "xrp_volume_24h",
    "xrp_percent_change_1h",
    "xrp_percent_change_24h",
    "xrp_percent_change_7d",
    "xrp_percent_change_30d",
    "dogecoin_volume_24h",
    "dogecoin_percent_change_1h",
    "dogecoin_percent_change_24h",
    "dogecoin_percent_change_7d",
    "dogecoin_percent_change_30d",
    "toncoin_volume_24h",
    "toncoin_percent_change_1h",
    "toncoin_percent_change_24h",
    "toncoin_percent_change_7d",
    "toncoin_percent_change_30d",
    "cardano_volume_24h",
    "cardano_percent_change_1h",
    "cardano_percent_change_24h",
    "cardano_percent_change_7d",
    "cardano_percent_change_30d",
    "shiba_inu_volume_24h",
    "shiba_inu_percent_change_1h",
    "shiba_inu_percent_change_24h",
    "shiba_inu_percent_change_7d",
    "shiba_inu_percent_change_30d",
    "avalanche_volume_24h",
    "avalanche_percent_change_1h",
    "avalanche_percent_change_24h",
    "avalanche_percent_change_7d",
    "avalanche_percent_change_30d",
    "tron_volume_24h",
    "tron_percent_change_1h",
    "tron_percent_change_24h",
    "tron_percent_change_7d",
    "tron_percent_change_30d",
    "polkadot_new_volume_24h",
    "polkadot_new_percent_change_1h",
    "polkadot_new_percent_change_24h",
    "polkadot_new_percent_change_7d",
    "polkadot_new_percent_change_30d",
    "bitcoin_cash_volume_24h",
    "bitcoin_cash_percent_change_1h",
    "bitcoin_cash_percent_change_24h",
    "bitcoin_cash_percent_change_7d",
    "bitcoin_cash_percent_change_30d",
    "chainlink_volume_24h",
    "chainlink_percent_change_1h",
    "chainlink_percent_change_24h",
    "chainlink_percent_change_7d",
    "chainlink_percent_change_30d",
    "near_protocol_volume_24h",
    "near_protocol_percent_change_1h",
    "near_protocol_percent_change_24h",
    "near_protocol_percent_change_7d",
    "near_protocol_percent_change_30d",
]


def get_metrics():
  # returns dict with values to each metric
  output = {}
  
  #request
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  
  #logic
  for slug in slugs:
    for dat in data['data']:
      if dat['slug']==slug:
        for interval in ["volume_24h", "percent_change_1h", "percent_change_24h", "percent_change_7d", "percent_change_30d"]:
          output[str(slug.replace('-', '_'))+"_"+str(interval)] = float(dat['quote']["USD"][interval])
        mc = float(dat['quote']["USD"]["market_cap"])
        output[str(slug.replace('-', '_'))+"_volume_24h"] = output[str(slug.replace('-', '_'))+"_volume_24h"]/mc
        break
      
  return output

# print(get_metrics())









def get_ids(data):
  ids=[]
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
  
# ids = get_ids()