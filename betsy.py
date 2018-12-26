#!/usr/bin/env python3
import sys
import copy
import time 
import math
import numpy as np
import sys
import math

'''
Arriving at a suitable heuristic is a trick task for this game. 
While solving this question I tried out various heuristic functions. 

I started with the simplest heuristics: 
1. Number of elements current - Number of elements opponent
2. Number of continous rows current - Number of continous rows opponent
3. Number of continous columns current - Number of continous columns opponent

After playing with other player on silo, I realized that:
1. No of elements do no neccessarily matter. As there are limited number of pebbles, saving pebbles for
later can be actually used as a strategy. 

2. Number of continous row are not necessarily informative as the row can be easily broken by the opponent by rotating.

3. While counting the continous columns we have to consider the wrap due to rotate operation. Also we have to consider only
those elements which are not block on both the sides by the opponent. 

Finally, I came up with the following heuristics:

1. No of continuous columns with wrap:
As the no of columns increase, the chances of winning also increase significantly. 
Hence, an exponential function is used to map this relation. Also the columns which ar in the top n rows are given
higher values. 

2. Variance from middle column: 
Similar to the case of tic-tac-toe the changes of winning increase if the element is in the center. 

3. Row weight: 
This function return the row number of each element. Rows at the top have higher weightage. 

The final heuristic function is a combination of these 3 functions. 


Another issue that I was facing was that the algorithm was not giving the shortest path to the goal. 
For eg. Even though there a move that will gaurantee a win in 1 move, it might play another move and then
eventually win later.

To prevent this from happening, I provides the value to goal according to depth. The goal at a lower depth has a higher value.

Finally, in order to the handle the variable size of n and the time limit. An iterative search is used. This quickly prints 
a solution and then looks for better solutions. 

'''

# prints the board in the required format
def printable_board(board):
	for row in range(n + 3):
		for col in range(n):
			print(board[col][row], end= "")

# for inserting the element to the lowest empty row in a column
def insert_top(board, col, n_col, current):
			if(col[0] != '.'):
				return None
			for l in range(len(col) - 1) :
				if((col[l+1] != '.' and col[l] == '.')):
					board[n_col] = col[0:l] + [current,] + col[l+1::]
					return board
			if(col[len(col) - 1] == '.'):
				board[n_col] = col[0:(len(col)-1)] + [current,] 
				return board
			return None

# count the no of elements
def no_of_element(board, player):
	result = 0
	for col in board:
		for row in col:
			if(row == player):
				result+= 1

	return result

# count the no of continous rows
def no_of_cont_row(board):
	result = 0
	for col in range(n):
		for row in range(n+2):
			if(board[col][row] == board[col][row + 1] ==  current):
				result+= 1
			elif(board[col][row] == board[col][row + 1] ==  opponent):
				result-= 1
	return result

# this gives a sum of the continuous columns considering a wrap
def continuous_col(board, player):
	result = 0
	start = 0
	start_counting = False
	start_count = 0
	for col in range(n):
		start_counting = False
		start_count = 0	
		count = 0
		for row in range(n+2):
			if(board[col][0] == '.'):
				start_counting = True
			if(board[col][row] == board[col][(row+1)] == player):
				
				start = row
				if(not start_counting):
					start_count+=1
				else:
					count+=1
			
			else:
				if(board[col][row] != player and board[col][row] != '.'):
					start_counting = True
				elif((board[col][(row + 1)] == '.' and board[col][row] == player) or count >= n):
					start_counting = True
					result+= 5**(count+1)
					count = 0
				elif((start != 0) and (start - 1 == ".")):
					result+= 5**(count+1)
					count = 0
		if(board[col][0] == '.'):
			result+= 5**(count+1)
			
		elif(board[col][0] == player):
			
			if(count+start_count+1>=n):
				result+= 5**(count + 10*(start_count +1))
			else:
				result+= 5**(count + start_count +1)
		else:
			result+= 5**(start_count+1)
	return result

# this function assign values according to the deviation for the middle column and the row no
def counts(board, player):
	result = 0
	for col in range(n):
		for row in range(n+3):
			if(board[col][row] == player):
				result+= 5*((n+3) - row)
				result-= abs((n/2) - col)
	return result

# find the heuristic values for nodes at the cutoff depth
def heuristics(board):
	cont_current = continuous_col(board, current)
	cont_opp = continuous_col(board, opponent)
	count_current = counts(board, current)
	count_opp = counts(board, opponent)
	x = cont_current - 2*cont_opp + count_current - count_opp
	return x
	
