import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk

class WebcamPage(tk.Frame):
    def __init__(self, master, second_page, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.second_page = second_page
        
        # Отобразить окно с видеопотоком с вебкамеры
        self.video_label = tk.Label(self)
        self.video_label.pack()
        self.cap = cv2.VideoCapture(0)
        self.recording = False
        
        # Создание кнопки "Включить запись"
        self.record_button = ttk.Button(self, text="Включить запись", command=self.toggle_record)
        self.record_button.pack(pady=10)
        
        # Создание кнопки "Стоп и Сохранить"
        self.stop_save_button = ttk.Button(self, text="Стоп и Сохранить", command=self.stop_and_save_video)
        self.stop_save_button.pack(pady=10)
        
        # Создание кнопки "Назад"
        self.back_button = ttk.Button(self, text="Назад", command=lambda: self.second_page.pack())
        self.back_button.pack(pady=10)

        
        # Создание кнопки "Закрыть"
        self.close_button = ttk.Button(self, text="Закрыть", command=self.master.destroy)
        self.close_button.pack(pady=10)
    
    def toggle_record(self):
        self.recording = not self.recording
    
    def stop_and_save_video(self):
        self.recording = False
        file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(file_path, fourcc, 20.0, (640, 480))
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        out.release()
    
    def show_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)
            self.video_label.img = frame
            self.video_label.config(image=frame)
            if self.recording:
                frame_cv2 = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                self.out.write(frame_cv2)
            if self.recording:  # Добавляем проверку на переменную recording
                frame_cv2 = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                self.out.write(frame_cv2)
            self.video_label.after(10, self.show_webcam)



class SecondPage(tk.Frame):
    def __init__(self, master, first_page, background_image, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.first_page = first_page
        self.background_image = background_image
        self.video_playing = False
        self.playing_video = False
        
        # Создаем Canvas для отображения элементов GUI
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(expand=True, fill='both')
        
        # Отображаем фоновое изображение
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        
        # Создаем Frame для кнопок "Загрузить видео" и "Включить вебкамеру"
        button_frame = tk.Frame(self.canvas, width=400, height=100)
        button_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Создание кнопки "Загрузить видео"
        self.load_video_button = ttk.Button(button_frame, text="Загрузить видео", command=self.load_video)
        self.load_video_button.grid(row=0, column=1, padx=5, pady=0)
        
        # Создание кнопки "Включить вебкамеру"
        self.webcam_button = ttk.Button(button_frame, text="Включить вебкамеру", command=self.enable_webcam)
        self.webcam_button.grid(row=0, column=0, padx=5, pady=0)
        button_frame.columnconfigure(0, pad=50)
        button_frame.columnconfigure(1, pad=50)
        
        # Создание кнопки "Назад"
        self.back_button = ttk.Button(self, text="Назад", command=self.back_to_first_page)
        self.canvas.create_window(150, 300, window=self.back_button)
        
        # Создание кнопки "Закрыть"
        self.close_button = ttk.Button(self, text="Закрыть", command=self.master.destroy)
        self.canvas.create_window(450, 300, window=self.close_button)
    
    def load_video(self):
    # Вызываем диалоговое окно для выбора видеофайла
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        if file_path:
            # Отобразить видео в новом окне
            video_window = tk.Toplevel(self)
            video_label = tk.Label(video_window)
            video_label.pack()

            cap = cv2.VideoCapture(file_path)
            self.show_video(cap, video_label)

            # Создать кнопки управления видео: Включить, Стоп, Назад, Закрыть
            play_button = ttk.Button(video_window, text="Включить видео", command=lambda: self.show_video(cap, video_label, play_video=True))
            play_button.pack(pady=5)

            stop_button = ttk.Button(video_window, text="Стоп", command=lambda: cap.release())
            stop_button.pack(pady=5)

            back_button = ttk.Button(video_window, text="Назад", command=video_window.destroy)
            back_button.pack(pady=5)

            close_button = ttk.Button(video_window, text="Закрыть", command=self.master.destroy)
            close_button.pack(pady=5)

            # Кнопка Включить видео
            resume_button = ttk.Button(video_window, text="Включить видео", command=lambda: self.show_video(cap, video_label, play_video=True))
            resume_button.pack(pady=5)

    
    def show_video(self, cap, video_label, play_video=False):
        ret, frame = cap.read()
        if ret and (play_video or self.playing_video):  # Добавим проверку на флаг воспроизведения видео
            self.playing_video = True
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)
            video_label.img = frame
            video_label.config(image=frame)
            video_label.after(10, lambda: self.show_video(cap, video_label, play_video=True))


    
    def enable_webcam(self):
        # Переходим к странице с видеопотоком с вебкамеры
        self.pack_forget()
        webcam_page = WebcamPage(self.master, self)
        webcam_page.pack(expand=True, fill='both')
        webcam_page.out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

    
    def back_to_first_page(self):
        # Скрыть текущую страницу и вернуться к первой странице
        self.pack_forget()
        self.first_page.pack(expand=True, fill='both')

class FirstPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Создаем Canvas для отображения изображения и элементов GUI
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(expand=True, fill='both')
        
        # Загрузка изображения фона и создание объекта PhotoImage
        background_image = Image.open("logo.jpg")  # Подставьте путь к вашему изображению фона
        self.background_photo = ImageTk.PhotoImage(background_image)
        
        # Отображение фона в Canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)
        
        # Создание кнопки "Начать"
        self.start_button = ttk.Button(self, text="Начать", command=self.show_second_page)
        self.canvas.create_window(250, 300, window=self.start_button)
        
        # Создание кнопки "Закрыть"
        self.close_button = ttk.Button(self, text="Закрыть", command=self.master.destroy)
        self.canvas.create_window(350, 300, window=self.close_button)
    
    def show_second_page(self):
        # Скрыть текущую страницу и отобразить вторую страницу с переданным фоновым изображением и ссылкой на первую страницу
        self.pack_forget()
        second_page = SecondPage(self.master, self, self.background_photo)
        second_page.pack(expand=True, fill='both')

def main():
    root = tk.Tk()
    root.title("Первая страница")
    
    # Отображаем первую страницу
    first_page = FirstPage(root)
    first_page.pack(expand=True, fill='both')
    
    root.mainloop()

if __name__ == "__main__":
    main()
