assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def only_square(values):
    """If there are 7 boxes within a unit that have been already solved
        len == 1
        then find the other 2 boxes in that unit and assign the remaining two digits to those boxes"""
    for unit in unitlist:
        solved_values = [box for box in unit if len(values[box]) == 1] # get all the solved values in a unit
        if len(solved_values) == 7: # if 7 values are solved in a unit..
            digits_that_are_already_set = []
            for box_already_set in solved_values: # get all the digits that already have been set from 1-9
                value = values[box_already_set]
                digits_that_are_already_set.append(value)

            two_digits = []
            for digit in '123456789':
                if digit not in digits_that_are_already_set: # find digits that have not yet been set in the 7 boxes
                    two_digits.append(digit)
                    if len(two_digits) == 2:
                        two_digits_joined = str(''.join(str(i) for i in two_digits)) # append list of two digits into a string
                        for box in unit:
                            if box not in solved_values: # for box not in solved values apply only square
                                assign_value(values, box, two_digits_joined)
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        # dict with keys for boxes with 2 values
        twins = {}
        # finding twin in each unit
        for box in unit:
            # store the value of the current box in 'value'
            value = values[box]
            # if the length of value is 2 then store these boxes
            if len(value) == 2:
                twins[value] = twins[value] + [box] if value in twins else [box]

        # eliminate naked twins from the current unit
        for twin_values, boxes_with_twins in twins.items():
            if len(boxes_with_twins) == 2:
                # naked twins confirmed
                for box in unit:
                    # for every box in unit except naked twins
                    if box not in boxes_with_twins:
                        values = assign_value(values, box, values[box].replace(twin_values[0], ''))
                        values = assign_value(values, box, values[box].replace(twin_values[1], ''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols) # each individual square in the 9x9 grid (81 in total)
row_units = [cross(r, cols) for r in rows] # each row in the grid (9 in total)
col_units = [cross(rows, c) for c in cols] # each column in the grid (9 in total)
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] # each 3x3 square in the grid (9 in total)
diag_fwd = [[d[0]+d[1] for d in zip(rows, cols)]] # Forward diagonal A1, B2, C3, D4, E5, F6, G7, H8, I9
diag_bwd = [[d[0]+d[1] for d in zip(rows, cols[::-1])]] # Backward diagonal I1, H2, G3, F4, E5, D4, C3, B2, A1

# add all the units into one list 9 rows, columns and square units
unitlist = row_units + col_units + square_units + diag_fwd + diag_bwd # Just add fwd and bkwd diagonals to the unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81" # check that length of input strength consists of 81 characters
    grid = [d.replace('.', '123456789') for d in grid] # replace the .'s in the input string with digits '123456789'
    return dict(zip(boxes, grid)) # return the string as a dictionary with box values e.g. A1 as keys and value of each box as values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1] # find all boxes which have already been solved by checking if length of their value ==1
    for box in solved_values: # go through all these solved boxes
        digit = values[box] # assign the value of the current selected (and solved) box to digit
        for peer in peers[box]: # find the peers of this current box
            assign_value(values, peer, values[peer].replace(digit, '')) # if we find the solved digit in any of these boxes replace it with ''
    return values

def only_choice(values):
    for unit in unitlist: # for each in the list of all units
        for digit in '123456789': # each digit from 123456789
            dplaces = [box for box in unit if digit in values[box]] # if any of the digit exists in any of the boxes in the current unit
            if len(dplaces) == 1: # if only one instance of this digit is found in the current unit in one box
                assign_value(values, dplaces[0], digit) # then that box should be the only one which can take this digit
    return values

def reduce_puzzle(values):
    stalled = False # check to see if our model is stuck and can no longer solve the given sudoku
    while not stalled: # if it is not stalled
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1]) # find the number of solved values before we run our techniques

        # Only Square
        values = only_square(values)
        # Naked Twins
        values = naked_twins(values)
        # then Eliminate
        values = eliminate(values)
        # then Only Choice
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])  # find the number of solved values after we have ran our techniques
        stalled = solved_values_before == solved_values_after # if the solved values before and after are the same we are stuck and can no longer progress in solving our puzzle
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values) # apply only square, naked twins, eliminate and only choice on the dict of the current unsolved sudoku
    if values is False: # if reduce puzzle is stuck return False that we cannot solve this puzzle
        return False
    if all(len(values[s])  == 1 for s in boxes): # if all values in each box is 1 it means we have solved the Sudoku completely
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]: # create a new instance of sudoku that has all the solved values (uptil now) and even those that have not been 'completely' solved
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku) # try to solve the sudoku again using the techniques in the reduce puzzle function
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid) # tha main function that sends the grid_values function a str which is returned as dict
    values = search(values) # keep on iterating on the puzzle until it is solved
    return values # the final state of the solved puzzle



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
