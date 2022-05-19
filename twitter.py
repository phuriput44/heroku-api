import tweepy
import sys
import csv
from multiprocessing import Process, Pipe


def mainTw(child_conn, twt_name):
    consumer_key = "Ge1Knvav47fKzAlVKZOsTciBf"
    consumer_secret = "DB0kVFP7SEXatfjxzuF5oU6L6KBoONBeU5dbj7qWb5CgxLT1p7"
    access_token = "884608372825137152-1GHCjPPI7SuBTQN9jcMwM89bDRTT3hq"
    access_token_secret = "L8UKwlvPekNtPXTRA3WY5dhusoj9jNaGlDSimKSq8qOpd"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    twitter = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAN0SUgEAAAAApXywqASai39qKqXYDc2AuxwowAQ"
                            "%3Dlt6VRpzAXKnq01cSTSBL2y55PILUMQNHiyBuIbohsXDOYp7fmf")
    if not api:
        print("Authentication failed!")
        sys.exit(-1)

    
    return_data = {"follower_count": "", "tweet": [{}, {}, {}, {}, {}]}
    follower_count = int(twitter.get_user(username=twt_name, user_fields=[
                         "public_metrics"]).data.public_metrics['followers_count'])
    
    return_data["follower_count"] = (f'{follower_count:,}')
    search_results = api.user_timeline(screen_name = twt_name,count=5)

    for i in range(len(search_results)):
        return_data["tweet"][i]["name"] = search_results[i].user.screen_name
        return_data["tweet"][i]["text"] = search_results[i].text
        return_data["tweet"][i]["created_at"] = str(search_results[i].created_at)
    if return_data["tweet"][0] == {}:
        return_data["tweet"] = None
    
    child_conn.send(return_data)
    child_conn.close()

