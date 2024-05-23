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
app.geometry("800x600")  # Увеличиваем размер окна
app.title("app")
ctk.set_appearance_mode("dark")  # Установка темного режима для customtkinter

# Виджет для видео теперь будет вверху
vidFrame = tk.Frame(app, height=480, width=500)
vidFrame.pack(side=tk.TOP, padx=10, pady=10)  # Добавляем отступы от краев
vid = ctk.CTkLabel(vidFrame, text="")  # Убедитесь, что текст пустой

vid.pack()

# Текстовый виджет теперь будет ниже видео
results_text = tk.Text(app, height=10, width=50)  # Уменьшаем высоту текстового виджета
results_text.pack(side=tk.TOP, padx=10, pady=10)  # Добавляем отступы от краев

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
        print("Ошибка захвата видео")
        return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)
    img = np.squeeze(results.render())
    results.print()
    
    # Фильтрация результатов для отображения только "awake" или "drowsy"
    df = results.pandas().xyxy[0]
    filtered_df = df[df['name'].isin(['awake', 'drowsy'])]
    
    # Обновление текстового виджета с отфильтрованными результатами
    results_text.delete('1.0', tk.END)
    results_text.insert(tk.END, filtered_df.to_string(index=False, header=False))
    
    imgarr = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    if cap is not None:
        vid.after(10, detect)  # Увеличиваем интервал для снижения нагрузки на процессор

# Кнопка для начала захвата видео
start_button = ctk.CTkButton(app, text="Начать", command=start_capture)
start_button.pack(side=tk.BOTTOM, padx=10, pady=10)  # Добавляем отступы от краев

app.mainloop()
