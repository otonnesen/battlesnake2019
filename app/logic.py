import json
from copy import deepcopy

import obj
from heuristic import get_board_value

def logic(data):
    '''
    Get current time
    while time_elapsed < 190ms
       do minimax
    return highest value move
    '''
    moves = {p:minimax(get_state(data, {data.you.id:p}), 2, data.you.id) for p in data.you.body[0].neighbors() if p.valid(data.board)}
    return data.you.body[0].direction_str(max(moves, key=moves.get))

def get_max_move(data, snakeid):
    snake = data.get_snake(snakeid)

def minimax(data, depth, snakeid):
    '''
    currently only accounting for myself
    '''
    if depth == 0:
        return get_board_value(data.board, snakeid)
    if snakeid == data.you.id:
        value = -float('inf')
        for i in data.you.body[0].neighbors():
            if i.valid(data.board):
                value = max(value, minimax(get_state(data, {data.you.id:i}), depth-1, snakeid))
        return value
    else:
        # TODO
        pass

def get_state(data, moves):
    r = deepcopy(data)
    for snakeid, move in moves.items():
        snake = r.board.get_snake(snakeid)
        if snake == None:
            continue
        if not move.valid(r.board):
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

def main():
    with open('../data/move.json') as move:
        data = obj.data(json.loads(move.read()))
        print(logic(data))

if __name__ == '__main__':
    main()
