import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image
from imageHandler import ImageHandler
from tkcalendar import DateEntry

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
        self.dot_pressed = False
        self.comma_pressed = False
        self.outerFrameX = 900
        self.outerFrameY = 580
               
        # Create the main window
        self.root = tk.Tk()
        self.root.configure(bg='#FFFDEE')  # Set the background color
        self.root.title("BMP Converter")
        self.root.geometry("1000x650")
        self.root.minsize(300 + self.outerFrameX, self.outerFrameY)
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
        self.left_frame = tk.Frame(self.root, bg='#FFFDEE')  # Set the background color
        # Configure the rows
        for i in range(8):
            self.left_frame.grid_rowconfigure(i, weight=1)


        # Configure the columns
        for i in range(2):
            self.left_frame.grid_columnconfigure(i, weight=1)
            

        self.left_frame.grid(row=0, column=0)

        # Create the left buttons and lists inside the frame
        buttonLoading = tk.Button(self.left_frame, text="Bilder Laden", command=self.imageHandler.loadImages, width= 14, bg='#8fc9e8')
        buttonLoading.grid(row=0, column=0, sticky="nsew")
        buttonExport = tk.Button(self.left_frame, text="Bilder Exportieren", command=self.imageHandler.exportImages, width= 14, bg='#8fc9e8')
        buttonExport.grid(row=0, column=1, sticky="nsew")
        self.listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, height =18)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # self.listbox.bind('<Return>', self.on_selection_change)
        self.listbox.bind('<<ListboxSelect>>', self.on_selection_change)

        buttonDelete = tk.Button(self.left_frame, text="Löschen" ,command=self.imageHandler.deleteImage, bg='#8fc9e8')
        buttonDelete.grid(row=2, column=0, sticky="nsew")
        buttonDeleteAll = tk.Button(self.left_frame, text="Alles Löschen" ,command=self.imageHandler.deleteAllImages, bg='#8fc9e8')
        buttonDeleteAll.grid(row=2, column=1, sticky="nsew")
        buttonMinus = tk.Button(self.left_frame, text="-", command=lambda :self.imageHandler.changeScale(-.1), bg='#8fc9e8')

        buttonMinus.grid(row=3, column=0, sticky="nsew")
        buttonPlus = tk.Button(self.left_frame, text="+", command=lambda :self.imageHandler.changeScale(.1), bg='#8fc9e8')
        buttonPlus.grid(row=3, column=1, sticky="nsew")
        buttonRotateLeft = tk.Button(self.left_frame, text="⟲", command=lambda :self.imageHandler.rotateImage(90), bg='#8fc9e8')
        buttonRotateLeft.grid(row=4, column=0, sticky="nsew")
        buttonRotateRight = tk.Button(self.left_frame, text="⟳", command=lambda :self.imageHandler.rotateImage(-90), bg='#8fc9e8')
        buttonRotateRight.grid(row=4, column=1, sticky="nsew")
        # Create a DateEntry widget for the date input
        self.date_entry = DateEntry(self.left_frame, date_pattern='dd.mm.yyyy', bg='#8fc9e8')
        self.date_entry.delete(0, 'end')
        self.date_entry.grid(row=7, column=0, sticky="nsew")  # Place it at the bottom
        self.date_entry.bind("<<DateEntrySelected>>", self.imageHandler.setImageDate)

        # Create a Button widget for changing the date
        self.change_date_button = tk.Button(self.left_frame, text="Reset", command=lambda :self.imageHandler.deleteImageDate(), bg='#8fc9e8')
        self.change_date_button.grid(row=7, column=1, sticky="nsew")  # Place it at the bottom
        # Create a DateEntry widget for the Offset input
        self.offset_date_entry = DateEntry(self.left_frame, date_pattern='dd.mm.yyyy', bg='#8fc9e8')
        self.offset_date_entry.grid(row=8, column=0, sticky="nsew")  # Place it at the bottom
        # Create a Button widget for changing the Offset
        self.offset_change_date_button = tk.Button(self.left_frame, text="Bilder Fangen an am", command=self.change_date, bg='#8fc9e8')
        self.offset_change_date_button.grid(row=8, column=1, sticky="nsew")  # Place it at the bottom
        # Create a Button widget for changing the date



        # Create a frame to hold the arrows
        self.arrow_frame = tk.Frame(self.left_frame, bg='#FFFDEE')
        # configure the rows
        for i in range(3):
            self.arrow_frame.grid_rowconfigure(i, weight=1)

        # Configure the columns
        for i in range(3):
            self.arrow_frame.grid_columnconfigure(i, weight=1)
        
        # Place the frame inside the left frame
        self.arrow_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        # Create a slider with a range of 1-10
        self.slider = tk.Scale(self.arrow_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg='#8fc9e8')
        self.slider.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.label = tk.Label(self.arrow_frame, text="Pixel Bewegungsdistanz", bg='#8fc9e8')
        self.label.grid(row=4, column=0, columnspan=3, sticky="nsew")

        # Create the arrows inside the frame
        buttonTop = tk.Button(self.arrow_frame, text="↑", command= lambda :self.imageHandler.changeOffset(0, -self.slider.get()), bg='#8fc9e8')
        buttonTop.grid(row=0, column=1, sticky="nsew")
        buttonLeft = tk.Button(self.arrow_frame, text="←", command= lambda :self.imageHandler.changeOffset(-self.slider.get(), 0), bg='#8fc9e8')
        buttonLeft.grid(row=1, column=0, sticky="nsew")
        buttonRight = tk.Button(self.arrow_frame, text="→", command= lambda :self.imageHandler.changeOffset(self.slider.get(), 0), bg='#8fc9e8')
        buttonRight.grid(row=1, column=2, sticky="nsew")
        buttonBottom = tk.Button(self.arrow_frame, text="↓", command= lambda :self.imageHandler.changeOffset(0, self.slider.get()), bg='#8fc9e8')
        buttonBottom.grid(row=2, column=1, sticky="nsew")
        buttonReset = tk.Button(self.arrow_frame, text="Reset", command= lambda :self.imageHandler.resetImage(self.imageHandler.imageSelected), bg='#8fc9e8')
        buttonReset.grid(row=1, column=1, sticky="nsew")


        # Create a frame to hold the canvas
        self.right_frame = tk.Frame(self.root, bg='#8fc9e8')  # Set the background color
        self.right_frame.grid(row=0, column=1)

        self.canvas = Canvas(
            self.right_frame,
            width=self.outerFrameX,  # Change the width to 1200
            height=self.outerFrameY,   # Change the height to 840
            bg='#8fc9e8'
        )
        self.canvas.pack()

        # Calculate the coordinates for the rectangle
        self.offsetFrameX = (self.outerFrameX - 800) / 2
        self.offsetFrameY = (self.outerFrameY - 480) / 2
        

        self.canvas.bind('<KeyPress>', self.key_press)
        self.canvas.bind('<KeyRelease>', self.key_release)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.focus_set()

    def on_selection_change(self, event):
        selection = event.widget.curselection()
        if selection:
            self.imageHandler.imageSelected = selection[0]
            self.imageHandler.canvasImage(self.imageHandler.imageSelected)

    def change_date(self):
        # Get the date from the Entry widget
        date = self.date_entry.get()

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
        elif event.keysym == 'period':
            self.dot_pressed = True
        elif event.keysym == 'comma':
            self.comma_pressed = True


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
        elif event.keysym == 'period':
            self.dot_pressed = False
        elif event.keysym == 'comma':
            self.comma_pressed = False
        

    def update(self):
        # Get the current value of the slider
        offset_value = self.slider.get()

        if self.up_pressed:
            self.imageHandler.changeOffset(0, -offset_value)
        if self.down_pressed:
            self.imageHandler.changeOffset(0, offset_value)
        if self.left_pressed:
            self.imageHandler.changeOffset(-offset_value, 0)
        if self.right_pressed:
            self.imageHandler.changeOffset(offset_value, 0)
        if self.plus_pressed:
            self.imageHandler.changeScale(.1)
        if self.minus_pressed:
            self.imageHandler.changeScale(-.1)
        if self.delete_pressed:
            self.imageHandler.deleteImage()
        if self.dot_pressed:
            self.imageHandler.rotateImage(-90)
        if self.comma_pressed:
            self.imageHandler.rotateImage(90)
        self.root.after(100, self.update)  # Call update every 100 ms

if __name__ == "__main__":
    app = ImageApp()
    app.run()