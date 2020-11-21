from collections import defaultdict, deque
from random import Random, randint
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = deque()
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.popleft()
        else:
            return None
    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = deque()
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_id = []
player_map = {}

def reverse_direction(direction):
    opposite = {"n": "s", "e": "w", "s": "n", "w": "e"}
    return opposite[direction]

def random_direction(prev_direction):
    exits = list()
    for exit in player.current_room.get_exits():
        if player.current_room.id in player_map and exit in player_map[player.current_room.id]:
            if player_map[player.current_room.id][exit] == "?" and exit != reverse_direction(prev_direction):
                exits.append(exit)
                
        else:
            exits.append(exit)
    
    if len(exits) == 0:
        return reverse_direction(prev_direction)
    else:
        dir = exits[randint(0, len(exits) - 1)]
        return dir
    # if prev_direction:
    #     if dir == reverse_direction(prev_direction):
    #         dir = 
    
    

def dft(visited = set()):
    # s = Stack()
    prev_exit = None
    direction = random_direction(None)

    while len(visited) < len(room_graph):
        # print(player.current_room.id)

        if player.current_room.id not in visited:
            visited.add(player.current_room.id)
            for exit in player.current_room.get_exits():
                player_map[player.current_room.id] = {}
                player_map[player.current_room.id][exit] = '?'
            if prev_exit is not None:
                # pass
                player_map[prev_exit][direction] = player.current_room.id
                player_map[player.current_room.id][reverse_direction('n')] = prev_exit
            prev_exit = player.current_room.id

        direction = random_direction(direction)
        if "?" in player_map[player.current_room.id].values():
            # print(player_map[player.current_room.id])
            # print(player_map)
            traversal_path.append(direction)
            traversal_id.append(player.current_room.id)
            player.travel(direction)
        else:
            print(player_map)
            reverse = reverse_direction(traversal_path[-1])
            traversal_path.append(reverse)
            player.travel(reverse)
            # break
            # 

dft()

def explore():
    stack = Stack()
    pass


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
