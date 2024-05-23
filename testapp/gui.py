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
app.geometry("800x600")  # Увеличиваем размер окна, чтобы уместить текстовый виджет
app.title("app")
ctk.set_appearance_mode("dark")  # Установка темного режима для customtkinter

vidFrame = tk.Frame(app, height=480, width=500)  # Указываем родительский виджет
vidFrame.pack(side=tk.LEFT)
vid = ctk.CTkLabel(vidFrame)
vid.pack()

# Текстовый виджет для отображения результатов
results_text = tk.Text(app, height=30, width=50)
results_text.pack(side=tk.RIGHT)

# Загрузка модели YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/last.pt', force_reload=True)

# Инициализация захвата видео отложена до нажатия кнопки
cap = None

def start_capture():
    global cap, start_button
    cap = cv2.VideoCapture(0)
    detect()
    start_button.configure(text="Закончить", command=stop_capture)

def stop_capture():
    global cap
    if cap is not None:
        cap.release()
    cap = None
    start_button.configure(text="Начать", command=start_capture)

def detect():
    global cap
    if cap is None or not cap.isOpened():
        return
    ret, frame = cap.read()
    if not ret:
        print("Error")
        return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)
    img = np.squeeze(results.render())
    results.print()
    
    # Обновление текстового виджета с результатами
    filtered_results = results.pandas().xyxy[0]
    states = filtered_results[filtered_results['name'].isin(['awake', 'drowsy'])]['name']
    
    # Обновление текстового виджета только с состояниями "awake" или "drowsy"
    results_text.delete('1.0', tk.END)
    for state in states:
        results_text.insert(tk.END, state + '\n')
    results_text.delete('1.0', tk.END)
    results_text.insert(tk.END, results.pandas().xyxy[0].to_string(index=False))
    
    imgarr = Image.fromarray(img)  # Используем img вместо frame
    imgtk = ImageTk.PhotoImage(image=imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    if cap is not None:
        vid.after(1, detect)  # Увеличиваем интервал для снижения нагрузки на процессор

# Кнопка для начала захвата видео
start_button = ctk.CTkButton(app, text="Начать", command=start_capture)
start_button.pack(side=tk.BOTTOM)

app.mainloop()
