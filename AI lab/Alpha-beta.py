Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import math
... 
... MAX = 1000
... MIN = -1000
... 
... scores = [3, 5, 6, 9, 1, 2, 0, -1]
... 
... def alphabeta(depth, nodeIndex, maximizingPlayer,
...               values, alpha, beta, maxDepth):
... 
...     if depth == maxDepth:
...         return values[nodeIndex]
... 
...     if maximizingPlayer:
... 
...         best = MIN
... 
...         for i in range(2):
...             value = alphabeta(depth + 1,
...                               nodeIndex * 2 + i,
...                               False,
...                               values,
...                               alpha,
...                               beta,
...                               maxDepth)
... 
...             best = max(best, value)
...             alpha = max(alpha, best)
... 
...             if beta <= alpha:
...                 break
... 
...         return best
... 
...     else:
... 
...         best = MAX

        for i in range(2):
            value = alphabeta(depth + 1,
                              nodeIndex * 2 + i,
                              True,
                              values,
                              alpha,
                              beta,
                              maxDepth)

            best = min(best, value)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best

treeDepth = int(math.log2(len(scores)))

result = alphabeta(0, 0, True,
                   scores,
                   MIN,
                   MAX,
                   treeDepth)

