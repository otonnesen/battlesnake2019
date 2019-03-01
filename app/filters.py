'''
Contains a bunch of filters -- denoted by a '_f' appended to the function
name -- and sorters -- denoted by a '_s' appended to the function name.
A filter attempts to remove any moves not satisfying a particular property.
A sorter rearranges the order of the moves (and should thus be applied last)
'''
import json
import sys
import functools
from datetime import datetime as dt

import obj
import test

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
    # TODO: Maybe size of snake + amount of food in space + a margin?
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
Filters moves that do not lead to a direct snake kill.
'''
def track_f(data, moves):
    r = list(filter(lambda x: data.metadata.moves[x].smallhead, moves))
    return r if len(r) != 0 else moves

'''
Kills a snake directly if possible.
'''
def kill_f(data, moves):
    r = list(filter(lambda x: x in data.metadata.smaller_snake_heads(data.you), moves))
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

'''
Sorts moves by distance to smaller snake head.
'''
# TODO NEEDS TO BE TESTED, I WROTE THIS ON THE BUS TODO
def track_s(data, moves):
    h = lambda x: {s:x.distance_to(s) for s in data.metadata.smaller_snake_heads(data.you)}
    return sorted(moves, key=lambda x: float('inf') if not\
            data.metadata.moves[x].smallhead else min(h(x), key=h(x).get))

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
Returns True if this move leads to a loss within x turns, else False.
(Pretty much depth-limited minimax)
'''
def going_to_die(data, move, x):
    #TODO:  Find distance between you and the other snakes' heads.
    #       If greater than x, these snakes' moves cannot directly
    #       affect you during the timeframe being considered, and
    #       so its moves need not be calculated.
    affecting_snakes = [s for i in data.board.snakes if data.you.head().distance_to(s.head()) <= x]
    pass

'''
Takes your move and returns a list of possible board states.
'''
def get_states(data, move, x):
    pass

'''
Warning: Using more than one sorting filter will obviously wipe
out the sorting done by all but the last (first in the list)
filter applied
'''

grow = [food_s, food_f, freespace_f, head_f, legal_f]

starving = [food_s, food_f, head_f, legal_f]

stagnate = [freespace_s, tail_f, avoidfood_f, head_f, legal_f]

aggressive = [track_s, kill_f, track_f, freespace_f, head_f, legal_f]

def get_move(data):
    if foodratio(data) > 50 and len(data.you.body) > 10:
        return apply_filters(aggressive, data)[0] #TODO: For testing; remove
    return apply_filters(grow, data)[0]
    # TODO: Add logic to choose different sets of filters
    # TODO: Take into account whether or not another snake
    # will get to the food I'm trying to get before me
    if len(data.board.snakes) < 4:
        pass # Look some moves ahead
    if foodratio(data) < 20:
        return apply_filters(grow, data)[0]
    if health < 10:
        return apply_filters(starving, data)[0]
    return apply_filters(stagnate, data)[0]

def main():
    data = obj.Data(test.g1)
    print(apply_filters(aggressive, data))
    return
    with open('../data/move.json') as move:
        data = obj.Data(json.loads(move.read()))
        # print(apply_filters(aggressive, data)[0])
        print(track_s(data, legal_f(data, data.you.head().neighbors())))
        # print(head_f(data, data.you.head().neighbors()))
        # print(data.metadata.headmeta)
        # print(apply_filters(grow, data))
        # print(foodratio(data))

if __name__ == '__main__':
    main()
