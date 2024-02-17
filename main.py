from pynput.keyboard import Listener, Key
import numpy as np
from time import sleep

from block import Block
from block_shapes import choose_random_shape


final_array_state = np.zeros((20, 10))


# colors
YELLOW = "\033[93m"
BLUE = "\033[38;5;45m"
RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;201m"
PURPLE = "\033[38;5;93m"

COLOR_CODES = {
    1: YELLOW,  # Yellow
    2: BLUE,  # Blue
    3: RED,  # Red
    4: GREEN,  # Green
    5: ORANGE,  # Orange
    6: PINK, # Pink
    7: PURPLE # Purple
}

GREY_CODE = "\033[38;5;238m"
RESET_CODE = "\033[0m"


def update_game_matrix(final_game_array, block):
    """
    :param final_game_array: The array where there are no moving blocks. Every block is on surface.

    Updates the game array to make it seem like the block is moving. 
    Gets the position of the only legal to move block (there will always be one) and its shape. 
    It looks at the values of the block array and changes the non zero values into the game matrix. 
    Returns a new fresh game matrix where there is one block in the air and other are on the surface - matrix of zeros and numbers from 1 to 7 corresponding to block array number.
    The returned matrix is used in combination with printing the game matrix and changing the original matrix if the block touches the surface.
    """
    fresh_tetris_array = np.copy(final_game_array)

    block_rows, block_cols = block.block_form.shape
    start_row, start_col = block.position

    for row_index in range(block_rows):
        for col_index in range(block_cols):
            if block.block_form[row_index, col_index] != 0 and fresh_tetris_array[start_row + row_index, start_col + col_index] == 0:
                fresh_tetris_array[start_row + row_index, start_col + col_index] = block.color_num

    return fresh_tetris_array


def greet_user():
    T = """
     ______  
    /\__  _\ 
    \/_/\ \/ 
       \ \_\ 
        \/_/ 
         
    """
    E = """
     ______    
    /\  ___\   
    \ \  __\   
     \ \_____\ 
      \/_____/ 
           
    """
    R = """
     ______    
    /\  == \   
    \ \  __<   
     \ \_\ \_\ 
      \/_/ /_/ 
           
    """
    I = """
     __    
    /\ \   
    \ \ \  
     \ \_\ 
      \/_/ 
       
    """
    S = """
     ______    
    /\  ___\   
    \ \___  \  
     \/\_____\ 
      \/_____/ 
           
    """
    T_lines = T.splitlines()
    E_lines = E.splitlines()
    R_lines = R.splitlines()
    I_lines = I.splitlines()
    S_lines = S.splitlines()
    
    message = ""
    for i in range(len(T_lines)):
        message += RED + T_lines[i] + RESET_CODE + ORANGE + E_lines[i] + RESET_CODE + YELLOW + T_lines[i] + RESET_CODE + GREEN + R_lines[i] + RESET_CODE + BLUE + I_lines[i] + RESET_CODE + PURPLE + S_lines[i] + RESET_CODE + "\n"
    
    print(message)
    print("Welcome to terminal Tetris!")
    # user_preference = input("")
    # add something here

print_option = "g"
def print_game_matrix(game_array, print_option=print_option):
    """
    Prints the given matrix with corresponding block colors.
    """
    print(chr(27) + "[2J")  # clear the screen
    visual_game_matrix = ""
    row_lenght = len(game_array[0])
    for row in game_array:
        row_str = "|"
        for cell in row:
            if cell != 0:
                color_code = COLOR_CODES.get(cell, RESET_CODE)
                row_str += color_code + "▄" + RESET_CODE + ' '
            else:
                row_str += "_" + " "
        row_str += "|"
        visual_game_matrix += row_str + "\n"
    bottom_line = "+" + "-" * row_lenght * 2 + "+"
    visual_game_matrix += bottom_line
    print(visual_game_matrix)


def update_and_print_game(final_game_array, block):
    """
    Combines two functions. It updates the game array and then prints it.
    """
    fresh_matrix = update_game_matrix(final_game_array=final_game_array, block=block)
    print_game_matrix(game_array=fresh_matrix)

# TODO 1: Measure game score and print it everytime the matrix is printed
def measure_game_score():
    pass


def check_row_completion(game_matrix):
    indexes_rows_completed = []
    for row_index, row in enumerate(game_matrix):
        if not np.any(row == 0):
            indexes_rows_completed.append(row_index)
    return indexes_rows_completed

# TODO 2: Make the row disappear animation to look cool
def row_disappear(indexes_rows, game_matrix):
    pass


def move_block(key):
    try:
        if key == Key.left:
            block.move_left()
        elif key == Key.right:
            block.move_right()
        elif key == Key.space:
            block.instant_fall()
        elif key == Key.down:
            block.fall_down()
        else:
            if hasattr(key, 'char') and key.char == "r":
                block.rotate()
    except AttributeError:
        pass
    finally:
        update_and_print_game(final_game_array=final_array_state, block=block)



greet_user()
sleep(2)

block = Block(position=(0, 4), block_form=choose_random_shape(), game_matrix=final_array_state)

listener = Listener(on_press=move_block)
listener.start()


game_on = True
game_score = 0
i = 0
while game_on:
    if i > 8:
        game_on = False

    block.fall_down()
    update_and_print_game(final_game_array=final_array_state, block=block)
    sleep(3)  # TODO 3: Make the sleep go shorter and shorter as the game goes for longer    

    if block.is_on_surface():
        i += 1
        game_score += block.score_from_block
        final_array_state = update_game_matrix(final_game_array=final_array_state, block=block)
        
        block = Block(position=(0, 4), block_form=choose_random_shape(), game_matrix=final_array_state)
        update_and_print_game(final_game_array=final_array_state, block=block)

print(game_score)
listener.stop()
