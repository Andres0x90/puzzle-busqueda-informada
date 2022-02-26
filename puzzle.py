import collections
import queue
import time

class Node:

    def __init__(self, puzzle, last=None):
        self.puzzle = puzzle
        self.last = last

    @property
    def seq(self): # to keep track of the sequence used to get to the goal
        node, seq = self, []
        while node:
            seq.append(node)
            node = node.last
        yield from reversed(seq)

    @property
    def state(self):
        return str(self.puzzle.board) # hashable so it can be compared in sets

    @property
    def isSolved(self):
        return self.puzzle.isSolved

    @property
    def getMoves(self):
        return self.puzzle.getMoves

    def getMTcost(self):
        """
        A* Heuristic where the next node to be expanded is chosen based upon how 
        many misplaced tiles (MT) are in the state of the next node 
        """
        totalMTcost = 0
        b = self.puzzle.board[:]
        # simply +1 if the tile isn't in the goal position
        # the zero tile doesn't count
        if b[1] != 1:
            totalMTcost += 1
        if b[2] != 2:
            totalMTcost += 1
        if b[3] != 3:
            totalMTcost += 1
        if b[4] != 4:
            totalMTcost += 1
        if b[5] != 5:
            totalMTcost += 1
        if b[6] != 6:
            totalMTcost += 1
        if b[7] != 7:
            totalMTcost += 1
        if b[8] != 8:
            totalMTcost += 1

        return totalMTcost


class Puzzle:

    def __init__(self, startBoard):
        self.board = startBoard

    @property
    def getMoves(self):

        possibleNewBoards = []

        zeroPos = self.board.index(0) # find the zero tile to determine possible moves

        if zeroPos == 0:
            possibleNewBoards.append(self.move(0,1))
            possibleNewBoards.append(self.move(0,3))
        elif zeroPos == 1:
            possibleNewBoards.append(self.move(1,0))
            possibleNewBoards.append(self.move(1,2))
            possibleNewBoards.append(self.move(1,4))
        elif zeroPos == 2:
            possibleNewBoards.append(self.move(2,1))
            possibleNewBoards.append(self.move(2,5))
        elif zeroPos == 3:
            possibleNewBoards.append(self.move(3,0))
            possibleNewBoards.append(self.move(3,4))
            possibleNewBoards.append(self.move(3,6))
        elif zeroPos == 4:
            possibleNewBoards.append(self.move(4,1))
            possibleNewBoards.append(self.move(4,3))
            possibleNewBoards.append(self.move(4,5))
            possibleNewBoards.append(self.move(4,7))
        elif zeroPos == 5:
            possibleNewBoards.append(self.move(5,2))
            possibleNewBoards.append(self.move(5,4))
            possibleNewBoards.append(self.move(5,8))
        elif zeroPos == 6:
            possibleNewBoards.append(self.move(6,3))
            possibleNewBoards.append(self.move(6,7))
        elif zeroPos == 7:
            possibleNewBoards.append(self.move(7,4))
            possibleNewBoards.append(self.move(7,6))
            possibleNewBoards.append(self.move(7,8))
        else:
            possibleNewBoards.append(self.move(8,5))
            possibleNewBoards.append(self.move(8,7))

        return possibleNewBoards # returns Puzzle objects (maximum of 4 at a time)

    def move(self, current, to):

        changeBoard = self.board[:] # create a copy
        changeBoard[to], changeBoard[current] = changeBoard[current], changeBoard[to] # switch the tiles at the passed positions
        return Puzzle(changeBoard) # return a new Puzzle object

    def printPuzzle(self): # prints board in 8 puzzle style

        copyBoard = self.board[:]
        for i in range(9):
            if i == 2 or i == 5:
                print(str(copyBoard[i]))
            else:
                print(str(copyBoard[i])+" ", end="")
        print('\n')

    @property
    def isSolved(self):
        return self.board == [0,1,2,3,4,5,6,7,8] # goal board

class Solver:

    def __init__(self, Puzzle):
        self.puzzle = Puzzle

    def FindLowestMTcost(NodeList):
        print(len(NodeList))
        lowestMTcostNode = NodeList[0]
        lowestMTcost = lowestMTcostNode.getMTcost()
        for i in range(len(NodeList)):
            if NodeList[i].getMTcost() < lowestMTcost:
                lowestMTcostNode = NodeList[i]
        return lowestMTcostNode # returns Node object

    def AStarMT(self):
        visited = set()
        myPQ = queue.PriorityQueue(0)
        myPQ.put((0, 0, Node(self.puzzle)))
        ctr = 0
        while myPQ:
            closetChild = myPQ.get()[2]
            visited.add(closetChild.state)
            for board in closetChild.getMoves:
                newChild = Node(board, closetChild)
                if newChild.state not in visited:
                    if newChild.getMTcost() == 0:
                        return newChild.seq
                    ctr += 1
                    myPQ.put((newChild.getMTcost(), ctr, newChild))

startingBoard = [7,2,4,5,0,6,8,3,1]

myPuzzle = Puzzle(startingBoard)
mySolver = Solver(myPuzzle)
start = time.time()
goalSeq = mySolver.AStarMT()
end = time.time()

counter = -1 # starting state doesn't count as a move
for node in goalSeq:
    counter = counter + 1
    node.puzzle.printPuzzle()
print("Total number of moves: " + str(counter))
totalTime = end - start
print("Total searching time: %.2f seconds" % (totalTime))