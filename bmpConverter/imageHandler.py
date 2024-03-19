import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image
from tkinter import Tk, messagebox

class ImageHandler:
    main = None
    imageSelected = None

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

        # Put the fileNames into a scrollable listbox
        index = 0
        for filename in self.fileNames:
            self.initImage(index)
            self.main.listbox.insert(tk.END, filename.split('/')[-1])
            index += 1
        self.main.listbox.bind('<<ListboxSelect>>', self.on_selection_change)
        self.imageSelected = 0
        self.main.listbox.selection_set(0)
        self.canvasImage(0)

    def exportImages(self):
        print("Exporting Images")

        # Create a file dialog
        filename = fd.asksaveasfilename(
            title="Save images as BMP",
            initialdir="/",
            filetypes=(("BMP files", "*.bmp"),)
        )

        # Check if a file was selected
        if filename:
            print (filename)
            # Loop over the selected images
            if len(self.fileNames) == 0:
                messagebox.showinfo("Error", "Es wurden keine Bilder geladen.", parent=self.main.root)
                return
            for i in range(len(self.fileNames)):
                # Open the image file
                img = self.getAdaptedImage(i)

                # Save the image as BMP
                img.save(self.fileNames[i].split('/')[-1].split('.')[0] + ".bmp")

                print("Exportiert", self.fileNames[i], "as", filename + str(i) + ".bmp")

        # When the export is done, show a message box
        messagebox.showinfo("Export fertig", "Bilder wurden Erfolgreich Exportiert.", parent=self.main.root)
        self.main.root.destroy()  # This will close the message box and the root window

    def on_selection_change(self, event):
        selection = event.widget.curselection()
        if selection:
            self.imageSelected = selection[0]
            self.canvasImage(self.imageSelected)

    def initImage(self, index):
        self.fileSizes.append({'x': 0, 'y': 0, 'rotate' : 0})
        self.setImageSize(index)

    def setImageSize(self, index):
        img = Image.open(self.fileNames[index])
        if(self.fileSizes[index]["rotate"]%180 != 0):            
            aspect_ratio = img.width / img.height
            new_height = 800
            new_width = round(new_height * aspect_ratio)
            if new_width < 480:
                new_width = 480
                new_height = round(new_width / aspect_ratio)
        else:
            aspect_ratio = img.width / img.height

            new_width = 800
            new_height = round(new_width / aspect_ratio)
            if new_height < 480:
                new_height = 480
                new_width = round(new_height * aspect_ratio)

        self.fileSizes[index]["x"] = new_width
        self.fileSizes[index]["y"] = new_height

    def getAdaptedImage(self,index):
        img = Image.open(self.fileNames[index])
        img = img.rotate(self.fileSizes[index]["rotate"])
        img = img.resize((self.fileSizes[index]["x"], self.fileSizes[index]["y"]))

        return img
    def rotateImage(self, angle):
        print(self.imageSelected)
        if(self.imageSelected == None):
            return
        self.fileSizes[self.imageSelected]["rotate"] += angle
        self.setImageSize(self.imageSelected)
        self.canvasImage(self.imageSelected)

    def canvasImage(self, index):
        img = self.getAdaptedImage(index)
        photo = ImageTk.PhotoImage(img)

        self.main.canvas.image = photo
        self.main.canvas.create_image(
            400,  # half of 800
            240,
            image=self.main.canvas.image,
            anchor='center'
        )
