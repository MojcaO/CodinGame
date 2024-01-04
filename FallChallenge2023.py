import sys
import math

# Score points by scanning valuable fish faster than your opponent.


class Creature:
    def __init__(self, creature_id, color, _type):
        self.creature_id = creature_id
        self.color = color
        self._type = _type


class VisibleCreature: # Unscanned
    def __init__(self, creature_id, creature_x, creature_y, creature_vx, creature_vy):
        self.creature_id = creature_id
        self.creature_x = creature_x
        self.creature_y = creature_y
        self.creature_vx = creature_vx
        self.creature_vy = creature_vy


class Drone:
    def __init__(self, drone_id, drone_x, drone_y, emergency, battery):
        self.drone_id = drone_id
        self.drone_x = drone_x
        self.drone_y = drone_y
        self.emergency = emergency
        self.battery = battery


creature_count = int(input())
creatures = {}
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    creature = Creature(creature_id, color, _type)
    creatures[creature_id] = creature

# Constants
MAP_MAX_X = 9999
MAP_MAX_Y = 9999
MAX_MOVEMENT = 600
SINKING_IF_MOTOR_OFF = 300
SCAN_RANGE = 800 # Automatically scans creatures within range at end of turn
SCAN_RANGE_WITH_LIGHT = 2000
BATTERY_MAX = 30
BATTERY_RECHARGE = 1
BATTERY_DRAIN_WITH_LIGHT = 5

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

        print("WAIT 1")
