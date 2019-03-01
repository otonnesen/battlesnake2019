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
Filters move which __may__ contain a snake of equal
or greater length's head next turn.
'''
def head_f(data, moves):
    head_moves = sum([s.head().neighbors() for s in data.board.snakes\
            if s.id != data.you.id and len(s.body) >= len(data.you.body)], [])
    r = list(filter(lambda x: x not in head_moves, moves))
    # TODO: Probably doesn't hurt to do a quick lookahead here to see
    # if any spots are gonna open up in the next few turns
    if len(r) == 0:
        head_moves = sum([s.head().neighbors() for s in data.board.snakes if\
                s.id != data.you.id and len(s.body) > len(data.you.body)], [])
        r = list(filter(lambda x: x not in head_moves, moves))
    return r if len(r) != 0 else moves

'''
Filters moves which contain food.
If no moves satisy this property, returns moves.
'''
def avoidfood_f(data, moves):
    r = list(filter(lambda x: x not in data.metadata.food, moves))
    return r if len(r) != 0 else moves

'''
Filters moves from which no food is reachable.
If no moves satisy this property, returns moves.
'''
def food_f(data, moves):
    r = list(filter(lambda x: data.metadata.moves[x].close_food is not None, moves))
    return r if len(r) != 0 else moves

'''
Sorts moves by available free space in decreasing order.
'''
def freespace_s(data, moves):
    s = {m:data.metadata.moves[m].free_space for m in moves}
    return sorted(moves, key=lambda x: s[x], reverse=True)

'''
Sorts moves by distance to food in increasing order.
'''
def food_s(data, moves):
    return sorted(moves, key=lambda x: dist_to_food(data, x))

def dist_to_food(data, move):
    assert move in data.metadata.moves
    food = data.metadata.moves[move].close_food
    return float('inf') if food is None else move.distance_to(food)

'''
Returns nearest the ratio of your health to distance to food
'''
def foodratio(data):
    food = data.metadata.headmeta.close_food
    print(data.metadata.headmeta.close_food)
    return 0 if food is None else data.you.health/data.you.head().distance_to(food)

'''
Warning: Using more than one sorting filter will obviously wipe
out the sorting done by all but the last (first in the list)
filter applied
'''

grow = [food_s, food_f, freespace_f, head_f, legal_f]

starving = [food_s, food_f, ead_f, legal_f]

stagnate = [freespace_s, tail_f, avoidfood_f, head_f, legal_f]

aggressive = [legal_f]

def get_move(data):
    # TODO: Add logic to choose different sets of filters
    # TODO: Take into account whether or not another snake
    # will get to the food I'm trying to get before me
    if foodratio(data) < 20:
        return apply_filters(grow, data)[0]
    if health < 10:
        return apply_filters(starving, data)[0]
    return apply_filters(stagnate, data)[0]

def main():
    with open('../data/move.json') as move:
        data = obj.Data(json.loads(move.read()))
        # print(head_f(data, data.you.head().neighbors()))
        # print(data.metadata.headmeta)
        # print(apply_filters(grow, data))
        # print(foodratio(data))

if __name__ == '__main__':
    main()
