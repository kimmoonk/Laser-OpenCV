from turtle import distance, done, xcor
import cv2
import numpy as np
from numpy import array as a

import potrace
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from PIL import Image
from Bezier import Bezier
from math import *
from ArcApp import *

from PathCodeMaker import *

PI = 3.1415926535
quart = PI / 2

# Make a numpy array with a rectangle in the middle
data = np.zeros((50, 50), np.uint32)
data[8:32-8, 8:32-8] = 1

#img2 = Image.open('Star2.png') 

img = Image.open('vector.png')
img2 = img.convert('1')

MakePathCode(img2,0.0)

plt.show()
