import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import json
import subprocess


class Notepad:
    FONTS = ('Georgia', 'Palatino', 'Linotype', 'Times', 'Times New Roman', 'Arial', 'Geneva', 'Helvetica', 'Impact',
            'Lucida Grande', 'Lucida Sans', 'Tahoma', 'Trebuchet MS', 'Verdana', 'Monaco', 'Lucida Console', 'Courier',
            'New Courier')

    files = (('All files', '*.txt, *.py'), ('Text Document', '.txt'), ('Python', '.py'))
    file = '\\Note.txt'

    with open('src/settings.json', 'r') as settingsFile:
        data = settingsFile.read()

    data = json.loads(data)

    defaultDir = data["DefaultDir"]
    FONT = data["Font"], data["FontSize"]
    color = data["FontColor"]

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Notebook')
        self.root.iconbitmap('src/Icons/notes.ico')
        self.root.configure(background='#0C0C0C')

        self.resizeTextArea()

        self.textArea = tkinter.Text(self.root, bg='#141414', fg=self.color, width=self.WIDTH, height=self.HEIGHT,
                                     font=self.FONT)
        self.textArea.grid(row=0, columnspan=3, padx=25, pady=20)

        self.saveButton = tkinter.Button(self.root, text='Save', cursor='hand2', bg='#141414', fg='white',
                                         width=15, command=self.save)
        self.saveButton.grid(row=1, column=0, pady=15)

        self.settingsButton = tkinter.Button(self.root, text='Settings', cursor='hand2', bg='#141414', fg='white',
                                             width=15, command=self.settings)
        self.settingsButton.grid(row=1, column=1, pady=15)

        self.loadButton = tkinter.Button(self.root, text='Load', cursor='hand2', bg='#141414', fg='white', width=15,
                                         command=self.loadData)
        self.loadButton.grid(row=1, column=2, pady=15)

        playImg = tkinter.PhotoImage(master=self.root, file='src/Pictures/play.png')
        self.runButton = tkinter.Button(self.root, image=playImg, bg='#141414', cursor='hand2', width=50,
                                        command=self.runCode)
        self.runButton.grid(row=2, column=1, pady=15)

        self.root.resizable(width=False, height=False)
        self.root.mainloop()

    def resizeTextArea(self):
        if int(self.data["FontSize"]) >= 16 and int(self.data["FontSize"]) < 30:
            self.HEIGHT = int(int(self.data["FontSize"]) // 2)
            self.WIDTH = int(int(self.data["FontSize"]) ** 1.2)
        elif int(self.data["FontSize"]) >= 30 and int(self.data["FontSize"]) < 50:
            self.HEIGHT = int(int(self.data["FontSize"]) // 5)
            self.WIDTH = int(int(self.data["FontSize"]) ** 0.8)
        elif int(self.data["FontSize"]) >= 50 and int(self.data["FontSize"]) < 75:
            self.HEIGHT = int(int(self.data["FontSize"]) // 8)
            self.WIDTH = int(int(self.data["FontSize"]) ** 0.8)
        elif int(self.data["FontSize"]) >= 75 and int(self.data["FontSize"]) < 100:
            self.HEIGHT = int(int(self.data["FontSize"]) // 22.5)
            self.WIDTH = int(int(self.data["FontSize"]) ** 0.6)
        elif int(self.data["FontSize"]) >= 100:
            self.HEIGHT = int(int(self.data["FontSize"]) // 60)
            self.WIDTH = int(int(self.data["FontSize"]) // 20)
        else:
            self.HEIGHT = 30
            self.WIDTH = 100

    def save(self):
        text = self.textArea.get('1.0', 'end')

        if text.replace('\n', '') == '':
            self.textArea.insert('end', 'Enter some text before save!')
            return

        file = filedialog.asksaveasfile(initialfile=self.file.replace('\\', '/').split('/')[-1],
                                        title="Save file",
                                        initialdir=self.defaultDir,
                                        filetypes=self.files)

        self.file = file.name
        file.write(text)

        del file

    def loadData(self):
        file = filedialog.askopenfile(title='Open file',
                                      initialdir=self.defaultDir,
                                      initialfile=self.file.replace('\\', '/').split('/')[-1],
                                      filetypes=self.files)

        text = file.read()

        self.textArea.delete("1.0", "end")
        self.textArea.insert('1.0', str(text))

        self.file = file.name

        del file

    def settings(self):
        self.settingsWin = tkinter.Tk()
        self.settingsWin.title('Settings')
        self.settingsWin.iconbitmap('src/Icons/setting.ico')
        self.settingsWin.configure(background='#0C0C0C')

        changeImg = tkinter.PhotoImage(master=self.settingsWin, file='src/Pictures/change.png')
        colorPalettImg = tkinter.PhotoImage(master=self.settingsWin, file='src/Pictures/color-palette.png')

        defaultDirecLabel = tkinter.Label(self.settingsWin, text=f'Default directory: {self.defaultDir}', bg='#141414', fg='white')
        defaultDirecLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        changeDefaultDirec = tkinter.Button(self.settingsWin, cursor='hand2', image=changeImg, width=20, height=20, bg='#141414', command=self.changeDefaultDir)
        changeDefaultDirec.grid(row=0, column=3, padx=20, pady=10)

        defaultFontSizeLabel = tkinter.Label(self.settingsWin, text='Font-size:', bg='#141414', fg='white')
        defaultFontSizeLabel.grid(row=1, column=0, columnspan=2, pady=10)

        self.fontSizeChooser = tkinter.Spinbox(self.settingsWin, cursor='hand2', from_=1, to=100, width=5)
        self.fontSizeChooser.grid(row=1, column=3, pady=10)

        defaultFontLabel = tkinter.Label(self.settingsWin, text="Font:", bg='#141414', fg='white')
        defaultFontLabel.grid(row=2, column=0, columnspan=2, pady=10)

        self.fontChooser = ttk.Combobox(self.settingsWin, values=self.FONTS, width=10)
        self.fontChooser.grid(row=2, column=3, pady=10, padx=10)

        chooseFontColorLabel = tkinter.Label(self.settingsWin, text='Choose color: ', bg='#141414', fg='white')
        chooseFontColorLabel.grid(row=3, column=0, columnspan=2, pady=10)

        chooseFontColorButton = tkinter.Button(self.settingsWin, image=colorPalettImg, cursor='hand2', width=20, height=20, bg='#141414', command=self.chooseFontColor)
        chooseFontColorButton.grid(row=3, column=3, pady=10, padx=10)

        saveButton = tkinter.Button(self.settingsWin, text='Save', bg='#141414', fg='white', width=20, command=self.saveSettings)
        saveButton.grid(row=4, column=0, columnspan=4, pady=20)
        
        self.settingsWin.mainloop()

    def chooseFontColor(self):
        color = colorchooser.askcolor(color='#000000')
        color = color[1]

        location = self.data["DefaultDir"]
        font = self.data["Font"]
        fontsize = self.data["FontSize"]

        self.data = {}
        self.data["DefaultDir"] = location
        self.data["Font"] = font
        self.data["FontSize"] = fontsize
        self.data["FontColor"] = color

        with open('src/settings.json', 'w') as file:
            json.dump(self.data, file, indent=4)

        self.defaultDir = location
        self.FONT = font, fontsize
        self.color = color

        self.textArea.configure(fg=color)

        self.settingsWin.destroy()

    def changeDefaultDir(self):
        location = filedialog.askdirectory(initialdir='C:', title="Select default dir")
        self.data = {}
        self.data["DefaultDir"] = location

        with open('src/settings.json', 'w') as file:
            json.dump(self.data, file, indent=4)

        self.defaultDir = self.data["DefaultDir"]

    def saveSettings(self):
        fontsize = int(self.fontSizeChooser.get())
        print("Font-size: " + str(fontsize))

        font = self.fontChooser.get()
        if font == '':
            font = 'Arial'
        print("Font: " + font)

        location = self.data["DefaultDir"]
        self.data = {}
        self.data["DefaultDir"] = location
        self.data["Font"] = font
        self.data["FontSize"] = fontsize

        with open('src/settings.json', 'w') as file:
            json.dump(self.data, file, indent=4)

        self.defaultDir = location
        self.FONT = font, fontsize

        self.resizeTextArea()
        self.textArea.configure(width=self.WIDTH, height=self.HEIGHT, font=self.FONT)

        self.settingsWin.destroy()

    def runCode(self):
        code = self.textArea.get('1.0', 'end')
        if code.replace('\n', '') == '':
            messagebox.showerror("Terminal", "You have to enter some text before run!")
            return
        if self.file == '':
            messagebox.showerror("Safe file before run", "You have to save the file before run!")
            return

        command = f"python {self.file}"

        terminal = tkinter.Tk()
        terminal.title("Terminal")
        terminal.iconbitmap('src/Icons/terminal.ico')
        terminal.configure(background='#0C0C0C')

        codeArea = tkinter.Text(terminal, font=self.FONT, bg='#141414', fg=self.color, width=100, height=30)
        codeArea.pack(pady=15, padx=15)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        codeArea.insert('1.0', output)
        codeArea.insert('1.0', error)

        terminal.mainloop()


if __name__ == '__main__':
    Notepad()
