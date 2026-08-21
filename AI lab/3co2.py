def alphabeta(depth, node, alpha, beta, maximizing):

    if depth == 0:
        return node

    if maximizing:

        best = -1000

        for value in [node + 1, node + 2]:
            best = max(best, alphabeta(depth - 1, value,
                                       alpha, beta, False))
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:

        best = 1000

        for value in [node + 1, node + 2]:
            best = min(best, alphabeta(depth - 1, value,
                                       alpha, beta, True))
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


alpha = -1000
beta = 1000

result = alphabeta(3, 0, alpha, beta, True)

print("Best value:", result)