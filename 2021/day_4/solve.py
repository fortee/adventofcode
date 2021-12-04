# https://adventofcode.com/2021/day/3
from collections import defaultdict

with open(r"input.txt") as file:

    # Set the defaults
    board = {}
    boards = []
    winning_numbers = False
    for line in file.readlines():
        # Loop trough all lines

        if not winning_numbers:
            # Set the input numbers from the first line
            winning_numbers = [int(x) for x in line.strip().split(',')]
            continue

        if line == '\n':
            # If this is an empty line
            if board:
                # Save the current board
                boards.append(board)
            # And start a new board
            board = []
            continue
        else:
            # Add the line numbers as integers to the board
            board.append([int(x) for x in line.strip().split()])

    # After we looped trough all lines we still need to save the last board
    boards.append(board)


def is_finished(row_or_column):
    # If the row or column has 5 numbers it won
    return len(row_or_column) >= 5


def get_winners():

    # Set the defaults
    finished_boards = []
    first_winner = last_winner = False
    marked = defaultdict(
        lambda: {'rows_matching': defaultdict(list), 'colums_matching': defaultdict(list), 'matching': []}
    )

    # We need to loop trough the winning numbers first
    # so we find the winning boards in order
    for winning_number in winning_numbers:
        for board_idx, board in enumerate(boards):

            # We only care about boards that are non finished
            # This will also speed up the process
            if board_idx in finished_boards:
                continue

            # Loop trough each row and each number
            for row_idx, row in enumerate(board):
                for column_idx, number in enumerate(row):

                    if number != winning_number:
                        # Skip the number if it's not what we are looking for
                        continue

                    # Save all winning numbers
                    # We save columns and all matching so we don't have to loop trough them once again
                    marked[board_idx]['matching'].append(number)
                    marked[board_idx]['rows_matching'][row_idx].append(number)
                    marked[board_idx]['colums_matching'][column_idx].append(number)

                    # If either the row or column is finished
                    if is_finished(marked[board_idx]['rows_matching'][row_idx]) or is_finished(
                        marked[board_idx]['colums_matching'][column_idx]
                    ):

                        # The data we will need for the final puzzle result
                        winner_data = {
                            'board': board,
                            'marked_numbers': marked[board_idx]['matching'],
                            'winning_number': number,
                        }

                        if not first_winner:
                            # If this is the fist winner, save the information
                            first_winner = winner_data

                        # Take note if this board is finished
                        finished_boards.append(board_idx)

                        # Always mark the currenty fionished board as the last winner
                        last_winner = winner_data

    return [first_winner, last_winner]


for idx, winner_data in enumerate(get_winners()):
    all_board_numbers = set([n for r in winner_data['board'] for n in r])
    unmarked_numbers = all_board_numbers - set(winner_data['marked_numbers'])
    print(f"Part {idx+1} solution: {sum(unmarked_numbers) * winner_data['winning_number']}")