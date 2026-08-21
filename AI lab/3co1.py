from collections import deque

def water_jug():

    capacity1 = 4
    capacity2 = 3
    goal = 2

    queue = deque()
    visited = set()

    queue.append((0, 0))
    visited.add((0, 0))

    while queue:

        jug1, jug2 = queue.popleft()

        print(jug1, jug2)

        if jug1 == goal or jug2 == goal:
            print("Goal Reached")
            return

        states = [
            (capacity1, jug2),   # Fill Jug 1
            (jug1, capacity2),   # Fill Jug 2
            (0, jug2),           # Empty Jug 1
            (jug1, 0),           # Empty Jug 2
            (min(capacity1, jug1 + jug2), 
             jug2 - (min(capacity1, jug1 + jug2) - jug1)),  # Jug 2 -> Jug 1
            (jug1 - (min(capacity2, jug1 + jug2) - jug2),
             min(capacity2, jug1 + jug2))                    # Jug 1 -> Jug 2
        ]

        for state in states:

            if state not in visited:
                visited.add(state)
                queue.append(state)


water_jug()