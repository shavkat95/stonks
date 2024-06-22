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

slugs = ['bitcoin', 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba-inu', 'avalanche', 'tron', 'polkadot-new', 'bitcoin-cash', 'chainlink', 'near-protocol', 
         'polygon', 'litecoin','unus-sed-leo', 'pepe', 'kaspa', 'ethereum-classic', 'aptos', 'monero', 'render', 'hedera', 'stellar', 'cosmos', 'mantle', 'arbitrum', 'okb', 'filecoin', 
         'cronos', 'stacks', 'immutable-x', 'maker', 'sui', 'vechain', 'the-graph']

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
    "polygon_volume_24h",
    "polygon_percent_change_1h",
    "polygon_percent_change_24h",
    "polygon_percent_change_7d",
    "polygon_percent_change_30d",
    "litecoin_volume_24h",
    "litecoin_percent_change_1h",
    "litecoin_percent_change_24h",
    "litecoin_percent_change_7d",
    "litecoin_percent_change_30d",
    "unus_sed_leo_volume_24h",
    "unus_sed_leo_percent_change_1h",
    "unus_sed_leo_percent_change_24h",
    "unus_sed_leo_percent_change_7d",
    "unus_sed_leo_percent_change_30d",
    "pepe_volume_24h",
    "pepe_percent_change_1h",
    "pepe_percent_change_24h",
    "pepe_percent_change_7d",
    "pepe_percent_change_30d",
    "kaspa_volume_24h",
    "kaspa_percent_change_1h",
    "kaspa_percent_change_24h",
    "kaspa_percent_change_7d",
    "kaspa_percent_change_30d",
    "ethereum_classic_volume_24h",
    "ethereum_classic_percent_change_1h",
    "ethereum_classic_percent_change_24h",
    "ethereum_classic_percent_change_7d",
    "ethereum_classic_percent_change_30d",
    "aptos_volume_24h",
    "aptos_percent_change_1h",
    "aptos_percent_change_24h",
    "aptos_percent_change_7d",
    "aptos_percent_change_30d",
    "monero_volume_24h",
    "monero_percent_change_1h",
    "monero_percent_change_24h",
    "monero_percent_change_7d",
    "monero_percent_change_30d",
    "render_volume_24h",
    "render_percent_change_1h",
    "render_percent_change_24h",
    "render_percent_change_7d",
    "render_percent_change_30d",
    "hedera_volume_24h",
    "hedera_percent_change_1h",
    "hedera_percent_change_24h",
    "hedera_percent_change_7d",
    "hedera_percent_change_30d",
    "stellar_volume_24h",
    "stellar_percent_change_1h",
    "stellar_percent_change_24h",
    "stellar_percent_change_7d",
    "stellar_percent_change_30d",
    "cosmos_volume_24h",
    "cosmos_percent_change_1h",
    "cosmos_percent_change_24h",
    "cosmos_percent_change_7d",
    "cosmos_percent_change_30d",
    "mantle_volume_24h",
    "mantle_percent_change_1h",
    "mantle_percent_change_24h",
    "mantle_percent_change_7d",
    "mantle_percent_change_30d",
    "arbitrum_volume_24h",
    "arbitrum_percent_change_1h",
    "arbitrum_percent_change_24h",
    "arbitrum_percent_change_7d",
    "arbitrum_percent_change_30d",
    "okb_volume_24h",
    "okb_percent_change_1h",
    "okb_percent_change_24h",
    "okb_percent_change_7d",
    "okb_percent_change_30d",
    "filecoin_volume_24h",
    "filecoin_percent_change_1h",
    "filecoin_percent_change_24h",
    "filecoin_percent_change_7d",
    "filecoin_percent_change_30d",
    "cronos_volume_24h",
    "cronos_percent_change_1h",
    "cronos_percent_change_24h",
    "cronos_percent_change_7d",
    "cronos_percent_change_30d",
    "stacks_volume_24h",
    "stacks_percent_change_1h",
    "stacks_percent_change_24h",
    "stacks_percent_change_7d",
    "stacks_percent_change_30d",
    "immutable_x_volume_24h",
    "immutable_x_percent_change_1h",
    "immutable_x_percent_change_24h",
    "immutable_x_percent_change_7d",
    "immutable_x_percent_change_30d",
    "maker_volume_24h",
    "maker_percent_change_1h",
    "maker_percent_change_24h",
    "maker_percent_change_7d",
    "maker_percent_change_30d",
    "sui_volume_24h",
    "sui_percent_change_1h",
    "sui_percent_change_24h",
    "sui_percent_change_7d",
    "sui_percent_change_30d",
    "vechain_volume_24h",
    "vechain_percent_change_1h",
    "vechain_percent_change_24h",
    "vechain_percent_change_7d",
    "vechain_percent_change_30d",
    "the_graph_volume_24h",
    "the_graph_percent_change_1h",
    "the_graph_percent_change_24h",
    "the_graph_percent_change_7d",
    "the_graph_percent_change_30d",
]



def print_metrics():
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
          print(str(slug.replace('-', '_'))+"_"+str(interval))
        mc = float(dat['quote']["USD"]["market_cap"])
        output[str(slug.replace('-', '_'))+"_volume_24h"] = output[str(slug.replace('-', '_'))+"_volume_24h"]/mc
        break
      
  return output

print_metrics()
  
def print_slugs():
    #request
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  for dat in data['data']:
    print(dat['slug'])


# print_slugs()

# ids = get_ids()