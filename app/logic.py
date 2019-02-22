class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def up(self):
        return point(self.x, self.y-1)

    def down(self):
        return point(self.x, self.y+1)

    def left(self):
        return point(self.x-1, self.y)

    def right(self):
        return point(self.x+1, self.y)

    def neighbors(self):
        return [self.up(), self.down(), self.left(), self.right()]

    def valid(self, data):
        if (self.x < 0 or self.x >= data['board']['width'] or
            self.y < 0 or self.y >= data['board']['height']):
            return False
        for snake in data['board']['snakes']:
            for p in snake['body']:
                if p['x'] == self.x and p['y'] == self.y:
                    return False
        return True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x)+str(self.y))

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __repr__(self):
        return 'point(x:{},y:{})'.format(self.x, self.y)


def logic(data):
    '''
    Get current time
    while time_elapsed < 190ms
       do minimax
    return value
    '''
    return 'up'

def get_board_value(data):
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

def main():
    data =  {   'board': {   'food': [   {'x': 11, 'y': 15},
                                         {'x': 2, 'y': 12},
                                         {'x': 13, 'y': 8},
                                         {'x': 1, 'y': 9},
                                         {'x': 10, 'y': 15}],
                             'height': 20,
                             'snakes': [   {   'body': [   {'x': 5, 'y': 4},
                                                           {'x': 5, 'y': 5},
                                                           {'x': 5, 'y': 6},
                                                           {'x': 4, 'y': 6},
                                                           {'x': 3, 'y': 6},
                                                           {'x': 2, 'y': 6},
                                                           {'x': 2, 'y': 5},
                                                           {'x': 2, 'y': 4},
                                                           {'x': 1, 'y': 3}],
                                               'health': 91,
                                               'id': 'af1b9cb9-3c7a-44c0-8ef7-9850e19ca0af',
                                               'name': 't1'}],
                             'width': 20},
                'game': {'id': '3720daeb-cb2b-4588-99a8-1952d27b96d1'},
                'turn': 9,
                'you': {   'body': [   {'x': 5, 'y': 4},
                                       {'x': 5, 'y': 5},
                                       {'x': 5, 'y': 6},
                                       {'x': 4, 'y': 6},
                                       {'x': 3, 'y': 6},
                                       {'x': 2, 'y': 6},
                                       {'x': 2, 'y': 5},
                                       {'x': 2, 'y': 4},
                                       {'x': 1, 'y': 3}],
                           'health': 91,
                           'id': 'af1b9cb9-3c7a-44c0-8ef7-9850e19ca0af',
                           'name': 't1'}}
    print(floodfill(data, point(data['you']['body'][0]['x']+1, data['you']['body'][0]['y'])))

if __name__ == '__main__':
    main()
