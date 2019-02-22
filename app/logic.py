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

    def direction_str(self, p):
        dx = p.x - self.x
        dy = p.y - self.y
        if abs(dy) > abs(dx):
            if dy < 0:
                return 'up'
            return 'down'
        if dx < 0:
            return 'left'
        return 'right'

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

def parse_point(point_json):
    return point(point_json['x'], point_json['y'])


def logic(data):
    '''
    Get current time
    while time_elapsed < 190ms
       do minimax
    return highest value move
    '''
    moves = {p:floodfill(data, p) for p in parse_point(data['you']['body'][0]).neighbors()}
    return parse_point(data['you']['body'][0]).direction_str(max(moves, key=moves.get))

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
    data2 = {   'board': {   'food': [{'x': 8, 'y': 1}, {'x': 6, 'y': 8}],
                         'height': 11,
                         'snakes': [   {   'body': [   {'x': 8, 'y': 8},
                                                       {'x': 9, 'y': 8},
                                                       {'x': 9, 'y': 9}],
                                           'health': 98,
                                           'id': 'gs_j8j6TVk7ykQfMfv7mQqd8kWP',
                                           'name': 'otonnesen/Test Snake Please '
                                                   'Ignore'}],
                         'width': 11},
            'game': {'id': '820c1d82-cd8c-414d-846b-34dfb6bfa93e'},
            'turn': 2,
            'you': {   'body': [{'x': 1, 'y': -1}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}],
                       'health': 98,
                       'id': 'gs_7X6KXcCRwWc9qkFPGxTr6HYX',
                       'name': 'otonnesen/test snake 2'}}
    print(floodfill(data, point(data['you']['body'][0]['x']+1, data['you']['body'][0]['y'])))
    print(logic(data))

if __name__ == '__main__':
    main()
