import sys
import math

# Grow and multiply your organisms to end up larger than your opponent.

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

# game loop
while True:
    entity_count = int(input())
    entities = []
    myEntities = []
    enemyEntities = []
    walls = []
    proteins = []

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

    print(f"Walls:{walls}", file=sys.stderr, flush=True)
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


        print("WAIT")
