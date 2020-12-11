# https://adventofcode.com/2020/day/19
from collections import defaultdict


class Solution:
    def __init__(self, part):
        self.messages = set()
        self.rules = defaultdict(lambda: {'sub_rules': [], 'rule_strings': set(), 'child_ids': set()})
        self.base_rules = []
        self.part = part
        # The currently active cubes active
        # self.input_file = "input_part1.txt"
        # self.input_file = "input_test.txt"
        self.input_file = "input_part2.txt"
        # self.input_file = "input_test2.txt"
        self.process_input()

    def process_input(self):
        """
        Parse the input file
        """

        rules_block = True

        with open(self.input_file) as file:

            for line in file.readlines():

                if line == '\n':
                    rules_block = False
                    continue

                if rules_block:

                    res = line.strip().split(':')
                    rule_id = int(res[0])

                    if '"' in line:
                        # This is a base rule
                        self.rules[rule_id]['rule_strings'].add(res[1].replace('"', '').strip())
                        self.base_rules.append(int(res[0]))
                        continue

                    for rule in res[1].split('|'):
                        self.rules[rule_id]['sub_rules'].append([int(x) for x in rule.strip().split(' ')])

                else:
                    self.messages.add(line.strip())

    def solve(self):

        rule_id = 0
        self.rules[rule_id]['rule_strings'] = self.get_rule_strings(rule_id=rule_id)

        # Get messages that are allowed by the rules
        good_messages = self.messages & self.rules[rule_id]['rule_strings']

        if self.part == 2:
            # We need to the check the messages for all the possible rule results from the infinite loops
            valid_for_infinite_loops = self.filter_for_loop_rules()
            good_messages |= valid_for_infinite_loops

        print(f"Part {self.part}: {len(good_messages)}")

    def filter_for_loop_rules(self):

        # Stupid way of getting the length of the rules in `31` & `42`
        rule_lengths = {
            len(x) for x in set.union(*[self.rules[42]['rule_strings'], self.rules[31]['rule_strings']])
        }
        assert len(rule_lengths) == 1
        rule_length = list(rule_lengths)[0]  # We know by experience that this is 5 for tests and 8 for the real input

        filtered_messages = set()
        for message in self.messages:
            # Loop over all messages

            original_message = message
            message_length = len(message)

            if (
                message[:rule_length] not in self.rules[42]['rule_strings']
                or message[message_length - rule_length :] not in self.rules[31]['rule_strings']
            ):
                # If the message doesn't start with a rule_string from `42`
                # or ends with one from `31` it can't be a valid for rule 0
                continue

            # Reverse engineer the Infinite Loop Rules `8` and `11`
            if self.peel(message) == '':
                # Empty string means the message obeys all possible infinite loop rules
                filtered_messages.add(original_message)

        return filtered_messages

    def peel(self, message):
        """

        The idea is that all messages that are valid by the Infinite Loop rules `8` and `31`
        at least must have an equal number of 31 and 42 strings as a result of rule `11`,
        if we remove all of those we should still have left at least one `42` string as a result of rule `8`.

        Possible variants of rule 8 ~> `42 | 42 8`:
            - 42
            - 42 (42)
            - 42 42 (42)
            - 42 42 42 (42)
            - 42 42 42 42 (42)

        Possible variants of rule 11 ~> `42 31 | 42 11 31`:
            - 42 31
            - 42 (42 31) 31
            - 42 (42 42 31 31) 31
            - 42 (42 42 42 31 31 31) 31
            - 42 (42 42 42 42 31 31 31 31) 31

        These result in the following rule 0 -> 8 11
            - 42 42 31
            - 42 42 42 42 31 31
            - 42 42 42 42 42 42 31 31 31
            - 42 42 42 42 42 42 42 42 31 31 31 31
            - 42 42 42 42 42 42 42 42 42 42 31 31 31 31 31

        There could be many more variants if we mix the "normal" and "infinite" sub_rule blocks of rule `8` and `11`
        """

        rounds_31 = 0
        # Remove all the rule `31` strings from the end of the strings
        while True:
            message, valid = self.remove_rule_31(message)
            if not valid:
                break
            rounds_31 += 1

        # There must be as many rule `42`s as rule `31`
        for i in range(rounds_31):
            message, valid = self.remove_rule_42(message)
            if not valid:
                # We should be able to remove as many 42's as 31's
                # If this is not the case the message is invalid
                return False

        if not message:
            # We should have some strings left after we remove the base 31 & 42
            # The from the rule `8`
            return False

        # Remove rule 42 strings until we are left with an empty string
        # or something breaks, which would mean this message is not valid
        while message:
            message, valid = self.remove_rule_42(message)
            if not valid:
                break

        return message

    def remove_rule_42(self, message):
        """
        Try to remove a rule_string 42 from the start of the message
        If possible return the message without that rule_string or return False
        """

        for rule_string in self.rules[42]['rule_strings']:

            if message[: len(rule_string)] != rule_string:
                # This message doesn't start with this rule_string from rule 42
                continue

            # Remove the rule_string 42 from the message
            new_message = message[len(rule_string) :]
            return new_message, True

        return message, False

    def remove_rule_31(self, message):
        """
        Try to remove a rule_string 31 from the end of the message
        If possible return the message without that rule_string or return False
        """

        for rule_string in self.rules[31]['rule_strings']:

            if message[len(message) - len(rule_string) :] != rule_string:
                # This message doesn't start with this rule_string from rule 31
                continue

            # Remove the rule_string 31 from the message
            new_message = message[: len(message) - len(rule_string)]
            return new_message, True

        return message, False

    def get_rule_strings(self, rule_id):

        parent_rule_strings = set()
        parent_rule = self.rules[rule_id]

        for sub_rules in parent_rule['sub_rules']:

            if rule_id in sub_rules:
                # We don't want to calculate infinite loops
                continue

            sub_rule_strings = set()
            for sub_rule_id in sub_rules:

                sub_rule = self.rules[sub_rule_id]

                if not sub_rule['rule_strings']:
                    # If the strings were not set previously do it now
                    sub_rule['rule_strings'] = self.get_rule_strings(sub_rule_id)

                if not sub_rule_strings:
                    # If no strings were set for these sub rules
                    # We don't need to loop we can just directly set it
                    sub_rule_strings = sub_rule['rule_strings']
                else:
                    # If strings were set previously
                    # we need to loop trough all of them and add this sub_rules strings
                    # We collect these in a new set and replace the old one at the end

                    new_rule_strings = set()
                    for rule_string in sub_rule_strings:
                        for sub_rule_string in sub_rule['rule_strings']:
                            new_rule_strings.add(f"{rule_string}{sub_rule_string}")

                    sub_rule_strings = new_rule_strings
            parent_rule_strings |= sub_rule_strings

        return parent_rule_strings


Solution(part=1).solve()
Solution(part=2).solve()
