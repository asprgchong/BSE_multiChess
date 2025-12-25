from chessdotcom import ChessDotComClient
import board
import json

def getDaysPuzzle(board):
    client = ChessDotComClient(user_agent = "chess puzzler")
    r = client.get_current_daily_puzzle()
    response = json.loads(r.text)
    
    return response['fen']

