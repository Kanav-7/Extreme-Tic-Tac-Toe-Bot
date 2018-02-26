import random
from time import time

class Team19:
	def __init__(self):
		# self.board = board
		self.initdepth = 6
		self.maxdepth = 300
		self.sign = ' '
		self.opposite_sign = ' '
		# self.timeLmt = datetime.timedelta(seconds = 14)
		self.timeLmt = 14
		self.INT_MAX = 100000000000
		self.INT_MIN = -100000000000



	def move(self, board, old_move, flag):

		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		self.startTime = time()
		self.sign = flag
		if(flag == 'x'):
			self.opposite_sign = 'o'
		else:
			self.opposite_sign = 'x'	
		ansMove = self.iterative_search(board,old_move,flag)
		return ansMove

	def iterative_search(self,board,old_move,flag):
		for deep in range(self.initdepth,self.maxdepth):
			print deep
			valid_moves = board.find_valid_move_cells(old_move)
			maxval = self.INT_MIN
			max_set = []
			for move in valid_moves:
				tempval = self.minimax(board, move, deep,  False, self.INT_MIN, self.INT_MAX)	
				if time() - self.startTime > self.timeLmt:
					break	
				if tempval > maxval:
					maxval = tempval
					max_set = [move]
				elif tempval == maxval:
					max_set.append(move)	
			if time() - self.startTime > self.timeLmt:
				break
			output_move = random.choice(max_set)
		return output_move
						
	#Source GFG
	def minimax(self,board,move,depth,isMaximizingPlayer, alpha, beta):
		if time() - self.startTime > self.timeLmt:
			return self.INT_MIN - 1

		if depth == 0 or board.find_terminal_state() != ('CONTINUE', '-'):
			# return self.heuristic(board, old_move, not max_player)
			# Apna heuristic likhna hai
			return 10

		if isMaximizingPlayer:
			bestVal = self.INT_MIN
			# print v
			moves = board.find_valid_move_cells(move)
			for new_move in moves:
				board.update(move, new_move, self.sign)
				bestVal = max(bestVal, self.minimax(board, new_move, depth - 1, False,alpha, beta))
				board.board_status[new_move[0]][new_move[1]] = '-'
				board.block_status[new_move[0]/4][new_move[1]/4] = '-'
				if time() - self.startTime > self.timeLmt:
					return self.INT_MIN - 1
				alpha = max(alpha, bestVal)
				if beta <= alpha:
					break
			return bestVal

		else:
			bestVal = self.INT_MAX
			# print v
			moves = board.find_valid_move_cells(move)
			# print moves
			for new_move in moves:
				# temp_board = copy.copy(board)
				board.update(move, new_move,self.opposite_sign)
				bestVal = min(bestVal, self.minimax(board, new_move, depth - 1,True, alpha, beta))
				board.board_status[new_move[0]][new_move[1]] = '-'
				board.block_status[new_move[0]/4][new_move[1]/4] = '-'
				if time() - self.startTime > self.timeLmt:
					return self.INT_MIN - 1
				beta = min(beta, bestVal)
				if beta <= alpha:
					break		
			return bestVal





