import sys
import math
# Score points by scanning valuable fish faster than your opponent.


class Creature:
    def __init__(self, creature_id, color, _type):
        self.creature_id = creature_id
        self.color = color
        self._type = _type

    def __str__(self):
        return f'ID:{self.creature_id}, C:{self.color}, T:{self._type}'


class VisibleCreature:  # Unscanned
    def __init__(self, creature_id, creature_x, creature_y, creature_vx, creature_vy):
        self.creature_id = creature_id
        self.x = creature_x
        self.y = creature_y
        self.creature_vx = creature_vx
        self.creature_vy = creature_vy

    def __str__(self):
        return f'ID:{self.creature_id} POS({self.x}, {self.y}), V:({(self.creature_vx, self)},  {(self.creature_vy, self)})'


class Drone:
    def __init__(self, drone_id, drone_x, drone_y, emergency, battery):
        self.drone_id = drone_id
        self.x = drone_x
        self.y = drone_y
        self.emergency = emergency
        self.battery = battery

    def __str__(self):
        return f'ID:{self}, ({self.x}, {self.y}), E:{emergency}, B:{self.battery}'


def creatures_in_big_light(d, target_x, target_y):

    if target_x == -1 and target_y == -1:
        future_x = d.x
        future_y = d.y-SINKING_IF_MOTOR_OFF
    else:
        distance = math.sqrt((d.x - target_x)**2 + (d.y - target_y)**2)
        future_x = d.x + (target_x - d.x) * MAX_MOVEMENT/distance
        future_y = d.y + (target_y - d.y) * MAX_MOVEMENT/distance
    print(f'Predicted pos: {future_x}, {future_y}', file=sys.stderr, flush=True)

    for c in visible_creatures.values():
        distance = math.dist([future_x, future_y], [c.x + c.creature_vx, c.y + c.creature_vy])
        if c.creature_id not in my_scanned_creatures and SCAN_RANGE < distance <= SCAN_RANGE_WITH_LIGHT:
            return "1"
    return "0"


def horizontal_target(d, current_target):
    print(f"pos: {d.x} target: {current_target}", file=sys.stderr, flush=True)
    if str(d.x) == current_target:
        current_target = "2000" if current_target == "8000" else "8000"
    return current_target


creature_count = int(input())
creatures = {}
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    creature = Creature(creature_id, color, _type)
    creatures[creature_id] = creature

# Constants
MAP_MAX_X = 9999
MAP_MAX_Y = 9999
MAP_ZONE_Y = 2500
MAX_MOVEMENT = 600
SINKING_IF_MOTOR_OFF = 300
SCAN_RANGE = 800  # Automatically scans creatures within range at end of turn
SCAN_RANGE_WITH_LIGHT = 2000
BATTERY_MAX = 30
BATTERY_RECHARGE = 1
BATTERY_DRAIN_WITH_LIGHT = 5
target_y = ""

# game loop
while True:
    my_score = int(input())
    foe_score = int(input())

    my_scan_count = int(input())
    my_scanned_creatures = {}
    for i in range(my_scan_count):
        creature_id = int(input())
        my_scanned_creatures[creature_id] = creatures[creature_id]

    foe_scan_count = int(input())
    foe_scanned_creatures = {}
    for i in range(foe_scan_count):
        creature_id = int(input())
        foe_scanned_creatures[creature_id] = creatures[creature_id]

    my_drone_count = int(input())
    my_drones = {}
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        drone = Drone(drone_id, drone_x, drone_y, emergency, battery)
        my_drones[drone_id] = drone

    foe_drone_count = int(input())
    foe_drones = {}
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        drone = Drone(drone_id, drone_x, drone_y, emergency, battery)
        foe_drones[drone_id] = drone

    drone_scan_count = int(input())
    drone_scans = {}
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        drone_scans[drone_id] = creatures[creature_id]

    visible_creature_count = int(input())
    visible_creatures = {}
    for i in range(visible_creature_count):
        creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
        creature = VisibleCreature(creature_id, creature_x, creature_y, creature_vx, creature_vy)
        visible_creatures[creature_id] = creature

    radar_blip_count = int(input())
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]

    for i in range(my_drone_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>
        d = my_drones[i]
        print(d.battery, file=sys.stderr, flush=True)

        if d.y == 500:  # Starting y
            target_x_changed = 0
            target_x = 2000 if d.x < 5000 else 8000
            target_y = 4500
        if d.y < target_y:
            print(f"MOVE {target_x} {target_y} {creatures_in_big_light(d, target_x, target_y)}")
        elif d.y == target_y:
            if d.x == target_x:
                if target_x_changed == 0:
                    target_x = 2000 if target_x == 8000 else 8000
                    target_x_changed = 1
                else:
                    target_x_changed = 0
                    target_y = 8000
            print(f"MOVE {target_x} {target_y} {creatures_in_big_light(d, target_x, target_y)}")
        elif len(my_scanned_creatures) < 12:
            print(f"MOVE {horizontal_target(d, target_x)} 8750 {creatures_in_big_light(d)}")
        else: print("WAIT 1")
