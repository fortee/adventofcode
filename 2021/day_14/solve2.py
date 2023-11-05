from collections import Counter, defaultdict
from collections import OrderedDict

import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process the steps.")

# Add the integer argument
parser.add_argument('steps', type=int, help='Number of steps')

# Parse the arguments
args = parser.parse_args()
steps = args.steps


"""
CCNBCNCCN
CCNBCNCCN
CNCCNBBBCCNBCNCCN
"""

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

# with open(r"input") as file:
# data = file.read()

split = data.split('\n\n')
poli = split[0]
known = defaultdict(lambda: defaultdict(str))

# Create a dict that will give the new inserted value based on the key
for item in split[1].split('\n'):
    if item == '':
        continue
    pair_split = item.split(' -> ')
    key = pair_split[0]
    known[key][1] = f"{key[0]}{pair_split[1]}{key[1]}"


def get_pairs(string):
    length = len(string)
    return [string[i : i + 2] for i in range(0, length) if i + 2 <= length]


# poli="NN"
total_calls = 0


def get_known(input, lvl):
    known_data = known.get(input, None)
    if not known_data:
        return input, 0
    max_known_lvl = max([x for x in known_data.keys() if x <= lvl])
    return known_data[max_known_lvl], max_known_lvl


def mprint(msg):
    return
    print(msg)

calc = defaultdict(lambda: defaultdict(int))

def calculate(input, lvl):
    calc[input][lvl] +=1
    
    # Get the highest existing level
    known_value, known_lvl = get_known(input, lvl)

    # Or further process the string
    new_value = ''
    pairs = get_pairs(known_value)
    # Adjust the lvl requirement with on the existing max level
    sub_lvl = max(lvl - known_lvl, 1)
    mprint(" " * ((int(steps - lvl)) * 2) + f"{input} | CALCULATE: {pairs} | LVL: {lvl}")
    for pair in pairs:
        pair_output = process(pair, sub_lvl)
        new_value += pair_output[1:] if new_value else pair_output
    
    known[known_value][sub_lvl] = new_value
    known[input][lvl] = new_value
    return new_value


def process(input, lvl):
    global total_calls
    total_calls += 1
    # Try to get the existing data for the given level
    known_value = known.get(input, {}).get(lvl, None)
    if known_value:
        # We already know the value of the processed string, so just return it
        mprint(" "*((steps-lvl)*4)+f"{input} | KNOWN: {known_value} | LVL: {lvl}")
        return known_value
    print(lvl)
    mprint(" " * ((steps - lvl) * 2) + f"{input} | LVL: {lvl}")

    new_value = calculate(input, lvl)
    mprint(" " * ((int(steps - lvl)) * 2) + f"{input} | CALCULATED: {new_value} | LVL: {lvl}")
    mprint(" " * ((int(steps - lvl)) * 2) + "-" * 25)
    # print(f"{input} | CALCULATED | LVL: {lvl}")
    return new_value


poli = process(poli, steps)
# print(f"TOTAL CALLS: {total_calls}")
char_count = dict(Counter(poli))
print(f"SOLUTION: {max(char_count.values()) - min(char_count.values())}")
