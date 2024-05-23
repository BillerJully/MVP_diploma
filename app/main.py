import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class SecondPage(tk.Frame):
    def __init__(self, master, first_page, background_image, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.first_page = first_page
        
        # Создаем Canvas для отображения элементов GUI
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(expand=True, fill='both')
        
        # Отображаем фоновое изображение
        self.background_image = background_image
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
            # Действие при выборе файла
            print(f"Выбран видеофайл: {file_path}")
    
    def enable_webcam(self):
        # Здесь вы можете определить действие при нажатии кнопки "Включить вебкамеру"
        pass
    
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
