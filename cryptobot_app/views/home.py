from django.shortcuts import render
import requests
import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging

def mapTrandingCrypto(coin):
    return {
      'name': coin['name'],
      'cmc_rank': coin['cmc_rank'],
      'symbol': coin['symbol'],
      'market_cap': coin['quote']['USD']['market_cap'],
      'percent_change_1h': coin['quote']['USD']['percent_change_1h'],
      'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
      'percent_change_7d': coin['quote']['USD']['percent_change_7d'],
      'price': coin['quote']['USD']['price'],
      'volume_24h': coin['quote']['USD']['volume_24h'],
      'volume_change_24h': coin['quote']['USD']['volume_change_24h']
    }

def get_history_price(market, interval):
    history_price_url = 'https://api.binance.com/api/v3/klines?symbol='+market+'USDT'+'&interval='+interval

    try:
        response = requests.get(history_price_url)
        response.raise_for_status()
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None  # Or you can return an error message or fallback data


def get_trending_list():
    v1_api = 'https://pro-api.coinmarketcap.com/v1'
    API_KEY = '2fcc3835-95d4-4dab-8554-959978205c1e'
    trending_crypto_url = v1_api + '/cryptocurrency/listings/latest'
    
    headers = {
      'X-CMC_PRO_API_KEY': API_KEY
    }

    params = {
      'market_cap_min': '300000000',
      'sort': 'percent_change_24h',
      'sort_dir': 'desc'
    }

    try:
        response = requests.get(trending_crypto_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return list(map(mapTrandingCrypto, data['data']))
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None  # Or you can return an error message or fallback data


def home_view(request):
    trending_list = get_trending_list()
    history_price_list = {}
    topTen = 10
    interval = '5m'
    for market in trending_list[:topTen]:
      history_price_list[market['symbol']] = get_history_price(market['symbol'], interval)

    # print("history_price_list :",history_price_list)
    trending_crypto_data = get_trending_list()
    # trending_crypto_data = [
      # {
      #         "name": "Rollbit Coin",
      #         "cmc_rank": 263,
      #         "symbol": "RLB",
      #         "market_cap": 159741854.98851687,
      #         "percent_change_1h": 2.99131063,
      #         "percent_change_24h": 0.44823264,
      #         "percent_change_7d": 5.90666433,
      #         "price": 0.06704097125295011,
      #         "volume_24h": 607703.90051317,
      #         "volume_change_24h": -47.9445
      #     },
      #     {
      #         "name": "FLEX",
      #         "cmc_rank": 215,
      #         "symbol": "FLEX",
      #         "market_cap": 325611719.6660673,
      #         "percent_change_1h": 0.00523404,
      #         "percent_change_24h": 0.05625899,
      #         "percent_change_7d": 0.12723189,
      #         "price": 3.3001765770086267,
      #         "volume_24h": 0,
      #         "volume_change_24h": 0
      #     },
      #     {
      #         "name": "TNC Coin",
      #         "cmc_rank": 8063,
      #         "symbol": "TNC",
      #         "market_cap": 0,
      #         "percent_change_1h": 0.00523404,
      #         "percent_change_24h": 0.05625899,
      #         "percent_change_7d": -0.54514599,
      #         "price": 0.0002879154050062981,
      #         "volume_24h": 2.00539311,
      #         "volume_change_24h": 0.0481
      #     },
      #     {
      #         "name": "USDD",
      #         "cmc_rank": 83,
      #         "symbol": "USDD",
      #         "market_cap": 753894737.7581522,
      #         "percent_change_1h": -0.02382449,
      #         "percent_change_24h": 0.05333451,
      #         "percent_change_7d": 0.16678268,
      #         "price": 0.9993671665999839,
      #         "volume_24h": 1732247.14060945,
      #         "volume_change_24h": -25.0732
      #     },
      #     {
      #         "name": "TrueUSD",
      #         "cmc_rank": 123,
      #         "symbol": "TUSD",
      #         "market_cap": 494093835.6986197,
      #         "percent_change_1h": -0.00828564,
      #         "percent_change_24h": 0.05288108,
      #         "percent_change_7d": 0.10005979,
      #         "price": 0.996957804301782,
      #         "volume_24h": 41364389.71967246,
      #         "volume_change_24h": -40.3933
      #     },
      #     {
      #         "name": "Dai",
      #         "cmc_rank": 19,
      #         "symbol": "DAI",
      #         "market_cap": 5365429083.7183275,
      #         "percent_change_1h": 0.00430635,
      #         "percent_change_24h": 0.01816331,
      #         "percent_change_7d": 0.02635994,
      #         "price": 1.0000086445004999,
      #         "volume_24h": 70591317.07885687,
      #         "volume_change_24h": -36.0976
      #     },
      #     {
      #         "name": "UNUS SED LEO",
      #         "cmc_rank": 17,
      #         "symbol": "LEO",
      #         "market_cap": 5600433516.048052,
      #         "percent_change_1h": -0.0220618,
      #         "percent_change_24h": -0.00534591,
      #         "percent_change_7d": 0.85822088,
      #         "price": 6.054105465212805,
      #         "volume_24h": 14297525.50207484,
      #         "volume_change_24h": 5.224
      #     },
      #     {
      #         "name": "USDJ",
      #         "cmc_rank": 285,
      #         "symbol": "USDJ",
      #         "market_cap": 146532962.24382463,
      #         "percent_change_1h": 0.35195412,
      #         "percent_change_24h": -0.00792107,
      #         "percent_change_7d": -0.06166798,
      #         "price": 1.1329820635590817,
      #         "volume_24h": 220148.91617105,
      #         "volume_change_24h": -6.6834
      #     },
      #     {
      #         "name": "Tether USDt",
      #         "cmc_rank": 3,
      #         "symbol": "USDT",
      #         "market_cap": 120541559516.44017,
      #         "percent_change_1h": -0.00333996,
      #         "percent_change_24h": -0.00957489,
      #         "percent_change_7d": 0.08947961,
      #         "price": 0.9997118721626824,
      #         "volume_24h": 54532845682.83297,
      #         "volume_change_24h": -27.342
      #     },
      #     {
      #         "name": "Frax",
      #         "cmc_rank": 206,
      #         "symbol": "FRAX",
      #         "market_cap": 647119786.74292,
      #         "percent_change_1h": -0.00892753,
      #         "percent_change_24h": -0.01604488,
      #         "percent_change_7d": -0.04440695,
      #         "price": 0.9964374310174914,
      #         "volume_24h": 3884990.18654719,
      #         "volume_change_24h": -68.7382
      #     }
      #   ]

    llm_result = ""
    # Send history_price_list to ChatpGpt and analize
    # Get the result and show in llm_result
    # Show result and create selection to choose which coin will be executed
    return render(request, 'home.html', {
      'trending_crypto': trending_crypto_data[:topTen],
      'history_price': history_price_list,
      'result': llm_result
    }) 