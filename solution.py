assignments = []

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
cols_rev = cols[::-1]
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
d1_units = [[rows[i]+cols[i] for i in range(len(rows))]]
d2_units = [[rows[i]+cols_rev[i] for i in range(len(rows))]]

do_diagonal = 1 # Set this flag = 0 for non-diagonal sudoku
if do_diagonal == 1:
    unitlist = row_units + column_units + square_units + d1_units + d2_units

else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    for unit in unitlist:
        potential_twins = [box for box in values.keys() if len(values[box])==2]

        twinlist = [[box1, box2] for box1 in potential_twins \
                            for box2 in peers[box1] \
                            if set(values[box1]) == set(values[box2])]

        for i in range(len(twinlist)):
            twinlist[i].sort()
        twinlist.sort()

        seen = set()
        naked_twins = []
        for item in twinlist:
            t = tuple(item)
            if t not in seen:
                naked_twins.append(item)
                seen.add(t)

        for i in range(len(naked_twins)):
            delset = {}
            box1 = naked_twins[i][0]
            box2 = naked_twins[i][1]
            for i in range(len(d1_units)):
                if (box1 in d1_units[i] and box2 in d1_units[i]):
        # or (box1 in d2_units and box2 in d2_units):
                    b1 = list(box1)
                    b2 = list(box2)
#                    print (b1[1], "  b1b2   ", b2)
                    elem1 = b1[0] + b2[1]
                    elem2 = b2[0] + b1[1]
                    delset = {elem1,elem2}
#                    print ("box 1 = ", box1, " box 2 = ", box2, "  elem1 = ", elem1, " elem2 ", elem2)
            for i in range(len(d2_units)):
                if (box1 in d2_units[i] and box2 in d2_units[i]):
        # or (box1 in d2_units and box2 in d2_units):
                    b1 = list(box1)
                    b2 = list(box2)
#                    print (b1[1], "  b1b2   ", b2)
                    elem1 = b1[0] + b2[1]
                    elem2 = b2[0] + b1[1]
                    delset = {elem1,elem2}
                    print ("box 1 = ", box1, " box 2 = ", box2, "  elem1 = ", elem1, " elem2 ", elem2)



            peers1 = set(peers[box1])
            peers2 = set(peers[box2])
            peers_int1 = peers1 & peers2
            peers_int = peers_int1.difference(delset)
#            print("box1 =", box1, "   box 2 = ", box2, " peers int  =  ", peers_int)
#            if peers_int1 <> peers_int:
#                print ("peers_int1   = ", peers_int1)
#                print ("peers_int   = ", peers_int)

            for peer_val in peers_int:
                if len(values[peer_val])>2:
                    for rm_val in values[box1]:
                        values = assign_value(values, peer_val , values[peer_val].replace(rm_val,''))



    return values






def naked_twins2(values):
    potential_twins = [box for box in values.keys() if len(values[box])==2]

    naked_twins = [[box1, box2] for box1 in potential_twins \
                    for box2 in peers[box1] \
                    if set(values[box1]) == set(values[box2])]
    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1 & peers2
        for peer_val in peers_int:
            if len(values[peer_val])>2:
                for rm_val in values[box1]:
                    values = assign_value(values, peer_val , values[peer_val].replace(rm_val,''))

    return values


def naked_twins3(values):
    listoftwins = [box for box in values.keys() if len(values[box])==2]
    listoftwinsvalue = []
    for x in listoftwins:
        listoftwinsvalue.append(values[x])
    listfinal= dict(zip(listoftwins,listoftwinsvalue))
    i = 0
    while i < len(listoftwins):
        j = i + 1
        while j < len(listoftwins):
            if listoftwinsvalue[i] == listoftwinsvalue[j] :
                count = 0
                twinvalue = listoftwinsvalue[i]
                while count < 29:
                    if listoftwins[i]  in unitlist[count] and  listoftwins[j] in unitlist[count]:
                        peers1 = set(peers[listoftwins[i]])
                        peers2 = set(peers[listoftwins[j]])
                        peers_int = peers1 & peers2
                        for peer_val in peers_int:
                            if len(values[peer_val])>2:
                                for rm_val in values[listoftwins[i]]:
                                    values = assign_value(values, peer_val , values[peer_val].replace(rm_val,''))

                    count += 1
            j += 1
        i += 1
    return values


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
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def grid_values_unsolved(grid):
    """
    Convert grid into a dict of {square: char} with '.' for empties to be displayed as unsolved grid.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
    """
    values = []
    all_digits = '.'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        else:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """This function will Eliminate values from peers of each box with a single value.
    It will go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for temp in solved_values:
        digit = values[temp]
        peers_solv = peers[temp]
        for peer in peers_solv:
            #values[peer] = values[peer].replace(digit,'')
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values


def only_choice(values):
    """This function willl Finalize all values that are the only choice for a unit.
    It will go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values



def reduce_puzzle(values):
    """ This function will iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twin Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        #Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
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
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#    diag_sudoku_grid = '.4..8.........6.........5..358..91.....................9.....8....97.34...7....9.'

    # To print unsolved grid
    values = grid_values_unsolved(diag_sudoku_grid)
    display(values)
    # To print solved grid
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
