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
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid(row=0, column=0)

        # Create two buttons inside the frame
        button1 = tk.Button(self.left_frame, text="Bilder Laden", command=self.imageHandler.loadImages)
        button1.place(relx=0.5, rely=0.5, anchor='center')
        button1.pack()

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