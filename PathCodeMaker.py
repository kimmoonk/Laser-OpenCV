from turtle import distance, done, xcor
import cv2
import numpy as np
from numpy import array as a

import potrace
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from matplotlib.figure import Figure

from PIL import Image
from Bezier import Bezier
from math import *
from ArcApp import *

def MakePathCode(image,alpha=0.0):
    x = np.asarray(image)
    bitmap = potrace.Bitmap(x)
    path = bitmap.trace(turdsize = 3, alphamax = alpha)
    points = np.empty((0,2)) 
    
    fig_PathCode = Figure(figsize=(5, 5), dpi=100)
    ax = fig_PathCode.add_subplot()
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.set(xlim=(0, 100), 
        ylim=(0, 100) )


    t_points = np.arange(0, 1, 0.01)
    Contour_Num = 0
    count = 0
    set_error = 0.01
    
    memo = open('code.txt', 'w')
    # plt.axes().set_aspect('equal', 'box')


    
    for curve in path:
        Contour_Num += 1
        # 몇번째 Contour(윤곽선) , 시작점 표현
        # print (Curve_Num,"st Curve", curve.start_point)
    
        # print ("L   " + 
        #        "X"    ,  round(curve.start_point.x,1) + " "
        #        "Y"    ,  round(curve.start_point.y,1) )
        print ("S1000") # Laser ON

        
        # 전송할 Memo 파일 작성
        sentence = ("L" + 
                    "X" + str(round(curve.start_point.x, 1)).zfill(4) +
                    "Y" + str(round(curve.start_point.y, 1)).zfill(4) + "\n")
        
        print (sentence)
        
        memo.write(sentence)    
        memo.write("S1000\n")
        
        
        
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
                            "L" + 
                            "X" + str(round(c_x.x, 1)).zfill(4) + 
                            "Y" + str(round(c_y.y, 1)).zfill(4) + "\n"
                            "L" + 
                            "X" + str(round(end_point.x, 1)).zfill(4) +
                            "Y" + str(round(end_point.y, 1)).zfill(4) + "\n"
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
                #plt.plot(points_set_0[:, 0], # X 좌표
                #       points_set_0[:, 1]) # Y 좌표 
                ax.plot(points_set_0[:, 0], # X 좌표
                        points_set_0[:, 1]) # Y 좌표 
                            
                

            # 만약 Segment가 Bezier곡선일 경우
            else:
                c1 = segment.c1
                c2 = segment.c2
                
                # 목표지점 제어점1 제어점2
                
                # 전송할 Memo 파일 작성          
                #//////////////////////////////////////////////////////////////////////////////////////////////
                #시스템설계 파트      
                
                sentence =  (
                            "X" + str(round(points[-1][0], 1)).zfill(4) + " "
                            "Y" + str(round(points[-1][1], 1)).zfill(4) + " "
                    
                            "X" + str(round(end_point.x, 1)).zfill(4) + " "
                            "Y" + str(round(end_point.y, 1)).zfill(4) + " "
                            #C1 (제어점)
                            "X" + str(round(c1.x, 1)).zfill(4) + " "
                            "Y" + str(round(c1.y, 1)).zfill(4) + " "
                            #C2 (제어점)
                            "X" + str(round(c2.x, 1)).zfill(4) + " "
                            "Y" + str(round(c2.y, 1)).zfill(4) + "\n"                                                                        
                            )
                
                #//////////////////////////////////////////////////////////////////////////////////////////////
                #베지에곡선을 위해서는 이전 endpoint, c1,c2, 이번 endpoint 필요
                
                
                points_set_1 = a([
                    points[-1],[c1.x,c1.y],[c2.x,c2.y],[end_point.x,end_point.y]
                    ])
                
                # 베지어로 보내기
                
                # 원호 
                BezierCurveTo_circular(set_error,points_set_1,200,memo)
                
                
                curve_set_1 = Bezier.Curve(t_points, points_set_1)                

            # print ("EndPoint ", end_point)        
            points = np.append(
            points,np.array([[end_point.x, 
                            end_point.y]]) , 
            axis = 0)
        
        # 한 Contour 끝
        memo.write("S0\n")

            

    print ("S    0")
    memo.write("Z\n")
    memo.close()
    plt.grid()
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    title = 'Set_Error : ' + str(set_error)
    plt.title(title)   
    print(count)

    plt.show

    return fig_PathCode        


     

    