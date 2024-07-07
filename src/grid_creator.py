maze = "\n" * 5
for k in range(0, 121):
    if k % 15 == 0:
        maze += " "*5 + "O"*121 + " "*5 + "\n"
    else:
        maze += " "*5 + ("O" + " "*14)*8 + "O" + " "*5 + "\n"
maze += "\n" * 5
print(maze)