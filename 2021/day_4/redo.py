with open(r"input.txt") as file:
    data = file.read()

# data = """
# ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm

# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929

# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm

# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in
# """

required_strings = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
required_amount = len(required_strings) - 1
import re

valid = 0
for passport in data.split('\n\n'):
    blocks = list(filter(None, re.split(r'[\n\s]+', passport)))
    if len(blocks) < required_amount:
        continue

    keys = 0
    for block in blocks:
        key_value = block.split(':')
        key = key_value[0]
        value = key_value[1]
        if key != 'cid' and key in required_strings:
            keys += 1
    if keys == required_amount:
        valid += 1
print(valid)
