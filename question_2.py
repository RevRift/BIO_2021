"""
when i'm adjust where a player lands on each traversals,
i'm not accounting for cases where the triangles are just touching at a corner like a moustache, or a bowtie
to handle this case, i could check for valid landing corner anticlockwise instead
and the first valid one i find is the one i land on

maybe change the num_of_ways_to_score back to can_win

I'VE DEFINED THE POSITIVE X DIRECTION AS RIGHT AND THE POSITIVE Y DIRECTION AS DOWN (so that the the coordinate at (min_x, min_y) is the 'most top left' coordinate)

testing question_2b yields a wrong answer so find out what going on there
"""

debug = False

class Board:
    def __init__(self, triangles): # contains a dictionary of triangles {position of triangle: triangle object}
        self.triangles = triangles
        self.top_left_triangle = self.triangles[min(self.triangles)]

    def place_triangle(self, triangle_pos, number): # places triangle and updates top left triangle
        self.triangles[triangle_pos] = Triangle(triangle_pos[0], triangle_pos[1], number)

        if min(self.triangles) == triangle_pos:
            self.top_left_triangle = self.triangles[triangle_pos]
    
    def perimeter(self): # uses a bot that traverses the outer perimeter of the board and counts the number of edges
        outer_edges = set()
        bot = Player(-1, float('inf'), self.top_left_triangle, 1 if self.top_left_triangle.points_up else 2)
        count = 0
        while (bot.triangle.pos, bot.edge_type) not in outer_edges:
            if debug: a, b, c = bot.triangle.pos[0], bot.triangle.pos[1], bot.edge_type
            count += 1
            outer_edges.add((bot.triangle.pos, bot.edge_type))
            bot.traverse()
            if debug: d, e, f = bot.triangle.pos[0], bot.triangle.pos[1], bot.edge_type
            if debug: print(f'Bot moved from {a, b, c} to {d, e, f}')
        return count
    
    def count_holes(self):
        return 0
    
    def print(self):
        min_x = self.triangles[min(self.triangles, key=lambda t: t[0])].pos[0]
        max_x = self.triangles[max(self.triangles, key=lambda t: t[0])].pos[0]
        min_y = self.triangles[min(self.triangles, key=lambda t: t[1])].pos[1]
        max_y = self.triangles[max(self.triangles, key=lambda t: t[1])].pos[1]

        arr = [[str(self.triangles[(x, y)].number) if (x,y) in self.triangles else ' ' for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
        for row in arr: print(''.join(row))
        print()
    
class Triangle:
    def __init__(self, x, y, number = 0):
        self.pos = (x, y)
        self.number = number
        self.points_up = (x % 2 == y % 2)
    
    def get_adjacent_triangle_pos(self, edge_type):
        directions = { # the position of the adjacent triangle depends on whether this triangle points up and the edge that the player stands on
            (True, 0): (0, 1),
            (True, 1): (-1, 0),
            (True, 2): (1, 0),
            (False, 0): (0, -1),
            (False, 1): (1, 0),
            (False, 2): (-1, 0)
        }
        direction = directions[(self.points_up, edge_type)]

        return (self.pos[0] + direction[0], self.pos[1] + direction[1])
    
class Player:
    def __init__(self, number, max_traversals, triangle: Triangle, edge_type):
        self.number = number
        self.max_traversals = max_traversals
        self.triangle = triangle
        self.adjacent_triangle_pos = triangle.get_adjacent_triangle_pos(edge_type) # stores the position of the unfilled triangle next to the current triangle where the player could score
        self.edge_type = edge_type # stores 0 for horizontal side of triangle, 1 for side of triangle with positive gradient, 2 for side of triangle with negative gradient
                                   # defining it this way means any two edges of type will with either be parallel or will be along the same diagonal. the same 2.
        self.score = 0
    
    def print_pos(self):
        print(f'Player {self.number}: pos = {self.triangle.pos[0], self.triangle.pos[1], self.edge_type}, adjacent triangle pos = {self.adjacent_triangle_pos}')
    
    def print(self):
        print(f'Player {self.number}: max traversals = {self.max_traversals}, score = {self.score}')
        print_pos()
    
    def traverse(self): # moves the player one edge clockwise around the perimeter
        self.edge_type = (self.edge_type + 1) % 3
        self.adjacent_triangle_pos = self.triangle.get_adjacent_triangle_pos(self.edge_type)
        while self.adjacent_triangle_pos in board.triangles: # player will collide with an existing triangle if they move here, find another spot for the player to move
            if debug: print(f'Adjust traversal of Player {self.number} because {self.adjacent_triangle_pos} is in board')
            self.triangle = board.triangles[self.adjacent_triangle_pos]
            self.edge_type = (self.edge_type + 1) % 3
            self.adjacent_triangle_pos = self.triangle.get_adjacent_triangle_pos(self.edge_type)
        
    def move(self): # moves the player 'max_traversals' edges clockwise around perimeter
        pos_adjacent_to_original_triangle = self.triangle.get_adjacent_triangle_pos(self.edge_type)

        for m in range(self.max_traversals):
            self.traverse()
            if debug: print(f'Player {self.number} is at {self.triangle.pos[0], self.triangle.pos[1], self.edge_type}, the adjacent triangle pos is {self.adjacent_triangle_pos}')
            if self.num_of_ways_to_score(self.adjacent_triangle_pos): 
                if debug: print(f'Player {self.number} stops their move early (after {m+1} traversals instead of {self.max_traversals})')
                break
        
        board.place_triangle(pos_adjacent_to_original_triangle, self.number)
        self.score += self.num_of_ways_to_score(pos_adjacent_to_original_triangle)
        if debug: print(f'Player {self.number}\'s new score is {self.score}')
    
    def num_of_ways_to_score(self, triangle_pos): # finds number of ways to score by placing a triangle of your number at this position
                                                  # the type scoring patterns you can get with the triangle depends on whether it points up or down
        directions_to_other_two_triangles = ( # if the triangle points up
            ((1, -1), (2, 0)), # if this triangle is at the bottom left in the scoring pattern (remember i've defined down as the positive y direction)
            ((-1, -1), (-2, 0)), # if this triangle is at the bottom right in the scoring pattern
            ((1, 1), (-1, 1)) # if this triangle is at the top in the scoring pattern
        ) if (triangle_pos[0] % 2 == triangle_pos[1] % 2) else ( # if the triangle points down
            ((-2, 0), (-1, 1)), # if this triangle is at the top right of a scoring pattern
            ((2, 0), (1, 1)), # if this triangle is at the top left of a scoring pattern
            ((1, -1), (-1, -1)) # if this triangle is at the bottom of a scoring pattern
        )
        count = 0
        for (d1, d2), (d3, d4) in directions_to_other_two_triangles:
            triangle_pos1, triangle_pos2 = (triangle_pos[0] + d1, triangle_pos[1] + d2), (triangle_pos[0] + d3, triangle_pos[1] + d4)
            if (triangle_pos1 in board.triangles and board.triangles[triangle_pos1].number == self.number and
                triangle_pos2 in board.triangles and board.triangles[triangle_pos2].number == self.number): count += 1
        return bool(count)

    def reposition_if_necessary(self):
        if debug: a, b, c = self.triangle.pos[0], self.triangle.pos[1], self.edge_type
        if self.adjacent_triangle_pos in board.triangles:
            self.triangle = board.top_left_triangle
            self.edge_type = 1 if self.triangle.points_up else 2
            self.adjacent_triangle_pos = self.triangle.get_adjacent_triangle_pos(self.edge_type)
            if debug: d, e, f = self.triangle.pos[0], self.triangle.pos[1], self.edge_type
            if debug: print(f'Player {self.number} was repositioned from {a, b, c} to {d, e, f} because {self.adjacent_triangle_pos} is in {board.triangles.keys()}')
        

num_of_players, num_of_moves = map(int, input().split())
base = Triangle(0, 0, 0) # parameters are: x, y, number
board = Board({base.pos: base}) # the parameter is a dictionary of triangles, there must be at least one element in the list at all times
players = [Player(number, int(max_traversals), base, 1) for number, max_traversals in enumerate(input().split(), 1)]

print()

for move_number in range(num_of_moves):
    if debug: print(board.triangles.keys())
    player = players[move_number % num_of_players]
    if debug: a, b, c = player.triangle.pos[0], player.triangle.pos[1], player.edge_type
    if debug: print(f'Player {player.number} starts to move, from {a, b, c}')
    player.move()
    if debug: d, e, f = player.triangle.pos[0], player.triangle.pos[1], player.edge_type
    if debug: print(f'Player {player.number} moved from {a, b, c} to {d, e, f}')
    if debug: print(f'Player {player.number}\'s score is {player.score}')
    for p in players:
        p.reposition_if_necessary()
    board.print()
    player.print_pos(); print()
    if debug: print()

# board.print()

print()
for player in players:
    print(f'Player {player.number} score: {player.score}')
print(f'Board perimeter: {board.perimeter()}')