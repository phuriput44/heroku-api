from coinmarketcapapi  import CoinMarketCapAPI, CoinMarketCapAPIError
from multiprocessing import Process, Pipe



def Detail(child_conn, get_search):
    cmc = CoinMarketCapAPI('130a1d81-7986-45b9-ad32-372d7b0ce73b')
    coin_list = ["AXS","ILV","ATLAS","SPS","TLM"]
    sentiment_list = [3.2,4,3,3.7,3]
    search = get_search
    try :
        r = cmc.cryptocurrency_info(symbol=search)
        data = r.data[search]
        filtered_data = {}
        if data["twitter_username"] is not None:
                filtered_data["twitter"] = data["twitter_username"]
        else:
                filtered_data["twitter"] = ""
        if data["twitter_username"] is not None:
                filtered_data["reddit"] = data["subreddit"]
        else:
                filtered_data["reddit"] = ""    
        filtered_data["name"] = data["name"]
        filtered_data["symbol"] = data["symbol"]
        filtered_data["src"] = data["logo"]
        filtered_data["urls"] = data["urls"]
        filtered_data["date_added"] = data["date_added"]
        filtered_data["score"] = sentiment_list[coin_list.index(search)]
        filtered_data["status_sentiment"] = "Neutral" if filtered_data["score"] == 3 else "positive" if filtered_data["score"] > 3 else "Negative"

    except CoinMarketCapAPIError as e:
        r = e.rep
        filtered_data = r
    
    
    child_conn.send(filtered_data)
    child_conn.close()