'''
Contains a bunch of filters -- denoted by a '_f' appended to the function
name -- and sorters -- denoted by a '_s' appended to the function name.
A filter attempts to remove any moves not satisfying a particular property.
A sorter rearranges the order of the moves (and should thus be applied last)
'''
import json
import sys
import functools
import itertools
from datetime import datetime as dt
from copy import deepcopy

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
Returns a filter that filters moves that will lead to your
certain death in x turns.
If no moves satisy this property, returns moves.
'''
def die_in_x_f_generator(x):
    def die_in_x_f(data, moves):
        r = list(filter(lambda x: not going_to_die(data, moves, x), moves))
        return r if len(r) != 0 else moves
    return r

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
    return 0 if food is None else data.you.health/data.you.head().distance_to(food)

'''
Returns True if this move leads to a loss within x turns, else False.
(Pretty much depth-limited minimax)
'''
def going_to_die(data, move, depth):
    # TODO: Find distance between you and the other snakes' heads.
    #       If greater than twice depth, these snakes' moves cannot
    #       directly affect you during the timeframe being considered,
    #       and so its moves need not be calculated.
    die = False
    if depth == 0:
        return len(legal_f(data, move.neighbors())) == 0
    affecting_snakes = list(filter(lambda x: x.id != data.you.id and\
            data.you.head().distance_to(x.head()) <= 2*depth, data.board.snakes))
    for m in get_potential_moves(data, affecting_snakes):
        state = get_state(data, m)
        die = going_to_die(data, get_move(data), depth-1)
    # TODO: Use data here to determine whether or not I actually die
    return die

'''
Takes your move and returns a list corresponding to the cartesian product
of possible moves by snakes in affecting_snakes.
'''
def get_potential_moves(data, affecting_snakes):
    r = []
    for i in itertools.product(*[legal_f(data, s.head().neighbors()) for s in affecting_snakes]):
        m = {affecting_snakes[j]:i[j] for j in range(len(i))}
        r.append(m)
    return r

def get_state(data, moves):
    r = deepcopy(data)
    for s, move in moves.items():
        snake = r.board.get_snake(s.id)
        if not move.valid(r.board):
            r.board.snakes.remove(snake)
            continue
        if move in [sn.head() for sn in r.board.snakes if sn.id != s.id]:
            r.board.snakes.remove(s if len(s.body) < len(sn.body) else sn)
        snake.body.insert(0, move)
        food = False
        for f in r.board.food:
            if f == move:
                food = True
        if not food:
            snake.body.pop()
        if s.id == data.you.id:
            if not food:
                r.you.body.pop()
            r.you.body.insert(0, move)
    return r

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
        for i in apply_filters(aggressive, data): #TODO: For testing; remove
            if not going_to_die(data, i, 4):
                return i
    for i in apply_filters(grow, data):
        if not going_to_die(data, i, 4):
            return i
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
    data = obj.Data(test.g4)
    # print(going_to_die(data, data.you.head().left(), 10))
    affecting_snakes = list(filter(lambda x: x.id != data.you.id and data.you.head().distance_to(x.head()) <= 8, data.board.snakes))
    s = dt.now()
    for i in apply_filters(aggressive, data):
        if not going_to_die(data, i, 4):
            print(i)
    s = dt.now()-s
    print(s.microseconds/1000)
    # print(len(data.metadata.safe))
    # print(data.board.width*data.board.height)

if __name__ == '__main__':
    main()
