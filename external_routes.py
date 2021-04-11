import requests
from secrets import client_id


def search_board_games(data={}):
    url = 'https://api.boardgameatlas.com/api/search?'
    data['client_id'] = client_id
    print(data, flush=True)
    response = requests.get(url, params=data).json()
    return response['games']
