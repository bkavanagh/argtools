__author__ = 'brendan'
from collections import Counter
import re
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import string
from collections import defaultdict
import operator
import re
import time
class Coord(tuple):

    def __add__(self, other):
        return self.__class__(map(operator.add, self, other))


class PCB(object):

    def __init__(self, fn):
        self.raw =  open(fn, 'r').read()
        self._flat = None
        self._array = None
        self._counter = None
        self._letter_coords = None
        self._width = None
        self._height = None

    def __getitem__(self, item):
        print item
        try:
            return self.as_array()[item[1]][item[0]]
        except IndexError as e:
            raise ValueError()

    def as_list(self):
        if not  self._flat:
            self._flat = [x for x in self.raw if not re.match('\s', x)]
        return self._flat

    def as_array(self):
        if not self._array:
            self._array = [x.split() for x in [y for y in self.raw.split('\n')] if x]
        return self._array

    def as_counter(self):
        if not self._counter:
            self._counter = Counter(self.as_list())
        return self._counter

    def iterate_with_coords(self):
        for idx, letter in enumerate(self.as_list()):
            yield letter, idx%self.width, idx//self.height

    @property
    def width(self):
        if not self._width:
            self._width = len(self.as_array()[0])
        return self._width

    @property
    def height(self):
        if not self._height:
            self._height = len(self.as_array())
        return self._height

    def as_image(self, valid_letters=None, mapped=False, scale=1):
        """
        create an image with the ord value of each character mapped to an int 0-255
        :param valid_letters: list(str), list of characters that will be plotted (rest will be ignored)
        :param mapped: bool, map letters to grayscale based on ord rather than making all valid solid
        :return: None
        """
        if  valid_letters: valid_letters = valid_letters.upper()
        im = Image.new('RGB', (self.width, self.height), 'white')
        pix = im.load()
        for letter, x, y in self.iterate_with_coords():
            if not valid_letters or letter in valid_letters:
                if mapped:
                    pix[x, y] = (256/len(string.ascii_uppercase) * (ord(letter) - ord(string.ascii_uppercase[0])),) *3
                else:
                    pix[x, y] = (0,)*3
        im = im.resize((self.width*scale, self.height*scale), Image.NEAREST)
        im.show()

    @property
    def letter_coord_tpls(self):
        if not self._letter_coords:
            self._letter_coords = defaultdict(list)
            for letter, x, y in self.iterate_with_coords():
                self._letter_coords[letter].append((x, y))
        return self._letter_coords

    @property
    def unique(self):
        return [x for x in self.as_counter().keys()]



if __name__ == '__main__':
    pcb = PCB('./pcb.txt')

    # PCB as a 2d array (list of lists)
    # print p.as_array()

    # PCB as one long list
    # print p.as_list()

    # Unique letters in PCB
    # print p.unique

    # Counter of letters in PCB
    # print p.as_counter

    # Grayscale image showing only the valid_letters mapped to their relative value
    #pcb.as_image(mapped=True, valid_letters='archer')

    # B+W image showing only the valid_letters
    #pcb.as_image(mapped=False, valid_letters='krieger')

    # Grayscale image shwoing the relatiuve value of all the letters
    pcb.as_image(mapped=True, scale=10)