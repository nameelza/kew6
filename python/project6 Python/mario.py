from cs50 import get_int

# Prompts user for height int between 1 and 8 inclusive
while True:
    height = get_int("Height: ")
    if 0 < height < 9:
        break

# Prints out the height number of blocks
def blocks(h):
    for i in range(1, h + 1):
        space = " "*(h-i)
        hashes = "#"*i
        print(f"{space}{hashes}  {hashes}")


blocks(height)