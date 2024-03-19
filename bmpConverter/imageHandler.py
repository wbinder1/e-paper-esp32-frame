import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image

class ImageHandler:
    main = None

    def __init__(self, main):
        self.main = main
        self.fileNames = []
        self.fileSizes = []


    def loadImages(self):
        filetypes = (
            ('Images', '*.jpg'),
            ('Images', '*.png')
        )

        self.fileNames = fd.askopenfilenames(
            title='Open image Files',
            initialdir='/',
            filetypes=filetypes)
        
        if(len(self.fileNames) == 0):
            return
        
        # Clear the button frame
        for widget in self.main.left_frame.winfo_children():
            widget.destroy()

        # Put the fileNames into a scrollable listbox
        listbox = tk.Listbox(self.main.left_frame, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True)
        for filename in self.fileNames:
            self.setfileSize(filename)
            listbox.insert(tk.END, filename.split('/')[-1])
        listbox.bind('<<ListboxSelect>>', self.on_selection_change)
        listbox.selection_set(0)
        self.canvasImage(0)

    def on_selection_change(self, event):
        selection = event.widget.curselection()
        if selection:
            self.canvasImage(selection[0])

    def setfileSize(self, filepath):
        img = Image.open(filepath)
        aspect_ratio = img.width / img.height
        new_width = 800
        new_height = round(new_width / aspect_ratio)
        if new_height < 480:
            new_height = 480
            new_width = round(new_height * aspect_ratio)
        self.fileSizes.append({'x': new_width, 'y': new_height})

    def canvasImage(self, index):
        img = Image.open(self.fileNames[index])
        img_resized = img.resize((self.fileSizes[index]["x"], self.fileSizes[index]["y"]))
        photo = ImageTk.PhotoImage(img_resized)
        self.main.canvas.image = photo
        self.main.canvas.create_image(
            400,  # half of 800
            240,
            image=self.main.canvas.image,
            anchor='center'
        )

