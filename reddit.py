
from re import sub
import praw as praw
from multiprocessing import Process, Pipe


def mainRd(child_conn, sub):

    reddit = praw.Reddit(client_id='x8RjJFhFLvZcVMJbyKSN0A',
                         client_secret='7oyyggcIFYB1vhnpuwOVee3CoLk4IA',
                         username='Muted-Unit-1829',
                         password='m4a1m4a1',
                         user_agent='testapiV1')
    
    subs = reddit.subreddit(sub).subscribers
    hotpost = reddit.subreddit(sub).hot(limit=5)
    return_data = {"follower_count": "", "hotpost": [{}, {}, {}, {}, {}]}
    return_data['follower_count'] = subs
    for inx, x in enumerate(hotpost):
        return_data["hotpost"][inx]["title"] = x.title
        return_data["hotpost"][inx]["subreddit"] = str(x.subreddit)
        selftext = (x.selftext[:150] +
                    '..') if len(x.selftext) > 75 else x.selftext
        return_data["hotpost"][inx]["selftext"] = selftext
        return_data["hotpost"][inx]["url"] = x.url
        return_data["hotpost"][inx]["date"] = x.created_utc
        return_data["hotpost"][inx]["name"] = x.author
    child_conn.send(return_data)
    child_conn.close()
    # print(data)
