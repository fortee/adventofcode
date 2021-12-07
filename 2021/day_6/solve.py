# https://adventofcode.com/2021/day/6
from datetime import datetime
from math import floor
from os import path

with open(r"input.txt") as file:
    all_fish = [int(x) for x in file.readline().split(',')]

for part, days in enumerate([80, 256]):
    known_spawns = {}
    def spawn_fish(fish, birthday):
        """
        Find the amount of spawned fish based on the fish value and it's birth date
        """
        combination = (fish, birthday)  # Tuple to identify the fish birthday combo

        if combination in known_spawns:
            # If we already encountered this combination, just return it's value
            # Dynamic proghraming ftw
            return known_spawns[combination]

        total = 1

        # The first day this fish will spawn
        spawn_date = fish + birthday + 1

        # Iterate until the max number of days
        while spawn_date <= days:
            # Recursion to find how many the spawned fish will spawn
            total += spawn_fish(8, spawn_date)
            spawn_date += 7

        # Save this value so we can look it up in the future
        known_spawns[combination] = total
        return total

    total_fish = 0
    for fish in all_fish:
        total_fish += spawn_fish(fish, 0)
    print(f"Part {part+1}: {total_fish}")