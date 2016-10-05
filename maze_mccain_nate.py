# Name: Nate McCain
# Date: October 23, 2014
# Class: CS 142
# Pledge: I have neither given nor received unauthorized aid on this program.
# Description: TurtleMaze is a class object that creates a maze and defines the
#                         functions to navigate the maze. The function searchFrom finds
#                         the correct path to the end of the maze through recursive calls.
# Input: The user provides a maze for the program that includes a starting
#             point as well as the end point of the maze.
# Output: The program draws the maze using Turtle, and then the turtle navigates
#                the maze. It leaves a trail of "bread crumbs" to show all of the paths it
#                has attempted. Red indicates it is not a valid path and green indicates
#                the correct path.

import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'
GOAL = 'G'

class TurtleMaze(object):
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        self.goalRow = -1
        self.goalColumn = -1
        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            line = line.rstrip()
            rowList = []
            col = 0
            for ch in line:
                rowList.append(ch)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                elif ch == GOAL:
                    self.goalRow = rowsInMaze
                    self.goalColumn = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)
        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        #Allows for Turtle drawing
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-(columnsInMaze-1)/2-.5,-(rowsInMaze-1)/2-.5,(columnsInMaze-1)/2+.5,(rowsInMaze-1)/2+.5)

    def getStartRow(self):
        return self.startRow
    
    def getStartCol(self):
        return self.startCol
    
    def drawMaze(self):
        self.t.speed(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'blue')
                elif self.mazelist[y][x] == GOAL:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'yellow')
        self.t.color('black')
        self.t.fillcolor('blue')

    def drawCenteredBox(self,x,y,color):
        self.t.up()
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    # Tells user that the turtle has been there
    def dropBreadcrumb(self,color):
        self.t.dot(10,color)

    # Marks the passed in location with a dot - colored according to status
    def updatePosition(self,row,col,val=None):
        if val != None:
            self.mazelist[row][col] = val
        self.moveTurtle(col,row)

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color != None:
            self.dropBreadcrumb(color)

    def foundGoal(self,row,col):
        return row == self.goalRow and col == self.goalColumn

    def __getitem__(self,idx):
        return self.mazelist[idx]

# Recursive function traverses through the maze starting at start point
# until it finds the goal point or traverses entire maze.
# Parameters: maze object of type TurtleMaze,
# startRow, startColumn, starting row and column for turtle.
# Returns: True if goal has been found, False otherwise.
def searchFrom(maze, startRow, startColumn):
    # This will draw the current position of the turtle in the maze
    maze.updatePosition(startRow, startColumn)
    # Try each of four directions from this point until we find a way out.
    # Base Case return values:
    #  1. We have run into an obstacle, return False
    if maze[startRow][startColumn] == OBSTACLE:
        return False
    #  2. We have found a square that has already been explored, return False
    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        return False
    #  3. We have found our goal, return True
    if maze.foundGoal(startRow, startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        return True
    # This will update the color at the current position of the turtle in the maze
    # This line should occur after all base cases and before the recursive cases
    maze.updatePosition(startRow, startColumn, TRIED)

    # Recursive cases - try each direction (north, south, east and west)
    # Use logical short circuiting to try each direction in turn (if needed)
    # If you can't go North (obstacle), then try South, if you can't go South
    # try East, if you can't go East, try West
    # If none of those directions work, you have exhausted all your options and your turtle 
    # should return to his start point.
    found = searchFrom(maze, startRow - 1, startColumn) or \
                   searchFrom(maze, startRow + 1, startColumn) or \
                   searchFrom(maze, startRow, startColumn + 1) or \
                   searchFrom(maze, startRow, startColumn - 1)

    # You shouldn't need to change the code below this line - unless you'd like to customize the outputs
    if found:
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
            print("Success! We are retracing the path now.")
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)
        print("I'm afraid that won't work.")
    return found

def main():
    # Be sure that maze2.txt resides in the same folder as your python file
    myMaze = TurtleMaze('maze2.txt')
    # Uses turtle to draw the maze from the input file
    myMaze.drawMaze()
    # Places the turtle on his starting location (according to the S in the input file)
    myMaze.updatePosition(myMaze.getStartRow(),myMaze.getStartCol())

    # Call recursive function to traverse turtle through the maze
    searchFrom(myMaze, myMaze.getStartRow(), myMaze.getStartCol())

main()
