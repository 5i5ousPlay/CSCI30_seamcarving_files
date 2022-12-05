#!/usr/bin/env python3

from picture import Picture
from PIL import Image

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        height = self.height()
        width = self.width()

        left = i - 1 if (i >= 1) else width - 1
        right = i + 1 if (i < width - 1) else 0
        top = j - 1 if (j >= 1) else height - 1
        bottom = j + 1 if (j < height - 1) else 0

        # get RBG value of pixel
        x_1 = self[right, j]   # right pixel
        x_2 = self[left, j]   # left pixel
        y_1 = self[i, top]   # top pixel
        y_2 = self[i, bottom]   # bottom pixel
        
        # x values
        r_x = abs(x_1[0] - x_2[0])
        g_x = abs(x_1[1] - x_2[1])
        b_x = abs(x_1[2] - x_2[2])

        # y values
        r_y = abs(y_1[0] - y_2[0])
        g_y = abs(y_1[1] - y_2[1])
        b_y = abs(y_1[2] - y_2[2])

        delta_x = pow(r_x, 2) + pow(g_x, 2) + pow(b_x, 2)
        delta_y = pow(r_y, 2) + pow(g_y, 2) + pow(b_y, 2)

        energy = delta_x + delta_y

        return energy

        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        
        # initialize a matrix of the energies and direction
        energies = [[]]
        direction = [[]]
        for x in range(self.width()):
            energies[0].append(self.energy(x,0)) 
            direction[0].append(0)

        # fill out subsequent rows with the least energy
        for y in range(1, self.height()):
            energies.append([])
            direction.append([])
            
            for x in range(self.width()):
                if x == 0:   # at the left-most edge
                    min_above = min(energies[y-1][x], energies[y-1][x+1])

                    if min_above == energies[y-1][x]:
                        min_dir = 0
                    elif min_above == energies[y-1][x+1]:
                        min_dir = 1
                
                elif x == self.width() - 1:   # at the right-most edge
                    min_above = min(energies[y-1][x-1], energies[y-1][x])

                    if min_above == energies[y-1][x]:
                        min_dir = 0
                    elif min_above == energies[y-1][x-1]:
                        min_dir = -1

                else:   # pixels in between
                    min_above = min(energies[y-1][x-1], energies[y-1][x], energies[y-1][x+1])

                    if min_above == energies[y-1][x]:
                        min_dir = 0
                    elif min_above == energies[y-1][x+1]:
                        min_dir = 1
                    elif min_above == energies[y-1][x-1]:
                        min_dir = -1

                least_energy = self.energy(x,y) + min_above
                energies[y].append(least_energy)
                direction[y].append(min_dir)
        
        dist = energies[self.height() - 1]
        min_dist = dist.index( min(dist) )

        # initialize empty array for the least energy vertical seam
        v_seam = []
        v_seam.append(min_dist)
        
        for y in range(1, self.height()):
            v_seam.append(v_seam[y-1] + direction[self.height() - y][v_seam[y-1]])
        
        return v_seam[::-1]

        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''

        transposed_image = SeamCarver(self.picture().rotate(90, expand=1))
        h_seam = transposed_image.find_vertical_seam()
        
        return h_seam[::-1]

        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):

        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass