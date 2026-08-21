import tkinter as tk # it is used to create a graphical user interface

N = 8
SIZE = 60

board = [["." for _ in range(N)] for _ in range(N)]
step = 0

# ---------------- GUI ----------------

root = tk.Tk()
root.title("8-Queen Problem - Backtracking Algorithm")

title = tk.Label(root,
                 text="8-Queen Problem using Backtracking",
                 font=("Arial",16,"bold"))
title.pack()

step_label = tk.Label(root,
                      text="Step : 0",
                      font=("Arial",12))
step_label.pack()

canvas = tk.Canvas(root,
                   width=N*SIZE,
                   height=N*SIZE)
canvas.pack()


# Draws a chessboard
def draw_board():

    canvas.delete("all")

    for r in range(N):
        for c in range(N):

            color = "#F0D9B5" if (r+c)%2==0 else "#B58863"

            x1 = c*SIZE
            y1 = r*SIZE
            x2 = x1+SIZE
            y2 = y1+SIZE

            canvas.create_rectangle(x1,y1,x2,y2,
                                    fill=color,
                                    outline="black")

            if board[r][c]=="Q":
                canvas.create_text(
                    x1+SIZE/2,
                    y1+SIZE/2,
                    text="♛",
                    font=("Arial",30),
                    fill="red"
                )

    root.update()


# ---------------- Algorithm ----------------

def is_safe(row,col):

    for i in range(col):
        if board[row][i]=="Q":
            return False

    i,j=row,col
    while i>=0 and j>=0:
        if board[i][j]=="Q":
            return False
        i-=1
        j-=1

    i,j=row,col
    while i<N and j>=0:
        if board[i][j]=="Q":
            return False
        i+=1
        j-=1

    return True


def solve(col):

    global step

    if col==N:
        return True

    for row in range(N):

        if is_safe(row,col):

            board[row][col]="Q"

            step+=1
            step_label.config(
                text=f"Step : {step}  |  Place Queen at Row {row+1}, Column {col+1}"
            )

            draw_board()

            root.after(500)

            if solve(col+1):
                return True

            board[row][col]="."

            step+=1
            step_label.config(
                text=f"Step : {step}  |  Backtracking..."
            )

            draw_board()

            root.after(500)

    return False


draw_board()

root.after(1000, lambda: solve(0))

root.mainloop()