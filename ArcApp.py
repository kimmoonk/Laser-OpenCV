from turtle import distance, done, xcor

from math import *
from Bezier import Bezier
import numpy as np
from numpy import array as a

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PI = 3.1415926535
quart = PI / 2


def b3p0(t,p):
    k = 1- t
    return k * k * k * p

def b3p1(t,p):
    k = 1- t
    return 3 * k * k * t * p

def b3p2(t,p):
    k = 1- t
    return 3 * k * t * t * p

def b3p3(t,p):
    k = 1- t
    return t * t * t * p

def b3(t,p0,p1,p2,p3):
    return b3p0(t, p0) + b3p1(t, p1) + b3p2(t, p2) + b3p3(t, p3)

def bezierCurve(t, p0x, p0y, 
                p1x, p1y, 
                p2x, p2y, 
                p3x, p3y ):
    return [b3(t, p0x, p1x, p2x, p3x), b3(t, p0y, p1y, p2y, p3y)]

def midpoint(x1, y1, x2, y2):
  return [(x1 + x2) / 2, (y1 + y2) / 2]

def perpendicularToLine(P1 , P2):
    return [P2.x - (25 * (y1 - y2)) / distance([x1, y1], [x2, y2]), y2 + (25 * (x1 - x2)) / distance([x1, y1], [x2, y2])]

def circleFromThreePoints(p1,p2,p3):
    mp1 = midpoint(p1,p2)
    mp2 = midpoint(p1,p3)

def getCircleCenter(p1 = [], p2 = [], p3 = []) :
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    
    dx2 = p3[0] - p2[0]
    dy2 = p3[1] - p2[1]
    
    dx1p = dx1 * cos(quart) - dy1 * sin(quart)
    dy1p = dx1 * sin(quart) + dy1 * cos(quart)
    dx2p = dx2 * cos(quart) - dy2 * sin(quart)
    dy2p = dx2 * sin(quart) + dy2 * cos(quart)                       
                    
    # 중간점 찍기                
    mx1 = (p1[0] + p2[0]) / 2
    my1 = (p1[1] + p2[1]) / 2
    mx2 = (p2[0] + p3[0]) / 2
    my2 = (p2[1] + p3[1]) / 2                     
                
    # 중간점 Offset
    mx1n = mx1 + dx1p
    my1n = my1 + dy1p
    mx2n = mx2 + dx2p
    my2n = my2 + dy2p
    
    arc = lineLineIntersection_8(mx1, my1, mx1n, my1n, mx2, my2, mx2n, my2n) # 두점
    r = dist(arc,p1) #반지름 R
    
    s = atan2(p1[1] - arc[1], p1[0] - arc[0])
    m = atan2(p2[1] - arc[1], p2[0] - arc[0])
    e = atan2(p3[1] - arc[1], p3[0] - arc[0])
    
    # 방향 결정 CW, CCW
    #if s<m<e, arc(s, e)
    #if m<s<e, arc(e, s + tau)
    #if s<e<m, arc(e, s + tau)                
    if s < e :
        if s > m or m > e :
            s += tau
        
        if s > e :
            tmp = e
            e = s
            s = tmp
    
    else :
        if e < m and m < s :
            tmp = e
            e = s
            s = tmp
        
        else :
            e += tau
        
    '''
    arc[0] = 시작 각도
    arc[1] = End 각도
    arc[2] = 반지름
    '''
    arc.append(s) # 호의 시작 각도
    arc.append(e) # 호의 마지막 각도
    arc.append(r) # 호의 반지름
    
    return arc

def lineLineIntersection_8(x1, y1, x2, y2, x3, y3, x4, y4):
    nx = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    ny = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)              
    
    #If d === 0, the lines are paralllel and there is no intersection.
    if d == 0 :
        return False
                                
    return [nx/d,ny/d]    

#distance 
def dist (p1 = [], p2 = []): 
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return sqrt(dx * dx + dy * dy)    

