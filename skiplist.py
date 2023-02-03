import algviz
# Create a visualizer object.
# The default duration of each frame of animation is 3.0 seconds.
# The interval between two frames of animation is 0.5 seconds.
viz = algviz.Visualizer(delay=3.0, wait=0.5)

viz.display()               # Display the firt animation frame.
# Do something...
viz.display(delay=2.0)      # Display the second animation frame.

root1 = algviz.parseBinaryTree([1, 2, 3, 4, None, 5, 6])
binary_tree = viz.createGraph(data=root1, name='Binary Tree')
viz.display()
