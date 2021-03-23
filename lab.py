import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fd
import tkinter.messagebox as mb

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        master.title("Отражатель")
        master.geometry("600x400")
        
        self.CreateWidgets()

        #Инициализация матрицы
        self.size1 = 0
        self.size2 = 0
        self.matrix = []

    def CreateWidgets(self):
        font = tkFont.Font(size=20)
        
        self.loadFileButton = tk.Button(root,
                                        text="Загрузить из файла",
                                        bg="Gold", fg="PaleGreen4",
                                        activebackground="Yellow",
                                        activeforeground="PaleGreen4",
                                        command=self.LoadFile)
        self.loadFileButton.pack(expand=True)
        self.loadFileButton.pack(fill="both")
        self.loadFileButton.pack(side="top")
        self.loadFileButton["font"] = font;

        self.writeFileButton = tk.Button(root,
                                         text="Записать в файл",
                                         bg="Gold",
                                         fg="PaleGreen4",
                                         activebackground="Yellow",
                                         activeforeground="PaleGreen4",
                                         command=self.WriteFile)
        self.writeFileButton.pack(expand=True)
        self.writeFileButton.pack(fill="both")
        self.writeFileButton.pack(side="top")
        self.writeFileButton["font"] = font;
        
        self.processButton = tk.Button(root,
                                       text="Зеркально отразить",
                                       bg="DarkOrange1",
                                       fg="PaleGreen4",
                                       activebackground="DarkOrange2",
                                       activeforeground="PaleGreen4",
                                       command=self.Process)
        self.processButton.pack(expand=True)
        self.processButton.pack(fill="both")
        self.processButton.pack(side="bottom")
        self.processButton["font"] = font;

        self.inputText = tk.Text(bd="5", width="30")
        self.inputText.pack(side="left")
        self.inputText.pack(expand=True)
        self.inputText.pack(fill="both")
        self.inputText.bind("<<Modified>>", self.ClearOutput)
        self.inputText.bind("<Key>", self.ClearOutput)

        self.outputText = tk.Text(bd="5", width="30", state="disabled")
        self.outputText.pack(side="right")
        self.outputText.pack(expand=True)
        self.outputText.pack(fill="both")

    def LoadFile(self):
        filename = fd.askopenfilename(title = "Выберите файл", filetypes = [("Файлы матриц","*.mtr")])
        if filename:
            #Очистка текстовых полей
            self.inputText.delete("1.0", "end")

            #Получение матрицы из файла
            file = open(filename, 'r')
            
            text = file.read()
            if self.ReadMatrix(text) and self.CheckMatrix():
                self.inputText.insert("1.0", text)
            else:
                self.size1 = 0
                self.size2 = 0
                self.matrix = []
            
            file.close()

    def WriteFile(self):
        text = self.outputText.get("1.0", "end").rstrip();
        
        if text:
            filename = fd.asksaveasfile(title = "Выберите или создайте файл",
                                    filetypes = [("Файлы матриц","*.mtr")],
                                    defaultextension = ".mtr")
        
            if filename:
                file = open(filename.name, 'w')
                file.write(text)
                file.close()
        else:
            mb.showerror(title = "Ошибка!", message = "Размер матрицы за пределами диапазона")

    def ReadMatrix(self, text):
        try:
            self.matrix = []
            if text:
                for x in text.split('\n'):
                    self.matrix.append(list(map(int, x.split(' '))))
        except ValueError:
            mb.showerror(title = "Ошибка!", message = "Формат файла не соответствует требуемому")
            return False

        self.size1 = len(self.matrix)
        if self.size1 == 0:
            self.size2 = 0
        else:
            self.size2 = len(self.matrix[0])

        return True

    def CheckMatrix(self):
        #Проверка размерности матрицы
        if self.size1 <= 0 or self.size1 > 10 or self.size2 <= 0 or self.size2 > 10:
            mb.showerror(title = "Ошибка!", message = "Размер матрицы за пределами диапазона")
            return False

        #Проверка равенства размеров строк матрицы
        for i in range(self.size1):
            if len(self.matrix[i]) != self.size2:
                mb.showerror(title = "Ошибка!", message = "Размер строк матрицы не равны")
                return False

        #Проверка элементов матрицы
        for i in range(self.size1):
            for j in range(self.size2):
                if self.matrix[i][j] < -2147483648 or self.matrix[i][j] > 2147483647:
                    mb.showerror(title = "Ошибка!", message = "Элемент матрицы за пределами диапазона")
                    return False

        return True

    def Process(self):
        #Чтение матрицы из текстового поля
        text = self.inputText.get("1.0", "end").rstrip()
        if not self.ReadMatrix(text) or not self.CheckMatrix():
            self.size1 = 0
            self.size2 = 0
            self.matrix = []
            return
            
        #Отражение матрицы
        for i in range(self.size1):
            for j in range(self.size2 - i):
                self.matrix[i][j], self.matrix[self.size2 - j - 1][self.size1 - i - 1] = self.matrix[self.size2 - j - 1][self.size1 - i - 1], self.matrix[i][j]

        #Преобразование матрицы в строку
        text = "\n".join([" ".join(str(elem) for elem in row) for row in self.matrix])
        
        #Вывод матрицы
        self.outputText["state"] = "normal"
        self.outputText.insert("1.0", text)
        self.outputText["state"] = "disabled"

    def ClearOutput(self, event):
        self.outputText["state"] = "normal"
        self.outputText.delete("1.0", "end")
        self.outputText["state"] = "disabled"
    

root = tk.Tk()
app = App(root)
app.mainloop()
