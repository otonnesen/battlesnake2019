class point:
    def __init__(self, point):
        self.x = point['x']
        self.y = point['y']

    def move(self, move):
        if move == 'up':
            return self.up()
        if move == 'down':
            return self.down()
        if move == 'left':
            return self.left()
        if move == 'right':
            return self.right()

    def up(self):
        return point({'x':self.x, 'y':self.y-1})

    def down(self):
        return point({'x':self.x, 'y':self.y+1})

    def left(self):
        return point({'x':self.x-1, 'y':self.y})

    def right(self):
        return point({'x':self.x+1, 'y':self.y})

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
        if (self.x < 0 or self.x >= data.board.width or
            self.y < 0 or self.y >= data.board.height):
            return False
        for snake in data.board.snakes:
            for p in snake.body[:-1]:
                if p == self:
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

class board:
    def __init__(self, board):
        self.food = [point(i) for i in board['food']]
        self.height = board['height']
        self.width= board['width']
        self.snakes = [snake(i) for i in board['snakes']]

    def __str__(self):
        s = []
        for i in range(self.width):
            t = []
            for j in range(self.height):
                p = False
                for k in self.food:
                    if point({'x':i,'y':j}) == k:
                        t.append('F')
                        p = True
                        break
                for l in self.snakes:
                    for m in l.body:
                        if point({'x':i,'y':j}) == m:
                            t.append('S')
                            p = True
                            break
                    if p:
                        break
                if not p:
                    t.append('_')
            s.append(' '.join(t))
        return '\n'.join(s)

    def __repr__(self):
        return 'board(height:{},width:{},food:{},snakes:{})'\
                .format(self.height, self.width, self.food, self.snakes)
                
class snake:
    def __init__(self, snake):
        self.body = [point(i) for i in snake['body']]
        self.health = snake['health']
        self.id = snake['id']
        self.name = snake['name']

    def __str__(self):
        return '['+','.join([str(i) for i in self.body])+']'

    def __repr__(self):
        return 'snake(name:{},id:{},health:{},body:{})'\
                .format(self.name, self.id, self.health, self.body)

class data:
    def __init__(self, data):
        self.board = board(data['board'])
        self.gameid = data['game']['id']
        self.turn = data['turn']
        self.you = snake(data['you'])

    def __str__(self):
        return self.board.__str__()
    
    def __repr__(self):
        return 'data(id:{},turn:{},you:{},board:{})'\
                .format(self.gameid, self.turn, self.you.id, self.board.__repr__())

