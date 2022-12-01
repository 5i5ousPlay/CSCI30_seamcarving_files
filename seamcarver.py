#!/usr/bin/env python3

from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        height = self.height()
        width = self.width()
        left = i - 1
        right = i + 1
        top = j - 1
        bottom = j + 1

        # coordinate wrapping
        if left < 0:
            left = width - 1
        if right >= width:
            right = 0
        if top < 0:
            top = height - 1
        if bottom >= height:
            bottom = 0

        # get pixel values
        x_1 = self[left, j]
        x_2 = self[right, j]
        y_1 = self[i, top]
        y_2 = self[i, bottom]

        # x values
        # could maybe be converted into a for loop
        # feel free to try
        R_x = abs(x_1[0] - x_2[0])
        G_x = abs(x_1[1] - x_2[1])
        B_x = abs(x_1[2] - x_2[2])

        # y values
        R_y = abs(y_1[0] - y_2[0])
        G_y = abs(y_1[1] - y_2[1])
        B_y = abs(y_1[2] - y_2[2])

        delta_x = pow(R_x, 2) + pow(G_x,2) + pow(B_x,2)
        delta_y = pow(R_y, 2) + pow(G_y,2) + pow(B_y,2)

        energy = delta_x + delta_y
        return energy

        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
