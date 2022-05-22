# UART Tx/Rx demo
import tkinter as tk
from tkinter import ttk
from turtle import delay

from tkinter import filedialog

import serial
import threading

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np

from PathCodeMaker import *

import cv2
from PIL import Image
import matplotlib.pyplot as plt
import multiprocessing
from PIL import Image, ImageTk
        
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


f = open("code.txt", 'r')
video = cv2.VideoCapture(0) # 카메라 생성, 0번 카메라(노트북)로 live feed 받기

#video = cv2.VideoCapture(1) # 카메라 생성, 1번 카메라(웹캠)로 live feed 받기

# A simple Information Window
class InformWindow:
    def __init__(self,informStr):
        self.window = tk.Tk()
        self.window.title("Information")
        self.window.geometry("220x60")
        label = tk.Label(self.window, text=informStr)
        buttonOK = tk.Button(self.window,text="OK",command=self.processButtonOK)
        label.pack(side = tk.TOP)
        buttonOK.pack(side = tk.BOTTOM)
        self.window.mainloop()

    def processButtonOK(self):
        self.window.destroy()
    
class App(customtkinter.CTk):
    WIDTH = 1400
    HEIGHT = 1000
    
    def __init__(self):
        super().__init__() 
               
        # window = tk.Tk()
        self.title("GUI UART Tx/Rx Demo")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.uartState = False # is uart open or not


        # ============ create two frames ============
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=140,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============
        # configure grid layout (1x13)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        #self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        #self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(12, minsize=20)  # empty row with minsize as spacing        
        self.frame_left.grid_rowconfigure(13, minsize=20)  # empty row with minsize as spacing


        # ========frame _left (0~2,0)
        # a frame contains COM's information, and start/stop button
        self.frame_COMinf = customtkinter.CTkFrame(master=self.frame_left,
                                              corner_radius=0)
        self.frame_COMinf.grid(row=0, column=0, rowspan=3, columnspan = 1, sticky="nswe")
        
        # self.frame_COMinf.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        # self.frame_COMinf.grid_rowconfigure(5, weight=1)  # empty row as spacing
        # self.frame_COMinf.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        # self.frame_COMinf.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.labelCOM = customtkinter.CTkLabel(master=self.frame_COMinf,
                                               width=60,
                                              text="COM Port: ",
                                               text_font=("Roboto Medium", -12))  # font name and size in px

        self.COM = tk.StringVar(value = "COM3")
        
        self.ertryCOM = customtkinter.CTkEntry(master=self.frame_COMinf, 
                                               width=60,
                                               textvariable = self.COM)
        
        self.labelCOM.grid(row = 1, column = 1, padx = 5, pady = 3)
        self.ertryCOM.grid(row = 1, column = 2, columnspan = 1, padx = 5, pady = 3)

        labelBaudrate = customtkinter.CTkLabel(master=self.frame_COMinf,
                                               width=60,
                                               text="Baudrate: ",
                                               text_font=("Roboto Medium", -12))  # font name and size in px

        self.Baudrate = tk.IntVar(value = 9600)
        ertryBaudrate = customtkinter.CTkEntry(master=self.frame_COMinf, 
                                               width=60,
                                               textvariable = self.Baudrate)
        labelBaudrate.grid(row = 2, column = 1, padx = 5, pady = 3)
        ertryBaudrate.grid(row = 2, column = 2, columnspan = 1, padx = 5, pady = 3)

        labelParity = tk.Label(self.frame_COMinf,text="Parity: ")
        self.Parity = tk.StringVar(value ="NONE")
        comboParity = ttk.Combobox(self.frame_COMinf, width = 17, textvariable=self.Parity)
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"
        # labelParity.grid(row = 2, column = 1, padx = 5, pady = 3)
        # comboParity.grid(row = 2, column = 2, padx = 5, pady = 3)

        labelStopbits = tk.Label(self.frame_COMinf,text="Stopbits: ")
        self.Stopbits = tk.StringVar(value ="1")
        comboStopbits = ttk.Combobox(self.frame_COMinf, width = 17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1","1.5","2")
        comboStopbits["state"] = "readonly"
        # labelStopbits.grid(row = 2, column = 3, padx = 5, pady = 3)
        # comboStopbits.grid(row = 2, column = 4, padx = 5, pady = 3)
        
        self.buttonSS = tk.Button(master=self.frame_COMinf, 
                                                text = "Connect", 
                                                #fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 1, columnspan=2, padx = 5, pady = 3, sticky = "S")

        # ============= frame left_(3~10,0) (Pathcode 표기) ============= 
#        self.frame_CodeEntry = customtkinter.CTkFrame(master=self.frame_left,
#                                                        corner_radius=0)
#        self.frame_CodeEntry.grid(row=3, column=0, rowspan=8, sticky="nswe")
        
        # self.frame_CodeEntry.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
#        self.frame_CodeEntry.grid_rowconfigure(0, weight=1)  # empty row as spacing
        # self.frame_CodeEntry.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        # self.frame_CodeEntry.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        
        self.frame_label_PathCode = tk.Frame(master = self.frame_left)
        self.frame_label_PathCode.grid(row=3, column=0, rowspan=8, columnspan = 1, sticky="nswe")
        self.frame_label_PathCode.grid_rowconfigure(0, weight=1)  # empty row as spacing
        

        
        self.label_PathCode = tk.Listbox(master=self.frame_label_PathCode,
                                                   width = 20
                                                   #fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   #justify=tk.LEFT,
                                                   #corner_radius=0
                                                   )
        
        
        
        self.scrollbarTrans = tk.Scrollbar(master = self.frame_label_PathCode,
                                           command = self.label_PathCode.yview,
                                           orient='vertical')
        self.label_PathCode.config(yscrollcommand=self.scrollbarTrans.set)
        
        self.label_PathCode.grid(column=0, row=0, rowspan=8, sticky="nswe", padx=15, pady=15)  
        self.scrollbarTrans.grid(column=1, row=0, rowspan=8, sticky="ns")
        
        # ============= frame left_(11~12,0) (Buttons) ============= 
        self.frameFunction = customtkinter.CTkFrame(master=self.frame_left,
                                                corner_radius=0)
        self.frameFunction.grid(row = 11, column = 0, rowspan = 2, columnspan = 1, sticky="nswe")
                
        self.buttonStartPoint = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "원점 검색",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonStartPoint)
        self.buttonStartPoint.grid(row = 0, column = 0, padx = 5, pady = 3,sticky='we')
        
        self.buttonMoveZeroPos = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "영점 이동",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonMoveZeroPos)
        self.buttonMoveZeroPos.grid(row = 0, column = 1, padx = 5, pady = 3,sticky='we')
        
        self.buttonMakePathCode_LoadImage = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "코드 변환",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonMakePathCode_LoadImage)
        self.buttonMakePathCode_LoadImage.grid(row = 1, column = 0, padx = 5, pady = 3,sticky='we')        
                
                
        self.buttonSendPathCode = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "코드 전송",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonSendPathCode)
        self.buttonSendPathCode.grid(row = 1, column = 1, padx = 5, pady = 3, sticky='we')  


        # ---------- left frame status -------------
        
        self.label_status = customtkinter.CTkLabel(master=self.frame_left,
                                                   text = 'Line = 200')
        self.label_status.grid(row=13,column=0,padx=10,sticky='we')
        


        # ============ frame_right PathCode 및 영상보여주기 ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
