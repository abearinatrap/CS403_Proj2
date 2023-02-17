import algviz
# Create a visualizer object.
# The default duration of each frame of animation is 3.0 seconds.
# The interval between two frames of animation is 0.5 seconds.
viz = algviz.Visualizer(delay=3.0, wait=0.5)

viz.display()               # Display the firt animation frame.
# Do something...
viz.display(delay=2.0)      # Display the second animation frame.

tab = viz.createTable(
    row=3,                    # The table has 3 rows.
    col=1,                    # The table has 3 columns
    data=None,                # The initial data in table.
    name="Table",             # The name of table.
    cell_size=(40, 40),       # The table cell (width, height).
    show_index=True           # Whether to display subscripts.
)
viz.display()

curNum = input("Enter a number: ")
tab[1][0] = int(curNum)
viz.display(0.5)
curNum = input("Choose an index to flash green: ")
tab.mark(algviz.color_green, int(curNum), 0)
viz.display(0.5)
tab.removeMark(algviz.color_green)
viz.display(0.5)
print('time to resize')
tab.reshape(row=3, col=2)  # Change the table shape to (row:2, col:2).
viz.display(1)
