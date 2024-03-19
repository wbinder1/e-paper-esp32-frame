import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image
from imageHandler import ImageHandler

class ImageApp:
    def __init__(self):
        self.imageHandler = ImageHandler(self)
               
        # Create the main window
        self.root = tk.Tk()
        self.root.title("BMP Converter")
        self.root.geometry("1000x480")
        self.root.minsize(1000, 480)
        self.root.grid_rowconfigure(0, minsize=480)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, minsize=800)

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
        buttonDelete = tk.Button(self.left_frame, text="Löschen"
                                #   ,command=self.deleteImage
                                 )
        buttonDelete.grid(row=2, column=0, columnspan=2, sticky="nsew")
        buttonMinus = tk.Button(self.left_frame, text="-"
                                #, command=self.decreaseSize
                                )

        buttonMinus.grid(row=3, column=0, sticky="nsew")
        buttonPlus = tk.Button(self.left_frame, text="+"
                               #, command=self.increaseSize
                               )
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
        buttonTop = tk.Button(self.arrow_frame, text="↑", command= lambda :self.imageHandler.changeOffset(0,-1))
        buttonTop.grid(row=0, column=1, sticky="nsew")
        buttonLeft = tk.Button(self.arrow_frame, text="←", command= lambda :self.imageHandler.changeOffset(-1,0))
        buttonLeft.grid(row=1, column=0, sticky="nsew")
        buttonRight = tk.Button(self.arrow_frame, text="→", command= lambda :self.imageHandler.changeOffset(1,0))
        buttonRight.grid(row=1, column=2, sticky="nsew")
        buttonBottom = tk.Button(self.arrow_frame, text="↓", command= lambda :self.imageHandler.changeOffset(0,1))
        buttonBottom.grid(row=2, column=1, sticky="nsew")

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1)

        self.canvas = Canvas(
            self.right_frame,
            width=800,
            height=480
        )
        self.canvas.pack()

        self.canvas.create_rectangle(0, 0, 800, 480, fill="grey")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageApp()
    app.run()