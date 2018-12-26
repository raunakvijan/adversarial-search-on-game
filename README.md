# adversarial search on game

## Betsy
A popular game in a certain exotic, far-off land1
is called Betsy. It’s played on a vertical board that is
n squares wide and n + 3 squares tall (where n is often 5 for beginners, but can grow quite large in the
professional tournaments). The board starts off empty, with each of the two players (red and blue) given
1
2
n × (n + 3) pebbles of their own color. Blue goes first, choosing one of two possible types of moves.
• Drop: Choose one of the n columns, and drop a blue pebble into that column. The pebble falls to
occupy the bottom-most empty square in that column. The player is not allowed to choose a column
that is already full (i.e., already has n + 3 pebbles in it).
• Rotate: Choose one of the n columns, remove the pebble from the bottom of that column (whether
red or blue) so that all pebbles fall down one square, and then drop that same pebble into the top of
that column. The player is not allowed to choose an empty column for this type of move.
After making a move, blue checks the top n rows of the board to see if they have completed a row of n blue
pebbles, a column of n blue pebbles, or one of the two diagonals of blue pebbles. The bottom three rows
of the board are ignored during this check. If a row, column, or diagonal has been completed in blue, blue
wins! Otherwise, red makes the same check and wins if any row, column, or diagonal has been completed
with red. Note this means that if blue completes a row, column, or diagonal of blue pebbles, they win even
if they have also completed a row, column, or diagonal of red. If no one has won, player red takes their turn,
either dropping a red pebble into an incomplete column or rotating a non-empty column. Figure 1 shows
several sample moves from a game in progress, with n = 3.
Your task is to write a Python program that plays Betsy well. Use the minimax algorithm with alpha-beta
search and a suitable heuristic evaluation function.
Your program should accept a command line argument that gives the value of n, and the current state of the
board as a string of n × (n + 3) characters (from top to bottom and left to right, i.e. in row-major order),
each of which is one of: . for an empty square, x for blue pebble, and o for a red pebble. For example, the
encoding of the board in Figure 1(a) would be:
...x..o.ox.oxxxoxo
More precisely, your program will be called with three command line parameters: (1) the value of n, (2) the
current player (x or o), (3) the state of the board, encoded as above, and (4) a time limit in seconds. Your 
program should then decide a recommended single move for the given player from the given current board
state, and display the recommend move and the new state of the board after making that move, within the
number of seconds specified, in a format like this:
move new board
where move is either a positive number indicating a column (ranging from 1 to n) in which to drop a pebble,
or a negative number indicating a column to rotate (e.g., -3 means to rotate column 3). Displaying multiple
lines of output is fine as long as the last line is the recommended move and board state.
For example, two runs of your program (corresponding to the first two moves of Fig. 1) might look like:2
[djcran@macbook]$ ./betsy.py 3 o ...x..o.ox.oxxxo.o 5
Shhh... I’m thinking!
Hey, in the time it takes you to read this sentence, I’ll have considered
5 billion board positions. But it’s cute that you’re still trying to beat me...
I’d recommend dropping a pebble in column 2.
2 ...x..o.oxooxxxoxo
[djcran@macbook]$ ./betsy.py 3 x ...x..o.oxooxxxoxo 5
Shhh... I’m thinking!
Sure, you could unplug me, but within 500ms I can command every computer on Earth
to delete any trace that you ever existed. You’re welcome.
I’d recommend rotating column 1
-1 ...o..x.ooooxxxxxo
In your source code comments, explain your heuristic function and how you arrived at it, and any other
interesting approaches you tried, problems you faced, etc.
The tournament. To make things more interesting, we will hold a competition among all submitted solutions.
We will not reveal ahead of time the time limit or board size, but we plan to hold multiple tournaments
with different values of each. While the majority of your grade will be on correctness, programming style,
etc., a small portion may be based on how well your code performs in the tournaments, with particularly
well-performing programs eligible for prizes including extra credit points.
Notes and hints: Your code must conform to the interface standards mentioned above! The last line of the
output must be the move and new board in the format given, without any extra characters or empty lines.
We will provide an output checker to help you verify this. We will also provide a program that will allow
you to play against other teams in the class without having to share your Python code (which would violate
the academic integrity policies of the course).
Note also that your program cannot assume that the game will be run in sequence from start to end; given
a current board position on the command line, your code must find a recommended next best move. Your
program can write files to disk to preserve state between runs, but should correctly handle the case when a
new board state is presented to your program that is unrelated to the last state it saw.
Our test program will enforce the time limit by killing your program after the time limit is exceeded. Since
we will only look at the last line that your program produces, an easy way of dealing with the time limit is
to quickly calculate and print a suggested “rough-draft” move, and then print out better moves as it finds
them. Our test program will kill your program after the time limit and only look at the best move it has
displayed, which presumably is the best it know about so far.
