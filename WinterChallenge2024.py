import sys
import math

# Grow and multiply your organisms to end up larger than your opponent.

'''
# Game Protocol
## Initialization Input
First line: two integers width and height for the size of the grid.

## Input for One Game Turn
First line: one integer entityCount for the number of entities on the grid.

Next entityCount lines: the following 7 inputs for each entity:

    - x: X coordinate (0 is leftmost)
    - y: Y coordinate (0 is topmost)
    - type:
        WALL for a wall
        ROOT for a ROOT type organ
        BASIC for a BASIC type organ. Requires 1 A protein.
        HARVESTER for a HARVESTER type organ. Requires 1 C and 1 D protein.
        TENTACLE for a TENTACLE type organ. Requires 1 B and 1 C protein.
        SPORER for a SPORER type organ. Requires 1 B and 1 D protein to grow and 1 of each to spawn new ROOT.
        A/B/C/D for A/B/C/D protein sources
    - owner:
        1 if you are the owner of this organ
        0 if your opponent owns this organ
        -1 if this is not an organ
    - organId: unique id of this entity if it is an organ, 0 otherwise
    - organDir: N, W, S, or E for the direction in which this organ is facing
    - organParentId: if it is an organ, the organId of the organ that this organ grew from (0 for ROOT organs), else 0.
    - organRootId: if it is an organ, the organId of the ROOT that this organ originally grew from, else 0.

Next line: 4 integers: myA,myB,myC,myD for the amount of each protein type you have.
Next line: 4 integers: oppA,oppB,oppC,oppD for the amount of each protein type your opponent has.
Next line: the integer requiredActionsCount which equals 1 in this league.

## Output
A single line with your action: GROW id x y type direction : attempt to grow a new organ of type type at location x, y 
from organ with id id. If the target location is not a neighbour of id, the organ will be created on the shortest path to x, y.
'''

# width: columns in the game grid
# height: rows in the game grid
width, height = [int(i) for i in input().split()]
detour = False

class Entity:
    def __init__(self, x, y, _type, owner, organ_id, organ_dir, organ_parent_id, organ_root_id):
        self.x = x
        self.y = y
        self._type = _type
        self.owner = owner
        self.organ_id = organ_id
        self.organ_dir = organ_dir
        self.organ_parent_id = organ_parent_id
        self.organ_root_id = organ_root_id

    def __str__(self):
        return f'Type:{self._type}, ({self.x}, {self.y}), Owner:{self.owner}, Organ:{self.organ_id}, Direction:{self.organ_dir}'

    def __repr__(self):
        return f'Type:{self._type}, ({self.x}, {self.y}), Owner:{self.owner}, Organ:{self.organ_id}, Direction:{self.organ_dir}'

    def coords_str(self):
        return f'{self.x} {self.y}'

    def facing_coords(self):
        if self.organ_dir == 'N':
            return self.x, self.y - 1
        elif self.organ_dir == 'E':
            return self.x + 1, self.y
        elif self.organ_dir == 'S':
            return self.x, self.y + 1
        elif self.organ_dir == 'W':
            return self.x - 1, self.y
        else:
            return None

    def neighbouring_entities(self, grid):
        neighbours = []
        if (self.x, self.y-1) in grid.keys():
            neighbours.append(grid[(self.x, self.y-1)])
        if (self.x, self.y+1) in grid.keys():
            neighbours.append(grid[(self.x, self.y+1)])
        if (self.x-1, self.y) in grid.keys():
            neighbours.append(grid[(self.x-1, self.y)])
        if (self.x+1, self.y) in grid.keys():
            neighbours.append(grid[(self.x+1, self.y)])
        return neighbours

    def harvested_by(self, grid):
        neighbours = self.neighbouring_entities(grid)
        my_harvesters, enemy_harvesters = 0, 0
        for neighbour in neighbours:
            if neighbour._type == 'HARVESTER' and neighbour.facing_coords() == (self.x, self.y):
                if neighbour.owner == 1:
                    my_harvesters += 1
                else:
                    enemy_harvesters += 1
        return my_harvesters, enemy_harvesters

    def closest_by_taxicab(self, organisms):
        #TODO: Avoid full tiles
        closest = organisms[0]
        closest_distance = 99
        self_direction = ''
        for o in organisms:
            dist = abs(self.x - o.x) + abs(self.y - o.y)
            if dist < closest_distance:
                closest = o
                closest_distance = dist

        if self.y > closest.y:
            self_direction += 'S'
        elif self.y < closest.y:
            self_direction += 'N'
        if self.x > closest.x:
            self_direction += 'E'
        elif self.x < closest.x:
            self_direction += 'W'

        return closest, closest_distance, self_direction


'''class Tile:
    def __init__(self, x, y, entity):
        self.x = x
        self.y = y
        self.entity = entity

    def __str__(self):
        return f'Tile: ({self.x}, {self.y})'

    def __repr__(self):
        if self.entity is None:
            return f'Tile: ({self.x}, {self.y}) is empty'
        else:
            entity_info = ''
            if entity.organ_id:
                entity_info = f'O:{self.entity.organ_id}, P:{self.entity.organ_parent_id}, R:{self.entity.organ_root_id}'
            return f"Tile: ({self.x}, {self.y}) has {self.entity.owner}'s {self.entity._type} {entity_info}"
    '''


