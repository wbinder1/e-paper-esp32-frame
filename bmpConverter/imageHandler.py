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
            ('Images', '*.jpeg'),
            ('Images', '*.png')
        )

        newFileNames = fd.askopenfilenames(
            title='Open image Files',
            initialdir='/',
            filetypes=filetypes)

        if len(newFileNames) == 0:
            return

        # Initialize self.fileNames if it doesn't exist
        if len(self.fileNames) == 0:
            self.fileNames = newFileNames
        else:
            # Append new files to the existing list
            self.fileNames.extend(newFileNames)

        index = len(self.fileNames) - len(newFileNames)
        # Put the fileNames into a scrollable listbox
        for filename in newFileNames:
            self.initImage(index)  # Use the last index
            self.main.listbox.insert(tk.END, filename.split('/')[-1])
            index += 1
        self.imageSelected = 0
        self.main.listbox.selection_set(0)
        self.canvasImage(0)

    def exportImages(self):
        print("Exporting Images")
        if(len(self.fileNames) == 0):
            messagebox.showinfo("Error", "Es wurden keine Bilder geladen.", parent=self.main.root)
            return

        # Create a file dialog
        filename = fd.asksaveasfilename(
            title="Save images as BMP",
            initialdir="/",
            initialfile="this-file-name-doesnt-matter.bmp",  # Preset filename
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
                if img.mode == 'RGBA':
                    background = Image.new('RGBA', img.size, (255,255,255))
                    img = Image.alpha_composite(background, img)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                background = Image.new('RGB', (800, 480), (255, 255, 255))
                background.paste(img, (int(-self.fileSizes[i]["x_offset"]), int(-self.fileSizes[i]["y_offset"])))
                path = '/'.join(filename.split('/')[:-1]) + "/" + self.fileNames[i].split('/')[-1].split('.')[0] + ".bmp"
                # Save the image as BMP
                background.save(path)
                print(path)
        else:
            return

        # When the export is done, show a message box
        messagebox.showinfo("Export fertig", "Bilder wurden Erfolgreich Exportiert.", parent=self.main.root)
        # self.main.root.destroy()  # This will close the message box and the root window
    def deleteImage(self):
        if(self.imageSelected == None):
            return
        self.main.listbox.delete(self.imageSelected)
        self.fileNames = list(self.fileNames)
        self.fileNames.pop(self.imageSelected)
        self.fileNames = tuple(self.fileNames)
        self.fileSizes.pop(self.imageSelected)
        if(len(self.fileNames) == 0):
            self.imageSelected = None
            self.main.canvas.delete("all")
            return
        if(self.imageSelected >= len(self.fileNames)):
            self.imageSelected = len(self.fileNames) - 1
        else:
            self.imageSelected = 0
        self.main.listbox.selection_set(self.imageSelected)
        self.canvasImage(self.imageSelected)
    def deleteAllImages(self):
        self.main.listbox.delete(0, tk.END)
        self.fileNames = []
        self.fileSizes = []
        self.imageSelected = None
        self.main.canvas.delete("all")

    def initImage(self, index):
        self.fileSizes.append({'x': 0, 'y': 0, 'x_offset' : 0, 'y_offset' : 0, 'rotate' : 0, 'scale' : 1})
        self.setImageSize(index)

    def resetImage(self, index):
        self.fileSizes[index]["x_offset"] = 0
        self.fileSizes[index]["y_offset"] = 0
        self.fileSizes[index]["scale"] = 1
        self.fileSizes[index]["rotate"] = 0
        self.setImageSize(index)
        self.canvasImage(index)

    def setImageSize(self, index):
        img = Image.open(self.fileNames[index])
        x_offset = 0
        y_offset = 0

        if(self.fileSizes[index]["rotate"]%180 != 0):            
            aspect_ratio = img.width / img.height
            new_height = 800
            new_width = round(new_height * aspect_ratio)
            if new_width < 480:
                new_width = 480
                new_height = round(new_width / aspect_ratio)
                x_offset = (new_height - 800) / 2
            else:
                y_offset = (new_width - 480) / 2
        else:
            aspect_ratio = img.width / img.height

            new_width = 800
            new_height = round(new_width / aspect_ratio)
        
            if new_height < 480:
                new_height = 480
                new_width = round(new_height * aspect_ratio)
                x_offset = (new_width - 800) / 2
            else:
                y_offset = (new_height - 480) / 2

        self.fileSizes[index]["x"] = new_width
        self.fileSizes[index]["y"] = new_height
        self.fileSizes[index]["x_offset"] = x_offset
        self.fileSizes[index]["y_offset"] = y_offset

    def getAdaptedImage(self,index):
        img = Image.open(self.fileNames[index])
        img = img.resize((int(self.fileSizes[index]["x"] * self.fileSizes[index]["scale"]), int(self.fileSizes[index]["y"] * self.fileSizes[index]["scale"])))        
        img = img.rotate(self.fileSizes[index]["rotate"], expand = True)

        return img
    def rotateImage(self, angle):
        if(self.imageSelected == None):
            return
        self.fileSizes[self.imageSelected]["rotate"] += angle
        self.fileSizes[self.imageSelected]["scale"] = 1
        self.setImageSize(self.imageSelected)
        self.canvasImage(self.imageSelected)
    def changeOffset(self, x, y):
        if(self.imageSelected == None):
            return
        self.fileSizes[self.imageSelected]["x_offset"] += x
        self.fileSizes[self.imageSelected]["y_offset"] += y
        self.canvasImage(self.imageSelected)

    def changeScale(self, value):
        if(self.imageSelected == None):
            return
        new_scale = self.fileSizes[self.imageSelected]["scale"] + value
        if new_scale <= 0.05:
            return
        print(new_scale)
        self.fileSizes[self.imageSelected]["scale"] = new_scale
        self.fileSizes[self.imageSelected]["x_offset"] += self.fileSizes[self.imageSelected]["x"]/2 * value
        self.fileSizes[self.imageSelected]["y_offset"] += self.fileSizes[self.imageSelected]["y"]/2 * value
        # self.setImageSize(self.imageSelected)
        self.canvasImage(self.imageSelected)

    def canvasImage(self, index):
        img = self.getAdaptedImage(index)
        photo = ImageTk.PhotoImage(img)


        self.main.canvas.image = photo
        self.main.canvas.create_image(
            0 - self.fileSizes[index]["x_offset"] + self.main.offsetFrameX,
            0 - self.fileSizes[index]["y_offset"] + self.main.offsetFrameY,
            image=self.main.canvas.image,
            anchor=tk.NW)
        
        x2 = self.main.offsetFrameX + 800
        y2 = self.main.offsetFrameY + 480

        # Draw a red rectangle on the canvas
        self.main.canvas.create_rectangle(self.main.offsetFrameX, self.main.offsetFrameY, x2, y2, outline='red', width=2, dash=(3,5) ) 
