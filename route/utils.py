import math
import decimal

from fare.models import Fare

valid_mrt_stations = [
    'Taft Avenue Station',
    'Magallanes Station',
    'Ayala Station',
    'Buendia Station',
    'Guadalupe Station',
    'Boni Avenue Station',
    'Shaw Boulevard Station',
    'Ortigas Avenue Station',
    'Santolan Anapoils Station',
    'Cubao Station',
    'GMA - Kamuning Station',
    'Quezon Avenue Station',
    'North Avenue Station',
]

def calculate_train_cost(origin_station, destination_station):
    difference = abs(decimal.Decimal(valid_mrt_stations.index(origin_station)) - decimal.Decimal(valid_mrt_stations.index(destination_station))) + 1

    if difference > 0 and difference < 3:
        return 10
    elif difference >= 3 and difference <= 5:
        return 11
    elif difference >= 6 and difference <= 8:
        return 12
    elif difference >= 9 and difference < 12:
        return 14
    else:
        return 15


def calculate_cost(mode, distance):
    mode = str(mode)
    base = Fare.objects.get(mode=mode).base
    increment = Fare.objects.get(mode=mode).increment
    base_distance = decimal.Decimal(4)
    distance = decimal.Decimal(distance)

    if mode == 'Jeep':
        if distance > base_distance:
            distance -= base_distance
            add_per_km = distance * increment
            return math.ceil((base + add_per_km)*100/100)
        else:
            return base
    elif mode == 'Bus':
        if distance > base_distance:
            distance -= base_distance
            add_per_km = distance * increment
            return math.ceil((base + add_per_km)*100/100)
        else:
            return base

def get_city(city):
    count = 0
    for letter in city:
        if letter != ',':
            count += 1
        else:
            return city[count:].strip(',').strip(' ')

def distance_total(lists):
    path = lists.path.all()
    train_path = lists.train_path.all()
    total = 0

    for x in path:
        total += x.distance

    for x in train_path:
        total += x.distance

    return total


def cost_total(lists):
    path = lists.path.all()
    train_path = lists.train_path.all()
    total = 0

    for x in path:
        total += x.cost

    for x in train_path:
        total += x.cost

    return total
