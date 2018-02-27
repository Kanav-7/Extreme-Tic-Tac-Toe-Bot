import random
import datetime
import copy

class Player7:

	def __init__(self):
		
		self.ALPHA = -100000000
		self.BETA = 100000000
		self.dict = {}
		# self.lenght = 0
		self.HIGH_POS = [(0,1),(1,0),(2,1),(1,2),(0,2),(1,1),(2,2),(1,3),(2,0),(3,1),(3,2),(2,3)]
		self.LOW_POS = [(0,0),(0,3),(3,0),(3,3)]
		self.timeLimit = datetime.timedelta(seconds = 14.9)
		self.begin = 0
		self.WIN_UTILITY = 1000000
		self.cell_win = 1000


	def minimax(self,old_move, depth, max_depth, alpha, beta, isMax, p_board, p_block, flag1, flag2, best_node):
		if datetime.datetime.utcnow() - self.begin > self.timeLimit:
			return (-111,(-1,-1))
		terminal_state = p_board.find_terminal_state()
		if terminal_state[1] == 'WON' :
			if terminal_state[0] == flag1 :
				return (self.WIN_UTILITY,old_move)
			if terminal_state[0] == flag2 :
				return (-self.WIN_UTILITY,old_move)

		if depth==max_depth:
			utility = self.check_utility(p_block,p_board)
			if flag1 == 'o':
				return (-utility,old_move)
			return (utility,old_move)
		else:
			children_list = p_board.find_valid_move_cells(old_move)
			random.shuffle(children_list)
			if len(children_list) == 0:
				utility = self.check_utility(p_block,p_board)
				if flag1 == 'o':
					return (-utility,old_move)
				return (utility,old_move)
			for child in children_list:
				if isMax:
					p_board.update(old_move,child,flag1)
				else:
					p_board.update(old_move,child,flag2)
				if isMax:
					score = self.minimax (child,depth+1,max_depth,alpha,beta,False,p_board,p_block,flag1,flag2,best_node)
					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.board_status[child[0]][child[1]] = '-'
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						return (-111,(-1,-1))
					if (score[0] > alpha):
						alpha = score[0]
						best_node = child
				else:
					score = self.minimax (child,depth+1,max_depth,alpha,beta,True,p_board,p_block,flag1,flag2,best_node)
					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.board_status[child[0]][child[1]] = '-'
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						return (-111,(-1,-1))
					if (score[0] < beta):
						beta = score[0]
						best_node = child
				p_board.board_status[child[0]][child[1]] = '-'
				p_board.block_status[child[0]/4][child[1]/4] = '-'
				if (alpha >= beta):
					break
			if isMax:
				return (alpha, best_node)
			else:
				return(beta, best_node)

	def check_utility(self,block,board) :
		ans = 0
		ans += 100*self.block_utility(board.block_status,1,'x')
		ans -= 100*self.block_utility(board.block_status,1,'o')
		temp_block = []
		for i in range(0,4):
			for j in range(0,4):
				if(board.block_status[i][j] == '-'):
					temp_block = [[board.board_status[4*i+k][4*j+l] for l in range(0,4)] for k in range(0,4)]
		 			ans += self.block_utility(temp_block,1,'x')
		 			ans -= self.block_utility(temp_block,1,'o')
				elif(board.block_status[i][j] == 'x'):
					ans += self.cell_win
				elif(board.block_status[i][j] == 'o'):
					ans -= self.cell_win
		return ans

	def move(self,board,old_move,flag1) :
		self.timeLimit = datetime.timedelta(seconds = 14.9)
		self.begin = 0
		self.begin = datetime.datetime.utcnow()
		temp_board = copy.deepcopy(board)
		if flag1 == 'x' :
			flag2 = 'o'
		else :
			flag2 = 'x'
		maxDepth = 3
		while datetime.datetime.utcnow() - self.begin < self.timeLimit:
			(g,g_node) = self.minimax(old_move,0,maxDepth,self.ALPHA,self.BETA,True,temp_board, (1,1), flag1, flag2, (7,7))
			if g != -111 :
				best_node = g_node
			maxDepth += 1
		return best_node

	def block_utility(self,block,value,flag):
		block_1 = tuple([tuple(block[i]) for i in range(4)])
		ans = 0
		if (block_1, flag) not in self.dict:
			for pos in self.HIGH_POS:
				if block[pos[0]][pos[1]]==flag:
					ans += value*2

			for pos in self.LOW_POS:
				if block[pos[0]][pos[1]]==flag:
					ans += value

			if flag == 'x':
				flag2 = 'o'
			else:
				flag2 = 'x'
			for row in range(4):
				countflag = 0
				opponentflag = 0
				for col in range(4):
					if(block[row][col] == flag):
						countflag += 1
					elif((block[row][col] == flag2) or (block[row][col] == 'd')):
						opponentflag += 1
					if opponentflag == 0:
						if countflag == 2:
							ans += value*10
						elif countflag == 3:
							ans += value*100
						elif countflag == 4:
							ans = value*500

				for col in range(4):
					countflag = 0
					opponentflag = 0
					for row in range(4):
						if(block[row][col] == flag):
							countflag += 1
						elif((block[row][col] == flag2) or (block[row][col] == 'd')):
							opponentflag += 1
						if opponentflag == 0:
							if countflag == 2:
								ans += value*10
							elif countflag == 3:
								ans += value*100
							elif countflag == 4:
								ans = value*500

				countflag = 0
				opponentflag = 0
				






				# diamond1:
				if(block[0][1] == flag):
					countflag += 1
				elif((block[0][1] == flag2) or (block[0][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[1][0] == flag):
					countflag += 1
				elif((block[1][0] == flag2) or (block[1][0] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[2][1] == flag):
					countflag += 1
				elif((block[2][1] == flag2) or (block[2][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[1][2] == flag):
					countflag += 1
				elif((block[1][2] == flag2) or (block[1][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

								





				countflag = 0
				opponentflag = 0
				
				#diamnod 2
				
				if(block[0][2] == flag):
					countflag += 1
				elif((block[0][2] == flag2) or (block[0][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500
					
				if(block[1][1] == flag):
					countflag += 1
				elif((block[1][1] == flag2) or (block[1][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500
					
				if(block[2][2] == flag):
					countflag += 1
				elif((block[2][2] == flag2) or (block[2][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[1][3] == flag):
					countflag += 1
				elif((block[1][3] == flag2) or (block[1][3] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

									





				countflag = 0
				opponentflag = 0
					



				#diamond 3



				if(block[1][1] == flag):
					countflag += 1
				elif((block[1][1] == flag2) or (block[1][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[2][0] == flag):
					countflag += 1
				elif((block[2][0] == flag2) or (block[2][0] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[3][1] == flag):
					countflag += 1
				elif((block[3][1] == flag2) or (block[3][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[2][2] == flag):
					countflag += 1
				elif((block[2][2] == flag2) or (block[2][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500
									





				countflag = 0
				opponentflag = 0
					





				#diamond4

				if(block[1][2] == flag):
					countflag += 1
				elif((block[1][2] == flag2) or (block[1][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[2][1] == flag):
					countflag += 1
				elif((block[2][1] == flag2) or (block[2][1] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500
					
				if(block[3][2] == flag):
					countflag += 1
				elif((block[3][2] == flag2) or (block[3][2] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500

				if(block[2][3] == flag):
					countflag += 1
				elif((block[2][3] == flag2) or (block[2][3] == 'd')):
					opponentflag += 1
				if opponentflag == 0:
					if countflag == 2:
						ans += value*10
					elif countflag == 3:
						ans += value*100
					elif countflag == 4:
						ans = value*500
				


				self.dict[(block_1, flag)] = ans
				return self.dict[(block_1, flag)]

		else :
			return self.dict[(block_1, flag)]
