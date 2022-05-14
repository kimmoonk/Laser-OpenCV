def getCurve(ts,tm,te,points_set_1,set_error):

    arc = []
    currGood = False
    prevGood = False
    
    prev_e = 1
    step = 0
    done = 0
    
    set_error = 0.001
    
    while not(done) :
        prevGood = currGood
        tm = (ts + te) / 2 # 0.5
        step += 1
        
        arc_Points = Bezier.Curve([ts,tm,te],points_set_1)
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
        
        q = (te - ts) / 4
        Error = Bezier.Curve([ts+q , te-q],points_set_1)
        
        con1 = Error[0]
        con2 = Error[1]
    
        ref = dist(arc , np1)
        d1 = dist(arc , con1)
        d2 = dist(arc , con2)
        
        Error_var = abs(d1 - ref) + abs(d2 -ref)
                    
        
        #계산한 Error 값이 설정 Error보다 작으면 현재 굿
        currGood = (Error_var <= set_error)
        
        done = prevGood and not(currGood)
        
        # 만약 Error 때문에 재시행시 te를 이전 e에 저장.
        if not(done) :
            prev_e = te
        
        elif done :
            ts = prev_e
            break
            
            
        # 만약 현재 좋으면
        if currGood :
            
            #if te가 최대치이면 끝.
            if te >= 1 :                    
                te = 1
                prev_e = te
                                        
                done = True
                break
                                    
            # 더 넓게 잡아보자. e 를
            elif te < 1 :
                te = te + (te - ts) / 2
        
        # 현재 호가 안좋으면 좁게 잡아보자.
        else :
            te = tm
            
            
            
            
if (curr_good) {
    if e is already at max, then we're done for this arc.
          if (t_e >= 1) {
            // make sure we cap at t=1
            arc.interval.end = prev_e = 1;
            prev_arc = arc;
            // if we capped the arc segment to t=1 we also need to make sure that
            // the arc's end angle is correct with respect to the bezier end point.
            if (t_e > 1) {
              let d = {
                x: arc.x + arc.r * cos(arc.e),
                y: arc.y + arc.r * sin(arc.e),
              };
              arc.e += utils.angle({ x: arc.x, y: arc.y }, d, this.get(1));
            }
            break;
          }
          // if not, move it up by half the iteration distance
          t_e = t_e + (t_e - t_s) / 2;
        } 
        
        else {
          // this is a bad arc: we need to move 'e' down to find a good arc
          t_e = t_m;
        }