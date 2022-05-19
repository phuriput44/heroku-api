from tracemalloc import start
from coinmarketcapapi  import CoinMarketCapAPI, CoinMarketCapAPIError
from multiprocessing import Process, Pipe
import requests




def Overview(child_conn):
    cmc = CoinMarketCapAPI('130a1d81-7986-45b9-ad32-372d7b0ce73b')
    coin_list = ["AXS","ILV","ATLAS","SPS","TLM"]
    sentiment_list = [3.2,4,3,3.7,3]
    params = {
            'start': 1,
            'limit': 500,
            'sort': 'market_cap',
            'CMC_PRO_API_KEY': '130a1d81-7986-45b9-ad32-372d7b0ce73b'
        }
    r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', params=params)
    all = r.json()
    output_list = {}
    for search in coin_list:
        try :
            r = cmc.cryptocurrency_info(symbol=search)
            data = r.data[search]
            filtered_data = {}
            filtered_data["name"] = data["name"]
            filtered_data["symbol"] = data["symbol"]
            filtered_data["src"] = data["logo"]
            for i in range(len(all)):
                if search == all["data"][i]["name"]:
                    filtered_data["volume"] = all["data"][i]["volume_24h"],
                    filtered_data["cap"] = all["data"][i]["quote"]["USD"]["market_cap"]
            filtered_data["score"] = sentiment_list[coin_list.index(search)]

        except CoinMarketCapAPIError as e:
            filtered_data = e
        output_list[search] = filtered_data
    
    
    child_conn.send(output_list)
    child_conn.close()
    
    # print(data)
    # for i in data:
    # print(i+" : "+str(data[i]))

    
    #priceTHB = getPrice.data["quote"]["THB"]["price"]
    #priceTHB = ("1 %s = %f THB" % (search, priceTHB))
