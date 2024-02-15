import numpy as np
class Block:
    def __init__(self, position, block_form, game_matrix) -> None:
        self.position = list(position)
        self.block_form = block_form
        self.color_num = self.get_color_num()
        self.game_matrix = game_matrix
        self.surface_points = self.calculate_surface_points(self.block_form)

    def get_color_num(self):
        for row in self.block_form:
            for val in row:
                if val != 0:
                    return val
                

    def valid_left_move(self):
        if 0 < self.position[1]:
            # check if block doesn't collde with another one to the left
            if not np.any(self.game_matrix[self.position[0]:self.position[0]+self.block_form.shape[0], self.position[1] - 1] != 0):
                return True
        return False

    def valid_right_move(self):
        if self.position[1] + self.block_form.shape[1] < self.game_matrix.shape[1]:
            # check if the block doesn't colide with another block to the right
            if not np.any(self.game_matrix[self.position[0]:self.position[0]+self.block_form.shape[0], self.position[1] + self.block_form.shape[1]] != 0):
                return True            
        return False

    def move_left(self):
        if self.valid_left_move():
            self.position[1] -= 1
            
    def move_right(self):
        if self.valid_right_move():
            self.position[1] += 1

    def fall_down(self):
        if not self.is_on_surface():
            self.position[0] += 1

    def is_on_surface(self, rotate_mode=False, given_shape=None):
        if not rotate_mode:
            for surface_point in self.surface_points:
                if self.game_matrix[self.position[0] + surface_point[0] + 1, self.position[1] + surface_point[1]] != 0:
                    return True
            return False
        
        else:
            surface_points = self.calculate_surface_points(given_shape)
            for surface_point in surface_points:
                if self.game_matrix[self.position[0] + surface_point[0] + 1, self.position[1] + surface_point[1]] != 0:
                    return True
            return False

        
    def calculate_surface_points(self, block_form):
        surface_connection_points = []
        for col_index in range(block_form.shape[1]):
            row_index = np.where(block_form[:, col_index] != 0)[0]
            if row_index.size > 0:
                surface_connection_points.append((row_index[-1], col_index))
        return surface_connection_points
    
    def instant_fall(self):
        while not self.is_on_surface():
            self.fall_down()

    def valid_to_rotate(self):
        shape = np.rot90(self.block_form)
        if not self.is_on_surface(rotate_mode=True, given_shape=shape):
            return True
        return False
    
    def rotate(self):
        if self.valid_to_rotate():
            self.block_form = np.rot90(self.block_form)
            self.surface_points = self.calculate_surface_points(self.block_form)