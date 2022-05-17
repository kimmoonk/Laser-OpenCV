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
        

f = open("code.txt", 'r')
video = cv2.VideoCapture(0) # 카메라 생성, 0번 카메라로 live feed 받기


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
    
class mainGUI:
    def __init__(self):
        window = tk.Tk()
        window.title("GUI UART Tx/Rx Demo")
        self.uartState = False # is uart open or not

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tk.Frame(window)
        frame_COMinf.grid(row = 1, column = 1)

        labelCOM = tk.Label(frame_COMinf,text="COMx: ")
        self.COM = tk.StringVar(value = "COM3")
        ertryCOM = tk.Entry(frame_COMinf, textvariable = self.COM)
        labelCOM.grid(row = 1, column = 1, padx = 5, pady = 3)
        ertryCOM.grid(row = 1, column = 2, padx = 5, pady = 3)

        labelBaudrate = tk.Label(frame_COMinf,text="Baudrate: ")
        self.Baudrate = tk.IntVar(value = 9600)
        ertryBaudrate = tk.Entry(frame_COMinf, textvariable = self.Baudrate)
        labelBaudrate.grid(row = 1, column = 3, padx = 5, pady = 3)
        ertryBaudrate.grid(row = 1, column = 4, padx = 5, pady = 3)

        labelParity = tk.Label(frame_COMinf,text="Parity: ")
        self.Parity = tk.StringVar(value ="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Parity)
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"
        labelParity.grid(row = 2, column = 1, padx = 5, pady = 3)
        comboParity.grid(row = 2, column = 2, padx = 5, pady = 3)

        labelStopbits = tk.Label(frame_COMinf,text="Stopbits: ")
        self.Stopbits = tk.StringVar(value ="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1","1.5","2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row = 2, column = 3, padx = 5, pady = 3)
        comboStopbits.grid(row = 2, column = 4, padx = 5, pady = 3)
        
        self.buttonSS = tk.Button(frame_COMinf, text = "Start", command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 4, padx = 5, pady = 3, sticky = tk.E)

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
        frameTrans = tk.Frame(window)
        frameTrans.grid(row = 3, column = 1)
        labelInText = tk.Label(frameTrans,text="To Transmit Data:")
        labelInText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row = 2, column =1)
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        self.InputText = tk.Text(frameTransSon, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tk.Button(frameTrans, text = "Send", command = self.processButtonSend)
        self.buttonSend.grid(row = 3, column = 1, padx = 5, pady = 3, sticky = tk.E)
        
        ''' Butoon 구현부 입니다'''
        frameFunction = tk.Frame(window)
        frameFunction.grid(row = 4, column = 1)
                
        self.buttonStartPoint = tk.Button(frameFunction, text = "원점 검색", command = self.processButtonStartPoint)
        self.buttonStartPoint.grid(row = 1, column = 1, padx = 5, pady = 3, sticky = tk.E)
                
        self.buttonMoveZeroPos = tk.Button(frameFunction, text = "영점 이동", command = self.processButtonMoveZeroPos)
        self.buttonMoveZeroPos.grid(row = 1, column = 2, padx = 5, pady = 3, sticky = tk.E)

        self.buttonMakePathCode = tk.Button(frameFunction, text = "Path Code 변환", command = self.processButtonMakePathCode)
        self.buttonMakePathCode.grid(row = 1, column = 3, padx = 5, pady = 3, sticky = tk.E)        
        
        self.buttonSendPathCode = tk.Button(frameFunction, text = "Path Code 보내기", command = self.processButtonSendPathCode)
        self.buttonSendPathCode.grid(row = 1, column = 4, padx = 5, pady = 3, sticky = tk.E)
        
        ''' 그려질 그림 입니다'''
        
        global frameCanvas 
        frameCanvas = tk.Frame(window)
        frameCanvas.grid(row = 2, column = 1)

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        
        global canvas
        canvas = FigureCanvasTkAgg(fig, master=frameCanvas)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        
        
        ''' 영상 처리 입니다'''
        global frameRGB
        global frameEdge
        global lmain
        
        frameRGB = tk.Frame(window, height = 300, width = 400)
        frameRGB.grid(row = 2, column = 2)


        
        # frameEdge = tk.Frame(window, height = 480, width = 640)
        # frameEdge.grid(row = 3, column = 2)

        self.CamThread = threading.Thread(target=self.startcam)
        self.CamThread.start()

        
        window.mainloop()


    def processButtonMakePathCode(self):
        global Select_image
        self.filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
                                                ('png files', '*.png'), 
                                                ('jpg files', '*.jpg'), 
                                                ('all files', '*.*')))

        Select_image = (Image.open(self.filename)).convert('1')

        # Frame Clear
        for widget in frameCanvas.winfo_children():
            widget.destroy()

        fig_PathCode = MakePathCode(Select_image,0.0)  
        canvas = FigureCanvasTkAgg(fig_PathCode, master=frameCanvas)


        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


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
            self.ser.baudrate = self.Baudrate.get()
            
            strParity = self.Parity.get()
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
                
            strStopbits = self.Stopbits.get()
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
        lmain = tk.Label(frameRGB)
        lmain.grid(row=0, column=0)      
        
        while (video.isOpened()):
        
            
            check, frame = video.read() # 카메라에서 이미지 얻기. 비디오의 한 프레임씩 읽기, 제대로 프레임을 읽으면 ret값이 True 실패하면 False, frame에는 읽은 프레임이 나옴
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gau_frame = cv2.GaussianBlur(frame, (5, 5), 0) # 노이즈 제거 - 얻어온 프레임에 대해 5x5 가우시안 필터 먼저 적용
            height = gau_frame.shape[0] # 이미지 높이
            width = gau_frame.shape[1] # 이미지 넓이
            depth = gau_frame.shape[2] # 이미지 색상 크기
            frame_canny = cv2.Canny(gau_frame, 50, 100) # 트랙바로부터 읽어온 threshold 1,2 값들을 사용하여 Canny 함수 실행
            # 화면에 표시할 이미지 만들기 (1 x 2)
            
  
            reversed_image = cv2.bitwise_not(frame_canny)

            img = Image.fromarray(hsv_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            lmain.configure(image=imgtk)
            lmain.image = imgtk #Shows frame for display 1




            

            
                   

mainGUI()
