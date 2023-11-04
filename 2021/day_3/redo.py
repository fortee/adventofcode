with open(r"input.txt") as file:
    # Clean the input, this is an extra loop but we don't really care
    data = [x.strip() for x in file.readlines()]

values = []
for i in data[0]:
    values.append(0)

for line in data:
    for idx, value in enumerate(line):
        values[idx] += int(value)

gamma = []
epsilon = []
row_count = len(data)
for value in values:
    if value > row_count / 2:
        gamma.append(1)
        epsilon.append(0)
    else:
        gamma.append(0)
        epsilon.append(1)


gamma_decimal = int(''.join([str(x) for x in gamma]), 2)
epsilon_decimal = int(''.join([str(x) for x in epsilon]), 2)

print(gamma_decimal * epsilon_decimal)
