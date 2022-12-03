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

        delta_x = pow(R_x, 2) + pow(G_x, 2) + pow(B_x, 2)
        delta_y = pow(R_y, 2) + pow(G_y, 2) + pow(B_y, 2)

        energy = delta_x + delta_y
        return energy

        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        # energy_matrix = dict()
        least_energy = dict()
        directions = dict()

        # initialize energy_matrix & first row of least_energy matrix
        # for y in range(self.height()):
        #     for x in range(self.width()):
        #         energy_matrix[x,y] = self.energy(x,y)
        #         if y == 0:
        #             least_energy[x,y] = self.energy(x,y)

        # print(energy_matrix)
        # print(least_energy)

        # initialize least_energy matrix
        for x in range(self.width()):
            least_energy[x,0] = self.energy(x,0)

        for y in range(1,self.height()):
            for x in range(self.width()):
                if x == 0:
                    least_energy[x,y] = min(least_energy[x,y-1], least_energy[x+1, y-1]) + self.energy(x,y)
                elif x == (self.width() - 1):
                    least_energy[x,y] = min(least_energy[x-1, y - 1], least_energy[x, y - 1]) + self.energy(x, y)
                else:
                    least_energy[x,y] = min(least_energy[x-1,y-1], least_energy[x, y-1], least_energy[x+1, y-1]) + self.energy(x,y)

        print(least_energy)

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
