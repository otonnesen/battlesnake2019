import obj
import json
import sys
import functools

def get_board_value(board, snakeid):
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
    snake = board.get_snake(snakeid)
    if snake == None: # Snake is dead
        return -float('inf')
    return max([floodfill(board, i, snake.id, True) for i in snake.body[0].neighbors()])

'''
Composes filters starting with moves
'''
def apply_filters(filters, data):
    compose = lambda f,g: lambda x: f(data, g(data, x))
    return functools.reduce(compose, filters)(data.metadata.moves)

'''
Filters illegal moves
'''
def legal_f(data, moves):
    return list(filter(lambda x: x in data.metadata.safe, moves))

'''
Filters moves leading to spaces smaller than the size of your snake.
If no moves satisfy this property, retuns a list sorted in decreasing
order of avaiable space it leads to.
'''
def floodfill_f(data, moves):
    s = {m:data.metadata.moves[m].free_space for m in moves}
    r = list(filter(lambda x: s[x] > len(data.you.body), s.keys()))
    return r if len(r) != 0 else sorted(moves, key=lambda x: s[x], reverse=True)

'''
Filters moves from which a tail is not reachable.
If no moves satisfy this property, retuns moves.
'''
def tail_f(data, moves):
    r = list(filter(lambda x: data.metadata.moves[x].tail, moves))
    return moves


def foodratio(data, snakeid):
    snake = data.board.get_snake(snakeid)

grow = [floodfill_f, legal_f]

stagnate = [tail_f, legal_f]

def get_move(data):
    # TODO: Add logic to choose different sets of filters
    return apply_filters(stagnate, data)[0]

def main():
    with open('../data/move.json') as move:
        data = obj.Data(json.loads(move.read()))
        print(apply_filters(stagnate, data))
        # print(data.metadata.moves[list(data.metadata.moves.keys())[2]])

if __name__ == '__main__':
    main()
