Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import math
... 
... scores = [3, 5, 2, 9, 12, 5, 23, 23]
... 
... def minimax(depth, nodeIndex, isMax, scores, height):
... 
...     if depth == height:
...         return scores[nodeIndex]
... 
...     if isMax:
...         return max(
...             minimax(depth + 1, nodeIndex * 2, False, scores, height),
...             minimax(depth + 1, nodeIndex * 2 + 1, False, scores, height)
...         )
...     else:
...         return min(
...             minimax(depth + 1, nodeIndex * 2, True, scores, height),
...             minimax(depth + 1, nodeIndex * 2 + 1, True, scores, height)
...         )
... 
... height = int(math.log2(len(scores)))
... 
... print("Optimal value is:",
