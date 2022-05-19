import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

video = cv2.VideoCapture(0) # 카메라 생성, 0번 카메라로 live feed 받기
# 비디오 캡쳐 객체가 정상적으로 open 되었는지 확인
if video.isOpened():
    print('width: {}, height : {}'.format(video.get(3), video.get(4)))

cv2.namedWindow('Canny Edge', 0)

# 트랙바를 조절할 때마다 실행할 명령이 따로 없으므로 dummy 함수를 하나 만들어준다.
def nothing(x):
    pass

# Canny Edge window에 0~255 임계값 조절 trackbar 두 개
cv2.createTrackbar('threshold 1', 'Canny Edge', 0, 500, nothing) # 트랙바 생성, 조정 범위는 0~500
cv2.createTrackbar('threshold 2', 'Canny Edge', 0, 500, nothing)
cv2.setTrackbarPos('threshold 1', 'Canny Edge', 50) # 트랙바의 초기값 지정
cv2.setTrackbarPos('threshold 2', 'Canny Edge', 200)
# 가로 세로 각 배수씩 더 크게 검정색 이미지를 생성
def create_image_multiple(h, w, d, hcout, wcout):
    image = np.zeros((h*hcout, w*wcout, d), np.uint8)
    color = tuple(reversed((0, 0, 0)))
    image[:] = color
    return image
# 통이미지 하나에 원하는 위치로 복사(표시)
# dst는 create_image_multiple 함수에서 만든 통이미지, src는 복사할 이미지
def showMultiImage(dst, src, h, w, d, col, row):
    # 3 color
    if d == 3:
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w] = src[0:h, 0:w]
    # 1 color
    elif d == 1:
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 0] = src[0:h, 0:w]
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 1] = src[0:h, 0:w]
        dst[(col*h):(col*h)+h, (row*w):(row*w)+w, 2] = src[0:h, 0:w]
while True:
    check, frame = video.read() # 카메라에서 이미지 얻기. 비디오의 한 프레임씩 읽기, 제대로 프레임을 읽으면 ret값이 True 실패하면 False, frame에는 읽은 프레임이 나옴
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gau_frame = cv2.GaussianBlur(frame, (5, 5), 0) # 노이즈 제거 - 얻어온 프레임에 대해 5x5 가우시안 필터 먼저 적용
    low = cv2.getTrackbarPos('threshold 1', 'Canny Edge') # 사용자 설정 신뢰도 임계값 1
    high = cv2.getTrackbarPos('threshold 2', 'Canny Edge') # 사용자 설정 신뢰도 임계값 2
    height = gau_frame.shape[0] # 이미지 높이
    width = gau_frame.shape[1] # 이미지 넓이
    depth = gau_frame.shape[2] # 이미지 색상 크기
    frame_canny = cv2.Canny(gau_frame, low, high) # 트랙바로부터 읽어온 threshold 1,2 값들을 사용하여 Canny 함수 실행
    # 화면에 표시할 이미지 만들기 (1 x 2)
    
    reversed_image = cv2.bitwise_not(frame_canny)
    
    result = create_image_multiple(height, width, depth, 1, 2) # 화면 표시할 1x2 검정 이미지 생성
    
    showMultiImage(result, gau_frame, height, width, depth, 0, 0) # 왼쪽 (0, 0)
    #showMultiImage(result, frame_canny, height, width, 1, 0, 1) # 오른쪽 (0, 1)
    showMultiImage(result, reversed_image, height, width, 1, 0, 1) # 오른쪽 (0, 1)
    cv2.imshow('Canny Edge', result)              
    if cv2.waitKey(1) == 32: #SpaceBar -> 종료
        break
    
    elif cv2.waitKey(1) == ord('q'):
        #화면캡쳐
        #반전 이미지 (흑 백)
        
        img22 = cv2.imread("11112.png",cv2.IMREAD_GRAYSCALE)
        img12 = cv2.Canny(img22, low, high)
        img33 = cv2.bitwise_not(img12)
        kernel = np.ones((1,1),np.uint8)
        img44 = cv2.morphologyEx(img33,cv2.MORPH_CLOSE,kernel)
        
        
        cv2.imwrite("capture" + ".png",img44 )  # 파일이름(한글안됨), 이미지 

        reversed_image = cv2.bitwise_not(frame_canny)
        #cv2.imwrite("capture" + ".png", img12)  # 파일이름(한글안됨), 이미지 
        
        #cv2.imwrite("capture" + ".png", frame_canny)  # 파일이름(한글안됨), 이미지 
        
    elif cv2.waitKey(1) == ord('w'):
       
        #별 이미지 생성      
        # Star_3 = cv2.imread('Star.png',0)
        # cv2.imwrite("Star2" + ".png", Star_3)
        # img2 = Image.open('Star2.png') 
        
        #왜 3차원 배열이야???
        # --> RGB 때문에.
        
        #영상을 전처리과정을 거친후 
        
        #영상처리 이미지                
        img2 = Image.open('capture.png') 
        
        img2.show()
        x = np.asarray(img2)
        #print(x)
        #print(x.shape)
        
        img_2 = Image.fromarray(x)
        img_2.show()
        f = open('coordin.txt', 'w')
        
        # 윤곽선 X Y 좌표 검출
        for i in range(0,481):
            for j in range(0,641):
                if x[i][j]==255:
                    num_i = str(i)
                    num_j = str(j)
                    sentance = 'x,y :' + num_i +" " + num_j + "\n"
                    f.write(sentance)
                    print('x,y :', i , j)
        
        # for i in range(0,100):
        #     for j in range(0,100):
        #         if x[i][j]==255:
        #             num_i = str(i)
        #             num_j = str(j)
        #             sentance = 'x,y :' + num_i +" " + num_j + "\n"
        #             f.write(sentance)
        #             print('x,y :', i , j)        
        
        f.close()
        
        plt.figure()
        plt.plot(111), plt.imshow(x, cmap = "gray"), plt.title("With [rows,cols]")
        #plt.show()
        

    
       
        



video.release()
cv2.destroyAllWindows()
