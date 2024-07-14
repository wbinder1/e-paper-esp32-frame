import tkinter as tk
import random
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image
from tkinter import Tk, messagebox
from datetime import datetime, timedelta

class ImageHandler:
    main = None
    imageSelected = None

    def __init__(self, main):
        self.main = main
        self.fileNames = []
        self.fileData = []

    def loadImages(self):
        filetypes = (
            ('Images', '*.jpg'),
            ('Images', '*.jpeg'),
            ('Images', '*.png'),
            ('Images', '*.bmp')
        )

        newFileNames = fd.askopenfilenames(
            title='Open image Files',
            initialdir='/',
            filetypes=filetypes)

        if len(newFileNames) == 0:
            return

        # Initialize self.fileNames if it doesn't exist
        if not hasattr(self, 'fileNames') or not isinstance(self.fileNames, list):
            self.fileNames = list(self.fileNames) if hasattr(self, 'fileNames') else []

        # Append new files to the existing list
        self.fileNames.extend(newFileNames)

        index = len(self.fileNames) - len(newFileNames)
        # Put the fileNames into a scrollable listbox
        for filename in newFileNames:
            self.initImage(index, filename)  # Use the last index
            self.main.listbox.insert(tk.END, filename.split('/')[-1])
            index += 1
        self.imageSelected = 0
        self.main.listbox.selection_set(0)
        self.canvasImage(0)

    def setImageDate(self, event):
        print("Setting Image Date")
        if(self.imageSelected == None):
            print("No Image Selected")
            self.main.date_entry.delete(0, 'end')
            return
        for i in range(len(self.fileData)):
            if self.fileData[i]["date"] == self.main.date_entry.get():
                messagebox.showinfo("Error", "Datum bereits vergeben.", parent=self.main.root)
                return
            
        self.fileData[self.imageSelected]["date"] = self.main.date_entry.get()
        # self.main.change_date_button.focus_set()
        # Change the name of the listbox item so that it has the leading date
        self.main.listbox.delete(self.imageSelected)
        self.main.listbox.insert(self.imageSelected, self.fileData[self.imageSelected]["date"] + " - " + self.fileNames[self.imageSelected].split('/')[-1])
        self.main.listbox.selection_set(self.imageSelected)
        self.main.listbox.itemconfig(self.imageSelected, {'bg':'#66f4b9'})

        self.canvasImage(self.imageSelected)

        
    def deleteImageDate(self):
        print("Setting Image Date")
        if(self.imageSelected == None):
            print("No Image Selectdfgfdged")
            self.main.date_entry.delete(0, 'end')
            return
        self.fileData[self.imageSelected]["date"] = None
        self.main.listbox.delete(self.imageSelected)
        self.main.listbox.insert(self.imageSelected, self.fileNames[self.imageSelected].split('/')[-1])
        # select the new inserted item
        self.main.listbox.selection_set(self.imageSelected)
        self.main.listbox.itemconfig(self.imageSelected, {'bg':'white'})
        self.canvasImage(self.imageSelected)


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

            dateSelectedFiles = [data.copy() for data in self.fileData if data["date"] is not None]
            dateNotSelectedFiles = [data.copy() for data in self.fileData if data["date"] is None]	
            #Shuffle dateNotSelectedFiles randomly
            random.shuffle(dateNotSelectedFiles)
            
            offsetDate = self.main.offset_date_entry.get()
            offsetDate = datetime.strptime(offsetDate, '%d.%m.%Y')

            newFileData = []

            for i in range(len(self.fileNames)):
                dateFound = False
                for data in dateSelectedFiles:
                    if data["date"] == offsetDate.strftime('%d.%m.%Y'):
                        print("Found Date")
                        newFileData.append(data)
                        dateFound = True
                        #continue the outer for loop
                        break

                if not dateFound:
                    #Append the next date from dateNotSelectedFiles and put it in newFileData
                    if len(dateNotSelectedFiles) == 0:
                        break

                    dateNotSelectedFile = dateNotSelectedFiles.pop()
                    dateNotSelectedFile["date"] = offsetDate.strftime('%d.%m.%Y')
                    newFileData.append(dateNotSelectedFile)
                offsetDate += timedelta(days=1)

            for i in range(len(newFileData)):
                # Open the image file
                img = self.getAdaptedImage(newFileData[i])
                if img.mode == 'RGBA':
                    background = Image.new('RGBA', img.size, (255,255,255))
                    img = Image.alpha_composite(background, img)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                background = Image.new('RGB', (800, 480), (255, 255, 255))
                background.paste(img, (int(-newFileData[i]["x_offset"]), int(-newFileData[i]["y_offset"])))
                ascii_filename = newFileData[i]["filename"].split('/')[-1].split('.')[0]
                ascii_filename = ascii_filename.encode("ascii", errors="ignore").decode()
                path = '/'.join(filename.split('/')[:-1]) + "/" + str(i).zfill(3) + "_" + newFileData[i]["date"] + "_" + ascii_filename + ".bmp"
                # Save the image as BMP
                background.save(path)
                print(path)
        else:
            return
        
        #generate a info.txt file and write the current timestamp in it
        with open('/'.join(filename.split('/')[:-1]) + "/info.txt", 'w') as f:
            f.write(str(datetime.now()))

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
        self.fileData.pop(self.imageSelected)
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
        self.fileData = []
        self.imageSelected = None
        self.main.canvas.delete("all")

    def initImage(self, index, filename):
        self.fileData.append({'x': 0, 'y': 0, 'x_offset' : 0, 'y_offset' : 0, 'rotate' : 0, 'scale' : 1, 'date' : None, 'filename': filename})
        self.setImageSize(index)

    def resetImage(self, index):
        self.fileData[index]["x_offset"] = 0
        self.fileData[index]["y_offset"] = 0
        self.fileData[index]["scale"] = 1
        self.fileData[index]["rotate"] = 0
        self.setImageSize(index)
        self.canvasImage(index)

    def setImageSize(self, index):
        img = Image.open(self.fileData[index]["filename"])
        x_offset = 0
        y_offset = 0

        if(self.fileData[index]["rotate"]%180 != 0):            
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

        self.fileData[index]["x"] = new_width
        self.fileData[index]["y"] = new_height
        self.fileData[index]["x_offset"] = x_offset
        self.fileData[index]["y_offset"] = y_offset

    def getAdaptedImage(self, fileData):
        img = Image.open(fileData["filename"])
        img = img.resize((int(fileData["x"] * fileData["scale"]), int(fileData["y"] * fileData["scale"])))        
        img = img.rotate(fileData["rotate"], expand = True)

        return img
    def rotateImage(self, angle):
        if(self.imageSelected == None):
            return
        self.fileData[self.imageSelected]["rotate"] += angle
        self.fileData[self.imageSelected]["scale"] = 1
        self.setImageSize(self.imageSelected)
        self.canvasImage(self.imageSelected)
    def changeOffset(self, x, y):
        if(self.imageSelected == None):
            return
        self.fileData[self.imageSelected]["x_offset"] += x
        self.fileData[self.imageSelected]["y_offset"] += y
        self.canvasImage(self.imageSelected)

    def changeScale(self, value):
        if(self.imageSelected == None):
            return
        new_scale = self.fileData[self.imageSelected]["scale"] + value
        if new_scale <= 0.05:
            return
        self.fileData[self.imageSelected]["scale"] = new_scale
        self.fileData[self.imageSelected]["x_offset"] += self.fileData[self.imageSelected]["x"]/2 * value
        self.fileData[self.imageSelected]["y_offset"] += self.fileData[self.imageSelected]["y"]/2 * value
        # self.setImageSize(self.imageSelected)
        self.canvasImage(self.imageSelected)

    def canvasImage(self, index):
        img = self.getAdaptedImage(self.fileData[index])
        photo = ImageTk.PhotoImage(img)


        self.main.canvas.image = photo
        self.main.canvas.create_image(
            0 - self.fileData[index]["x_offset"] + self.main.offsetFrameX,
            0 - self.fileData[index]["y_offset"] + self.main.offsetFrameY,
            image=self.main.canvas.image,
            anchor=tk.NW)
        
        x2 = self.main.offsetFrameX + 800
        y2 = self.main.offsetFrameY + 480

        # Draw a red rectangle on the canvas
        self.main.canvas.create_rectangle(self.main.offsetFrameX, self.main.offsetFrameY, x2, y2, outline='red', width=4, dash=(3,5) ) 

        if(self.fileData[index]["date"] != None):
            print("Setting Date")
            self.main.date_entry.set_date(self.fileData[index]["date"])
        else:
            print("Deleting Date")
            self.main.date_entry.delete(0, 'end')