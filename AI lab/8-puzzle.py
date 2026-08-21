Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
# Function to print the puzzle
def print_puzzle(state):
    for row in state:
        print(row)
    print()

# Function to find the blank space (0)
def find_blank(state):
...     for i in range(3):
...         for j in range(3):
...             if state[i][j] == 0:
...                 return i, j
... 
... # Function to move the blank tile
... def move(state, direction):
...     x, y = find_blank(state)
... 
...     new_state = [row[:] for row in state]
... 
...     if direction == "up" and x > 0:
...         new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
... 
...     elif direction == "down" and x < 2:
...         new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
... 
...     elif direction == "left" and y > 0:
...         new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
... 
...     elif direction == "right" and y < 2:
...         new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
... 
...     return new_state
... 
... # Initial State
... initial = [
...     [1, 2, 3],
...     [4, 0, 5],
...     [6, 7, 8]
... ]
... 
... # Goal State
... goal = [
...     [1, 2, 3],
...     [4, 5, 0],
...     [6, 7, 8]
... ]
... 
... print("Initial State:")
... print_puzzle(initial)
... 
... # Move blank tile to the right
... result = move(initial, "right")
... 
... print("After Moving Right:")
... print_puzzle(result)
... 
... # Check Goal State
... if result == goal:
...     print("Goal State Reached!")
... else:
...     print("Goal State Not Reached!")
>>> [DEBUG ON]
>>> [DEBUG OFF]
