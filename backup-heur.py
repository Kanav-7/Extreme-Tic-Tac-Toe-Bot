import random
from time import time

class Team19:
	def __init__(self):
		# self.board = board
		self.initdepth = 0
		self.maxdepth = 300
		self.sign = ' '
		self.opposite_sign = ' '
		# self.timeLmt = datetime.timedelta(seconds = 14)
		self.timeLmt = 1
		self.INT_MAX = 100000000000
		self.INT_MIN = -100000000000
		self.feature_weights = [
			3000,
			9000, -9000, 6000, -6000,
			300, -300,
			345, -345,

			6, -6, 3, -3,
			3, -3,
			3.45, -3.45,
		]
		self.blwts = [0, 0, 30, 300, 1500]
		self.clwts = [0, 0, 30, 300, 1500]



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
		# print "dqwefrbtnhjhm"
		# print ansMove
		return ansMove

	def iterative_search(self,board,old_move,flag):
		# print flag
		temparr = board.find_valid_move_cells(old_move)
		print board.find_valid_move_cells(old_move)
		output_move = random.choice(temparr)
		for deep in range(self.initdepth,self.maxdepth):
			valid_moves = board.find_valid_move_cells(old_move)
			maxval = self.INT_MIN
			max_set = []
			for move in valid_moves:
				tempval = self.minimax(board, move, deep,  False, self.INT_MIN, self.INT_MAX, flag)	
				# print tempval
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
		# print output_move
		return output_move
						
	#Source GFG
	def minimax(self,board,move,depth,isMaximizingPlayer, alpha, beta, flag):
		# print flag
		if time() - self.startTime > self.timeLmt:
			if isMaximizingPlayer:
				return self.INT_MAX + 1
			else:
				return self.INT_MIN - 1


		if depth == 0 or board.find_terminal_state() != ('CONTINUE', '-'):
			return self.heuristic(board, move, flag)
			# Apna heuristic likhna hai
			# return 10

		if isMaximizingPlayer:
			bestVal = self.INT_MIN
			# print v
			moves = board.find_valid_move_cells(move)
			for new_move in moves:
				board.update(move, new_move, self.sign)
				bestVal = max(bestVal, self.minimax(board, new_move, depth - 1, False,alpha, beta, flag))
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
				bestVal = min(bestVal, self.minimax(board, new_move, depth - 1,True, alpha, beta, flag))
				# print "dfg"
				board.board_status[new_move[0]][new_move[1]] = '-'
				board.block_status[new_move[0]/4][new_move[1]/4] = '-'
				if time() - self.startTime > self.timeLmt:
					return self.INT_MIN - 1
				beta = min(beta, bestVal)
				if beta <= alpha:
					break		
			return bestVal

			
	def heuristic(self,	board, old_move, flag):
		# print flag
		new_state = board.find_terminal_state()

		if new_state[1] == 'WON':
			if new_state[0] == self.sign:
				score = self.INT_MAX
			else:
				score = self.INT_MIN
			return score	

		features = self.getFeatures(board,old_move, flag)
		# print features
		total = 0
		length_feature = len(self.feature_weights)

		# print length_feature
		for i in range(length_feature):
			total += self.feature_weights[i] * features[i]
		
		# print total

		return total

	def getFeatures(self, board, old_move, sign):

		# print sign
		# print opposite_sign

		cc_block_won = cc_block_lost = 0
		edge_block_won = edge_block_lost = 0

		cc_cell_won = cc_cell_lost = 0
		edge_cell_won = edge_cell_lost = 0

		bl_won = bl_lost = 0
		block_diamond_won = block_diamond_lost = 0
		freedom = freemove = 0     # freemove = -1 if we lost block else freemove = 0/1 

		cl_won = cl_lost = 0
		cl_diamond_won = cl_diamond_lost = 0
		cfreedom = 0

		diamond1_stat = 2
		diamond1_count = 0
		diamond2_stat = 2
		diamond2_count = 0
		diamond3_stat = 2
		diamond3_count = 0
		diamond4_stat = 2
		diamond4_count = 0

		#diamond1 manipulation
		if board.block_status[0][1] == self.sign and board.block_status[1][0] == self.sign and board.block_status[2][1] == self.sign and board.block_status[1][2] == self.sign:
			if diamond1_stat == 2 or diamond1_stat == 1:
				diamond1_stat = 1
			else:
				diamond1_stat = 0

		
		elif board.block_status[0][1] == self.opposite_sign and board.block_status[1][0] == self.opposite_sign and board.block_status[2][1] == self.opposite_sign and board.block_status[1][2] == self.opposite_sign:
			if diamond1_stat == 2 or diamond1_stat == -1:
				diamond1_stat = -1
			else:
				diamond1_stat = 0

			

		#diamond2 manipulation
		if board.block_status[0][2] == self.sign and board.block_status[1][1] == self.sign and board.block_status[2][2] == self.sign and board.block_status[1][3] == self.sign:
			if diamond2_stat == 2 or diamond2_stat == 1:
				diamond2_stat = 1
			else:
				diamond2_stat = 0

		
		elif board.block_status[0][2] == self.opposite_sign and board.block_status[1][1] == self.opposite_sign and board.block_status[2][2] == self.opposite_sign and board.block_status[1][3] == self.opposite_sign:
			if diamond2_stat == 2 or diamond2_stat == -1:
				diamond2_stat = -1
			else:
				diamond2_stat = 0

		

		#diamond3 manipulation
		if board.block_status[1][1] == self.sign and board.block_status[2][0] == self.sign and board.block_status[3][1] == self.sign and board.block_status[2][2] == self.sign:
			if diamond3_stat == 2 or diamond3_stat == 1:
				diamond3_stat = 1
			else:
				diamond3_stat = 0

		
		elif board.block_status[1][1] == self.opposite_sign and board.block_status[2][0] == self.opposite_sign and board.block_status[3][1] == self.opposite_sign and board.block_status[2][2] == self.opposite_sign:
			if diamond3_stat == 2 or diamond3_stat == -1:
				diamond3_stat = -1
			else:
				diamond3_stat = 0



		#diamond4 manipulation
		if board.block_status[1][2] == self.sign and board.block_status[2][1] == self.sign and board.block_status[3][2] == self.sign and board.block_status[2][3] == self.sign:
			if diamond4_stat == 2 or diamond4_stat == 1:
				diamond4_stat = 1
			else:
				diamond4_stat = 0

		
		elif board.block_status[1][2] == self.opposite_sign and board.block_status[2][1] == self.opposite_sign and board.block_status[3][2] == self.opposite_sign and board.block_status[2][3] == self.opposite_sign:
			if diamond4_stat == 2 or diamond4_stat == -1:
				diamond4_stat = -1
			else:
				diamond4_stat = 0


		for i in range(4):
			row_stat = 2
			row_count = 0
			col_stat = 2
			col_stat = 0

			#row manipulation
			for j in range(4):
				if board.block_status[i][j] == self.sign:
					if row_stat == 2 or row_stat == 1:
						row_stat = 1
						row_count += 1

					else:
						row_stat = 0	
						row_count = 0

				elif board.block_status[i][j] == self.opposite_sign:
					if row_stat == 2 or row_stat == -1:
						row_stat = -1
						row_count += 1

					else:
						row_stat = 0
						row_count = 0

				elif board.block_status[i][j] == 'd':
						row_stat = 0

			#col manipulation
			# for j in range(4):
				if board.block_status[j][i] == self.sign:
					if col_stat == 2 or col_stat == 1:
						col_stat = 1
						col_count += 1

					else:
						col_stat = 0
						col_count = 0

				elif board.block_status[j][i] == self.opposite_sign:
					if col_stat == 2 or col_stat == -1:
						col_stat = -1
						col_count += 1

					else:
						col_stat = 0
						col_count = 0

				elif board.block_status[j][i] == 'd':
					col_stat = 0

				#Block manipulation
				if i == 0 or i == 3 != j == 0 or j == 3:
					if board.block_status[i][j] == self.sign:
						edge_block_won += 1
					elif board.block_status[i][j] == self.opposite_sign:
						edge_block_lost -= 1

				else:
					if board.block_status[i][j] == self.sign:
						cc_block_won += 1
					elif board.block_status[i][j] == self.opposite_sign:
						cc_block_lost += 1

				# Cell manipulation for blocks which have not been won or drawn
				if board.block_status[i][j] == '-':

					for bi in range(4):
						ci = 4*i + bi

						rowcell_stat = 2
						rowcell_count = 0
						colcell_stat = 2
						colcell_count = 0

						for bj in range(4):
							cj = 4*j + bj

							# Row statistics
							if board.board_status[4*i+bi][4*j+bj] == self.sign:
								if rowcell_stat == 2 or rowcell_stat == 1:
									rowcell_stat = 1
									rowcell_count += 1
								else:
									rowcell_stat = 0
									rowcell_count = 0
							elif board.board_status[4*i+bi][4*j+bj] == self.opposite_sign:
								if rowcell_stat == 2 or rowcell_stat == -1:
									rowcell_stat = -1
									rowcell_count += 1
								else:
									rowcell_stat = 0
									rowcell_count = 0


							# Col statistics
							if board.board_status[4*i+bj][4*j+bi] == self.sign:
								if colcell_stat == 2 or colcell_count == 1:
									colcell_stat = 1
									colcell_count += 1
								else:
									colcell_stat = 0
									colcell_count = 0
							elif board.board_status[4*i+bj][4*j+bi] == self.opposite_sign:
								if colcell_stat == 2 or colcell_stat == -1:
									colcell_stat = -1
									colcell_count += 1
								else:
									colcell_stat = 0
									colcell_count = 0


							if (bi == 0 or bi == 3) == (bj == 0 or bj == 3): # centre or corner squares
								if board.board_status[ci][cj] == self.sign:
									edge_cell_won += 1
								elif board.board_status[ci][cj] == self.opposite_sign:
									edge_cell_lost += 1
							else:
								if board.board_status[ci][cj] == self.sign:
									cc_cell_won += 1
								elif board.board_status[ci][cj] == self.opposite_sign:
									cc_cell_lost += 1
						

						
						if rowcell_stat == 2:
							cfreedom += 1
						elif rowcell_stat == 1:
							cl_won += self.clwts[rowcell_count]
							cfreedom += 1
						elif rowcell_stat == -1:
							cl_lost += self.clwts[rowcell_count]

						if colcell_stat == 2:
							cfreedom += 1
						elif colcell_stat == 1:
							cfreedom += 1
							cl_won += self.clwts[colcell_count]
						elif colcell_stat == -1:
							cl_lost += self.clwts[colcell_count]

				


					# some diag shit

			if row_stat == 2:
				freedom += 1
			elif row_stat == 1:
				freedom += 1
				bl_won += self.blwts[row_count]
			elif row_stat == -1:
				bl_lost += self.blwts[row_count]
			if col_stat == 2:
				freedom += 1
			elif col_stat == 1:
				freedom += 1
				bl_won += self.blwts[col_count]
			elif col_stat == -1:
				bl_lost += self.blwts[col_count]



			
		# some diamond shit

		


		return [
			freemove,
			cc_block_won, cc_block_lost, edge_block_won, edge_block_lost,
			bl_won, bl_lost,
			block_diamond_won, block_diamond_lost,

			cc_cell_won, cc_cell_lost, edge_cell_won, edge_cell_lost,
			cl_won, cl_lost,
			cl_diamond_won, cl_diamond_lost,
			# freedom/10.0,
			# cfreedom/160.0,
		]				

		





