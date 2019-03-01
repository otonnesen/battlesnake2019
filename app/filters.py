'''
Contains a bunch of filters -- denoted by a '_f' appended to the function
name -- and sorters -- denoted by a '_s' appended to the function name.
A filter attempts to remove any moves not satisfying a particular property.
A sorter rearranges the order of the moves (and should thus be applied last)
'''
import obj
import json
import sys
import functools
from datetime import datetime as dt

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
    pass

'''
Composes filters starting with moves
'''
def apply_filters(filters, data):
    return functools.reduce(lambda f,g: lambda x,y: f(x, g(x, y)), filters)(data, data.you.head().neighbors())

'''
Filters illegal moves
'''
def legal_f(data, moves):
    return list(filter(lambda x: x in data.metadata.safe, moves))

'''
Filters moves leading to spaces smaller than the size of your snake.
If no moves satisfy this property, retuns moves.
'''
def freespace_f(data, moves):
    s = {m:data.metadata.moves[m].free_space for m in moves}
    r = list(filter(lambda x: s[x] > len(data.you.body), s.keys()))
    return r if len(r) != 0 else moves

'''
Filters moves from which a tail is not reachable.
If no moves satisfy this property, retuns moves.
'''
def tail_f(data, moves):
    r = list(filter(lambda x: data.metadata.moves[x].tail, moves))
    return r if len(r) != 0 else moves

'''
Sorts moves by available free space in decreasing order.
'''
def freespace_s(data, moves):
    s = {m:data.metadata.moves[m].free_space for m in moves}
    return sorted(moves, key=lambda x: s[x], reverse=True)

'''
Filters moves from which no food is reachable.
If no moves satisy this property, returns moves.
'''
def food_f(data, moves):
    r = list(filter(lambda x: data.metadata.moves[x].close_food is not None, moves))
    return r if len(r) != 0 else moves
'''
Sorts moves by distance to food in increasing order.
'''
def food_s(data, moves):
    return sorted(moves, key=lambda x: dist_to_food(data, x))

def dist_to_food(data, move):
    assert move in data.metadata.moves
    food = data.metadata.moves[move].close_food
    return float('inf') if food is None else data.you.head().distance_to(food)

'''
Returns nearest integer to the ratio of your health to distance to food
'''
def foodratio(data, move):
    return data.you.health/dist_to_food(data, move)

'''
Warning: Using more than one sorting filter will obviously wipe
out the sorting done by all but the last (first in the list)
filter applied
'''

grow = [food_s, food_f, freespace_f, legal_f]

stagnate = [freespace_s, tail_f, legal_f]

def get_move(data):
    # TODO: Add logic to choose different sets of filters
    if min(foodratio(data, m) for m in data.metadata.moves) <= 2:
        return apply_filters(grow, data)[0]
    return apply_filters(stagnate, data)[0]

def main():
    with open('../data/move.json') as move:
        data = obj.Data(json.loads(move.read()))
        print(apply_filters(grow, data))

if __name__ == '__main__':
    main()
