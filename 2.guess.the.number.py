import math
import random
import simplegui

# Defaults for global variables
lower_boundary = 0
upper_boundary = 100
count = 7
secret_number = random.randrange(0, 100)

# Helper function to start and restart the game
def new_game():
    """ Reinitializes global variables and prints
    a message for a new game. """
    
    global secret_number, count
    secret_number = random.randrange(lower_boundary,
                                     upper_boundary)
    # calculating how much guesses will be enough to win the game
    # formula: 2 ** count == high - low + 1
    # it will always be either 7 or 10 in this version
    count = int(math.ceil(math.log
                          (upper_boundary - lower_boundary + 1,
                           2)))
    print
    print "A new game has started!"
    print "You have to guess a number in range from", \
    lower_boundary, "to", upper_boundary
    print "You have", count, "attempt(s) to go..."
    print "Good luck!"
    print

# Helper output function, should be called
# when user types in a wrong number
def print_input_error():
    """ Prints an error and asks user to put in a number
    whithin specified bounds """
    print "Error! The number must be in range from", \
    lower_boundary, "to", upper_boundary - 1
    print

# define event handlers for control panel
def range100():
    """ Handles the 0-99 range button.
    Starts a new game,
    picks a new secret_number value whithin [0, 100) range. """
    global lower_boundary, upper_boundary
    lower_boundary = 0
    upper_boundary = 100
    new_game()
    
def range1000():
    """ Handles the 0-999 range button.
    Starts a new game,
    picks a new secret_number value whithin [0, 1000) range. """
    global lower_boundary, upper_boundary
    lower_boundary = 0
    upper_boundary = 1000
    new_game()
    
def input_guess(guess):
    """ Handles the input from textbox, input must be a number """
    # main game logic goes here
    
    global count
    
    # converting input to integer, we don't need decimals
    guess_num = int(guess)
    print "Guess was", guess_num
    
    if guess_num < lower_boundary or guess_num >= upper_boundary:
        # anything but integer would trigger a ValueError
        # so this line only goes if the number is out of bounds    
        print_input_error()
        return
    
    if guess_num == secret_number:
        print "Correct!"
        # Player wins, starting a new game in the same range
        new_game()
        return
    # Last attempt. If player didn't guess the number it's a loss.
    elif count == 1:
        print "Game over."
        new_game()
        return
    elif guess_num < secret_number:
        print "Higher!"
    elif guess_num > secret_number:
        print "Lower!"
    # Don't need an else statement, it would never trigger
    
    # Decrement here to avoid double coding in higher/lower blocks.
    count -= 1
    print "You have", count, "attempt(s) left"
    print


# create frame
frame = simplegui.create_frame("Guess the number!", 150, 200)

# register event handlers for control elements and start frame
frame.add_input("Your guess: ", input_guess, 120)
frame.add_button("Range: 0-99", range100, 120)
frame.add_button("Range: 0-999", range1000, 120)
frame.start()

# call new_game 
new_game()