#        self.frame_right.rowconfigure(4, weight=1)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        ''' 그려질 그림 입니다'''

        global frame_right_Matplot
                
        self.frame_right_Matplot = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_right_Matplot.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nswe")
        
        self.frame_right_Matplot.rowconfigure(0, weight=1)
        self.frame_right_Matplot.columnconfigure(0, weight=1)

        fig = Figure(figsize=(7, 7), dpi=100)
        fig = Figure(figsize=(7, 7), dpi=100)

        ax = fig.add_subplot()
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.set(xlim=(0, 100), 
                ylim=(0, 100) )


        global canvas
        canvas = FigureCanvasTkAgg(fig, master=self.frame_right_Matplot)        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
        
        # -------------------------- frame_right 영상처리 frame ----------------------------
        
        self.frame_right_video = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_right_video.grid(row=0, column=2,rowspan=4, sticky="nswe", padx=20, pady=20)
        self.frame_right_video.rowconfigure(4, weight=1)

        

        ''' 영상 처리 입니다'''
        global frame_right_video_RGB
        global frame_right_video_Edge
        global lmain
        
        # ---------------------------------------- 원본 영상 -----------
        
        self.frame_right_video_RGB = tk.Label(master=self.frame_right_video)
        
        self.frame_right_video_RGB.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        
        # ---------------------------------------- 전처리한 영상 -------   
        
        self.frame_right_video_Edge = tk.Label(master=self.frame_right_video)
        
        self.frame_right_video_Edge.grid(row=1, column=0, sticky="nswe", padx=15, pady=15)        
        
        # ----------------------------------------threshold value slider---------        
        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right_video,
                                                from_=0,
                                                to=255,
                                                number_of_steps=255                                                
                                                )
        self.slider_1.grid(row=2, column=0, pady=10, padx=20, sticky="we")
        
        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right_video,
                                                from_=0,
                                                to=255,
                                                number_of_steps=255

                                                )
        self.slider_2.grid(row=3, column=0, pady=10, padx=20, sticky="we")
        
        self.slider_1.set(50)
        self.slider_2.set(200)
        
        self.buttonMakePathCode_CaptureImage = customtkinter.CTkButton(master=self.frame_right_video,
                                                        width = 30,
                                                        height = 15,
                                                        text = "Path Code 변환",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonMakePathCode_CaptureImage)
        self.buttonMakePathCode_CaptureImage.grid(row = 4, column = 0, padx = 5, pady = 3)  
        # ----------------------------------------
        
        self.CamThread = threading.Thread(target=self.startcam)
        self.CamThread.start()        


        # serial object
        self.ser = serial.Serial()
        # serial read threading
        # self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        # self.ReadUARTThread.start()

        '''Rx 부분 입니다.'''
        # Receive
        # frameRecv = tk.Frame(window)
        # frameRecv.grid(row = 2, column = 1)
        # labelOutText = tk.Label(frameRecv,text="Received Data:")
        # labelOutText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        # frameRecvSon = tk.Frame(frameRecv)
        # frameRecvSon.grid(row = 2, column =1)
        # scrollbarRecv = tk.Scrollbar(frameRecvSon)
        # scrollbarRecv.pack(side = tk.RIGHT, fill = tk.Y)
        # self.OutputText = tk.Text(frameRecvSon, wrap = tk.WORD, width = 60, height = 20, yscrollcommand = scrollbarRecv.set)
        # self.OutputText.pack()

        '''Tx 부분 입니다'''
        frameTrans = tk.Frame(self)
        # frameTrans.grid(row = 2, column = 1)
        labelInText = tk.Label(frameTrans,text="To Transmit Data:")
        # labelInText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        
        frameTransSon = tk.Frame(frameTrans)
        #frameTransSon.grid(row = 1, column =1, sticky = tk.W)
        
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        #scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        
        self.InputText = tk.Text(frameTransSon, wrap = tk.WORD,height = 50,width = 20, yscrollcommand = scrollbarTrans.set)
        #self.InputText.pack()
        
        self.buttonSend = tk.Button(frameTrans, text = "Send", command = self.processButtonSend)
        #self.buttonSend.grid(row = 3, column = 1, padx = 5, pady = 3, sticky = tk.E)

        # frameEdge = tk.Frame(window, height = 480, width = 640)
        # frameEdge.grid(row = 3, column = 2)

        #self.CamThread = threading.Thread(target=self.startcam)
        #self.CamThread.start()

        customtkinter.set_appearance_mode("dark")

        self.mainloop()

    def Fill_Path_Code(self):
        self.label_PathCode.delete(0,tk.END)
        memo = []
        line = 0
        index_num = 0 
        
        f = open("code.txt", 'r')
        memo = f.readlines()

        #self.label_PathCode.insert(tk.END,"1")        
        #self.label_PathCode.configure(text=" ")
          
        for line in memo:
            strToSend = str(line)

            self.label_PathCode.insert(tk.END, str(line))
            
            

            # text = self.label_PathCode.cget("text") + strToSend
            # self.label_PathCode.configure(text=text)
        
       # self.scrollbarTrans['command'] = self.label_PathCode.yview  
       # self.scrollbarTrans = tk.Scrollbar(master = self.frame_label_PathCode)
        #self.scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        self.label_status.configure(text = 'Line = ' + str(len(memo)))
            
            
        #self.label_PathCode.set_text(text = memo)

    def processButtonMakePathCode_CaptureImage(self):
        # Frame Clear
        for widget in self.frame_right_Matplot.winfo_children():
            widget.destroy()     
             
        fig_PathCode = MakePathCode(self.laser_resize_edge_img,0.0)  
        
        canvas = FigureCanvasTkAgg(fig_PathCode, master=self.frame_right_Matplot)
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
        
        self.Fill_Path_Code()

        return

    def processButtonMakePathCode_LoadImage(self):
        global Select_image
        self.filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
                                                ('png files', '*.png'), 
                                                ('jpg files', '*.jpg'), 
                                                ('all files', '*.*')))

        Select_image = (Image.open(self.filename)).convert('1')
        fliped_image_load = Select_image.transpose(Image.FLIP_TOP_BOTTOM)
        
   #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))        
  #      CVImage = cv2.imread(self.filename,cv2.IMREAD_GRAYSCALE)
 #       fliped_image_load = cv2.flip(CVImage)
