import obj
import json

def logic(data):
    '''
    Get current time
    while time_elapsed < 190ms
       do minimax
    return highest value move
    '''
    print(data)
    moves = {p:floodfill(data, p) for p in data.you.body[0].neighbors()}
    return data.you.body[0].direction_str(max(moves, key=moves.get))

def get_snake(data, snakeid):
    return {s.id:s for s in data.board.snakes}[snakeid]

def get_max_move(data, snakeid):
    snake = get_snake(data, snakeid)



def get_board_value(data, snakeid):
    '''
    Things to take into account:
    *Free space
    Ratio of hunger:distance to food
    *Kill smaller snake?
    *Die to larger/same size snake?
    ______________________________
    *Probably do these first
    '''
    return 10

def floodfill(data, point):
    if not point.valid(data):
        return 0
    visited = set()
    visited.add(point)
    s = 1
    for i in point.neighbors():
        s += floodfillr(data, i, visited)
    return s

def floodfillr(data, point, visited):
    if point in visited or not point.valid(data):
        return 0
    visited.add(point)
    s = 1
    for i in point.neighbors():
        s += floodfillr(data, i, visited)
    return s

def foodratio(data, snakeid):
    snake = get_snake(data, snakeid)


def main():
    with open('../data/move.json') as move:
        data = obj.data(json.loads(move.read()))
        print(logic(data))

if __name__ == '__main__':
    main()
