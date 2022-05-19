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
    
class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520
    
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
        self.frame_COMinf.grid(row=0, column=0, rowspan=3, sticky="nswe")
        
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
        self.ertryCOM.grid(row = 1, column = 2, padx = 5, pady = 3)

        labelBaudrate = customtkinter.CTkLabel(master=self.frame_COMinf,
                                               width=60,
                                               text="Baudrate: ",
                                               text_font=("Roboto Medium", -12))  # font name and size in px

        self.Baudrate = tk.IntVar(value = 9600)
        ertryBaudrate = customtkinter.CTkEntry(master=self.frame_COMinf, 
                                               width=60,
                                               textvariable = self.Baudrate)
        labelBaudrate.grid(row = 2, column = 1, padx = 5, pady = 3)
        ertryBaudrate.grid(row = 2, column = 2, padx = 5, pady = 3)

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
        
        self.buttonSS = customtkinter.CTkButton(master=self.frame_COMinf, 
                                                text = "Connect", 
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 1, columnspan=2, padx = 5, pady = 3, sticky = "S")

        # ============= frame left_(3~10,0) (Pathcode 표기) ============= 
        self.frame_CodeEntry = customtkinter.CTkFrame(master=self.frame_left,
                                                        corner_radius=0)
        self.frame_CodeEntry.grid(row=3, column=0, rowspan=8, sticky="nswe")
        
        # self.frame_CodeEntry.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_CodeEntry.grid_rowconfigure(0, weight=1)  # empty row as spacing
        # self.frame_CodeEntry.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        # self.frame_CodeEntry.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        
        self.label_PathCode = customtkinter.CTkLabel(master=self.frame_CodeEntry,
                                                   text="Path Code 들어갈 자리" ,
                                                   width = 130,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tk.LEFT,
                                                   corner_radius=0)
        
        self.label_PathCode.grid(column=0, row=0, rowspan=8, sticky="nswe", padx=15, pady=15)  
        
        # ============= frame left_(11~12,0) (Buttons) ============= 
        self.frameFunction = customtkinter.CTkFrame(master=self.frame_left,
                                                corner_radius=0)
        self.frameFunction.grid(row = 11, column = 0, rowspan = 2, sticky="nswe")
                
        self.buttonStartPoint = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "원점 검색",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonStartPoint)
        self.buttonStartPoint.grid(row = 0, column = 0, padx = 5, pady = 3)
        
        self.buttonMoveZeroPos = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "영점 이동",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonMoveZeroPos)
        self.buttonMoveZeroPos.grid(row = 0, column = 1, padx = 5, pady = 3)
        
        self.buttonMakePathCode = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "코드 변환",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonMakePathCode)
        self.buttonMakePathCode.grid(row = 1, column = 0, padx = 5, pady = 3)        
                
                
        self.buttonSendPathCode = customtkinter.CTkButton(master=self.frameFunction,
                                                        width = 30,
                                                        height = 15,
                                                        text = "코드 전송",
                                                        text_font=("Roboto Medium", -12),  # font name and size in px
                                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                        command = self.processButtonSendPathCode)
        self.buttonSendPathCode.grid(row = 1, column = 1, padx = 5, pady = 3)  

        # ============ frame_right PathCode 및 영상보여주기 ============
        
        
        # configure grid layout (3x7)

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
        
        
        ''' 그려질 그림 입니다'''
        
        global frameCanvas 
        frameCanvas = tk.Frame(self)
        # frameCanvas.grid(row = 2, column = 2)

        fig = Figure(figsize=(7, 7), dpi=100)

        ax = fig.add_subplot()
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.set(xlim=(0, 100), 
                ylim=(0, 100) )


    
        

        
        global canvas
        canvas = FigureCanvasTkAgg(fig, master=frameCanvas)
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        
        
        ''' 영상 처리 입니다'''
        global frameRGB
        global frameEdge
        global lmain
        
        frameRGB = tk.Frame(self, height = 300, width = 400)
        #frameRGB.grid(row = 2, column = 3)


        
        # frameEdge = tk.Frame(window, height = 480, width = 640)
        # frameEdge.grid(row = 3, column = 2)

        #self.CamThread = threading.Thread(target=self.startcam)
        #self.CamThread.start()

        customtkinter.set_appearance_mode("light")

        self.mainloop()


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
            
    def on_closing(self, event=0):
        self.destroy()        

App()