#        
        

        # Frame Clear
        for widget in self.frame_right_Matplot.winfo_children():
            widget.destroy()

        fig_PathCode = MakePathCode(fliped_image_load,0.0)  
        canvas = FigureCanvasTkAgg(fig_PathCode, master=self.frame_right_Matplot)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.Fill_Path_Code()



    def processButtonSendPathCode(self):
        '''Path Code Send 입니다'''
        if (self.uartState):
            
            memo = f.readlines()
            
            for line in memo:
                strToSend = str(line)
                bytesToSend = strToSend[:].encode(encoding='ascii')

                self.ser.write(bytesToSend)
                #time.sleep(0.5)
                
                print(bytesToSend)
            
            # strToSend = "LX0.0Y0.0"            
            # bytesToSend = strToSend[:].encode(encoding='ascii')
            # self.ser.write(bytesToSend)
            # print(bytesToSend)
            
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)


    def processButtonStartPoint(self):
        '''원점 검색 입니다'''
        return

    def processButtonMoveZeroPos(self):
        '''영점 이동 입니다'''
        return
    
    def processButtonSS(self):
        # print(self.Parity.get())
        if (self.uartState):
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            # restart serial port
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get() #9600
            
            strParity = self.Parity.get() # NONE
            if (strParity=="NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(strParity=="ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(strParity=="EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            elif(strParity=="MARK"):
                self.ser.parity = serial.PARITY_MARK
            elif(strParity=="SPACE"):
                self.ser.parity = serial.PARITY_SPACE
                
            strStopbits = self.Stopbits.get() # 1
            if (strStopbits == "1"):
                self.ser.stopbits = serial.STOPBITS_ONE
            elif (strStopbits == "1.5"):
                self.ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            elif (strStopbits == "2"):
                self.ser.stopbits = serial.STOPBITS_TWO
            
            try:
                self.ser.open()
            except:
                infromStr = "Can't open "+self.ser.port
                InformWindow(infromStr)
            
            if (self.ser.isOpen()): # open success
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if (self.uartState):
            strToSend = self.InputText.get(1.0,tk.END)
            bytesToSend = strToSend[0:-1].encode(encoding='ascii')
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)

    def ReadUART(self):
        # print("Threading...")
        while True:
            if (self.uartState):
                try:
                    ch = self.ser.read().decode(encoding='ascii')
                    print(ch,end='')
                    self.OutputText.insert(tk.END,ch)
                except:
                    infromStr = "Something wrong in receiving."
                    InformWindow(infromStr)
                    self.ser.close() # close the serial when catch exception
                    self.buttonSS["text"] = "Start"
                    self.uartState = False
                    
    def startcam(self):  
        lmain = tk.Label(master = self.frame_right_video_RGB)
        lmain.grid(row=0, column=0)      
        
        lmain2 = tk.Label(master = self.frame_right_video_Edge)
        lmain2.grid(row=0, column=0)
        
        
        while (video.isOpened()):
        
            threshold_1 = self.slider_1.get()
            threshold_2 = self.slider_2.get()
             
            
            check, frame = video.read() # 카메라에서 이미지 얻기. 비디오의 한 프레임씩 읽기, 제대로 프레임을 읽으면 ret값이 True 실패하면 False, frame에는 읽은 프레임이 나옴
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gau_frame = cv2.GaussianBlur(frame, (5, 5), 0) # 노이즈 제거 - 얻어온 프레임에 대해 5x5 가우시안 필터 먼저 적용
            
            gray = cv2.cvtColor(gau_frame, cv2.COLOR_BGR2GRAY)


            height = gau_frame.shape[0] # 이미지 높이
            width = gau_frame.shape[1] # 이미지 넓이
            depth = gau_frame.shape[2] # 이미지 색상 크기
            # frame_canny = cv2.Canny(gau_frame, threshold_1, threshold_2) # 트랙바로부터 읽어온 threshold 1,2 값들을 사용하여 Canny 함수 실행
            
            #이진화
            ret, frame_canny = cv2.threshold(gray, threshold_1, 255, cv2.THRESH_BINARY)


            # 화면에 표시할 이미지 만들기 (1 x 2)
            
            # 형태학적 처리 (팽창)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            self.dilate0 = cv2.morphologyEx(frame_canny, cv2.MORPH_DILATE, kernel)
            self.dilate = cv2.morphologyEx(self.dilate0, cv2.MORPH_DILATE, kernel)

            #self.reversed_image = cv2.bitwise_not(dilate)
            self.fliped_image = cv2.flip(self.dilate,0)
              
            # # Reverse 작업 수행
            # self.reversed_image = cv2.bitwise_not(dilate)
            # self.fliped_image = cv2.flip(self.reversed_image,0)
            
            self.laser_resize_edge_img = cv2.resize(self.fliped_image, (100, 100),interpolation = cv2.INTER_AREA)


#            reversed_image = cv2.bitwise_not(frame_canny)
            
            # GUI 표기 img
            resize_rgb_img = cv2.resize(rgb_frame, (300, 300))
            resize_edge_img = cv2.resize(self.dilate, (300, 300))
            
            
            rgb_img = Image.fromarray(resize_rgb_img)
            edge_img = Image.fromarray(resize_edge_img)


            #img = Image.fromarray(rgb_frame)
            imgtk_rgb = ImageTk.PhotoImage(image=rgb_img)
            imgtk_edge = ImageTk.PhotoImage(image=edge_img)

            lmain.configure(image=imgtk_rgb)
            lmain2.configure(image=imgtk_edge)
            lmain.image = imgtk_rgb #Shows frame for display 1
            lmain2.image = imgtk_edge
            
            
    def on_closing(self, event=0):
        self.destroy()        

App()
