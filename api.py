#from api.coinmarketcap import CoinMarketCapAPIError, Response
import csv
from coinmarketcapapi import CoinMarketCapAPIError, Response
from flask import Flask, jsonify
from flask_cors import CORS
from multiprocessing import Process, Pipe
from coinmarketcap import main
from reddit import mainRd
from twitter import mainTw
from getDetail import Detail
from getOverview import Overview
from getToCompare import toCompare



# กด Run แล้วเข้า path http://127.0.0.1:5000/getdata/(ชื่อเหรียญ) เพื่อดูตัวอย่างข้อมูล


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/*": {'origins': "*"}})


@app.route('/', methods=['GET'])
def hello():
    return ("Hello world")



@app.route('/getOverview', methods=['GET'])
def getOverview():
    parent_conn, child_conn = Pipe()
    p = Process(target=Overview, args=(child_conn,))
    p.start()
    recieve = parent_conn.recv()
    if type(recieve) != Response:
        return(recieve)
    else:
        return recieve.status,400

@app.route('/getDetail/<coin_name>', methods=['GET'])
def getDetail(coin_name):
    returnData = {"info": {}, "comment": {"twitter": {}, "reddit": {}}}
    parent_conn, child_conn = Pipe()
    p = Process(target=Detail, args=(child_conn,coin_name))
    p.start()
    recieve = parent_conn.recv()
    if type(recieve) != Response:
        returnData["info"] = recieve
        if (returnData["info"]["twitter"] != ""):
            twitter = returnData["info"]["twitter"]
            t = Process(target=mainTw, args=(child_conn, twitter))
            t.start()
            returnData["comment"]["twitter"] = parent_conn.recv()
        if (returnData["info"]["reddit"] != ""):
            reddit = returnData["info"]["reddit"]
            r = Process(target=mainRd, args=(child_conn, reddit))
            r.start()
            returnData["comment"]["reddit"] = parent_conn.recv()
        return(returnData)
    else:
        return recieve.status,400

@app.route('/getToCompare/<coin_name>', methods=['GET'])
def getToCompare(coin_name):
    parent_conn, child_conn = Pipe()
    p = Process(target=toCompare, args=(child_conn,coin_name))
    p.start()
    recieve = parent_conn.recv()
    if type(recieve) != Response:
        return(recieve)
    else:
        return recieve.status,400

if __name__ == "__main__":
    app.run(debug=True)
