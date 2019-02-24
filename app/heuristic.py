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
    return max([floodfill(board, i) for i in snake.body[0].neighbors()])

'''
return the number of spaces reachable from a given point
'''
def floodfill(board, point):
    if not point.valid(board):
        return 0
    visited = set()
    stack = [point]
    s = 0
    while len(stack) != 0:
        p = stack.pop()
        if p not in visited:
            s += 1
            visited.add(p)
            for i in p.neighbors():
                if i not in visited and p.valid(board):
                    stack.append(i)
    return s

def foodratio(data, snakeid):
    snake = data.board.get_snake(snakeid)

'''
Something like this could be cool, a list of heuristics to run
that we can change (or just have multiple) for different situations
'''
heuristics = [floodfill]
