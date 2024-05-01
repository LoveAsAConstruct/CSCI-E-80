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


def player(board):
    # Count the number of Xs and Os
    Xcount = 0
    Ocount = 0
    for row in board:
        Xcount += row.count(X)
        Ocount += row.count(O)
                
    # If Xcount equals Ocount, it's X's turn since X starts the game
    if Xcount == Ocount:
        return X
    else:
        return O

def actions(board):
    # Return all empty tiles
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if not (0 <= action[0] < 3 and 0 <= action[1] < 3):
        raise ValueError("Action is out of bounds")
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Action is not valid on a non-empty cell")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    # Check rows and columns for a winner
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    # No winner
    return None


# Quick function to prevent me from copying and pasting alot
def booleanParsing(state, bool, firstElement):
    if bool:
        return state
    else:
        if not state:
            return None
        return firstElement
    
def winCheck(board, bool_out = True):
    # Check for matching rows
    for row in board:
        firstElement = row[0]
        if firstElement != EMPTY and all(column == firstElement for column in row):
            return booleanParsing(True, bool_out, firstElement)
        
    # Check for matching columns
    for c in range(len(board[0])):
        firstElement = board[0][c]
        if firstElement != EMPTY and all(row[c] == firstElement for row in board):
            return booleanParsing(True, bool_out, firstElement)
        
    # Check for matching diagonals
    BOARD_SIZE = len(board[0])
    firstElement = board[0][0]
    if firstElement != EMPTY and all(board[i][i] == firstElement for i in range(0,BOARD_SIZE)):
        return booleanParsing(True, bool_out, firstElement)
    firstElement =  board[0][BOARD_SIZE - 1]
    if firstElement != EMPTY and all( board[i][BOARD_SIZE - 1 - i] == firstElement for i in range(0,BOARD_SIZE)):
        return booleanParsing(True, bool_out, firstElement)
    
    # Return if no matches are found
    return booleanParsing(False, bool_out, firstElement)

def terminal(board):
    # Check if there's a winner
    if winner(board) is not None:
        return True

    # Check for a draw by verifying if there are any EMPTY spots left
    for row in board:
        if EMPTY in row:
            return False  # Game is not over, there are still moves to be made

    # If there's no winner and no empty spots, the game is a draw and thus terminal
    return True


def utility(board):
    # Return 1, -1, 0, if winner is X, O, or none, respectively
    winResult = winner(board)
    #print(str(winResult) +" as winner")
    if winResult == X:
        return 1
    elif winResult == O:
        return -1
    return 0

def iterateMinimax(board, depth, alpha, beta, maximizingPlayer):
    # Checks if depth is exausted or a win condition is found, then returns win state
    if depth == 0 or terminal(board):
        return utility(board)
    
    if maximizingPlayer:
        # Maximizing player turn
        maxEval = -math.inf
        for action in actions(board):
            eval = iterateMinimax(result(board,action), depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        # Minimizing player turn
        minEval = +math.inf
        for action in actions(board):
            eval = iterateMinimax(result(board,action), depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def best_move(board, depth):
    best_score = -math.inf
    best_move = None
    for action in actions(board):
        score = iterateMinimax(result(board, action), depth, -math.inf, math.inf, True)
        print("Playing in " +str(action) +" results in a score of " +str(score))
        if score > best_score:
            best_score = score
            best_move = action

    return best_move

def minimax(board):
    # Get best action for the algorithm
    if terminal(board):
        return None

    if player(board) == X:
        best_val = float('-inf')
        func = max
    else:
        best_val = float('inf')
        func = min

    best_action = None
    for action in actions(board):
        new_val = iterateMinimax(result(board, action), depth=math.inf, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=player(board) == O)
        if func(best_val, new_val) == new_val:
            best_val = new_val
            best_action = action

    return best_action
