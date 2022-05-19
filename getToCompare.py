from tracemalloc import start
from coinmarketcapapi  import CoinMarketCapAPI, CoinMarketCapAPIError
from multiprocessing import Process, Pipe
import requests




def toCompare(child_conn,get_search):
    cmc = CoinMarketCapAPI('130a1d81-7986-45b9-ad32-372d7b0ce73b')
    search = get_search
    params = {
            'start': 1,
            'limit': 500,
            'sort': 'market_cap',
            'CMC_PRO_API_KEY': '130a1d81-7986-45b9-ad32-372d7b0ce73b'
        }
    r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', params=params)
    all = r.json()
    try :
            r = cmc.cryptocurrency_info(symbol=search)
            data = r.data[search]
            filtered_data = {}
            filtered_data["symbol"] = data["symbol"]
            filtered_data["src"] = data["logo"]
            getPrice = cmc.tools_priceconversion(amount=1, convert="USD", symbol=search)
            filtered_data["price"]= round(getPrice.data["quote"]["USD"]["price"],5)
            for i in range(len(all)):
                if search == all["data"][i]["name"]:
                    filtered_data["volume"] = all["data"][i]["volume_24h"],
                    filtered_data["cap"] = all["data"][i]["quote"]["USD"]["market_cap"]
                    filtered_data["totalSupply"] = all["data"][i]["total_supply"]
                    filtered_data["maxSupply"] = all["data"][i]["max_supply"]
    except CoinMarketCapAPIError as e:
            filtered_data = e
    
    
    child_conn.send(filtered_data)
    child_conn.close()
    
    # print(data)
    # for i in data:
    # print(i+" : "+str(data[i]))

    
    #priceTHB = getPrice.data["quote"]["THB"]["price"]
    #priceTHB = ("1 %s = %f THB" % (search, priceTHB))
