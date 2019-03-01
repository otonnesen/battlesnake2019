import json
from datetime import datetime as dt

import obj
from filters import get_move

def logic(data):
    s = dt.now()
    move = get_move(data)
    s = dt.now()-s
    print(s.microseconds/1000)
    return data.you.head().direction_str(move)

def main():
    with open('../data/move.json') as move:
        data = obj.Data(json.loads(move.read()))
        print(logic(data))

if __name__ == '__main__':
    main()
