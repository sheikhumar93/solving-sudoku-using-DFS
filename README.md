# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

![](https://github.com/sheikhumar93/solving-sudoku-using-DFS/blob/master/Sudoku.gif)

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: As Constraint Propagation is all about introducing local constraints in a space, in the case of Sudoku, thereby reducing the search space for a given problem. Naked Twins further helped with introducing these constraints along with Elimination and Only Choice. If in a unit there are only 2 boxes available that have the same values, we can safely say that only these two boxes can have these values (a constraint) and we can remove these digits from all the other boxes inside this unit reducing the search space and helping the agorithm solve the problem faster e.g. if in row 1 from A1-A9 if we have two boxes which can only take 2 values e.g. 2,3 we can say that only these boxes can have either 2 or 3 in which case we remove any instances of 2 or 3 from any other boxes in the same unit. In this way we reduce our search space in the next iteration of Depth First Search, and we can converge towards the solution one bit faster reducing the overall number of possibilities in our unsolved grid which is the main purpose of using DFS so that we do not have to brute force our way to finding a solution by using lots of computational power which is very expensive. Techniques like naked twins make our model more efficient. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Likewise, for solving the diagonal sudokus we have a constraint that no two boxes in the main forward and backward diagonals across the board can have the same values. We can then use elimination, only choice, naked twins and only square technique again to quickly solve this problem as well giving us numbers in each box in the diagonal that are unique in their respective units. We use constraints to say that we can only have one digit in each box along each diagonal. We narrow down the search space by using elimination, only choice, naked twins and only square one at a time again saving us on computing power which is very expensive to make our model more efficient and step by step eliminating obvious digits that cannot be part of some box by the end of which we have a solved sudoku that only has one digit in each box and does not overlap with any other peer in any other unit.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

