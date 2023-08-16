import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    #Trả về trạng thái bắt đầu
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    #Trả về người trên
    xCounter = 0
    oCounter = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1

    if xCounter > oCounter:
        return O
    else:
        return X


def actions(board):
    #Trả về các nước đã đánh
    possibleActions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    #Trả về bang mới
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    #Trả về chiến thắng
    #Kiểm tra hàng
    if all(i == board[0][0] for i in board[0]):
        return board[0][0]
    elif all(i == board[1][0] for i in board[1]):
        return board[1][0]
    elif all(i == board[2][0] for i in board[2]):
        return board[2][0]
    #Kiểm tra cột
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    #Kiểm tra đường chéo
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    #Trả về đúng thì dừng, sai thì không

    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False
    #Trả về True nếu winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None) else False # noqa E501


def utility(board):
    #Trả về 1 nếu x thắng, -1 nếu o thắng, và 0 nếu hòa
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        #v = max(v, min_value(result(board, action)))
        aux, act = min_value(result(board, action))
        if aux > v:
            v = aux
            move = action
            if v == 1:
                return v, move

    return v, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    move = None
    for action in actions(board):
        #v = max(v, min_value(result(board, action)))
        aux, act = max_value(result(board, action))
        if aux < v:
            v = aux
            move = action
            if v == -1:
                return v, move

    return v, move