"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def count(board):
    Xs = sum([i.count('X') for i in board])
    Ys = sum([i.count('O') for i in board])
    return Xs, Ys

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs, Ys = count(board)
    if Xs==Ys:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                all_actions.add((i,j))
    return all_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if action:
        i,j = action
        playerturn = player(board_copy)
        if board_copy[i][j] != EMPTY:
            raise Exception('Not valid move!')
        elif playerturn == X:
            board_copy[i][j] = X
        else:
            board_copy[i][j] = O
    return board_copy
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    Xs, Ys = count(board)
    if Xs <= 2 and Ys <= 2:
        return None
    else:
        if (board[0][0] == board[1][1] == board[2][2])  or (board[0][2] == board[1][1] == board[2][0]):
            return board[1][1]
        else:
            if (board[0][0] == board[1][0] == board[2][0]):
                return board[1][0] 
            elif (board[0][2] == board[1][2] == board[2][2]):
                return board[1][2]
            elif (board[2][0] == board[2][1] == board[2][2]):
                return board[2][1]
            elif (board[0][0] == board[0][1] == board[0][2]):
                return board[0][1]
            elif (board[1][0] == board[1][1] == board[1][2]):
                return board[1][1]
            elif (board[0][1] == board[1][1] == board[2][1]):
                return board[1][1]
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    status = winner(board)
    Xs, Ys = count(board)
    if status or ((Xs + Ys) == 9):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    whowon = winner(board)
    if whowon == X:
        return 1
    elif whowon == O:
        return -1
    return 0

def maximize(board, alpha, beta):
    max_val = float('-inf')
    max_action = ()
    if terminal(board):
        return utility(board)
    for action in actions(board):
        returnval = minimize(result(board, action), alpha, beta)
        if isinstance(returnval, tuple):
            val, _ = returnval
        else:
            val = returnval
        if val > max_val:
            max_action = action
            max_val = val
        alpha = max(alpha, max_val)
        if beta<= alpha:
            break
    return max_val, max_action

def minimize(board, alpha, beta):
    min_val = float('inf')
    min_action = ()
    if terminal(board):
        return utility(board)
    for action in actions(board):
        returnval = maximize(result(board, action),alpha, beta)
        if isinstance(returnval, tuple):
            val, _ = returnval
        else:
            val = returnval
        if val < min_val:
            min_action = action
            min_val = val
        beta = min(beta, min_val)
        if beta<=alpha:
            break
    return min_val, min_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Alpha worst case for X
    # Beta worst case for Y
    # beta less than alpha means that earlier X(root of current node which has explored atleast 1 node) had a better option available so
    # no use exploring further
    alpha = float('-inf')
    beta = float('inf')
    if terminal(board):
        return None
    chance = player(board)
    if chance == X:
        _, move = maximize(board, alpha, beta)
    else:
        _, move = minimize(board, alpha, beta)
    return move



