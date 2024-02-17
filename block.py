import numpy as np
class Block:
    def __init__(self, position, block_form, game_matrix) -> None:
        self.position = list(position)
        self.block_form = block_form
        self.color_num = self.get_color_num()
        self.game_matrix = game_matrix
        self.bottom_surface_points, self.left_side_points, self.right_side_points = self.calculate_surface_points(self.block_form)
        self.score_from_block = 0

    def get_color_num(self):
        """
        Get the number of the block that is not zero in order to show its color on the matrix.
        """
        for row in self.block_form:
            for val in row:
                if val != 0:
                    return val
                

    def valid_left_move(self):
        """
        Check if block can move left
        """
        if 0 < self.position[1]:
            # TODO: Zmienić tą logikę, aby dostać surface points left i zobaczyć czy surface point + 1 jest rowne 0
            for leftmost_surface_point in self.left_side_points:
                if self.game_matrix[self.position[0] + leftmost_surface_point[0], self.position[1] + leftmost_surface_point[1] - 1] != 0:
                    return False
            return True
        else:
            return False


    def valid_right_move(self):
        """
        Check if block can move right
        """
        if self.position[1] + self.block_form.shape[1] < self.game_matrix.shape[1]:
            # TODO: Zmienić tą logikę, aby dostać surface points right i zobaczyć czy surface point - 1 jest rowne 0
            for rightmost_surface_point in self.right_side_points:
                if self.game_matrix[self.position[0] + rightmost_surface_point[0], self.position[1] + rightmost_surface_point[1] + 1] != 0:
                    return False
            return True
        else:
            return False


    def move_left(self):
        """
        Move one tile block to the left
        """
        if self.valid_left_move():
            self.position[1] -= 1
            
    def move_right(self):
        """
        Move one tile block to the right
        """
        if self.valid_right_move():
            self.position[1] += 1

    def fall_down(self):
        """
        Make the block move one tile down
        """
        if not self.is_on_surface():
            self.position[0] += 1
            self.score_from_block += 1

    def is_on_surface(self, block_form=None):
        """
        Check if there is any non 0 tile beneath the block
        """
        if block_form is None:
            block_form = self.block_form

        if self.position[0] + block_form.shape[0] == self.game_matrix.shape[0]:
            return True
    
        for surface_point in self.bottom_surface_points:
            if self.game_matrix[self.position[0] + surface_point[0] + 1, self.position[1] + surface_point[1]] != 0:
                return True
        return False

    def calculate_surface_points(self, block_form):
        """
        Get the bottom, leftmost, rightmost surface points
        """
        bottom_surface_points = []
        right_side_points = []
        left_side_points = []
        
        for col_index in range(block_form.shape[1]):
            row_indices = np.where(block_form[:, col_index] != 0)[0]
            if row_indices.size > 0:
                bottom_surface_points.append((row_indices[-1], col_index))
        
        for row_index, row in enumerate(block_form):
            non_zero_indices = np.where(row != 0)[0]
            if non_zero_indices.size > 0:
                left_side_points.append((row_index, non_zero_indices[0]))  # Leftmost non-zero
                right_side_points.append((row_index, non_zero_indices[-1]))  # Rightmost non-zero
        
        return bottom_surface_points, left_side_points, right_side_points
        
    def instant_fall(self):
        """
        Makes block fall immediataly until it reaches a surface
        """
        while not self.is_on_surface():
            self.fall_down()

    def valid_to_rotate(self):
        """
        Check whether the block can legally rotate 90 degrees clockwise
        """
        shape = np.rot90(self.block_form)
        # change the logic to check if the block is in bounds and let it rotate when it is on surface
        # then check if the rotated version collides with any block.
        if self.is_in_bounds(block_form=shape) and not self.is_colliding(block_form=shape):
            return True
        return False
    
    def is_in_bounds(self, block_form):
        """
        Check if block is in the buonds of game matrix
        """
        if self.position[0] + block_form.shape[0] <= self.game_matrix.shape[0] and self.position[0] >= 0 and self.position[1] >= 0 and self.position[1] + block_form.shape[1] <= self.game_matrix.shape[1]:
            return True
        return False

    def is_colliding(self, block_form):
        non_zero_points_loc = self.calculate_non_zero_points(block_form=block_form)
        for point in non_zero_points_loc:
            if self.game_matrix[self.position[0] + point[0], self.position[1] + point[1]] != 0:
                return True
        return False

    def calculate_non_zero_points(self, block_form):
        non_zero_points_loc = []
        for row_index, row in enumerate(block_form):
            for col_index in range(len(row)):
                if block_form[row_index][col_index] != 0:
                    non_zero_points_loc.append((row_index, col_index))
        return non_zero_points_loc

    def rotate(self):
        """
        Rotate the block 90 degrees clockwise
        """
        if self.valid_to_rotate():
            self.block_form = np.rot90(self.block_form)
            self.bottom_surface_points, self.left_side_points, self.right_side_points = self.calculate_surface_points(self.block_form)