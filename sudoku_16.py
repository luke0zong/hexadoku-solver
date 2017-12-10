def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


def test():
    "A set of unit tests."
    assert len(squares) == 256
    assert len(unitlist) == 48
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 39 for s in squares)
    assert units['C2'] == [
        ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2'],
        ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'Ca', 'Cb', 'Cc', 'Cd', 'Ce', 'Cf', 'Cg'],
        ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'D3', 'D4']]
    assert peers['C2'] == {'A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2',
                           'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'Ca', 'Cb', 'Cc', 'Cd', 'Ce', 'Cf', 'Cg',
                           'A1', 'A3', 'A4', 'B1', 'B3', 'B4', 'D1', 'D3', 'D4'}
    print('All tests pass.')


# def parse_grid(grid):
#     """Convert grid to a dict of possible values, {square: digits}, or
# 	return False if a contradiction is detected."""
#     ## To start, every square can be any digit; then assign values from the grid.
#     values = dict((s, digits) for s in squares)
#     for s, d in grid_values(grid).items():
#         if d in digits and not assign(values, s, d):
#             return False  ## (Fail if we can't assign d to square s.)
#     return values


def parse_grid_16(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
	return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values_16(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values_16(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    print(len(chars))
    assert len(chars) == 256
    return dict(zip(squares, chars))

    """Eliminate all the other values (except d) from values[s] and propagate.
	Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
	Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
	Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, '')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
        return False  ## Contradiction: no place for this value
    elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
        if not assign(values, dplaces[0], d):
            return False
    return values


def display_16(values):
    # "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 4)] * 4)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '48c' else ''))
              for c in cols)
        if r in 'DHL': print(line)
    print()


def solve_16(grid): return search(parse_grid_16(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


import time


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
	When showif is a number of seconds, display puzzles that take longer.
	When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        values = solve_16(grid)
        t = time.clock() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display_16(grid_values_16(grid))
            if values: display_16(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


# def time_solve(grid):
#     start = time.clock()
#     values = solve(grid)
#     t = time.clock() - start
#     return (t, solved(values))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."

    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


if __name__ == '__main__':
    digits = '123456789abcdefg'
    rows = 'ABCDEFGHIJKLMNOP'
    cols = digits
    squares = cross(rows, cols)
    unitlist = ([cross(rows, c) for c in cols] +
                [cross(r, cols) for r in rows] +
                [cross(rs, cs) for rs in ('ABCD', 'EFGH', 'IJKL', 'MNOP') for cs in ('1234', '5678', '9abc', 'defg')])
    units = dict((s, [u for u in unitlist if s in u])
                 for s in squares)
    peers = dict((s, set(sum(units[s], [])) - {s})
                 for s in squares)

    hard1 = '.63B.EC..A..8....847..A6..B....9.....81.D.G...7E.......7..98...CF.D.....AC..2.......D.....E1..5.CE......6...GF.31A.9...B8G7.4..D2.E...45....69.F.7......E..A...5..94..6......D.....63..F79.5...A....E6.D.1...2.8...3G.FA56.......D.C...9...B1.6..2..B.5C9.....34'.lower()
    grid1 = '.B.293.F..C.......7.B..5......C..9..C...247.F...EF..6....9B.3D..F...58G...........B3......2F1.7.....E...1.8..C.D...1...3.D...G..4.6...2.3..9A.8.12..G.86.F......A7....C...419.G......E..5....7437..........B.3.C.8...DF......E96.E.6...9......D8..G..7..C..4...A'.lower()

    # display_16(parse_grid_16(hard1))
    solve_all([hard1, grid1])
