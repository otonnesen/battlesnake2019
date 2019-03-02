class Point:
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
        return Point({'x':self.x, 'y':self.y-1})

    def down(self):
        return Point({'x':self.x, 'y':self.y+1})

    def left(self):
        return Point({'x':self.x-1, 'y':self.y})

    def right(self):
        return Point({'x':self.x+1, 'y':self.y})

    def distance_to(self, other):
        return abs(self.x-other.x)+abs(self.y-other.y)

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

    def valid(self, board):
        if (self.x < 0 or self.x >= board.width or
            self.y < 0 or self.y >= board.height):
            return False
        return True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x)+str(self.y))

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __repr__(self):
        return 'Point(x:{},y:{})'.format(self.x, self.y)

class Board:
    def __init__(self, board):
        self.food = [Point(i) for i in board['food']]
        self.height = board['height']
        self.width= board['width']
        self.snakes = [Snake(i) for i in board['snakes']]

    def get_snake(self, snakeid):
        try:
            return {s.id:s for s in self.snakes}[snakeid]
        except KeyError:
            return None

    def __str__(self):
        s = []
        for i in range(self.width):
            t = []
            for j in range(self.height):
                p = False
                for k in self.food:
                    if Point({'x':i,'y':j}) == k:
                        t.append('F')
                        p = True
                        break
                for l in self.snakes:
                    for m in l.body:
                        if Point({'x':i,'y':j}) == m:
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
        return 'Board(height:{},width:{},food:{},snakes:{})'\
                .format(self.height, self.width, self.food, self.snakes)

class Snake:
    def __init__(self, snake):
        self.body = [Point(i) for i in snake['body']]
        self.health = snake['health']
        self.id = snake['id']
        self.name = snake['name']

    def head(self):
        return self.body[0]

    def tail(self):
        return self.body[-1]

    def smaller_than(self, other):
        return len(self.body) < len(other.body)

    def __str__(self):
        return self.name+': ['+','.join([str(i) for i in self.body])+']'

    def __repr__(self):
        return 'Snake(name:{},id:{},health:{},body:{})'\
                .format(self.name, self.id, self.health, self.body)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Movemetadata:
    def __init__(self, data, metadata, m, head=False):
        self.free_space = 0     # Space reachable from this point
        self.close_food = None  # Closest point containing food
        self.num_food = 0       # Amount of food reachable
        self.food = set()       # Food points reachable
        self.tail = False       # True if a snake's tail is reachable
        self.smallhead = False  # True if a smaller snake's head is reachable

        if not m.valid(data.board) and not head:
            return
        visited = set()
        queue = [m]
        b = [[0 for i in range(data.board.width) ] for j in range(data.board.height)]
        while len(queue) != 0:
            p = queue.pop()
            if p not in visited:

                self.free_space += 1
                if p in metadata.food:
                    if self.close_food is None:
                        self.close_food = p # BFS, so first food seen is closest
                    self.num_food += 1
                    self.food.add(p)
                if p in metadata.tails:
                    self.tail = True
                if p in [s.head() for s in data.board.snakes if\
                        s.id != data.you.id and len(s.body) < len(data.you.body)]:
                    self.smallhead = True

                visited.add(p)
                for i in p.neighbors():
                    if i not in visited and i in metadata.safe:
                        queue.insert(0, i)
    def __repr__(self):
        return\
            'Movemetadata(free_space:{},close_food:{},num_food:{},food:{},tail:{})'\
            .format(self.free_space,self.close_food,self.num_food,\
            self.food,self.tail)

class Metadata:
    def __init__(self, data):
        self.safe = set([Point({'x':x,'y':y})\
                for x in range(data.board.width)\
                for y in range(data.board.height)])
        for s in set(data.board.snakes+[data.you]):
            for i in s.body[:-1]:
                if i in self.safe:
                    self.safe.remove(i)
        # self.tails = set([s.body[-1] for s in data.board.snakes])
        self.tails = {s.tail():s for s in data.board.snakes}
        self.heads = {s.head():s for s in data.board.snakes if s.id != data.you.id}
        self.food = set(data.board.food)
        self.moves = {m:Movemetadata(data, self, m) for m in data.you.head().neighbors()}
        self.headmeta = Movemetadata(data, self, data.you.head(), True)

    '''
    Returns dict of smaller snakes' heads.
    '''
    def smaller_snake_heads(self, snake):
        return list(filter(lambda x: self.heads[x].smaller_than(snake), self.heads))

class Data:
    def __init__(self, data):
        self.board = Board(data['board'])
        self.gameid = data['game']['id']
        self.turn = data['turn']
        self.you = Snake(data['you'])
        self.metadata = Metadata(self)

    def __str__(self):
        return self.board.__str__()

    def __repr__(self):
        return 'Data(id:{},turn:{},you:{},board:{})'\
                .format(self.gameid, self.turn, self.you.id, self.board.__repr__())