def BezierCurveTo_circular(tolerance,
                           points_set,
                           m_safety):


    ts = 0
    te = 1
    tm = te
    safety = 0
    arc = []
    prev_e = 1
    step = 0    
    set_error = tolerance
    safety = m_safety

    currGood = False
    prevGood = False
    done = False
    end_flag = False
    
    while not(done) or not(end_flag) :
        prevGood = currGood
        tm = (ts + te) / 2 # 0.5
        step += 1
        
        arc_Points = Bezier.Curve([ts,tm,te],points_set)
        
        np1 = arc_Points[0]
        np2 = arc_Points[1]
        np3 = arc_Points[2]
        
        '''
        arc[0] = 시작 각도
        arc[1] = End 각도
        arc[2] = 반지름
        '''
        arc = getCircleCenter(np1 , np2 , np3)

        # error = computeError(arc,np1,ts,te,points_set_1)
        #Error_var = computeError(arc,np1,ts,te,points_set_1)
        
        q = (te - ts) / 4
        Error = Bezier.Curve([ts+q , te-q],points_set)
        
        con1 = Error[0]
        con2 = Error[1]

        ref = dist(arc , np1)
        d1 = dist(arc , con1)
        d2 = dist(arc , con2)        
    
        Error_var = abs(d1 - ref) + abs(d2 -ref)
        
        #계산한 Error 값이 설정 Error보다 작으면 현재 굿
        currGood = (Error_var <= set_error)
        
        #이전 호가 좋으면 끝.
        done = prevGood and not(currGood)
        
        # 만약 Error 때문에 재시행시 te를 이전 e에 저장.
        if not(done) :
            prev_e = te
            
        #끝났을때  
        if done or step > safety:
            if te > 1 :        
                Curve_End = Bezier.Curve([1],points_set)
                np3 = Curve_End[0]
                arc = getCircleCenter(np1 , np2 , np3)
                
                ''' PathCode 저장 '''
                # Sentance
                sentence =  (
                            "C   " + 
                            # Arc 중점좌표
                            "X" + str(round(arc[0], 1)) + " "
                            "Y" + str(round(arc[1], 1)) + " "
                            # Arc 반지름좌표
                            "R" + str(round(arc[4], 1)) + " "
                            # Arc 시작각도, 끝각도
                            "I" + str(round(arc[2]/PI * 180, 1)) + " "
                            "J" + str(round(arc[3]/PI * 180, 1)) + "\n"                                                                        
                            )            
                
                print(sentence)                     
                # memo.write(sentence)
                

                
                ''' 그림 그리기 '''
            pac = mpatches.Arc((arc[0],arc[1]), arc[4]*2, arc[4]*2, angle=0, theta1=arc[2]/PI * 180, theta2=arc[3]/PI * 180,linewidth=2,color=np.random.rand(3,))
            plt.gcf().gca().add_artist(pac)
            #circle = plt.Circle((arc[0],arc[1]),arc[4],fill=False,color=np.random.rand(3,)) # 원
            #plt.gcf().gca().add_artist(circle)


            ts = te
            te = 1
            prev_e = te
                
            prevGood = False
            currGood = False
            
            # 만약 현재 좋으면
        if currGood :
                
                #if te가 최대치이면 끝.
            if te >= 1 :                    
                    
                prev_e = te
                
                if te > 1 :
                    Curve_End = Bezier.Curve([1],points_set)
                    E_p = Curve_End[0]
                    
                    modify_x = arc[0] + arc[4] * cos(arc[3])
                    modify_y = arc[1] + arc[4] * sin(arc[3])
                    
                    dx1 = modify_x - arc[0]
                    dy1 = modify_y - arc[1]
                    dx2 = E_p[0] - arc[0]
                    dy2 = E_p[1] - arc[1]
                    cross = dx1 * dy2 - dy1 * dx2
                    dot = dx1 * dx2 + dy1 * dy2
                    modifyangle = atan2(cross,dot)
                    arc[3] += modifyangle
                        
                        
                    # arc = getCircleCenter(np1 , np2 , Curve_End)

                    
                end_flag=True
                        
                # te가 1보다 클 때 처리해줘야 할것. te를 1로 갈아버린다?       
                # if te > 1 :
                                            
                # break
                                        
                # 더 넓게 잡아보자. e 를
            if te <= 1 :
                prev_e = te            
                te = te + (te - ts) / 2
        
            # 현재 호가 안좋으면 좁게 잡아보자.
        elif not(currGood) and not(done) :
            te = tm
            
        if step > safety :
            break
        
                                
                
                

#error 계산
def computeError(pc, np1 , s , e, Curve =[]) :                
    q = (e - s) / 4
    Error = Bezier.Curve([s+q , e-q],Curve)
    
    c1 = Error[0]
    c2 = Error[1]
                    
    ref = dist(pc , np1)
    d1 = dist(pc , c1)
    d2 = dist(pc , c2)
    return abs(d1 - ref) + abs(d2 -ref)