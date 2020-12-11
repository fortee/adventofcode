# https://adventofcode.com/2020/day/4
import re
import shlex

required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])
int_validation_rules = {
    'byr': {'digits': 4, 'min': 1920, 'max': 2002},
    'iyr': {'digits': 4, 'min': 2010, 'max': 2020},
    'eyr': {'digits': 4, 'min': 2020, 'max': 2030},
    'pid': {'digits': 9},
}


def is_valid_int(key, value):
    """
    Try to validate the key value pair based on teh int rules
    """

    rule = int_validation_rules.get(key, False)

    if not rule:
        # We don't need to validate this key value pair as an int
        return True

    if rule.get('digits', False) and len(value) != rule['digits']:
        # Value has the wrong number of digits
        return False

    if rule.get('min', False) and not (rule['min'] <= int(value) <= rule['max']):
        # Value is outside of allowed range
        return False

    return True


def is_valid_hgt(key, value):
    """
    Specific validation for the `hgt` key
    """

    if key != 'hgt':
        # We only care about the `hgt` field
        return True

    unit_rules = {
        'cm': {'min': 150, 'max': 193},
        'in': {'min': 59, 'max': 76},
    }

    def validate(unit, value):
        height = int(value.replace(unit, ''))
        rule = unit_rules[unit]
        if rule['min'] <= height <= rule['max']:
            return True
        return False

    # Check the value against any rules that apply
    for unit in unit_rules.keys():
        if unit in value:
            return validate(unit, value)


def is_valid_hcl(key, value):
    """
    Specific validation for the `hcl` key
    """

    if key != 'hcl':
        # We only care about the `hcl` field
        return True

    if '#' not in value:
        return False

    code = re.findall('[a-f0-9]+', value)[0]
    if len(code) != 6:
        return False

    return True


def is_valid_ecl(key, value):
    """
    Specific validation for the `ecl` key
    """

    if key != 'ecl':
        # We only care about the `ecl` field
        return True

    valid_values = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    if len(value) != 3:
        # We only have 3 letter valid values
        return False

    if value not in valid_values:
        return False

    return True


def is_valid(passport, part2=False):
    """
    Validate the password data
    """

    # Find difference between fields
    diff = required_fields - set(passport.keys())

    if diff and diff != {'cid'}:
        # The passport counts as valid if no or only the `cid` field is missing
        return False

    if part2:
        # Extra checks if we do part2
        for key, value in passport.items():
            # Validate the values of the fields

            if not is_valid_int(key, value):
                return False

            if not is_valid_hgt(key, value):
                return False

            if not is_valid_hcl(key, value):
                return False

            if not is_valid_ecl(key, value):
                return False

    return True


# Get passport data
def get_passports(part2=False):

    passports = []

    with open(r"input.txt") as file:
        passport = {}
        lines = file.readlines()
        last_line = lines[-1]

        # Iterate over all lines
        for line in lines:

            if line == '\n':
                # An empty line signals that a new password block starts

                # Add the current passport
                if is_valid(passport, part2):
                    passports.append(passport)

                # Start a new passport
                passport = {}
                continue

            # Convert the string to an array based on white spaces
            line_data = shlex.split(line)

            # Iterate over the key value pairs
            for string in line_data:
                # Break the string into key value pairs
                pair = re.findall('(.*):(.*)', string)[0]
                # Add it to the current password
                passport[pair[0]] = pair[1].replace('\n', '')

            if line == last_line:
                # We also need to account for the end of file (last line)
                # Add the current passport
                if is_valid(passport, part2):
                    passports.append(passport)
    return passports


print(f'Part 1: {len(get_passports())}')
print(f'Part 2: {len(get_passports(part2=True))}')
