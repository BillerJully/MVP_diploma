import tkinter as tk
import customtkinter as ctk

import torch
import numpy as np

import cv2
from PIL import Image, ImageTk

import pathlib

# Используем pathlib.Path для автоматического определения типа пути
pathlib.PosixPath = pathlib.Path

app = tk.Tk()
app.geometry("600x600")
app.title("app")
ctk.set_appearance_mode("dark")  # Установка темного режима для customtkinter

vidFrame = tk.Frame(app, height=480, width=500)  # Указываем родительский виджет
vidFrame.pack()
vid = ctk.CTkLabel(vidFrame)
vid.pack()

# Загрузка модели YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/last.pt', force_reload=True)

cap = cv2.VideoCapture(0)

def detect():
    ret, frame = cap.read()
    if not ret:
        print("Error")
        return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)
    img = np.squeeze(results.render())
    imgarr = Image.fromarray(img)  # Используем img вместо frame
    imgtk = ImageTk.PhotoImage(image=imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    vid.after(100, detect)  # Увеличиваем интервал для снижения нагрузки на процессор

detect()

app.mainloop()
