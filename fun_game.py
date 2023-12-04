# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Caleb Mandapat
# Diego Arroyo
# Lisandro Demagistris
# Mason McIntosh
# Section: 509
# Assignment: Final Game Project (13)
# Date: 3 December 2023

import turtle


def instructions():
    """ Displays the instructions for the game, can be 'reprinted' onto the console through
    user input. """
    ins = ("Teeko is a game where two players alternate between moves on a 5x5 board.\nEach player is given four"
           " pieces, and the black piece starts off first.\nBoth players must place all pieces onto the board,"
           " then they can move one piece into an adjacent orthogonal or diagonal empty spot.\n"
           "For a win to happen, a player must have four pieces in a row, whether that be vertically, horizontally,"
           " diagonally, or if the pieces form a square.")

    print(ins)


def create_board():
    """ Creates the board"""
    return [['.' for _ in range(5)] for _ in range(5)]


def print_board(board):
    """ Prints current state of board """
    for row in board:
        print(' '.join(row))
    print()


def log(player, move):
    """ Writes out a step-by-step log for users to see game flow. """
    with open("log_data.txt", "a") as l:
        l.write(f'{player} moved at: {move}\n\n')


def endgame(player):
    """ Displays a congratulatory screen for the winning player at the end of a game """
    # Set up the screen
    wn = turtle.Screen()
    wn.title(f'Congratulations, {player}!')

    # Function to draw a circle with a fill color
    def draw_circle(color, x, y, radius):
        turtle.penup()
        turtle.fillcolor(color)
        turtle.goto(x, y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(radius)
        turtle.end_fill()

    # Function to draw an arc for the smile
    def draw_smile_arc(x, y, radius):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.setheading(-60)
        turtle.circle(radius, 120)

    turtle.speed(0)
    turtle.bgcolor("white")

    draw_circle("#ffff00", 0, -100, 100)

    draw_circle("#000000", -35, 35, 10)
    draw_circle("#000000", 35, 35, 10)

    turtle.width(5)
    draw_smile_arc(-35, 20, 40)

    # Write "Congrats"
    turtle.penup()
    turtle.goto(-60, 150)
    turtle.color("black")
    turtle.pendown()
    turtle.write("Congrats", font=("Arial", 24, "bold"))

    turtle.hideturtle()

    wn.exitonclick()


def check_win(board, player):
    """ Checks if player won if the pieces are vertical, horizontal, diagonal, or a square"""
    # Dimensions of the game board
    rows = len(board)
    cols = len(board[0])

    # Check vertical and horizontal lines
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player:
                # Check vertical (|)
                if r <= rows - 4 and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check horizontal (-)
                if c <= cols - 4 and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check diagonal (\)
                if r <= rows - 4 and c <= cols - 4 and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check other diagonal (/)
                if r >= 3 and c <= cols - 4 and all(board[r - i][c + i] == player for i in range(4)):
                    return True

    # Check for square pattern
    for r in range(rows - 1):
        for c in range(cols - 1):
            if board[r][c] == player:
                if (
                        board[r + 1][c] == player and
                        board[r][c + 1] == player and
                        board[r + 1][c + 1] == player
                ):
                    return True

    # No win condition met
    return False


def in_bounds(board, row, column):
    """ Determines if a row and column is in bounds. """
    return row >= 0 and column >= 0 and row < len(board) and column < len(board[0])


countX = 0
count0 = 0


def place_piece(board, player):
    """ Place a piece on the board at the specified row and column or show instructions if asked. """
    while True:
        # Firstly, check if the player has 4 spots already on the board.
        # If this is still the 'first phase' of the game and the player can still put more pieces
        # This will also determine our input prompt.

        four_spots = False

        # access the variables globally
        global countX
        global count0
        if player == 'X' and countX == 4:
            four_spots = True
        elif player == 'O' and count0 == 4:
            four_spots = True

        if four_spots:
            user_input = input(f"Player {player}, select a row and column with your piece to move (0-4, separated by "
                               f"space), or type "
                               f"\"instructions\" for the instructions: ").split()
        else:
            user_input = input(f"Player {player}, enter row and column (0-4, separated by space), or type "
                               f"\"instructions\" for the instructions: ").split()

        if len(user_input) == 1 and user_input[0].lower() == "instructions":
            instructions()
            continue

        try:
            if not four_spots:
                row, col = map(int, user_input)
                if board[row][col] == '.':
                    board[row][col] = player
                    mv = f'{row}, {col}'
                    log(player, mv)

                    # a valid spot was placed, so let us increase the count
                    if player == 'X':
                        countX += 1
                    else:
                        count0 += 1
                    break  # only break if valid
                else:
                    print("This spot is already taken!")
            else:
                # Otherwise, we are moving on to a new part of the game.
                row, col = map(int, user_input)
                # This must be the player's spot, and it must have an open adjacent space.
                if board[row][col] == player:
                    # check for adjacent space
                    adjacent = False
                    for r in range(row - 1, row + 2):
                        for c in range(col - 1, col + 2):
                            if not adjacent and in_bounds(board, r, c) and board[r][c] == '.':
                                adjacent = True
                    if adjacent:
                        # Then ask the user for input. Otherwise, it's an invalid choice.
                        user_input = input(
                            f"Player {player}, select an adjacent row and column with your piece to move (0-4, "
                            f"separated by"
                            f"space), or type "
                            f"\"instructions\" for the instructions: ").split()
                        new_row, new_col = map(int, user_input)
                        # Validity check: cannot be the same spot
                        if new_row == row and new_col == col:
                            print("You must move your piece!")
                        # Validity check: must be adjacent spot that is EMPTY
                        if abs(new_row - row) <= 1 and abs(new_col - col) <= 1:
                            if board[new_row][new_col] == '.':
                                # successful adjacent spot, remove the original spot
                                board[row][col] = '.'
                                board[new_row][new_col] = player
                                # then, move it
                                mv = f'{new_row}, {new_col}'
                                log(player, mv)
                                break  # break with a successful move
                        else:
                            print("Not an empty adjacent spot!")
                    else:
                        print("No adjacent spots found!")
        except ValueError:
            print("Please enter numeric row and column values!")
        except IndexError:
            print("Invalid board position!")


def main():
    """ Executes the game """
    instructions()
    b = open("log_data.txt", 'w')
    b.write("Data: \n\n")
    b.close()

    while True:

        board = create_board()
        current_player = 'X'

        while True:
            print_board(board)
            place_piece(board, current_player)
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                endgame(current_player)
                b = open("log_data.txt", 'a')
                b.write(f"{current_player} win\n")
                b.close()
                break

            current_player = 'O' if current_player == 'X' else 'X'

        # Ask if players want to play again
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("See you next time!")
            exit()
        else:
            b = open("log_data.txt", 'a')
            b.write("NEW GAME\n")
            b.close()


if __name__ == "__main__":
    main()