# find the successors for a board configuration
def successors(board, current):
	result = []
	for n_col, col in enumerate(board):
		res = 0
		
		# rotate the columns
		new_board = copy.deepcopy(board)
		element = new_board[n_col].pop()
		new_board[n_col].insert(0, ".")
		ans = insert_top(new_board, new_board[n_col], n_col, element )
		if(ans!= None and ans[n_col][-1]!='.'):
			result.append((ans, -1*(n_col + 1)))

		for col in board:
			for row in col:
				if(row == current):
					res+= 1

		# drop a pebbles in the columns
		if(res < max_pebbles):
			new_board = copy.deepcopy(board)
			ans = insert_top(new_board, new_board[n_col], n_col, current)
			if(ans!= None):
				result.append((ans, n_col + 1))

	return(result)

# this function checks the if a board is a goal state
# we return a very high value to ensure that a goal state always has higher value than heuristic
def isGoal(board, depth):

	# check columns
	for col in range(n):
		for row in range(n - 1):
			if((board[col][row] != board[col][row + 1]) or board[col][row] == "."):
				break
			if((row == n - 2) and (board[col][row] == current_saved)):
				return (100 - depth)*1000000

			elif((row == n - 2) and (board[col][row] == opponent_saved)):
				return (100 - depth)*-1000000

	#check row
	for row in range(n):
		for col in range(n - 1):
			if((board[col][row] != board[col+1][row]) or board[col][row] == "."):
				break
		
			if(col == n - 2 and board[col][row] == current_saved):
				return (100 - depth)*1000000

			elif(col   == n - 2 and board[col][row] == opponent_saved):
				return (100 - depth)*-1000000

	# check diagonal left to right
	flag = False
	
	for i in range(n - 1):
		if(board[i][i] != board[i+1][i+1] or board[i][i] == "."):
			flag = True
			break
		if(flag):
			break

		if(i == n - 2 and board[i][i] == current_saved):
			return (100 - depth)*1000000

		if(i == n - 2 and board[i][i] == opponent_saved):
			return (100 - depth)*-1000000

	#check right to left diagonal
	flag = False
	for i in range(n - 1):
		if(board[i][n  - i - 1] != board[i+1][n - i - 2] or board[i][n - i - 1] == "."):
			flag = True
			break
		if(flag):
			break
		if(i == n - 2 and board[i][n - i - 1] == current_saved):
			return (100 - depth)*1000000

		if(i == n - 2 and board[i][n - i - 1] == opponent_saved):
			return (100 - depth)*-1000000

	return False


def minimax(board_inp, depth, max_node, alpha, beta):
	
	# checking for goal
	goal = isGoal(board_inp, depth)
	if(goal):
		return goal, board_inp

	# depth cut-off
	if(depth == n_depth):
		value = heuristics(board_inp)
		return value, board_inp

	successor_ = successors(board_inp, (current if max_node else opponent))

	for board in successor_:
		val, _ = minimax(copy.deepcopy(board[0]), depth + 1,not max_node, alpha, beta)

		if((max_node) and (val > alpha)):
			alpha = val
			ret_board[depth] = board
			if(alpha >= beta):
				return alpha, ret_board[depth]

		if((not max_node) and (val < beta)):
			beta = val
			ret_board[depth] = board
			if(alpha >= beta):
				return beta, ret_board[depth]

	ret_val = alpha if max_node else beta
	return ret_val, ret_board[depth]

n = int(sys.argv[1])
inp =  "x.ox.xx.ox.xx.ox.x"

inp = sys.argv[3]
current = sys.argv[2]

if current == 'o':
	opponent = 'x'
else:
	opponent = 'o'

current_saved = copy.deepcopy(current)
opponent_saved = copy.deepcopy(opponent)
n_depth = 8
max_node = True
board = []
max_pebbles = (1/2)*(n*(n+3))

ret_board = [None]*(n_depth)

for col in range(n):
	board.append([])
	for row in range(n + 3):
		board[col].append(inp[(row*n)+col])

for i in range(2,10000):
	n_depth = 3
	ret_board = [None]*(n_depth)
	a, b  = minimax(board, 0, True, -1*math.inf, math.inf)
	print(b[1],end = " ")
	printable_board(b[0])
	print()