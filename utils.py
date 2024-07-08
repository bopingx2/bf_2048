import pygame
from pygame.locals import *

import random
from copy import deepcopy

from typing import List
Board = List[List[int]]

# Initialize pygame, display, font, color, and size
pygame.init()
display = pygame.display.set_mode((600, 600))
cell_font = pygame.font.SysFont('ClearSansBold', 64)
menu_font = pygame.font.SysFont('ClearSans', 36)
cell_color = {0: (205, 193, 180),
              2: (238, 228, 218),
              4: (237, 224, 200),
              8: (242, 177, 121),
              16: (245, 149, 99),
              32: (246, 124, 95),
              64: (246, 94, 59),
              128: (237, 207, 114),
              256: (237, 204, 97),
              512: (237, 200, 80),
              1024: (237, 197, 63),
              2048: (237, 194, 46)}
bg_color = (190, 169, 159)
font_color = (70, 60, 60)
box = 150
pad = 6

def add_two(board: Board, count:int = 1) -> Board:
    """Randomly add desired number of 2 on to the board

    Parameters
    ----------
    board : Board
        Game board that will be added with 2
    count : int
        Number of 2 will be added

    Returns
    -------
    Board
        Game board that has number of 2 added
    """

    for _ in range(count):
        # Random choose a cell
        row = random.randint(0, 3)
        col = random.randint(0, 3)

        # If cell has number, select another
        while board[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

        # Fill the cell with 2
        board[row][col] = 2

    return board

def check_status(board: Board) -> int:
    """Check the status of game board after player makes a operation

    Parameters
    ----------
    board : Board
        Game board after certain operation

    Returns
    -------
    int
        Game status, 1 if player can make further move, 2 if player
        has completed a 2048, 3 if player cannot make futher move
    """

    # Get distinct number on the board
    cells = set([j for i in board for j in i])

    # If 2048 is found, game stop and player wins
    if 2048 in cells:
        return 2

    # Check if there are potential merge
    for i in range(4):
        for j in range(4):
            # If potential merge found, keep playing
            if (j != 3 and board[i][j] == board[i][j + 1]) or\
               (i != 3 and board[i][j] == board[i + 1][j]):
                return 1

    # No potential merge and no empty cell, game stop and player lose
    if 0 not in cells:
        return 3

    # Have empty cell, keep playing
    return 1

def reset_board() -> Board:
    """Generate an empty board and randomly add two 2 on it.

    Returns
    -------
    Board
        Game board that has two of 2 added
    """

    # 0 for empty cell, 4 * 4
    board = [[0] * 4 for _ in range(4)]

    # Add two 2
    add_two(board, 2)

    # Show the board to player
    show_board(board)

    return board

def show_board(board: Board) -> None:
    """Visually present the board on screen to player

    Parameters
    ----------
    board : Board
        Game board that player will play with
    """

    # Fill the screen with background color
    display.fill(bg_color)

    # Fill every cell with corresponding color and text
    for i in range(4):
        for j in range(4):
            # Get current cell's color
            fill_color = cell_color[board[i][j]]

            # Create a square representing each cell
            pygame.draw.rect(display,
                             fill_color,
                             (j * box + pad,
                              i * box + pad,
                              box - 2 * pad,
                              box - 2 * pad), 0)

            # If cell isn't empty, display its number
            if board[i][j] != 0:
                display.blit(cell_font.render(f'{board[i][j]:>4}',
                                              1, font_color),
                             (j * box + 4 * pad, i * box + 9 * pad))

    # Update the screen to display all changes
    pygame.display.update()

def move(board: Board, direction: int) -> Board:
    """Make corresponding move operation.

    Parameters
    ----------
    board : Board
        Game board before move
    direction : int
        Direction of moving

    Returns
    -------
    Board
        Game board after move up
    """

    if direction == pygame.K_w:
        return move_up(board)

    if direction == pygame.K_s:
        return move_down(board)
    
    if direction == pygame.K_a:
        return move_left(board)

    if direction == pygame.K_d:
        return move_right(board)


def move_up(board: Board) -> Board:
    """Make move up operation. Move all cells up and merge with same
    cell if there are

    Parameters
    ----------
    board : Board
        Game board before move up

    Returns
    -------
    Board
        Game board after move up
    """

    # Move all cells up
    cell_up(board)

    # Find if there are potential merge on vertical axis from top
    # to bottom
    for j in range(4):
        for i in range(3):
            # If potential merge found, let the cell on top doubles
            # and clear bottom cell
            if board[i][j] == board[i + 1][j] and board[i][j] != 0:
                board[i][j] *= 2
                board[i + 1][j] = 0

                # Reset vertical index to find other potential merge
                i = 0

    # Move all cells up again
    cell_up(board)

    return board

def cell_up(board: Board) -> None:
    """Move all cells up that makes all cells are stacked vertically
    starting from the top most of the board

    Parameters
    ----------
    board : Board
        Game board before move up

    Returns
    -------
    Board
        Game board after move up
    """

    for j in range(4):
        # Store the order from top to bottom and count the number
        # of occupied cell
        nums = []
        count = 0

        for i in range(4):
            # Append occupied cell's number and count it
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1

        # Perform move up
        for i in range(4):
            # If there are occupied cell in this column, set the cell
            # from the top to bottom with the order of original column
            if count:
                board[i][j] = nums[i]
                count -= 1

            # If no occupied cell, set rest of them as empty
            else:
                board[i][j] = 0

def move_down(board: Board) -> Board:
    """Make move down operation. Move all cells down and merge with
    same cell if there are

    Parameters
    ----------
    board : Board
        Game board before move down

    Returns
    -------
    Board
        Game board after move down
    """

    # Move all cells down
    cell_down(board)

    # Find if there are potential merge on vertical axis from bottom
    # to top
    for j in range(4):
        for i in reversed(range(1,4)):
            # If potential merge found, let the cell on bottom doubles
            # and clear top cell
            if board[i][j] == board[i - 1][j] and board[i][j] != 0:
                board[i][j] *= 2
                board[i - 1][j] = 0

                # Reset vertical index to find other potential merge
                i = 3

    # Move all cells down again
    cell_down(board)

    return board

def cell_down(board: Board) -> None:
    """Move all cells down that makes all cells are stacked vertically
    starting from the bottom most of the board

    Parameters
    ----------
    board : Board
        Game board before move down

    Returns
    -------
    Board
        Game board after move down
    """

    for j in range(4):
        # Store the order from bottom to top and count the number
        # of occupied cell
        nums = []
        count = 0

        for i in reversed(range(4)):
            # Append occupied cell's number and count it
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1

        # Perform move down 
        for i in reversed(range(4)):
            # If there are occupied cell in this column, set the cell
            # from the bottom to top with the order of original column
            if count:
                board[i][j] = nums[3 - i]
                count -= 1

            # If no occupied cell, set rest of them as empty
            else:
                board[i][j] = 0

def move_left(board: Board) -> Board:
    """Make move left operation. Move all cells left and merge with
    same cell if there are

    Parameters
    ----------
    board : Board
        Game board before move left

    Returns
    -------
    Board
        Game board after move left
    """

    # Move all cells left
    cell_left(board)

    # Find if there are potential merge on horizontal axis from left
    # to right
    for i in range(4):
        for j in range(3):
            # If potential merge found, let the cell on left doubles
            # and clear right cell
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0

                # Reset horizontal index to find other potential merge
                j = 0

    # Move all cells left again
    cell_left(board)

    return board

def cell_left(board: Board) -> None:
    """Move all cells left that makes all cells are stacked horizontally
    starting from the left most of the board

    Parameters
    ----------
    board : Board
        Game board before move left

    Returns
    -------
    Board
        Game board after move left
    """

    for i in range(4):
        # Store the order from left to right and count the number
        # of occupied cell
        nums = []
        count = 0

        for j in range(4):
            # Append occupied cell's number and count it
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1

        # Perform move left
        for j in range(4):
            # If there are occupied cell in this row, set the cell
            # from the left to right with the order of original row
            if count:
                board[i][j] = nums[j]
                count -= 1

            # If no occupied cell, set rest of them as empty
            else:
                board[i][j] = 0

def move_right(board: Board) -> Board:
    """Make move right operation. Move all cells right and merge with
    same cell if there are

    Parameters
    ----------
    board : Board
        Game board before move right

    Returns
    -------
    Board
        Game board after move right
    """

    # Move all cells left
    cell_right(board)

    # Find if there are potential merge on vertical axis from right
    # to left
    for i in range(4):
        for j in reversed(range(4)):
            # If potential merge found, let the cell on right doubles
            # and clear left cell
            if board[i][j] == board[i][j - 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j - 1] = 0

                # Reset horizontal index to find other potential merge
                j = 3

    # Move all cells right again
    cell_right(board)

    return board

def cell_right(board: Board) -> None:
    """Move all cells right that makes all cells are stacked horizontally
    starting from the right most of the board

    Parameters
    ----------
    board : Board
        Game board before move right

    Returns
    -------
    Board
        Game board after move right
    """

    for i in range(4):
        # Store the order from right to left and count the number
        # of occupied cell
        nums = []
        count = 0

        for j in reversed(range(4)):
            # Append occupied cell's number and count it
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1

        # Perform move right
        for j in reversed(range(4)):
            # If there are occupied cell in this row, set the cell
            # from the right to left with the order of original row
            if count:
                board[i][j] = nums[3 - j]
                count -= 1

            # If no occupied cell, set rest of them as empty
            else:
                board[i][j] = 0

def play() -> None:
    """Main play function that keeps tracking player's operations and
    current game status
    """
    # Set game status to active
    status = 1

    # Create new board
    board = reset_board()

    # Main game loop, status equals 0 breaks loop
    while status:
        for event in pygame.event.get():
            # Set status to 0 if user want to quit
            if event.type == pygame.QUIT:
                status = 0

            # If status is win or lose, display corresponding message
            if status == 2 or status == 3:
                pygame.draw.rect(display, (255, 255, 255),
                                 (75, 250, 450, 100), 0)

                # Win message
                if status == 2:
                    display.blit(cell_font.render('You Win!', 1,
                                             (70, 60, 60)),
                                 (210, 260))

                # Lose message
                else:
                    display.blit(cell_font.render('You Lose!', 1,
                                             (70, 60, 60)),
                                 (200, 260))

                # Ask restart or quit
                display.blit(menu_font.render('Press Y to restart. Press N to quit.',
                                         1, (70, 60, 60)),
                             (105, 310))
                pygame.display.update()

                if event.type == pygame.KEYDOWN:
                    # If player want to restart, set status to 1
                    # and generate a new game board
                    if event.key == pygame.K_y:
                        board = reset_board()
                        status = 1

                    # If player want to quit, set status to 0
                    if event.key == pygame.K_n:
                        status = 0

            # If status is active, check player input
            else:
                if event.type == pygame.KEYDOWN:
                    # If input is invalid, wait for next input
                    if event.key not in [K_w, K_a, K_s, K_d]:
                        continue

                    # If input is valid, make corresponding move
                    else:
                        # Pass a deep copy for later comparison
                        new_board = move(deepcopy(board), event.key)

                        # If the board after move is diffrent than
                        # original, add one 2 and show it
                        if new_board != board:
                            board = add_two(new_board)
                            show_board(board)
                        
                        # Check the status of the board
                        status = check_status(board)