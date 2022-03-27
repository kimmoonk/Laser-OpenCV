from re import X
import numpy as np
from potrace import Bitmap
from potrace import Path
from potrace import Curve

import math


from typing import Optional, Tuple, Union


import potrace
import matplotlib.pyplot as plt
from PIL import Image

POTRACE_TURNPOLICY_BLACK = 0
POTRACE_TURNPOLICY_WHITE = 1
POTRACE_TURNPOLICY_LEFT = 2
POTRACE_TURNPOLICY_RIGHT = 3
POTRACE_TURNPOLICY_MINORITY = 4
POTRACE_TURNPOLICY_MAJORITY = 5
POTRACE_TURNPOLICY_RANDOM = 6

# /* segment tags */
POTRACE_CURVETO = 1
POTRACE_CORNER = 2

INFTY = float("inf")
COS179 = math.cos(math.radians(179))


class _Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)

class _Path:
    def __init__(self, pt: list, area: int, sign: bool):
        self.pt = pt  # /* pt[len]: path as extracted from bitmap */

        self.area = area
        self.sign = sign
        self.next = None
        self.childlist = []
        self.sibling = []

        self._lon = []  # /* lon[len]: (i,lon[i]) = longest straight line from i */

        self._x0 = 0  # /* origin for sums */
        self._y0 = 0  # /* origin for sums */
        self._sums = []  # / *sums[len + 1]: cache for fast summing * /

        self._m = 0  # /* length of optimal polygon */
        self._po = []  # /* po[m]: optimal polygon */
        self._curve = []  # /* curve[m]: array of curve elements */
        self._ocurve = []  # /* ocurve[om]: array of curve elements */
        self._fcurve = []  # /* final curve: this points to either curve or ocurve.*/

    def __len__(self):
        return len(self.pt)

    def init_curve(self, m):
        pass

def findpath(bm: np.array, x0: int, y0: int, sign: bool, turnpolicy: int) -> _Path:
    """
    /* compute a path in the given pixmap, separating black from white.
    Start path at the point (x0,x1), which must be an upper left corner
    of the path. Also compute the area enclosed by the path. Return a
    new path_t object, or NULL on error (note that a legitimate path
    cannot have length 0). Sign is required for correct interpretation
    of turnpolicies. */"""

    x = x0
    y = y0
    dirx = 0
    diry = -1  # diry-1
    pt = []
    area = 0

    while True:  # /* while this path */
        # /* add point to path */
        pt.append(_Point(int(x), int(y)))

        # /* move to next point */
        x += dirx
        y += diry
        area += x * diry

        # /* path complete? */
        if x == x0 and y == y0:
            break

        # /* determine next direction */
        cy = y + (diry - dirx - 1) // 2
        cx = x + (dirx + diry - 1) // 2
        try:
            c = bm[cy][cx]
        except IndexError:
            c = 0
        dy = y + (diry + dirx - 1) // 2
        dx = x + (dirx - diry - 1) // 2
        try:
            d = bm[dy][dx]
        except IndexError:
            d = 0

        if c and not d:  # /* ambiguous turn */
            if (
                turnpolicy == POTRACE_TURNPOLICY_RIGHT
                or (turnpolicy == POTRACE_TURNPOLICY_BLACK and sign)
                or (turnpolicy == POTRACE_TURNPOLICY_WHITE and not sign)
                or (turnpolicy == POTRACE_TURNPOLICY_RANDOM and detrand(x, y))
                or (turnpolicy == POTRACE_TURNPOLICY_MAJORITY and majority(bm, x, y))
                or (
                    turnpolicy == POTRACE_TURNPOLICY_MINORITY and not majority(bm, x, y)
                )
            ):
                tmp = dirx  # /* right turn */
                dirx = diry
                diry = -tmp
            else:
                tmp = dirx  # /* left turn */
                dirx = -diry
                diry = tmp
        elif c:  # /* right turn */
            tmp = dirx
            dirx = diry
            diry = -tmp
        elif not d:  # /* left turn */
            tmp = dirx
            dirx = -diry
            diry = tmp

    # /* allocate new path object */
    return _Path(pt, area, sign)


def findnext(bm: np.array) -> Optional[Tuple[Union[int,float], int]]:
    """
    /* find the next set pixel in a row <= y. Pixels are searched first
       left-to-right, then top-down. In other words, (x,y)<(x',y') if y>y'
       or y=y' and x<x'. If found, return 0 and store pixel in
       (*xp,*yp). Else return 1. Note that this function assumes that
       excess bytes have been cleared with bm_clearexcess. */
    """
    w = np.nonzero(bm)
    if len(w[0]) == 0:
        return None

    # Y축 데이터가 존재하는곳이 마지막 요소값 
    q = np.where(w[0] == w[0][-1])
    y = w[0][q]
    x = w[1][q]
    return y[0], x[0]

def xor_to_ref(bm: np.array, x: int, y: int, xa: int) -> None:
    """
     /* efficiently invert bits [x,infty) and [xa,infty) in line y. Here xa
    must be a multiple of BM_WORDBITS. */
    """

    if x < xa:
        bm[y, x:xa] ^= True
    elif x != xa:
        bm[y, xa:x] ^= True

def xor_path(bm: np.array, p: _Path) -> None:
    """
    a path is represented as an array of points, which are thought to
    lie on the corners of pixels (not on their centers). The path point
    (x,y) is the lower left corner of the pixel (x,y). Paths are
    represented by the len/pt components of a path_t object (which
    also stores other information about the path) */

    xor the given pixmap with the interior of the given path. Note: the
    path must be within the dimensions of the pixmap.
    """
    if len(p) <= 0:  # /* a path of length 0 is silly, but legal */
        return

    y1 = p.pt[-1].y
    xa = p.pt[0].x
    for n in p.pt:
        x, y = n.x, n.y
        if y != y1:
            # /* efficiently invert the rectangle [x,xa] x [y,y1] */
            xor_to_ref(bm, x, min(y, y1), xa)
            y1 = y


# Initialize data, for example convert a PIL image to a numpy array
# [...]
data = np.zeros((32, 32), np.uint32)
data[8:32-8, 8:32-8] = 1
image = np.asarray(data)

original = image.copy()

bitmap2 = Bitmap(data)
path2 = bitmap2.trace()


w = np.nonzero(image)

#print(np.where(w[1]))

#print(np.transpose(w))

# 31과 y축 데이터존재하는곳이 같은값을 가지는곳 31
#print(np.where(w[0] == w[0][-1]))

print(w[0])

print(w[0][-1])

q = np.where(w[0] == w[0][-1])

print(np.where(w[0] == w[0][-1]))

y = w[0][q] + 1
x = w[1][q]

print(w[0][q])
print(w[1][q])
print(y)

plist = [ ]  

test = findnext(image)

y0, x0 = test

sign = original[y0][x0] # 1 Or 0 

path = findpath(image, x0, y0 + 1 , sign, POTRACE_TURNPOLICY_MINORITY)

# path 지우기 
# xor_path(image,path)

#if path.area > 2:
#    plist.append(path)


abrcde = 112

print(plist)

for curve in path2:
    print ( "start_point ", curve.start_point)
    for segment in curve:
        print (segment)
        end_point_x = segment.end_point
        end_point_y = segment.end_point
        if segment.is_corner:
            c_x = segment.c
            c_y = segment.c
        else:
            c1_x, c1_y = segment.c1
            c2_x, c2_y = segment.c2



plt.figure()
plt.plot(111), plt.imshow(data, cmap = "gray"), plt.title("With [rows,cols]")
plt.show()