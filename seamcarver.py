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

        # throw IndexError for invalid values
        if i > width - 1 or i < 0 or j > height - 1 or j < 0:
            raise IndexError

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

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        least_energy = dict()
        directions = dict()

        # initialize least_energy matrix first row
        # initializes direction table first row
        for x in range(self.width()):
            least_energy[x,0] = self.energy(x,0)
            directions[x,0] = 0

        # fill in table with values of least_energy path
        # fills in direction table
        for y in range(1,self.height()):
            for x in range(self.width()):
                if x == 0:
                    # fills out cell
                    min_above = min(least_energy[x,y-1], least_energy[x+1, y-1])
                    least_energy[x,y] = min_above + self.energy(x,y)

                    # assigns direction
                    if min_above == least_energy[x,y-1]:
                        directions[x,y] = 0
                    else:
                        directions[x,y] = 1

                elif x == (self.width() - 1):
                    # fills out cell
                    min_above = min(least_energy[x-1, y - 1], least_energy[x, y - 1])
                    least_energy[x,y] = min_above + self.energy(x, y)

                    # assigns direction
                    if min_above == least_energy[x, y - 1]:
                        directions[x,y] = 0
                    else:
                        directions[x,y] = -1
                else:
                    # fills out cell
                    min_above = min(least_energy[x-1,y-1], least_energy[x, y-1], least_energy[x+1, y-1])
                    least_energy[x,y] = min_above + self.energy(x,y)

                    # assigns direction
                    if min_above == least_energy[x, y - 1]:
                        directions[x,y] = 0
                    elif min_above == least_energy[x+1, y-1]:
                        directions[x,y] = 1
                    elif min_above == least_energy[x-1,y-1]:
                        directions[x,y] = -1

        least_energy_vseam = []

        # gets minimum index from least_energy last row and appends to list
        last_row = dict()
        for x in range(self.width()):
            last_row[x] = least_energy[x,self.height() - 1]
        last_row_min = min(last_row, key=last_row.get)
        least_energy_vseam.append(last_row_min)

        # uses direction matrix to append index
        n = self.height()
        while n > 1:
            if directions[last_row_min,n-1] == 0:
                least_energy_vseam.insert(0, last_row_min)
                n -= 1
            elif directions[last_row_min, n-1] == 1:
                last_row_min += 1
                least_energy_vseam.insert(0, last_row_min)
                n -= 1
            elif directions[last_row_min, n-1] == -1:
                last_row_min -= 1
                least_energy_vseam.insert(0, last_row_min)
                n -= 1

        return least_energy_vseam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        # transpose picture sideways
        sideways_pic = SeamCarver(self.picture().rotate(90, expand=1))

        horizontal_seam = sideways_pic.find_vertical_seam()
        horizontal_seam.reverse()
        return horizontal_seam

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        # raise SeamError if the seam to be removed has a wrong length
        if len(seam) != self.height() or self.width() == 1:
            raise SeamError

        for i in range(1,len(seam)):
            if abs(seam[i]-seam[i-1]) > 1:
                raise SeamError

        for y in range(self.height()):
            for x in range(seam[y], self.width() - 1):
                self[x, y] = self[x + 1, y]

            del self[self.width() - 1, y]

        # decrement the width by 1
        self._width -= 1

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        # throw SeamErrors
        if len(seam) != self.width() or self.height() == 1:
            raise SeamError

        for i in range(1,len(seam)):
            if abs(seam[i]-seam[i-1]) > 1:
                raise SeamError

        # rotate the image and remove a vertical seam
        rotated_image = SeamCarver(self.picture().rotate(90, expand=1))
        rotated_image.remove_vertical_seam(seam[::-1])

        self._width = rotated_image._height
        self._height = rotated_image._width

        # reassign the pixels
        self.clear()
        for y in range(self._height):
            for x in range(self._width):
                self[x, y] = rotated_image[y, (rotated_image._height - 1) - x]

class SeamError(Exception):
    pass