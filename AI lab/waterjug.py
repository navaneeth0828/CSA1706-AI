Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> from collections import deque
... 
... def water_jug(jug1, jug2, target):
...     visited = set()
...     queue = deque()
... 
...     queue.append((0, 0, []))
... 
...     while queue:
...         x, y, path = queue.popleft()
... 
...         if (x, y) in visited:
...             continue
... 
...         visited.add((x, y))
...         path = path + [(x, y)]
... 
...         if x == target or y == target:
...             print("Solution Path:")
...             for state in path:
...                 print(state)
...             return
... 
...         next_states = [
...             (jug1, y),
...             (x, jug2),
...             (0, y),
...             (x, 0),
...             (min(jug1, x + y), max(0, y - (jug1 - x))),
...             (max(0, x - (jug2 - y)), min(jug2, x + y))
...         ]
... 
...         for state in next_states:
...             if state not in visited:
...                 queue.append((state[0], state[1], path))
... 
