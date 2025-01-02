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
        BASIC for a BASIC type organ
        A for an A protein source
    - owner:
        1 if you are the owner of this organ
        0 if your opponent owns this organ
        -1 if this is not an organ
    - organId: unique id of this entity if it is an organ, 0 otherwise
    - organDir: N, W, S, or E, not used in this league
    - organParentId: if it is an organ, the organId of the organ that this organ grew from (0 for ROOT organs), else 0.
    - organRootId: if it is an organ, the organId of the ROOT that this organ originally grew from, else 0.

Next line: 4 integers: myA,myB,myC,myD for the amount of each protein type you have.
Next line: 4 integers: oppA,oppB,oppC,oppD for the amount of each protein type your opponent has.
Next line: the integer requiredActionsCount which equals 1 in this league.

## Output
A single line with your action: GROW id x y type : attempt to grow a new organ of type type at location x, y from organ 
with id id. If the target location is not a neighbour of id, the organ will be created on the shortest path to x, y.
'''

# width: columns in the game grid
# height: rows in the game grid
width, height = [int(i) for i in input().split()]

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


class Tile:
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


# game loop
while True:
    entity_count = int(input())
    entities = []
    myEntities = []
    enemyEntities = []
    walls = []
    proteins = []
    tiles = []
    grid = {}

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
            myEntities.append(entity)
        elif owner == 0:
            enemyEntities.append(entity)
        else: # neutral
            if _type == 'WALL':
                walls.append(entity)
            elif _type == 'A' or _type == 'B' or _type == 'C' or _type == 'D':
                proteins.append(entity)
        # print(f"Entity added:{entity}", file=sys.stderr, flush=True)
        tile = Tile(x, y, entity)
        tiles.append(tile)
        grid[(x, y)] = tile


    #print(f"Walls:{walls}", file=sys.stderr, flush=True)
    print(f"Proteins:{proteins}", file=sys.stderr, flush=True)
    print(f"MyEntities:{myEntities}", file=sys.stderr, flush=True)
    print(f"EnemyEntities:{enemyEntities}", file=sys.stderr, flush=True)

    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]

    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order
    for i in range(required_actions_count):

        # Write an action using print, example: "GROW id x y type"
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # Wood League Logic
        # if the tile on the right side of my Root entity is empty, go there
        myRoot = myEntities[0]
        if (myRoot.x, 16) not in grid.keys() or grid[(myRoot.x, 16)].entity.owner == -1:
            print(f"GROW {myRoot.organ_id} {16} {myRoot.y} BASIC")
        elif myRoot.x == 1:
            print("WAIT")
