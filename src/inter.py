import os
import tkinter as tk

from PIL import ImageTk, Image
from idlelib.tooltip import Hovertip
from .file_worker import get_os_slash, change_name

class Interface:
    def __init__(self, min_width: int, min_height: int):
        self.slash = get_os_slash()
        self.root = tk.Tk()
        self.root.title("Hot Text Editor")
        path = os.getcwd() + self.slash + 'static' + self.slash + 'images' + self.slash + 'icon.ico'
        self.root.iconphoto(False, ImageTk.PhotoImage(Image.open(path)))
        self.root.minsize(width=min_width, height=min_height)
        self.text = tk.Text(self.root, height=min_height, width=min_height, wrap="word")
        self.FILE_NAME = change_name("Untitled")
        self.filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        self.window1 = None
        self.window2 = None

    def keypress(self, e: object):
        """
        Функиця позваоляет отслеживать нажатия горячих клавиш при русской раскладке
        """
        if e.keycode == 86 and e.keysym != 'v':
            text = self.text.selection_get(selection='CLIPBOARD')
            self.text.insert('insert', text)
        elif e.keycode == 67 and e.keysym != 'c':
            self.text.clipboard_clear()
            text = self.text.get("sel.first", "sel.last")
            self.text.clipboard_append(text)
        elif e.keycode == 88 and e.keysym != 'x':
            self.text.clipboard_clear()
            text = self.text.get("sel.first", "sel.last")
            self.text.clipboard_append(text)
            self.text.delete("sel.first", "sel.last")
        elif e.keycode == 83 and e.keysym != 's':
            self.save_file()
        elif e.keycode == 70 and e.keysym != 'f':
            self.find()
        elif e.keycode == 82 and e.keysym != 'r':
            self.change()
        elif e.keycode == 81 and e.keysym != 'q':
            self.on_closing()


    def menu(self):
        """
        Меню в редакторе
        """
        self.menuBar = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.menuBar)
        self.fileMenu.add_command(label="New", command=self.new_file)
        self.fileMenu.add_command(label="Open", command=self.open_file)
        self.fileMenu.add_command(label="Save", command=self.save_file)
        self.fileMenu.add_command(label="Save as", command=self.save_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_cascade(label="Exit", command=self.root.quit)

        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Info", command=self.info)

        self.root.config(menu=self.menuBar)


    def scroll_text(self):
        """
        Возможность скроллить текст в редакторе
        """
        self.scroll_y = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.text.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.text.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.text.configure(xscrollcommand=self.scroll_x.set)

    def new_file(self):
        """
        Создание нового файла
        """
        self.FILE_NAME = change_name("Untitled")
        self.text.delete('1.0', tk.END)

    def save_file(self, *args):
        """
        Сохранить файл (по умолчанию расширение txt)
        Файл сохраняется в корневой папке, если он был только создан
        """
        data = self.text.get('1.0', tk.END)
        out = open(self.FILE_NAME, 'w')
        out.write(data)
        out.close()

    def save_as(self):
        """
        Сохранить файл как
        """
        out = tk.filedialog.asksaveasfile(mode='w', defaultextension='txt', filetypes=self.filetypes)
        data = self.text.get('1.0', tk.END)
        try:
            out.write(data.rstrip())
        except Exception:
            tk.messagebox.showerror(title="Error", message="File wasn`t saved!")

    def open_file(self):
        """
        Открыть существующий файл
        """
        inp = tk.filedialog.askopenfile(mode="r", filetypes=self.filetypes)
        if inp is None:
            return
        self.FILE_NAME = inp.name
        data = inp.read()
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', data)

    def info(self):
        tk.messagebox.showinfo("Information", "This Sexy Text Redactor was made by one great programmer called Daler")

    def on_closing(self, *args):
        """
        Функция для проверки закрытия окна.
        Если в файле были внесены изменения, и он не был сохранен, то выйдет окно с предложением его сохранить
        """
        if not os.path.exists(self.FILE_NAME):
            if self.text.get(1.0, tk.END+"-1c") != "":
                if tk.messagebox.askokcancel("Quit", "Do you want to save file?"):
                    self.save_file()
                else:
                    self.root.quit()
        else:
            with open(self.FILE_NAME, "r") as f:
                text_f = f.read()
            if text_f[:-1] != self.text.get(1.0, tk.END+"-1c"):
                if tk.messagebox.askokcancel("Quit", "Do you want to save file?"):
                    self.save_file()
        self.root.quit()

    def start_parse(self):
        """
        Функция ищет и выделяет строку, которая была введена в форме в окне поиска, название поля из форы: entry_find
        Для поиска мы бежим по каждой строчке в виджете и с помощью встроенного метода find для строк мы ищем вхождение
        строки
        """
        self.text.tag_add('reset', 1.0, tk.END)
        self.text.tag_config('reset', foreground="black")
        what = self.window.entry_find.get()
        s = self.text.get(1.0, tk.END+"-1c")
        lines = s.split("\n")
        if s.find(what) == -1:
            tk.messagebox.showerror(title="Error", message="404, Nothing was found!")
        for line in lines:
            find_start = 0 # Счетчик, который позволяет искать вхождение подстроки, начиная с определенного индекса
            while line.find(what, find_start) != -1:
                tag = "f" + str(lines.index(line)) + str(line.find(what, find_start))
                self.text.tag_add(
                    tag,
                    # тут то, что стоит до '.' указывает tkinter на номер строки, а то, что стоит после '.'
                    # указывает на индекс подстроки в строке про это можно почитать в документации tkinter
                    float(str(lines.index(line) + 1)+ '.' + str(line.find(what, find_start))),
                    float(str(lines.index(line) + 1) + '.' + str(line.find(what, find_start) + len(what)))
                )
                self.text.tag_config(tag, foreground="blue")
                find_start = line.find(what, find_start) + len(what)

    def window_close(self):
        """
        Закрытие окна поиска
        Эта функция нужна, чтобы убрать выделение текста при закрытии окна
        """
        self.text.tag_add('all', 1.0, tk.END)
        self.text.tag_config('all', foreground="black")
        self.window.destroy()

    def find(self, *args):
        """
        Отрисовка окна поиска и формы поиска строки
        """
        self.window = tk.Toplevel()
        self.window.geometry('200x150')
        setattr(self.window, 'button', tk.Button(self.window, text="Find", command=self.start_parse))
        setattr(self.window, 'entry_find', tk.Entry(self.window))
        self.window.entry_find.pack()
        self.window.button.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)

    def window2_close(self):
        """
        Закрытие окна замены
        """
        self.window2.destroy()

    def start_replace(self):
        """
        Функция, которая проводит замену с помощью встроенных методов виждета Text() Tkinter-а
        """
        fr = self.window2.find.get()
        to = self.window2.change.get()
        new = self.text.get(1.0, tk.END).replace(fr, to)
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', new)

    def change(self, *args):
        """
        Отрисовка окна и формы замены строки
        """
        self.window2 = tk.Toplevel()
        self.window2.geometry('250x250')
        setattr(self.window2, 'button', tk.Button(self.window2, text="Replace", command=self.start_replace))
        setattr(self.window2, 'find', tk.Entry(self.window2))
        setattr(self.window2, 'change', tk.Entry(self.window2))
        setattr(self.window2, 'l1', tk.Label(text="find"))
        setattr(self.window2, 'l2', tk.Label(text="change to"))
        self.window2.l1.pack()
        self.window2.find.pack()
        self.window2.l2.pack()
        self.window2.change.pack()
        self.window2.button.pack()
        self.window2.protocol("WM_DELETE_WINDOW", self.window2_close)

    def run(self):
        """
        Функция запуска редактора
        """
        self.scroll_text()
        self.text.pack()
        self.menu()
        self.text.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-q>', self.on_closing)
        self.text.bind('<Control-f>', self.find)
        self.text.bind('<Control-r>', self.change)
        self.text.bind("<Control-KeyPress>", self.keypress)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()