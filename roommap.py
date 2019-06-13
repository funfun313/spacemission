roommap =[
        [1,1,1,1,1,1],
        [1,0,0,0,0,1],
        [1,0,0,0,0,1],
        [1,0,0,0,0,1],
        [1,0,0,2,0,1],
        [1,0,0,0,0,1],
        [1,1,1,1,1,1]
]
printrow = 0
newnum = 0
row = 0
column = 0
for i in range(6):
    for i in range(6):
        newnum = (roommap[column][row])
        printrow = (printrow + " " + newnum)

        row += 1
    print(printrow)
    column += 1
    row = 0