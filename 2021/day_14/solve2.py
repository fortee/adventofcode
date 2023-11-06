from collections import Counter, defaultdict

import argparse
from math import ceil

# Create the parser
parser = argparse.ArgumentParser(description="Process the steps.")

# Add the integer argument
parser.add_argument('steps', type=int, help='Number of steps')

# Parse the arguments
args = parser.parse_args()
steps = args.steps

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

with open(r"input") as file:
    data = file.read()

string, rules = data.split('\n\n')
pairs = {}

# Create a dict that will give the new inserted value based on the key
for pair in rules.split('\n'):
    if pair == '':
        continue
    key, value = pair.split(' -> ')
    pairs[key] = value


counts = defaultdict(int)
for i in range(len(string) - 1):
    found_pair = string[i : i + 2]
    counts[found_pair] += 1

for j in range(steps):
    overlaps = defaultdict(int)
    new_counts = defaultdict(int)
    for key, value in counts.items():
        overlaps[pairs[key]] += 1
        new_counts[f"{key[0]}{pairs[key]}"] += value
        new_counts[f"{pairs[key]}{key[1]}"] += value

    counts = new_counts

total_char_count = defaultdict(int)
for key, value in counts.items():
    for char, count in Counter(key).items():
        total_char_count[char] += count * value


for key, value in overlaps.items():
    total_char_count[key] = ceil(total_char_count[key]/2)

total_char_values = total_char_count.values()
print(f"Solution after {steps} rounds: {max(total_char_values)- min(total_char_values)}")