# game loop
while True:
    entity_count = int(input())
    entities = []
    my_entities = []
    enemy_entities = []
    walls = []
    proteins = []
    tiles = []
    grid = {}
    closest_a = None

    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        _type = inputs[2]  # WALL, ROOT, BASIC, TENTACLE, HARVESTER, SPORER, A, B, C, D
        owner = int(inputs[3])  # 1 if your organ, 0 if enemy organ, -1 if neither
        organ_id = int(inputs[4])  # id of this entity if it's an organ, 0 otherwise
        organ_dir = inputs[5]  # N,E,S,W or X if not an organ
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])

        entity = Entity(x, y, _type, owner, organ_id, organ_dir, organ_parent_id, organ_root_id)
        entities.append(entity)
        if owner == 1:
            my_entities.append(entity)
        elif owner == 0:
            enemy_entities.append(entity)
        else: # neutral
            if _type == 'WALL':
                walls.append(entity)
            elif _type == 'A' or _type == 'B' or _type == 'C' or _type == 'D':

                proteins.append(entity)
        # print(f"Entity added:{entity}", file=sys.stderr, flush=True)
        #tile = Tile(x, y, entity)
        #tiles.append(tile)
        grid[(x, y)] = entity

    print(f"Proteins:{proteins}", file=sys.stderr, flush=True)
    print(f"MyEntities:{my_entities}", file=sys.stderr, flush=True)
    print(f"EnemyEntities:{enemy_entities}", file=sys.stderr, flush=True)

    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]

    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order
    for i in range(required_actions_count):

        # Write an action using print, example: "GROW id x y type"
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        my_root = my_entities[0]
        my_last = my_entities[len(my_entities) - 1]
        closest_a = proteins[0]

        # Wood League Logic
        ## Wood 4: if the tile on the right side of the map of my Root entity is empty, go there.
        ## Wood 3: go to the closest protein source A and make a harvester next to it, then grow around.
        ## Wood 2: grid is 1,2 (self) -> 16,5 (enemy). Go to middle X then down/right tentacles.
        ## Wood 1: shoot spore next to protein source (not on), grow down, tentacle south. MUST "wait" on entities that can't act.

        if required_actions_count == 1:
            if my_last._type == 'ROOT':
                print(f"GROW {my_last.organ_id} {my_last.x + 1} {my_root.y} SPORER E")
            else:
                print(f"SPORE {my_last.organ_id} 16 {my_last.y}")
        elif len(my_entities) & 1:
            if len(my_entities) < 3:
                print(f"GROW {my_last.organ_id} {my_last.x} {my_root.y + 1} TENTACLE S attack!")
            elif len(my_entities) < 5:
                print(f"GROW {my_last.organ_id} {my_last.x} {my_root.y - 1} HARVESTER N nom!")

        else:
            print(f"GROW {my_root} {my_last.x+1} {my_root.y + 1} BASIC ok")



        '''
        if len(my_entities) < 8:
            print(f"GROW {my_last.organ_id} {my_last.x + 1} {my_root.y} BASIC")
        elif len(my_entities) == 8:
            print(f"GROW {my_last.organ_id} {my_last.x + 1} {my_last.y} TENTACLE E")
        elif my_last.y == 5:
            print(f"GROW {my_last.organ_id} {my_last.x + 1} {my_last.y} TENTACLE E")
        else:
            print(f"GROW {my_last.organ_id} {my_last.x + 1} {my_last.y + 1} TENTACLE E")'''


        #W4: if (myRoot.x, 16) not in grid.keys() or grid[(myRoot.x, 16)].owner == -1:
        '''W3: if not closest_a.harvested_by(grid)[0]:
            my_closest, distance, target_direction = closest_a.closest_by_taxicab(my_entities)

            if distance > 2:
                print(f"GROW {my_root.organ_id} 16 {my_root.y} BASIC basic chasing")
            elif distance == 2:
                if len(target_direction) == 1: # If protein is straight ahead
                    print(f"GROW {my_closest.organ_id} {closest_a.x} {my_closest.y} HARVESTER E {my_closest.organ_id} {target_direction}")
                    detour = True
                else: # If protein is diagonal
                    print(f"GROW {my_closest.organ_id} {closest_a.x} {my_closest.y} HARVESTER {target_direction[:1]} {target_direction} {target_direction[:1]}")

        else:
            if detour:
                print(f"GROW {my_last.organ_id} {my_last.x} {my_root.y+1} BASIC Detour")
                detour = False

            elif my_last.x < 16 and my_last.y < 5:
                print(f"GROW {my_last.organ_id} {16} {my_last.y} BASIC going")

            else:
                print(f"GROW {my_last.organ_id} {10} {6} BASIC going down")'''
