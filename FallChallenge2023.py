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
        self.blips = {}
        self.currentScans = []
        self.role = ""
        self.target_x = 0
        self.target_y = 0
        self.target_x_changed = 0

    def __str__(self):
        return f'ID:{self.drone_id}, ({self.x}, {self.y}), E:{emergency}, B:{self.battery}'

    def add_blip(self, creature_id, radar):
        self.blips[creature_id] = [radar]


    def add_scan(self, creature_id):
        self.currentScans.append(creature_id)


def creatures_in_big_light(d, target_x, target_y):

    if target_x == -1 and target_y == -1:
        future_x = d.x
        future_y = d.y-SINKING_IF_MOTOR_OFF
    else:
        distance = math.sqrt((d.x - target_x)**2 + (d.y - target_y)**2)
        if distance == 0: distance = 1
        future_x = d.x + (target_x - d.x) * MAX_MOVEMENT/distance
        future_y = d.y + (target_y - d.y) * MAX_MOVEMENT/distance
    print(f'Predicted pos: {future_x}, {future_y}', file=sys.stderr, flush=True)

    for c in visible_creatures.values():
        distance = math.dist([future_x, future_y], [c.x + c.creature_vx, c.y + c.creature_vy])
        if c.creature_id not in my_scanned_creatures and SCAN_RANGE < distance <= SCAN_RANGE_WITH_LIGHT:
            return "1"
    return "0"


def light(d):
    if d.y > 2000 and not d.target_y == SURFACE_Y:
        return "1" if not turn_counter % 4 else "0"
    else:
        return "0"


def horizontal_target(d, current_target):
    print(f"pos: {d.x} target: {current_target}", file=sys.stderr, flush=True)
    if str(d.x) == current_target:
        current_target = "2000" if current_target == "8000" else "8000"
    return current_target


# Constants
MAP_MAX_X = 9999
MAP_MAX_Y = 9999
SURFACE_Y = 500
MAP_ZONE_Y = 2500
MAX_MOVEMENT = 600
SINKING_IF_MOTOR_OFF = 300
SCAN_RANGE = 800  # Automatically scans creatures within range at end of turn
SCAN_RANGE_WITH_LIGHT = 2000
BATTERY_MAX = 30
BATTERY_RECHARGE = 1
BATTERY_DRAIN_WITH_LIGHT = 5
turn_counter = 0

# Initialization Input
creature_count = int(input())
creatures = {}
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    creature = Creature(creature_id, color, _type)
    creatures[creature_id] = creature

# game loop
while True:
    turn_counter += 1
    my_score = int(input())
    foe_score = int(input())

    my_scan_count = int(input()) # Amount of SAVED scans
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
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        if turn_counter == 1:
            if i == 0:
                my_drones = {}
            drone = Drone(drone_id, drone_x, drone_y, emergency, battery)
            my_drones[drone_id] = drone
            # all_drones[drone_id] = drone
            for d in my_drones.values():
                d.role = "righty" if d.x == max([dr.x for dr in my_drones.values()]) else "lefty" # Drone with higher x goes right
        else:
            drone = my_drones[drone_id]
            drone.x = drone_x
            drone.y = drone_y
            drone.emergency = emergency
            drone.battery = battery

    foe_drone_count = int(input())
    foe_drones = {}
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        drone = Drone(drone_id, drone_x, drone_y, emergency, battery)
        foe_drones[drone_id] = drone
        #all_drones[drone_id] = drone

    drone_scan_count = int(input()) # Scans currently within a drone
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        if drone_id in my_drones:
            my_drones[drone_id].add_scan(creatures[creature_id])
        else:
            foe_drones[drone_id].add_scan(creatures[creature_id])

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
        my_drones[drone_id].add_blip(creature_id, radar)

    for d in my_drones.values():
        print(d.battery, file=sys.stderr, flush=True)

        if d.y == SURFACE_Y and turn_counter == 1:
            d.target_x_changed = 0
            if d.role == "lefty":
                d.target_x = 2000
                d.target_y = 4500
            else:
                d.target_x = 8000
                d.target_y = 8750

        if d.y < d.target_y:
            print(f"MOVE {d.target_x} {d.target_y} {light(d)}")

        elif d.y == d.target_y:
            if d.x == d.target_x:
                if d.target_x_changed == 0:
                    d.target_x = 2000 if d.target_x == 8000 else 8000
                    d.target_x_changed = 1
                else:
                    d.target_x_changed = 0
                    d.target_y = SURFACE_Y
            print(f"MOVE {d.target_x} {d.target_y} {light(d)}")
        elif d.y > d.target_y:
            print(f"MOVE {d.target_x} {d.target_y} 0")
        else:
            print("WAIT 1 ok")
