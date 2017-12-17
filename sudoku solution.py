
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = unitlist + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    
    # First select boxes with 2 entries
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    # Collect boxes that have the same elements
    naked_twins = [[box1,box2] for box1 in potential_twins for box2 in peers[box1] if set(values[box1])==set(values[box2]) ]
    #print(naked_twins)
    
    for twins in naked_twins:
        box1 = twins[0]
        box2 = twins[1]
        # 1- compute intersection of peers
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1 & peers2
        # 2- Delete the two digits in naked twins from all common peers.
        for box in peers_int:
            if len(values[box])>=2:
                for rm_val in list(set(values[box1]+values[box2])):
                    #print (box, "=>", values[box], "removed", rm_val)
                    values = assign_value(values, box, values[box].replace(rm_val,''))

    return values 
    
def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    for box,value in values.items():
        #print (box,value)
        if len(values[box]) == 1:
            for peer in peers[box]:
                if value in values[peer]:
                    values[peer] = values[peer].replace(value,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        #print (unit)
        #solved_boxes = [box for box in unit if len(values[box]) == 1]
        #unsolved_boxes = [box for box in unit if len(values[box]) > 1]
        #print (unit,solved_values,unsolved_values)
        unit_minus = list(unit)
        for box in unit:
            unit_minus.remove(box)
            #print (unit)
            #print (unit_minus)
            #print (box, "=>", values[box])
            unit_values_minus = []
            for b in unit_minus:
                unit_values_minus += values[b]
            #print ("unopt", unsolved_values_minus)
            unit_values_minus = list(set(unit_values_minus))
            # print ("opt", unit_values_minus)
            for value in values[box]:
                if value not in unit_values_minus:
                    values[box] = value
                    # print (box, "=>", values[box])
            unit_minus = list(unit)
        #display(values)
        #print ("====")
    #print ("==== END ====")
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        
        # Naked Twin Strategy
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # First, reduce the puzzle using the previous function
    #print ("before")
    #display(values)
    reduce_puzzle(values)
    #print("after")
    #display(values)
    
    for box in boxes:
        if len(values[box]) < 1:
            return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #print (n,s,values[s])
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        values_copy = values.copy()
        values_copy[s] = value
        #print (s, "values:", values[s],"=>",value)
        #display(values_copy)
        attempt = search(values_copy)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    
    #print ('==== test naked twins ====')
    test_ex = {"B8": "3456789", "H5": "23456789", "C5": "23456789", 
               "C9": "124578","A2": "234568", "H8": "345678", "B9": "124578", 
               "G5": "23456789","G6": "1236789", "F4": "9", "G1": "23456789", 
               "A1": "2345689", "A6":"23689", "B4": "345678", "E5": "678", 
               "F3": "24", "H1": "23456789","H9": "24578", "A9": "2458", 
               "D4": "1", "F7": "58", "H4": "345678","A4": "34568", "F9": "6", 
               "E1": "567", "G7": "2345678", "E2": "567","I5": "2345678", 
               "B5": "23456789", "B6": "236789", "I3": "23456","D7": "47", 
               "G9": "24578", "B7": "2345678", "F1": "1", "E3": "56","F2": "24", 
               "I2": "2345678", "D1": "36", "B3": "1234569", "C2":"1234568", 
               "G8": "345678", "E7": "9", "H7": "2345678", "G2":"12345678", 
               "C1": "2345689", "E4": "2", "H2": "12345678", "C6":"236789", 
               "B1": "2345689", "A8": "345689", "E9": "3", "G4": "345678",
               "H6": "1236789", "I8": "345678", "C8": "3456789", "A7": "234568",
               "E8": "1", "D9": "47", "F8": "58", "D2": "9", "D3": "8", 
               "B2":"1234568", "C7": "2345678", "C4": "345678", "I9": "9", 
               "D6": "5","D8": "2", "I1": "2345678", "F6": "37", "A5": "1", 
               "G3": "1234569","D5": "36", "E6": "4", "H3": "1234569", 
               "A3": "7", "I7": "1", "I6":"23678", "F5": "37", "C3": "1234569", "I4": "345678"}
    #display(test_ex)
    #display(naked_twins(test_ex))
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
