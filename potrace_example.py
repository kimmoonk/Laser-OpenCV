from re import X
import numpy as np
from potrace import Bitmap
from potrace import Path
from potrace import Curve

import potrace
import matplotlib.pyplot as plt
from PIL import Image



# Initialize data, for example convert a PIL image to a numpy array
# [...]
data = np.zeros((32, 32), np.uint32)
data[8:32-8, 8:32-8] = 1

#x = np.asarray(data)
#--------------------------------
img2 = Image.open('Star2.png') 
x = np.asarray(img2)

nonzer = np.nonzero(x)
print(nonzer)

#return1 = potrace.process_path(x)
#print (return1)

bitmap = Bitmap(x)
path = bitmap.trace(alphamax=0.5)

print(path)
# print(path.decomposition_points)

memo = open('potrace.txt','w')

arr = []


for curve in path:
    print ("start_point =", curve.start_point)
    Str_Start_Point = str(curve.start_point)
    memo.write("start_point =" + Str_Start_Point + "\n")
    for segment in curve:
        #print (segment)
        end_point_x = segment.end_point
        end_point_y = segment.end_point
        
        print (end_point_x)
        
        #꼭지점 테스트중
        arr = np.append(arr,end_point_x)
        
        Str_Point = str(end_point_x)
        
        memo.write(Str_Point + "\n")
        
        
        
        if segment.is_corner:
            c_x = c_y = segment.c
        else:
            c1_x = c1_y = segment.c1
            c2_x = c2_y = segment.c2
            
print ("Print ARR : \n")            
print (arr)            

plt.figure()
plt.plot(111), plt.imshow(x, cmap = "gray"), plt.title("With [rows,cols]")
plt.show()