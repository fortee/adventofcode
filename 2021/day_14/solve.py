from collections import Counter

import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process the steps.")

# Add the integer argument
parser.add_argument('steps', type=int, help='Number of steps')

# Parse the arguments
args = parser.parse_args()
steps = args.steps

with open(r"input") as file:
    data = file.read()
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

split = data.split('\n\n')
poli = split[0]
pairs = {}
total_calls = 0


# Create a dict that will give the new inserted value based on the key
for pair in split[1].split('\n'):
    if pair == '':
        continue
    pair_split = pair.split(' -> ')
    key = pair_split[0]
    pairs[key] = f"{key[0]}{pair_split[1]}{key[1]}"

poli = "NNCB"
for i in range(steps):
    new_poli = poli[0]
    for idx in range(len(poli) - 1):
        total_calls +=1
        new_poli += pairs[poli[idx : idx + 2]][1:]
    poli = new_poli



print(f"TOTAL CALLS: {total_calls}")
char_count = dict(Counter(poli))
cmax = max(char_count.values())
cmin =  min(char_count.values())
print(f"MAX: {cmax}")
print(f"MIN: {cmin}")
print(f"Solution after {steps} rounds: {cmax- cmin}")
