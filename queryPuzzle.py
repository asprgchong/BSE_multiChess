from chessdotcom import ChessDotComClient
import json

def getDaysPuzzle():
    client = ChessDotComClient(user_agent = "chess puzzler")
    r = client.get_current_daily_puzzle()
    response = json.loads(r.text)
    list = response['fen'].split(" ")[0].split("/")
    list.append(response['fen'].split(" ")[1:])
    return list

def getSolution():
    client = ChessDotComClient(user_agent = "chess puzzler")
    r = client.get_current_daily_puzzle()
    response = json.loads(r.text)
    list = response['pgn'].split("]\r\n\r\n")[1]
    return list