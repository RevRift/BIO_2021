""" Note: The positive x direction is to the right and the positive y direction is down """

from collections import deque

class Board: # contains a dictionary of filled triangles {position of triangle: triangle object}
    def __init__(self, triangles): # must be initialised with at least one triangle
        self.triangles = triangles
        self.top_left_triangle = self.triangles[min(self.triangles, key = lambda pos: (pos[1], pos[0]))]

    def place_triangle(self, triangle_pos, number): # places triangle and updates top left triangle
        self.triangles[triangle_pos] = Triangle(triangle_pos[0], triangle_pos[1], number)
        if (triangle_pos[1], triangle_pos[0]) < (self.top_left_triangle.pos[1], self.top_left_triangle.pos[0]):
            self.top_left_triangle = self.triangles[triangle_pos]
    
    def get_outer_edges(self): # uses a bot that traverses the outer perimeter of the board
        outer_edges = set()
        bot = Player(0, float('inf'), self.top_left_triangle, 1 if self.top_left_triangle.points_up else 2)
        while (bot.triangle.pos, bot.edge_type) not in outer_edges:
            outer_edges.add((bot.triangle.pos, bot.edge_type))
            bot.traverse()
        return outer_edges

    def perimeter(self):
        return len(self.get_outer_edges())
    
    def count_holes(self): # counts the number of unfilled triangles in the perimeter of the board
        outer_triangle_positions = set(triangle_pos for triangle_pos, edge_type in self.get_outer_edges())
        test_triangle_positions = deque([(0, 0)])
        seen = set([(0, 0)])
        count = 0
        while test_triangle_positions:
            triangle_pos = test_triangle_positions.popleft()
            if triangle_pos in outer_triangle_positions: continue
            if triangle_pos not in board.triangles: count += 1
            directions_to_next_test_triangle_positions = (
                (1, 0), (-1, 0), (0, 1) if triangle_pos[0] % 2 == triangle_pos[1] % 2 else (0, -1)
            )
            for dx, dy in directions_to_next_test_triangle_positions:
                next_test_triangle_pos = (triangle_pos[0] + dx, triangle_pos[1] + dy)
                if next_test_triangle_pos not in seen:
                    test_triangle_positions.append(next_test_triangle_pos)
                    seen.add(next_test_triangle_pos)           
        return count
    
class Triangle:
    def __init__(self, x, y, number = 0):
        self.pos = (x, y) # you can think if (x, y) as being the center of the triangle. the centres of triangles on the board form a grid-like structure
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
        self.edge_type = edge_type # stores 0 for horizontal side of triangle, 1 for side of triangle with positive gradient, 2 for side of triangle with negative gradient
        self.adjacent_triangle_pos = triangle.get_adjacent_triangle_pos(edge_type)
        self.score = 0
    
    def traverse(self): # moves the player one edge clockwise around the perimeter
        dummy_edge_type = self.edge_type
        dummy_triangle = self.triangle
        dummy_adjacent_triangle_pos = self.adjacent_triangle_pos
        for landing_edge in range(5): # out of the 5 potential landing edges for the player, we want to choose the edge that requires the largest anti-clockwise aturn to move onto it
            dummy_edge_type = (dummy_edge_type + 1) % 3
            dummy_adjacent_triangle_pos = dummy_triangle.get_adjacent_triangle_pos(dummy_edge_type)
            if dummy_triangle.pos in board.triangles and dummy_adjacent_triangle_pos not in board.triangles:
                self.edge_type = dummy_edge_type
                self.triangle = board.triangles[dummy_triangle.pos]
                self.adjacent_triangle_pos = dummy_adjacent_triangle_pos
            dummy_triangle = Triangle(dummy_adjacent_triangle_pos[0], dummy_adjacent_triangle_pos[1], 0)

    def move(self): # moves the player 'max_traversals' edges clockwise around perimeter
        pos_adjacent_to_original_triangle = self.triangle.get_adjacent_triangle_pos(self.edge_type)
        for m in range(self.max_traversals):
            self.traverse()
            if self.num_of_ways_to_score(self.adjacent_triangle_pos) >= 1: break    
        board.place_triangle(pos_adjacent_to_original_triangle, self.number)
        self.score += self.num_of_ways_to_score(pos_adjacent_to_original_triangle)
    
    def num_of_ways_to_score(self, triangle_pos): # finds number of ways to score by placing a triangle of your number at this position
        directions_to_other_two_triangles = ( # if the triangle at triangle_pos points up
            ((1, -1), (2, 0)), ((-1, -1), (-2, 0)), ((1, 1), (-1, 1))
        ) if (triangle_pos[0] % 2 == triangle_pos[1] % 2) else ( # if the triangle points down
            ((2, 0), (1, 1)), ((-2, 0), (-1, 1)), ((1, -1), (-1, -1))
        )
        count = 0
        for (d1, d2), (d3, d4) in directions_to_other_two_triangles:
            triangle_pos1, triangle_pos2 = (triangle_pos[0] + d1, triangle_pos[1] + d2), (triangle_pos[0] + d3, triangle_pos[1] + d4)
            if (triangle_pos1 in board.triangles and board.triangles[triangle_pos1].number == self.number and
                triangle_pos2 in board.triangles and board.triangles[triangle_pos2].number == self.number): count += 1
        return count

    def reposition_if_necessary(self):
        if self.adjacent_triangle_pos in board.triangles:
            self.triangle = board.top_left_triangle
            self.edge_type = 1 if self.triangle.points_up else 2
            self.adjacent_triangle_pos = self.triangle.get_adjacent_triangle_pos(self.edge_type)
        
num_of_players, num_of_moves = map(int, input().split())
base = Triangle(0, 0, 0) # parameters: x, y, number
board = Board({base.pos: base}) # parameter: dictionary of triangles
players = [Player(number, int(max_traversals), base, 1) for number, max_traversals in enumerate(input().split(), 1)]

for move_number in range(num_of_moves):
    player = players[move_number % num_of_players]
    player.move()
    for p in players:
        p.reposition_if_necessary()

for player in players:
    print(f'Player {player.number} score: {player.score}')
print(f'Perimeter: {board.perimeter()}')
print(f'Number of unfilled triangles within perimeter: {board.count_holes()}')