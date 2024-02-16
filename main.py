from pynput.keyboard import Listener, Key
import numpy as np
from time import sleep

from block import Block
from block_shapes import choose_random_shape


final_array_state = np.zeros((20, 10))


# colors
COLOR_CODES = {
    1: "\033[93m",  # Yellow
    2: "\033[38;5;45m",  # Blue
    3: "\033[38;5;196m",  # Red
    4: "\033[38;5;46m",  # Green
    5: "\033[38;5;208m",  # Orange
    6: "\033[38;5;201m", # Pink
    7: "\033[38;5;93m" # Purple
}
GREY_CODE = "\033[38;5;238m"
RESET_CODE = "\033[0m"


def update_game_matrix(game_score, save_fresh_matrix=False):
    fresh_tetris_array = np.copy(final_array_state)

    block_rows, block_cols = block.block_form.shape
    start_row, start_col = block.position

    for row_index in range(block_rows):
        for col_index in range(block_cols):
            if block.block_form[row_index, col_index] != 0 and fresh_tetris_array[start_row + row_index, start_col + col_index] == 0:
                fresh_tetris_array[start_row + row_index, start_col + col_index] = block.color_num

    print_game_matrix(game_array=fresh_tetris_array, game_score=game_score)
    if save_fresh_matrix:
        return fresh_tetris_array


def print_game_matrix(game_array, game_score):
    print(chr(27) + "[2J")  # Clear the screen
    visual_game_matrix = ""
    for row in game_array:
        row_str = ''
        for cell in row:
            if cell != 0:
                color_code = COLOR_CODES.get(cell, RESET_CODE)
                row_str += color_code + "▄" + RESET_CODE + ' '
            else:
                row_str += "_" + " "
        visual_game_matrix += row_str + "\n"
    print(visual_game_matrix + str(game_score))


def check_row_completion(game_matrix):
    indexes_rows_completed = []
    for row_index, row in enumerate(game_matrix):
        if not np.any(row == 0):
            indexes_rows_completed.append(row_index)
    return indexes_rows_completed


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
        update_game_matrix()


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
    game_score = block.score_from_block
    update_game_matrix(game_score)
    sleep(3)    

    if block.is_on_surface():
        i += 1

        final_array_state = update_game_matrix(save_fresh_matrix=True)
        
        block = Block(position=(0, 4), block_form=choose_random_shape(), game_matrix=final_array_state)
        update_game_matrix()    

listener.stop()
