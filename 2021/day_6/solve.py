# https://adventofcode.com/2021/day/6
from math import floor

with open(r"input.txt") as file:
    all_fish = [int(x) for x in file.readline().split(',')]
original_fish = all_fish.copy()

print(f"Initial state:  {all_fish}")

spawn_counter = [0 for x in all_fish]

days = 18
total_spawns = 0
for day in range(days):
    spawned_fish = []
    daily_fish = []
    for idx, fish in enumerate(all_fish):
        new = fish - 1 if fish > 0 else 6
        daily_fish.append(new)
        if fish == 0:
            spawned_fish.append(8)
    all_fish = daily_fish + spawned_fish
    # print(f"After {day+1:3} days: {spawn_counter} | {all_fish} | Spawned Fish: {total_spawns}")
print(f"Slow  solution: {len(all_fish)} | Spawned Fish: {total_spawns}")


print(f"")
spawn_rate = 7
spawned_fish = 0
news_fishes = original_fish.copy()
for day in range(days):
    for fish in news_fishes:
        remainder = spawn_rate - 1 - fish
        adjusted_days = remainder + day
        cycles = adjusted_days / spawn_rate
        spawned_fish += floor(cycles)
        # print(f"N: {fish} R: {remainder} A: {adjusted_days} C: {cycles} R: {n}")
result = len(original_fish) + spawned_fish
print(f"Quick solution: {result} | Spawned Fish: {spawned_fish}")