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
    if board == initial_state():
        return X
    elif Xs==Ys:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
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
        if board_copy[i][j] != None:
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
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    status = winner(board)
    if status:
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

next_action = ()

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        current = min_value(result(board, action))
        if current>v:
            v = current
            next_action = action
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        current =  max_value(result(board, action))
        if current < v:
            v = current
            next_action = action
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    chance = player(board)
    if chance == X:
        _ = max_value(board)
    else:
        _ = min_value(board)
    return next_action
