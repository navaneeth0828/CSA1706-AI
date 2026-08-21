N = 8

board = [-1] * N


def is_safe(row, col):

    for i in range(row):

        # Same column
        if board[i] == col:
            return False

        # Same diagonal
        if abs(board[i] - col) == abs(i - row):
            return False

    return True


def solve(row):

    if row == N:
        print("Solution Found")
        print_board()
        return True

    for col in range(N):

        if is_safe(row, col):

            board[row] = col

            if solve(row + 1):
                return True

            board[row] = -1

    return False


def print_board():

    for row in range(N):
        for col in range(N):

            if board[row] == col:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        print()


solve(0)