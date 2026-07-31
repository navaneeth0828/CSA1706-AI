goal = [1,2,3,4,5,6,7,8,0]

visited = []

def solve(state):

    if state == goal:
        print("Goal Reached")
        print(state)
        return True

    visited.append(state)

    pos = state.index(0)

    moves = []

    if pos > 2:
        s = state[:]
        s[pos], s[pos-3] = s[pos-3], s[pos]
        moves.append(s)

    if pos < 6:
        s = state[:]
        s[pos], s[pos+3] = s[pos+3], s[pos]
        moves.append(s)

    if pos % 3 != 0:
        s = state[:]
        s[pos], s[pos-1] = s[pos-1], s[pos]
        moves.append(s)

    if pos % 3 != 2:
        s = state[:]
        s[pos], s[pos+1] = s[pos+1], s[pos]
        moves.append(s)

    for move in moves:
        if move not in visited:
            if solve(move):
                return True

start = [1,2,3,
         4,0,6,
         7,5,8]

solve(start)