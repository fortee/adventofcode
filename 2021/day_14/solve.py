from collections import Counter
from collections import OrderedDict

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


# Create a dict that will give the new inserted value based on the key
for pair in split[1].split('\n'):
    if pair == '':
        continue
    pair_split = pair.split(' -> ')
    key = pair_split[0]
    pairs[key] = f"{key[0]}{pair_split[1]}{key[1]}"

knowns = {}

for i in range(10):
    new_poli = poli[0]

    # for key, val in knowns.items():
    #     if key in poli:
    
    from datetime import datetime
    st = datetime.now()
    
    for idx in range(len(poli) - 1):
        new_poli += pairs[poli[idx : idx + 2]][1:]
    print(f"R{i+1}: {datetime.now() - st}")
    knowns[poli] = new_poli
    poli = new_poli

char_count = dict(Counter(poli))
print(max(char_count.values()) - min(char_count.values()))
