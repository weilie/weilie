# convert number representations to board pieces
SYMBOLS = {1: "x", -1: "o", 0: " "}

def avialablePositions(board):
    positions = []
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                positions.append((x, y))
    return positions

def printBoard(board):
    # shift the board to the right as number of placed pieces increases
    totalPiecesPlaced = 9 - len(avialablePositions(board))
    stepSize = 15
    whiteSpace = ' ' * totalPiecesPlaced * stepSize
    print(f"{whiteSpace}-------------")
    for x in range(3):
        print(
            "{}| {} | {} | {} |".format(
                whiteSpace, SYMBOLS[board[x][0]], SYMBOLS[board[x][1]], SYMBOLS[board[x][2]]
            )
        )
        print(f"{whiteSpace}-------------")

def determineWinner(board):
    if (
        board[0][0] + board[0][1] + board[0][2] == 3
        or board[1][0] + board[1][1] + board[1][2] == 3
        or board[2][0] + board[2][1] + board[2][2] == 3
    ):
        # horizontal
        return 1
    elif (
        board[0][0] + board[1][0] + board[2][0] == 3
        or board[0][1] + board[1][1] + board[2][1] == 3
        or board[0][2] + board[1][2] + board[2][2] == 3
    ):
        # vertical
        return 1
    elif (
        board[0][0] + board[1][1] + board[2][2] == 3
        or board[2][0] + board[1][1] + board[0][2] == 3
    ):
        # diagnal
        return 1
    elif (
        board[0][0] + board[0][1] + board[0][2] == -3
        or board[1][0] + board[1][1] + board[1][2] == -3
        or board[2][0] + board[2][1] + board[2][2] == -3
    ):
        # horizontal
        return -1
    elif (
        board[0][0] + board[1][0] + board[2][0] == -3
        or board[0][1] + board[1][1] + board[2][1] == -3
        or board[0][2] + board[1][2] + board[2][2] == -3
    ):
        # vertical
        return -1
    elif (
        board[0][0] + board[1][1] + board[2][2] == -3
        or board[2][0] + board[1][1] + board[0][2] == -3
    ):
        # diagnal
        return -1
    return None

def copyBoard(board):
    # there is an easier way than this
    newBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for x in range(3):
        for y in range(3):
            newBoard[x][y] = board[x][y]
    return newBoard

def scoreMove(board, position, side):
    printBoard(board)
    print(f"side {side} ({SYMBOLS[side]}) is considering placing {position} on board")

    x = position[0]
    y = position[1]

    # do some sanity checks
    if board[x][y] != 0 or side != -1 and side != 1:
        # this is unexpected
        print(f"something's wrong: board = {board}, side = {side}")
        return None

    # if someone already won, return that score
    winner = determineWinner(board)
    if winner != None:
        print(f'# scoreMove() returning {winner} because {winner} already won')
        return winner

    # place the move (x,y) and evaluate the results
    # first make a copy of the board so we don't change the originals
    newBoard = copyBoard(board)
    newBoard[x][y] = side
    nextPositions = avialablePositions(newBoard)

    # if the board is full, see if anybody wins
    if len(nextPositions) == 0:
        # this is our exit from the recursive function
        winner = determineWinner(newBoard)
        print(f"reached the end - and the winner is {winner}")
        # the score is determined by who wins
        if winner == None:
            score = 0
        else:
            score = winner
        print(f'# scoreMove() returning {score} because {winner} already won')
        return score

    # board not full, so a next step exists
    # try out every possible next move and get the minimum or maximum of them depending on whose turn it is
    if side == 1:
        # this was my move. My opponent is playing next, trying to minimize my board score
        lowestScore = 9999
        for nextPosition in nextPositions:
            score = scoreMove(newBoard, nextPosition, -1)
            if score < lowestScore:
                lowestScore = score
        print(f'# scoreMove() returning {lowestScore} for side -1 which is minimizing score')
        return lowestScore
    else:
        # this was my opponent's move. My move is next, trying to maximize my board score
        highestScore = -9999
        for nextPosition in nextPositions:
            score = scoreMove(newBoard, nextPosition, 1)
            if score > highestScore:
                highestScore = score
        print(f'# scoreMove() returning {highestScore} for side 1 which is maximizing score')
        return highestScore


board = [[1, 0, 0], [-1, 0, 1], [0, -1, 0]]
printBoard(board)
positions = avialablePositions(board)
bestScore = -9999
bestMove = None
for position in positions:
    score = scoreMove(board, position, 1)
    print(f'Finished evaluating position {position}. Score = {score}')
    if score > bestScore:
        bestScore = score
        bestMove = position
print(f'Finished evaluating all postions. The best move is {bestMove}, with score {bestScore}')
if bestScore > 0:
    print('Winning is guaranteed. Any effort by the opponent is futile.')
else:
    print('Winning is not guaranteed. Hope the opponent makes mistakes.')
printBoard(board)
