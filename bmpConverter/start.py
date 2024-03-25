import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image
from imageHandler import ImageHandler

class ImageApp:
    def __init__(self):
        self.imageHandler = ImageHandler(self)
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.plus_pressed = False
        self.minus_pressed = False
        self.delete_pressed = False
               
        # Create the main window
        self.root = tk.Tk()
        self.root.title("BMP Converter")
        self.root.geometry("1000x480")
        self.root.minsize(1000, 480)
        self.root.after(20, self.update)  # Call update every 100 ms
        self.root.grid_rowconfigure(0, minsize=480)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, minsize=800)
        self.root.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())
        self.root.unbind_class("Button", "<Key-space>")
        self.root.bind_class("Listbox", "<Key-Return>",  lambda event: event.widget.event_generate("<<ListboxSelect>>"))
        # self.root.bind_class("Listbox", "<Key-Return>", self.on_enter)
        # self.root.unbind_class("Listbox", "<Key-space>")

        # Create a frame to hold the buttons
        self.left_frame = tk.Frame(self.root)
        # Configure the rows
        for i in range(6):
            self.left_frame.grid_rowconfigure(i, weight=1)


        # Configure the columns
        for i in range(2):
            self.left_frame.grid_columnconfigure(i, weight=1)
            

        self.left_frame.grid(row=0, column=0)

        # Create the left buttons and lists inside the frame
        buttonLoading = tk.Button(self.left_frame, text="Bilder Laden", command=self.imageHandler.loadImages, width= 14)
        buttonLoading.grid(row=0, column=0, sticky="nsew")
        buttonExport = tk.Button(self.left_frame, text="Bilder Exportieren", command=self.imageHandler.exportImages, width= 14)
        buttonExport.grid(row=0, column=1, sticky="nsew")
        self.listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, height =18)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # self.listbox.bind('<Return>', self.on_selection_change)
        self.listbox.bind('<<ListboxSelect>>', self.on_selection_change)

        buttonDelete = tk.Button(self.left_frame, text="Löschen" ,command=self.imageHandler.deleteImage)
        buttonDelete.grid(row=2, column=0, sticky="nsew")
        buttonDeleteAll = tk.Button(self.left_frame, text="Alles Löschen" ,command=self.imageHandler.deleteAllImages)
        buttonDeleteAll.grid(row=2, column=1, sticky="nsew")
        buttonMinus = tk.Button(self.left_frame, text="-", command=lambda :self.imageHandler.changeScale(-.1))

        buttonMinus.grid(row=3, column=0, sticky="nsew")
        buttonPlus = tk.Button(self.left_frame, text="+", command=lambda :self.imageHandler.changeScale(.1))
        buttonPlus.grid(row=3, column=1, sticky="nsew")
        buttonRotateLeft = tk.Button(self.left_frame, text="⟲", command=lambda :self.imageHandler.rotateImage(90))
        buttonRotateLeft.grid(row=4, column=0, sticky="nsew")
        buttonRotateRight = tk.Button(self.left_frame, text="⟳", command=lambda :self.imageHandler.rotateImage(-90))
        buttonRotateRight.grid(row=4, column=1, sticky="nsew")


        # Create a frame to hold the arrows
        self.arrow_frame = tk.Frame(self.left_frame)
        # configure the rows
        for i in range(3):
            self.arrow_frame.grid_rowconfigure(i, weight=1)

        # Configure the columns
        for i in range(3):
            self.arrow_frame.grid_columnconfigure(i, weight=1)
        
        # Place the frame inside the left frame
        self.arrow_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        # Create the arrows inside the frame
        buttonTop = tk.Button(self.arrow_frame, text="↑", command= lambda :self.imageHandler.changeOffset(0,-5))
        buttonTop.grid(row=0, column=1, sticky="nsew")
        buttonLeft = tk.Button(self.arrow_frame, text="←", command= lambda :self.imageHandler.changeOffset(-5,0))
        buttonLeft.grid(row=1, column=0, sticky="nsew")
        buttonRight = tk.Button(self.arrow_frame, text="→", command= lambda :self.imageHandler.changeOffset(5,0))
        buttonRight.grid(row=1, column=2, sticky="nsew")
        buttonBottom = tk.Button(self.arrow_frame, text="↓", command= lambda :self.imageHandler.changeOffset(0,5))
        buttonBottom.grid(row=2, column=1, sticky="nsew")
        buttonReset = tk.Button(self.arrow_frame, text="Reset", command= lambda :self.imageHandler.resetImage(self.imageHandler.imageSelected))
        buttonReset.grid(row=1, column=1, sticky="nsew")

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1)

        self.canvas = Canvas(
            self.right_frame,
            width=800,
            height=480
        )
        self.canvas.pack()
        self.canvas.bind('<KeyPress>', self.key_press)
        self.canvas.bind('<KeyRelease>', self.key_release)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.focus_set()

    def on_selection_change(self, event):
        selection = event.widget.curselection()
        if selection:
            self.imageHandler.imageSelected = selection[0]
            self.imageHandler.canvasImage(self.imageHandler.imageSelected)

    def canvas_click(self, event):
        self.canvas.focus_set()

    def run(self):
        self.root.mainloop()
    
    def key_press(self, event):
        print(event.keysym)
        if event.keysym == 'Up':
            self.up_pressed = True
        elif event.keysym == 'Down':
            self.down_pressed = True
        elif event.keysym == 'Left':
            self.left_pressed = True
        elif event.keysym == 'Right':
            self.right_pressed = True
        elif event.keysym == 'plus':
            self.plus_pressed = True
        elif event.keysym == 'minus':
            self.minus_pressed = True
        elif event.keysym == 'Delete':
            self.delete_pressed = True

    def key_release(self, event):
        # print(event.keysym)
        if event.keysym == 'Up':
            self.up_pressed = False
        elif event.keysym == 'Down':
            self.down_pressed = False
        elif event.keysym == 'Left':
            self.left_pressed = False
        elif event.keysym == 'Right':
            self.right_pressed = False
        elif event.keysym == 'plus':
            self.plus_pressed = False
        elif event.keysym == 'minus':
            self.minus_pressed = False
        elif event.keysym == 'Delete':
            self.delete_pressed = False

    def update(self):
        # print("update")
        if self.up_pressed:
            self.imageHandler.changeOffset(0, -1)
        if self.down_pressed:
            self.imageHandler.changeOffset(0, 1)
        if self.left_pressed:
            self.imageHandler.changeOffset(-1, 0)
        if self.right_pressed:
            self.imageHandler.changeOffset(1, 0)
        if self.plus_pressed:
            self.imageHandler.changeScale(.1)
        if self.minus_pressed:
            self.imageHandler.changeScale(-.1)
        if self.delete_pressed:
            self.imageHandler.deleteImage()
        self.root.after(100, self.update)  # Call update every 100 ms

if __name__ == "__main__":
    app = ImageApp()
    app.run()