from collections import deque

def valid(m, c):
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False

    if m > 0 and c > m:
        return False

    if (3-m) > 0 and (3-c) > (3-m):
        return False

    return True

def bfs():
    start = (3,3,1)
    goal = (0,0,0)

    queue = deque([(start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if state == goal:
            for s in path+[state]:
                print(s)
            return

        if state in visited:
            continue

        visited.add(state)

        m,c,b = state

        moves = [(2,0),(0,2),(1,1),(1,0),(0,1)]

        for dm,dc in moves:

            if b:
                new = (m-dm,c-dc,0)
            else:
                new = (m+dm,c+dc,1)

            if valid(new[0],new[1]):
                queue.append((new,path+[state]))

bfs()
