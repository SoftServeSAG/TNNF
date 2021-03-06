# ---------------------------------------------------------------------#
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from numpy import *
from fDataWorkerCORE import *
# ---------------------------------------------------------------------#


class Graphic(object):
    @staticmethod
    def PicSaver(img, folder, name, color="L"):  # Saves picture to folder. Color "L" or "RGB"
        imsave = Image.fromarray(DataMutate.Normalizer(img))  # Normalizer(img).astype('uint8') for RGB
        imsave = imsave.convert(color)
        imsave.save(folder + name + ".jpg", "JPEG", quality=100)

# ---------------------------------------------------------------------#


class MultiWeights(object):

    def __init__(self, path='./', name='multi_weights.png', scale=1, border=1):


        self.pathToSave = path

        #Check last symbol to be '/'
        if self.pathToSave[-1] != '/':
            self.pathToSave += '/'

        #Filename to save
        if name != 'multi_weights.png':
            self.name = name + '.png'
        else:
            self.name = name

        #Pics list
        self.pictures = []

        #Pics location
        self.width = None
        self.height = None

        #Scale factor
        self.scale = int(scale)

        #Border
        self.border = border

    def defineOptimalPicLocation(self, n):

        self.width = int(np.ceil(np.sqrt(n) * 0.8))
        self.height = int(np.ceil(np.true_divide(n, self.width)))

    def draw(self):
        #Number of picture
        numOfPictures = len(self.pictures)

        #Check for pictures
        if numOfPictures == 0:
            print 'WARNING: There is nothing to draw there...'
            return

        #Picture's size
        #Check RGB
        if len(self.pictures[-1].shape) == 2:
            picH, picW = self.pictures[-1].shape
        elif len(self.pictures[-1].shape) == 3:
            picH, picW, colors = self.pictures[-1].shape
        else:
            raise NotImplementedError('Unknown number of channels (colors): ' + str(len(self.pictures[-1].shape)))

        #Define pictures location
        self.defineOptimalPicLocation(numOfPictures)

        #Prepare plate for weights
        plate = Image.new('RGBA',
                          (int(self.border + self.width * (picW + self.border)), int(self.border + self.height * (picH + self.border))),
                          (0, 0, 0, 255))

        #Plate's size
        plateW, plateH = plate.size

        #Iterate over picture's location
        count = 0
        for h in xrange(self.height):
            for w in xrange(self.width):

                offset = (self.border + w * (picW + self.border), self.border + h * (picH + self.border))
                plate.paste(Image.fromarray(DataMutate.Normalizer(self.pictures[count]).astype('uint8')), offset)

                count += 1
                if count == numOfPictures:
                    break

        plate.save(self.pathToSave + self.name)

    def add(self, p):

        #Scaling
        if self.scale != 1:
            if len(p.shape) == 2:
                p = np.kron(p, np.ones((self.scale, self.scale)))
            elif len(p.shape) == 3:
                p = np.kron(p, np.ones((self.scale, self.scale, 1)))
            else:
                raise NotImplementedError('Unknown number of channels (colors): ' + str(len(p.shape)))

        #Add pictures to list
        self.pictures.append(p)
