from turtle import xcor
import cv2
import numpy as np
from numpy import array as a

import potrace
import matplotlib.pyplot as plt
from PIL import Image
from Bezier import Bezier



# Make a numpy array with a rectangle in the middle
data = np.zeros((50, 50), np.uint32)
data[8:32-8, 8:32-8] = 1

#img2 = Image.open('Star2.png') 

img = Image.open('wooin.png')
img2 = img.convert('1')


x = np.asarray(img2)


# Create a bitmap from the array
bmp = potrace.Bitmap(x)

# Trace the bitmap to a path
path = bmp.trace(turdsize = 2, alphamax = 2)

# 시작점 중간점 종착점
points = np.empty((0,2))

# 베지에곡선 Plot 
t_points = np.arange(0, 1, 0.01)

Contour_Num = 0
count = 0

memo = open('code.txt', 'w')


for curve in path:
    Contour_Num += 1
    
    # 몇번째 Contour(윤곽선) , 시작점 표현
    # print (Curve_Num,"st Curve", curve.start_point)
   
    # print ("L   " + 
    #        "X"    ,  round(curve.start_point.x,1) + " "
    #        "Y"    ,  round(curve.start_point.y,1) )
    
    print ("S    1000") # Laser ON

    
    # 전송할 Memo 파일 작성
    sentence = ("L   " + 
                "X" + str(round(curve.start_point.x, 1)) + " "
                "Y" + str(round(curve.start_point.y, 1)) + "\n")
    
    print (sentence)
    
    memo.write(sentence)    
    memo.write("S   1000\n")
    
    
    
    #시작점 추가
    points = np.append(
        points,np.array([[curve.start_point.x,
                          curve.start_point.y]]), 
        axis = 0)
                       
    
    # print(points)
    
    for segment in curve:
                
        end_point = segment.end_point
        
        # 명령 회수 +1
        count += 1         
        
        # 만약 Segment가 직선일 경우
        if segment.is_corner:
            c_x = segment.c
            c_y = segment.c

            
            # 전송할 Memo 파일 작성    

            sentence = (
                        "L   " + 
                        "X" + str(round(c_x.x, 1)) + " "
                        "Y" + str(round(c_y.y, 1)) + "\n"
                        "L   " + 
                        "X" + str(round(end_point.x, 1)) + " "
                        "Y" + str(round(end_point.y, 1)) + "\n"
                        )            
            
            print(sentence)
            
            memo.write(sentence)    


            
            # points = np.append(
            #         points,np.array([[c_x.x, 
            #                           c_x.y]]) , 
            #         axis = 0)
            
            points_set_0 = a([
                points[-1],[c_x.x,c_x.y],[end_point.x,end_point.y]
                ])
            
            #plt 에 표기
            plt.plot(points_set_0[:, 0], # X 좌표
                     points_set_0[:, 1]) # Y 좌표 
                        
            

        # 만약 Segment가 곡선일 경우
        else:
            c1 = segment.c1
            c2 = segment.c2
            
            # 목표지점 제어점1 제어점2
            
            # 전송할 Memo 파일 작성                

            sentence = (
                        "C   " + 
                        "X" + str(round(end_point.x, 1)) + " "
                        "Y" + str(round(end_point.y, 1)) + " "
                        #C1 (제어점)
                        "X" + str(round(c1.x, 1)) + " "
                        "Y" + str(round(c1.y, 1)) + " "
                        #C2 (제어점)
                        "X" + str(round(c2.x, 1)) + " "
                        "Y" + str(round(c2.y, 1)) + "\n"                                                                        
                       )

            print(sentence)            
    
            
            memo.write(sentence)    


            #베지에곡선을 위해서는 이전 endpoint, c1,c2, 이번 endpoint 필요
            
            points_set_1 = a([
                points[-1],[c1.x,c1.y],[c2.x,c2.y],[end_point.x,end_point.y]
                ])
            
            curve_set_1 = Bezier.Curve(t_points, points_set_1)
            
            
            plt.plot(curve_set_1[:, 0], curve_set_1[:, 1])
            #plt.plot(points_set_1[:, 0], points_set_1[:, 1], 'ro:')

        
            
        
        # print ("EndPoint ", end_point)        
        points = np.append(
        points,np.array([[end_point.x, 
                          end_point.y]]) , 
        axis = 0)
        
    print ("S    0")
    memo.write("S   0\n")      

    #print (points)
          
            
memo.close()
            
plt.grid()

print(count)

plt.show()