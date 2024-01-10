import sys
import math


# Score points by scanning valuable fish faster than your opponent.


class Creature:
    def __init__(self, creature_id, color, _type):
        self.creature_id = creature_id
        self.color = color
        self._type = _type
        self.scanned_by_my_drones = []
        self.scanned_by_foe_drones = []

    def __str__(self):
        return f'ID:{self.creature_id}, C:{self.color}, T:{self._type}'


class VisibleCreature:
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
        self.current_scans = []
        self.role = ""
        self.target_x = 0
        self.target_y = 0
        self.target_x_changed = 0

    def __str__(self):
        return f'ID:{self.drone_id}, ({self.x}, {self.y}), E:{emergency}, B:{self.battery}'

    def add_blip(self, creature_id, radar):
        self.blips[creature_id] = radar

    def add_scan(self, creature_id):
        self.current_scans.append(creature_id)


def monsters_nearby_next_turn(d):
    if d.target_x == -1 and d.target_y == -1:
        future_x = d.x
        future_y = d.y - SINKING_IF_MOTOR_OFF
    else:
        distance = math.sqrt((d.x - d.target_x) ** 2 + (d.y - d.target_y) ** 2)
        if distance == 0: distance = 1
        future_x = d.x + (d.target_x - d.x) * MAX_MOVEMENT / distance
        future_y = d.y + (d.target_y - d.y) * MAX_MOVEMENT / distance
    # print(f'Predicted pos: {future_x}, {future_y}', file=sys.stderr, flush=True)

    monsters = {}
    for vc in visible_creatures.values():
        if creatures[vc.creature_id]._type == -1:
            print(f"M{vc.creature_id} pos: {vc.x} {vc.y} v: {vc.creature_vx} {vc.creature_vy}", file=sys.stderr,
                  flush=True)
            distance = math.dist([future_x, future_y], [vc.x + vc.creature_vx, vc.y + vc.creature_vy])
            monsters[vc.creature_id] = distance
    return monsters


def light(d):
    monster_counter = 0
    for distance in monsters_nearby_next_turn(d).values():
        if distance <= 2000:
            monster_counter += 1

    if d.y < 2000 or turn_counter % 4 or monster_counter:
        return "0 " + str(monster_counter)
    else:
        return "1"


def horizontal_target(d, current_target):
    print(f"pos: {d.x} target: {current_target}", file=sys.stderr, flush=True)
    if str(d.x) == current_target:
        current_target = "2000" if current_target == "8000" else "8000"
    return current_target


def find_unscanned_fish():
    unscanned = []
    for c in creatures.values():
        if (c._type > -1 and c.creature_id not in my_scanned_creatures.keys()
                and len(c.scanned_by_my_drones) == 0):
            unscanned.append(c)
    # filter extinct
    extinct = find_extinct_fish(unscanned)
    return list(filter(lambda i: i not in extinct, unscanned))


def find_extinct_fish(unscanned_fish):
    for f in unscanned_fish:
        for d in my_drones.values():
            if f not in fish_out_of_bounds and ((d.x == MAP_MAX_X and "R" in d.blips[f.creature_id]) \
                    or (d.x == 0 and d.y == MAP_MAX_Y and "BL" in d.blips[f.creature_id])):
                # x<0 is harder to determine because d.x==f.x shows as "L" in radar
                fish_out_of_bounds.append(f)
                print(f"{f.creature_id} extinct", file=sys.stderr, flush=True)
    return fish_out_of_bounds


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

# Initialization Input
turn_counter = 0
fish_out_of_bounds = []
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

    my_scan_count = int(input())  # Amount of SAVED scans
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
                d.role = "righty" if d.x == max(
                    [dr.x for dr in my_drones.values()]) else "lefty"  # Drone with higher x goes right
        else:
            drone = my_drones[drone_id]
            monsters_nearby_next_turn(drone)
            drone.x = drone_x
            drone.y = drone_y
            drone.emergency = emergency
            drone.battery = battery
            if emergency:
                print(f"Emergency! D{drone_id} lost scans {drone.current_scans}", file=sys.stderr, flush=True)
                for creature_id in drone.current_scans:
                    if drone_id in creatures[creature_id].scanned_by_my_drones:
                        creatures[creature_id].scanned_by_my_drones.remove(drone_id)
                drone.current_scans = []

    foe_drone_count = int(input())
    foe_drones = {}
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        drone = Drone(drone_id, drone_x, drone_y, emergency, battery)
        foe_drones[drone_id] = drone
        # all_drones[drone_id] = drone

    drone_scan_count = int(input())  # Scans currently within a drone
    for drone in my_drones.values() or foe_drones.values():
        drone.current_scans = []
    for creature in creatures.values():
        creature.scanned_by_my_drones = []
        creature.scanned_by_foe_drones = []
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        if drone_id in my_drones:
            my_drones[drone_id].current_scans.append(creature_id)
            creatures[creature_id].scanned_by_my_drones.append(drone_id)
        else:
            foe_drones[drone_id].current_scans.append(creature_id)
            creatures[creature_id].scanned_by_foe_drones.append(drone_id)

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

        if d.y == SURFACE_Y:
            if turn_counter == 1:
                d.target_x_changed = 0
                if d.role == "lefty":
                    d.target_x = 2000
                    d.target_y = 4500
                else:
                    d.target_x = 8000
                    d.target_y = 8750
            else:
                d.currentScans = []
                if my_scan_count < 12:
                    if find_unscanned_fish():
                        d.role = "hunting"
        if d.role == "hunting":
            hunted_fish = find_unscanned_fish()
            if hunted_fish:
                prey = hunted_fish[0]
                d.target_y = d.y + 600 if "B" in d.blips[prey.creature_id] else d.y - 600
                d.target_x = d.x + 600 if "R" in d.blips[prey.creature_id] else d.x - 600
            else:
                d.role == "done :)"
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
            print(f"MOVE {d.target_x} {d.target_y} {light(d)}")
        else:
            print("WAIT 1 ok")
