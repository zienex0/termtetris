from pynput.keyboard import Listener, Key
import numpy as np
from time import sleep

from block import Block
from block_shapes import choose_random_shape


final_array_state = np.zeros((20, 10))
final_array_state[-1, :] = 1


# colors
COLOR_CODES = {
    1: "\033[91m",  # Red
    2: "\033[92m",  # Green
    3: "\033[93m",  # Yellow
    4: "\033[94m",  # Blue
}
GREY_CODE = "\033[38;5;238m"
RESET_CODE = "\033[0m"


def print_game_matrix(game_array):
    print(chr(27) + "[2J")  # Clear the screen
    for row in game_array:
        row_str = ''
        for cell in row:
            if cell != 0:
                color_code = COLOR_CODES.get(cell, RESET_CODE)
                row_str += color_code + "▄" + RESET_CODE + ' '
            else:
                row_str += "-" + " "
        print(row_str)


def update_game_matrix(save_fresh_matrix=False):
    fresh_tetris_array = np.copy(final_array_state)

    block_rows, block_cols = block.block_form.shape
    start_row, start_col = block.position

    for row_index in range(block_rows):
        for col_index in range(block_cols):
            if block.block_form[row_index, col_index] != 0 and fresh_tetris_array[start_row + row_index, start_col + col_index] == 0:
                fresh_tetris_array[start_row + row_index, start_col + col_index] = block.color_num

    print_game_matrix(fresh_tetris_array)

    if save_fresh_matrix:
        return fresh_tetris_array


def move_block(key):
    if key == Key.left:
        block.move_left()
    elif key == Key.right:
        block.move_right()
    elif key == Key.down:
        block.instant_fall()
    elif key.char == "r":
        block.rotate()
    update_game_matrix()


block = Block(position=(0, 4), block_form=choose_random_shape(), game_matrix=final_array_state)

listener = Listener(on_press=move_block)
listener.start()

# Game loop
game_on = True
i = 0
while game_on:
    if i > 8:
        game_on = False

    for _ in range(100):

        if block.is_on_surface():
            i += 1
            final_array_state = update_game_matrix(save_fresh_matrix=True)
            update_game_matrix()
            block = Block(position=(0, 4), block_form=choose_random_shape(), game_matrix=final_array_state)
            update_game_matrix()

        sleep(0.01)
    
    
    block.fall_down()
    update_game_matrix()



    # This is where you'd handle game logic, like checking for completed lines, game over conditions, etc.

listener.stop()
