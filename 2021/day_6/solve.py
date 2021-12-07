# https://adventofcode.com/2021/day/6

with open(r"input.txt") as file:
    all_fish = [int(x) for x in file.readline().split(',')]

# `80` and `256` are the two puzzle part days
for part, days in enumerate([80, 256]):
    known_spawns = {}

    def spawn_fish(fish, birthday):
        """
        Find the amount of spawned fish based on the fish value and its birthday
        """

        # Tuple to identify the fish birthday combination
        combination = (fish, birthday)

        if combination in known_spawns:
            # Dynamic programing ftw: If we already encountered this combination, just return the already calculated value
            return known_spawns[combination]

        # The first day this fish will spawn
        spawn_date = fish + birthday + 1

        # Keep track of the total spawns
        total = 1

        # Iterate until the max number of days
        while spawn_date <= days:
            # Recursion to find how many the spawned fish will spawn
            # `8` based on the puzzle ruleset
            total += spawn_fish(8, spawn_date)
            # `7` days is the birth cycle
            spawn_date += 7

        # Save this value so we can look it up in the future
        known_spawns[combination] = total
        return total

    total_fish = 0
    for fish in all_fish:
        total_fish += spawn_fish(fish, 0)
    print(f"Part {part+1}: {total_fish}")
