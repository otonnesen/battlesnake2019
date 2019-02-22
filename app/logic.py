import json
from copy import deepcopy
import datetime

import obj

def logic(data):
    '''
    Get current time
    while time_elapsed < 190ms
       do minimax
    return highest value move
    '''
    start = datetime.datetime.now()
    moves = {p:minimax(get_board_state(data, {data.you.id:p}), 2, data.you.id) for p in data.you.body[0].neighbors() if p.valid(data)}
    diff = datetime.datetime.now()-start
    print(diff.microseconds/1000)
    return data.you.body[0].direction_str(max(moves, key=moves.get))

def get_snake(data, snakeid):
    try:
        return {s.id:s for s in data.board.snakes}[snakeid]
    except KeyError:
        return None

def get_max_move(data, snakeid):
    snake = get_snake(data, snakeid)

def minimax(data, depth, snakeid):
    '''
    currently only accounting for myself
    '''
    if depth == 0:
        return get_board_value(data, snakeid)
    if snakeid == data.you.id:
        value = -float('inf')
        for i in [i for i in data.you.body[0].neighbors() if i.valid(data)]:
            value = max(value, minimax(get_board_state(data, {data.you.id:i}), depth-1, snakeid))
        return value
    else:
        # TODO
        pass


def get_board_state(data, moves):
    r = deepcopy(data)
    for snakeid, move in moves.items():
        snake = get_snake(r, snakeid)
        if snake == None:
            continue
        if not move.valid(r):
            r.board.snakes.remove(snake)
            continue
        snake.body.insert(0, move)
        food = False
        for f in r.board.food:
            if f == move:
                food = True
        if not food:
            snake.body.pop()
        if snakeid == data.you.id:
            if not food:
                r.you.body.pop()
            r.you.body.insert(0, move)

    return r

def get_board_value(data, snakeid):
    '''
    Things to take into account:
    *Free space
    Number of escape paths available
    Ratio of hunger:distance to food
    *Kill smaller snake?
    *Die to larger/same size snake?
    ______________________________
    *Probably do these first
    '''
    snake = get_snake(data, snakeid)
    return -float('inf') if snake == None else max([floodfill(data, i) for i in snake.body[0].neighbors()])

'''
return the number of spaces reachable from a given point
'''
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
