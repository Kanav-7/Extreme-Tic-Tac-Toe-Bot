import random
import time
class Player57():
    def __init__(self):
        self.inf = 10 ** 18
        self.depth = 6
        self.flag = ''
        self.other = ''
        self.timeLimit = 14
        self.starttime=0
        pass

    def move(self, board, old_move, flag):
        self.flag = flag
        self.other = 'o' if flag == 'x' else 'x'
        ans = self.minimax(board, old_move, 0, -self.inf, self.inf)
        return ans[1]

    def undo(self, board, old_move):
        bx = old_move[0]/4
        by = old_move[1]/4
        board.block_status[bx][by] = '-'
        board.board_status[old_move[0]][old_move[1]] = '-'

    def cheapAssHeuristic(self, board):

        flag_attack = [[0 for i in range(4)] for j in range(4)]
        other_attack = [[0 for i in range(4)] for j in range(4)]
        totalResFlagAttack = 0
        totalResOtherAttack = 0
        resFlagAttack = 0
        resOtherAttack = 0

        for i in xrange(0, 16):
            for j in xrange(0, 13, 4):
                cnt_flag = (board.board_status[i][j] == self.flag) + (board.board_status[i][j + 1] == self.flag) + (board.board_status[i][j + 2] == self.flag) + (board.board_status[i][j + 3] == self.flag)
                cnt_hyphen = (board.board_status[i][j] == '-') + (board.board_status[i][j + 1] == '-') + (board.board_status[i][j + 2] == '-') + (board.board_status[i][j + 3] == '-')
                cnt_other = (board.board_status[i][j] == self.other) + (board.board_status[i][j + 1] == self.other) + (board.board_status[i][j + 2] == self.other) + (board.board_status[i][j + 3] == self.other)
                wt = 0
                if (i % 4 == 1 or i % 4 == 2) and (j % 4 == 1 or j % 4 == 2):
                    wt = 3
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)

        for i in xrange(0, 13, 4):
            for j in xrange(0, 16):
                cnt_flag = (board.board_status[i][j] == self.flag) + (board.board_status[i + 1][j] == self.flag) + (board.board_status[i + 2][j] == self.flag) + (board.board_status[i + 3][j] == self.flag)
                cnt_hyphen = (board.board_status[i][j] == '-') + (board.board_status[i + 1][j] == '-') + (board.board_status[i + 2][j] == '-') + (board.board_status[i + 3][j] == '-')
                cnt_other = (board.board_status[i][j] == self.other) + (board.board_status[i + 1][j] == self.other) + (board.board_status[i + 2][j] == self.other) + (board.board_status[i + 3][j] == self.other)
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)

        for i in xrange(0, 13, 4):
            for j in xrange(0, 13, 4):
                cnt_flag = (board.board_status[i+1][j] == self.flag) + (board.board_status[i][j + 1] == self.flag) + (board.board_status[i + 2][j + 1] == self.flag) + (board.board_status[i + 1][j + 2] == self.flag)
                cnt_hyphen = (board.board_status[i+1][j] == '-') + (board.board_status[i][j + 1] == '-') + (board.board_status[i + 2][j + 1] == '-') + (board.board_status[i + 1][j + 2] == '-')
                cnt_other = (board.board_status[i+1][j] == self.other) + (board.board_status[i][j + 1] == self.other) + (board.board_status[i + 2][j + 1] == self.other) + (board.board_status[i + 1][j + 2] == self.other)
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)
                
                cnt_flag = (board.board_status[i + 1][j+1] == self.flag) + (board.board_status[i + 2][j] == self.flag) + (board.board_status[i + 2][j + 2] == self.flag) + (board.board_status[i+3][j + 1] == self.flag)
                cnt_hyphen = (board.board_status[i + 1][j+1] == '-') + (board.board_status[i + 2][j] == '-') + (board.board_status[i + 2][j + 2] == '-') + (board.board_status[i+3][j + 1] == '-')
                cnt_other = (board.board_status[i + 1][j+1] == self.other) + (board.board_status[i + 2][j] == self.other) + (board.board_status[i + 2][j + 2] == self.other) + (board.board_status[i+3][j + 1] == self.other)
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)

                
                cnt_flag = (board.board_status[i ][j+2] == self.flag) + (board.board_status[i + 1][j+1] == self.flag) + (board.board_status[i + 2][j + 2] == self.flag) + (board.board_status[i+1][j + 3] == self.flag)
                cnt_hyphen = (board.board_status[i ][j+2] == '-') + (board.board_status[i + 1][j+1] == '-') + (board.board_status[i + 2][j + 2] == '-') + (board.board_status[i+1][j + 3] == '-')
                cnt_other = (board.board_status[i ][j+2] == self.other) + (board.board_status[i + 1][j+1] == self.other) + (board.board_status[i + 2][j + 2] == self.other) + (board.board_status[i+1][j + 3] == self.other)
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)


                cnt_flag = (board.board_status[i + 1][j+2] == self.flag) + (board.board_status[i + 2][j+1] == self.flag) + (board.board_status[i + 2][j + 3] == self.flag) + (board.board_status[i+3][j + 2] == self.flag)
                cnt_hyphen = (board.board_status[i + 1][j+2] == '-') + (board.board_status[i + 2][j+1] == '-') + (board.board_status[i + 2][j + 3] == '-') + (board.board_status[i+3][j + 2] == '-')
                cnt_other = (board.board_status[i + 1][j+2] == self.other) + (board.board_status[i + 2][j+1] == self.other) + (board.board_status[i + 2][j + 3] == self.other) + (board.board_status[i+3][j + 2] == self.other)
                if cnt_other == 0:
                    flag_attack[i/4][j/4] = max(flag_attack[i/4][j/4], cnt_flag)
                elif cnt_flag == 0:
                    other_attack[i/4][j/4] = max(other_attack[i/4][j/4], cnt_other)


        for i in xrange(0, 4):
            cnt_flag = (board.block_status[i][0] == self.flag) + (board.block_status[i][1] == self.flag) + (board.block_status[i][2] == self.flag) + (board.block_status[i][3] == self.flag)
            cnt_hyphen = (board.block_status[i][0] == '-') + (board.block_status[i][1] == '-') + (board.block_status[i][2] == '-') + (board.block_status[i][3] == '-')
            cnt_other = (board.block_status[i][0] == self.other) + (board.block_status[i][1] == self.other) + (board.block_status[i][2] == self.other) + (board.block_status[i][3] == self.other)
            if cnt_other == 0:
                resFlagAttack = max(resFlagAttack, cnt_flag)
            elif cnt_flag == 0:
                resOtherAttack = max(resOtherAttack, cnt_other)

        for i in xrange(0, 4):
            cnt_flag = (board.block_status[0][i] == self.flag) + (board.block_status[1][i] == self.flag) + (board.block_status[2][i] == self.flag) + (board.block_status[3][i] == self.flag)
            cnt_hyphen = (board.block_status[0][i] == '-') + (board.block_status[1][i] == '-') + (board.block_status[2][i] == '-') + (board.block_status[3][i] == '-')
            cnt_flag = (board.block_status[0][i] == self.flag) + (board.block_status[1][i] == self.flag) + (board.block_status[2][i] == self.flag) + (board.block_status[3][i] == self.flag)
            if cnt_other == 0:
                resFlagAttack = max(resFlagAttack, cnt_flag)
            elif cnt_flag == 0:
                resOtherAttack = max(resOtherAttack, cnt_other)

        cnt_flag = (board.block_status[0][1] == self.flag) + (board.block_status[1][0] == self.flag) + (board.block_status[1][2] == self.flag) + (board.block_status[2][1] == self.flag)
        cnt_hyphen = (board.block_status[0][1] == '-') + (board.block_status[1][0] == '-') + (board.block_status[1][2] == '-') + (board.block_status[2][1] == '-')
        cnt_other = (board.block_status[0][1] == self.other) + (board.block_status[1][0] == self.other) + (board.block_status[1][2] == self.other) + (board.block_status[2][1] == self.other)
        if cnt_other == 0:
            resFlagAttack = max(resFlagAttack, cnt_flag)
        elif cnt_flag == 0:
            resOtherAttack = max(resOtherAttack, cnt_other)

        cnt_flag = (board.block_status[1][1] == self.flag) + (board.block_status[2][0] == self.flag) + (board.block_status[2][2] == self.flag) + (board.block_status[3][1] == self.flag)
        cnt_hyphen = (board.block_status[1][1] == '-') + (board.block_status[2][0] == '-') + (board.block_status[2][2] == '-') + (board.block_status[3][1] == '-')
        cnt_other = (board.block_status[1][1] == self.other) + (board.block_status[2][0] == self.other) + (board.block_status[2][2] == self.other) + (board.block_status[3][1] == self.other)
        if cnt_other == 0:
            resFlagAttack = max(resFlagAttack, cnt_flag)
        elif cnt_flag == 0:
            resOtherAttack = max(resOtherAttack, cnt_other)

        cnt_flag = (board.block_status[0][2] == self.flag) + (board.block_status[1][1] == self.flag) + (board.block_status[2][2] == self.flag) + (board.block_status[1][3] == self.flag)
        cnt_hyphen = (board.block_status[0][2] == '-') + (board.block_status[1][1] == '-') + (board.block_status[2][2] == '-') + (board.block_status[1][3] == '-')
        cnt_other = (board.block_status[0][2] == self.other) + (board.block_status[1][1] == self.other) + (board.block_status[2][2] == self.other) + (board.block_status[1][3] == self.other)
        if cnt_other == 0:
            resFlagAttack = max(resFlagAttack, cnt_flag)
        elif cnt_flag == 0:
            resOtherAttack = max(resOtherAttack, cnt_other)

        cnt_flag = (board.block_status[3][2] == self.flag) + (board.block_status[2][1] == self.flag) + (board.block_status[1][2] == self.flag) + (board.block_status[2][3] == self.flag)
        cnt_hyphen = (board.block_status[3][2] == '-') + (board.block_status[2][1] == '-') + (board.block_status[1][2] == '-') + (board.block_status[2][3] == '-')
        cnt_other = (board.block_status[3][2] == self.other) + (board.block_status[2][1] == self.other) + (board.block_status[1][2] == self.other) + (board.block_status[2][3] == self.other)
        if cnt_other == 0:
            resFlagAttack = max(resFlagAttack, cnt_flag)
        elif cnt_flag == 0:
            resOtherAttack = max(resOtherAttack, cnt_other)    



        ans = 0
        wins = 0
        losses = 0
        for i in xrange(0, 4):
            for j in xrange(0, 4):
                ans += 2 * (2 * flag_attack[i][j] * flag_attack[i][j] - 3 * other_attack[i][j] * other_attack[i][j])
                wins += (board.block_status[i][j] == self.flag)
                losses += (board.block_status[i][j] == self.other)

        ans += 10 * (resFlagAttack * resFlagAttack - 3 * resOtherAttack * resOtherAttack)
        ans += 4 * (wins - losses)
        res = [ans, (0, 0), wins]
        return res

    def findBestBlock(self, board):

        allowed_cells = []
        x = -1
        y = -1
        bestAttack = -1

        for i in xrange(0, 4):
            cnt_flag = (board.block_status[i][0] == self.flag) + (board.block_status[i][1] == self.flag) + (board.block_status[i][2] == self.flag) + (board.block_status[i][3] == self.flag)
            cnt_hyphen = (board.block_status[i][0] == '-') + (board.block_status[i][1] == '-') + (board.block_status[i][2] == '-') + (board.block_status[i][3] == '-')
            cnt_other = (board.block_status[i][0] == self.other) + (board.block_status[i][1] == self.other) + (board.block_status[i][2] == self.other) + (board.block_status[i][3] == self.other)
            if cnt_other == 0 and cnt_flag > bestAttack:
                bestAttack = cnt_flag
                for j in xrange(0, 4):
                    if board.block_status[i][j] == '-':
                        x = i
                        y = j
                        break
            elif cnt_flag == 0 and cnt_other >= bestAttack:
                bestAttack = cnt_other
                for j in xrange(0, 4):
                    if board.block_status[i][j] == '-':
                        x = i
                        y = j
                        break


        for i in xrange(0, 4):
            cnt_flag = (board.block_status[0][i] == self.flag) + (board.block_status[1][i] == self.flag) + (board.block_status[2][i] == self.flag) + (board.block_status[3][i] == self.flag)
            cnt_hyphen = (board.block_status[0][i] == '-') + (board.block_status[1][i] == '-') + (board.block_status[2][i] == '-') + (board.block_status[3][i] == '-')
            cnt_other = (board.block_status[0][i] == self.other) + (board.block_status[1][i] == self.other) + (board.block_status[2][i] == self.other) + (board.block_status[3][i] == self.other)
            if cnt_other == 0 and cnt_flag > bestAttack:
                bestAttack = cnt_flag
                for j in xrange(0, 4):
                    if board.block_status[j][i] == '-':
                        x = j
                        y = i
                        break
            elif cnt_flag == 0 and cnt_other >= bestAttack:
                bestAttack = cnt_other
                for j in xrange(0, 4):
                    if board.block_status[j][i] == '-':
                        x = j
                        y = i
                        break

        cnt_flag = (board.block_status[0][1] == self.flag) + (board.block_status[1][0] == self.flag) + (board.block_status[1][2] == self.flag) + (board.block_status[2][1] == self.flag)
        cnt_hyphen = (board.block_status[0][1] == '-') + (board.block_status[1][0] == '-') + (board.block_status[1][2] == '-') + (board.block_status[2][1] == '-')
        cnt_other = (board.block_status[0][1] == self.other) + (board.block_status[1][0] == self.other) + (board.block_status[1][2] == self.other) + (board.block_status[2][1] == self.other)
        if cnt_other == 0 and cnt_flag > bestAttack:
            bestAttack = cnt_flag
            if board.block_status[0][1] == '-':
                x = 0
                y = 1
            elif board.block_status[1][0] == '-':
                x = 1
                y = 0
            elif board.block_status[1][2] == '-':
                x = 1
                y = 2
            elif board.block_status[2][1] == '-':
                x = 2
                y = 1

        elif cnt_flag == 0 and cnt_other >= bestAttack:
            bestAttack = cnt_other
            if board.block_status[0][1] == '-':
                x = 0
                y = 1
            elif board.block_status[1][0] == '-':
                x = 1
                y = 0
            elif board.block_status[1][2] == '-':
                x = 1
                y = 2
            elif board.block_status[2][1] == '-':
                x = 2
                y = 1            

        cnt_flag = (board.block_status[1][1] == self.flag) + (board.block_status[2][0] == self.flag) + (board.block_status[2][2] == self.flag) + (board.block_status[3][1] == self.flag)
        cnt_hyphen = (board.block_status[1][1] == '-') + (board.block_status[2][0] == '-') + (board.block_status[2][2] == '-') + (board.block_status[3][1] == '-')
        cnt_other = (board.block_status[1][1] == self.other) + (board.block_status[2][0] == self.other) + (board.block_status[2][2] == self.other) + (board.block_status[3][1] == self.other)
        if cnt_other == 0 and cnt_flag > bestAttack:
            bestAttack = cnt_flag
            if board.block_status[1][1] == '-':
                x = 1
                y = 1
            elif board.block_status[2][0] == '-':
                x = 2
                y = 0
            elif board.block_status[2][2] == '-':
                x = 2
                y = 2
            elif board.block_status[3][1] == '-':
                x = 3
                y = 1

        elif cnt_flag == 0 and cnt_other >= bestAttack:
            bestAttack = cnt_other
            if board.block_status[1][1] == '-':
                x = 1
                y = 1
            elif board.block_status[2][0] == '-':
                x = 2
                y = 0
            elif board.block_status[2][2] == '-':
                x = 2
                y = 2
            elif board.block_status[3][1] == '-':
                x = 3
                y = 1


        cnt_flag = (board.block_status[0][2] == self.flag) + (board.block_status[1][1] == self.flag) + (board.block_status[2][2] == self.flag) + (board.block_status[1][3] == self.flag)
        cnt_hyphen = (board.block_status[0][2] == '-') + (board.block_status[1][1] == '-') + (board.block_status[2][2] == '-') + (board.block_status[1][3] == '-')
        cnt_other = (board.block_status[0][2] == self.other) + (board.block_status[1][1] == self.other) + (board.block_status[2][2] == self.other) + (board.block_status[1][3] == self.other)
        if cnt_other == 0 and cnt_flag > bestAttack:
            bestAttack = cnt_flag
            if board.block_status[0][1] == '-':
                x = 0
                y = 1
            elif board.block_status[1][1] == '-':
                x = 1
                y = 1
            elif board.block_status[2][2] == '-':
                x = 2
                y = 2
            elif board.block_status[1][3] == '-':
                x = 1
                y = 3

        elif cnt_flag == 0 and cnt_other >= bestAttack:
            bestAttack = cnt_other
            if board.block_status[0][1] == '-':
                x = 0
                y = 1
            elif board.block_status[1][1] == '-':
                x = 1
                y = 1
            elif board.block_status[2][2] == '-':
                x = 2
                y = 2
            elif board.block_status[1][3] == '-':
                x = 1
                y = 3


        cnt_flag = (board.block_status[3][2] == self.flag) + (board.block_status[2][1] == self.flag) + (board.block_status[1][2] == self.flag) + (board.block_status[2][3] == self.flag)
        cnt_hyphen = (board.block_status[3][2] == '-') + (board.block_status[2][1] == '-') + (board.block_status[1][2] == '-') + (board.block_status[2][3] == '-')
        cnt_other = (board.block_status[3][2] == self.other) + (board.block_status[2][1] == self.other) + (board.block_status[1][2] == self.other) + (board.block_status[2][3] == self.other)
        if cnt_other == 0 and cnt_flag > bestAttack:
            bestAttack = cnt_flag
            if board.block_status[3][2] == '-':
                x = 3
                y = 2
            elif board.block_status[2][1] == '-':
                x = 2
                y = 1
            elif board.block_status[1][2] == '-':
                x = 1
                y = 2
            elif board.block_status[2][3] == '-':
                x = 2
                y = 3

        elif cnt_flag == 0 and cnt_other >= bestAttack:
            bestAttack = cnt_other
            if board.block_status[3][2] == '-':
                x = 3
                y = 2
            elif board.block_status[2][1] == '-':
                x = 2
                y = 1
            elif board.block_status[1][2] == '-':
                x = 1
                y = 2
            elif board.block_status[2][3] == '-':
                x = 2
                y = 3
                

        if x != -1:
            for i in xrange(4 * x, 4 * x + 4):
                for j in xrange(4 * y, 4 * y + 4):
                    if board.board_status[i][j] == '-':
                        allowed_cells.append((i, j))

        if len(allowed_cells) > 0:
            return allowed_cells


        #Have to change this to something more efficient
        for i in xrange(0, 16):
            for j in xrange(0, 16):
                if board.block_status[i/4][j/4] == '-' and board.board_status[i][j] == '-':
                    allowed_cells.append((i, j))
                    break

        return allowed_cells

    def minimax(self, board, prev_move, depth, alpha, beta):

        terminal_state = board.find_terminal_state();
        if terminal_state[1] == 'DRAW':
            val = self.cheapAssHeuristic(board)
            ret = [val[2], val[1]]
            return ret
        if terminal_state[1] == 'WIN' and terminal_state[0] == self.flag: return self.inf
        if terminal_state[1] == 'WIN': return -self.inf

        if depth >= self.depth :
            #print self.starttime
            #self.starttime=0
            val = self.cheapAssHeuristic(board)
            ret = [val[0], val[1]]
            
            return ret

        valid_moves = board.find_valid_move_cells(prev_move)
        random.shuffle(valid_moves)
        if len(valid_moves) > 16:
            valid_moves = []
            valid_moves = self.findBestBlock(board)
            random.shuffle(valid_moves)
        best_move = []
        if depth % 2 == 0:
            bestVal = -self.inf
            for cur_move in valid_moves:
                board.update(prev_move, cur_move, self.flag)
                x = self.minimax(board, cur_move, depth + 1, alpha, beta)
                if bestVal < x[0]:
                    bestVal = x[0]
                    best_move = cur_move
                self.undo(board, cur_move)
                alpha = max(alpha, bestVal);
                if beta <= alpha:
                    break
        else:
            bestVal = self.inf
            for cur_move in valid_moves:
                board.update(prev_move, cur_move, self.other)
                x = self.minimax(board, cur_move, depth + 1, alpha, beta)
                if bestVal > x[0]:
                    bestVal = x[0]
                    best_move = cur_move
                self.undo(board, cur_move)
                beta = min(bestVal, beta)
                if beta <= alpha:
                    break
        return bestVal, best_move
