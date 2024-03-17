import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Canvas
from PIL import ImageTk, Image

global fileNames
fileNames = []
global fileSizes
fileSizes = []

def loadImages():
    filetypes = (
        ('Images', '*.jpg'),
        ('Images', '*.png')
    )

    global fileNames
    fileNames = fd.askopenfilenames(
        title='Open image Files',
        initialdir='/',
        filetypes=filetypes)
    
    if(len(fileNames) == 0):
        return
    
    # Clear the button frame
    for widget in left_frame.winfo_children():
        widget.destroy()

    # Put the fileNames into a scrollable listbox
    listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE)
    listbox.pack(fill=tk.BOTH, expand=True)
    for filename in fileNames:
        setfileSize(filename)
        listbox.insert(tk.END, filename.split('/')[-1])
    #select the first item in the listbox
    listbox.bind('<<ListboxSelect>>', on_selection_change)
    #change the slecetion to the first item so that on_selection_change is called
    listbox.selection_set(0)
    canvasImage(0)

def on_selection_change(event):
    # Get the current selection
    selection = event.widget.curselection()
    # Check if there is a selection
    if selection:
        canvasImage(selection[0])

def setfileSize(filepath):
     # Open the image file
    img = Image.open(filepath)

    # Calculate the aspect ratio
    aspect_ratio = img.width / img.height

    # Calculate the new size
    new_width = 800
    new_height = round(new_width / aspect_ratio)

    # If the new height is less than 480, set it to 480 and adjust the width accordingly
    if new_height < 480:
        new_height = 480
        new_width = round(new_height * aspect_ratio)
    # Push x and y as object to the global variable fileSizes
    global fileSizes
    fileSizes.append({'x': new_width, 'y': new_height})
   
def canvasImage(index):
    # Open the image file
    img = Image.open(fileNames[index])
    test = fileSizes[index]
    # Resize the image
    img_resized = img.resize((fileSizes[index]["x"], fileSizes[index]["y"]))

    # Create a PhotoImage object
    photo = ImageTk.PhotoImage(img_resized)

    # Store a reference to the image in the canvas
    canvas.image = photo

    canvas.create_image(
        400,  # half of 800
        240,
        image=canvas.image,
        anchor='center'
    )

    
# Create the main window
root = tk.Tk()
root.title("BMP Converter")
root.geometry("1000x480")
root.minsize(1000, 480)
# make the grid row 0 the width of 800
root.grid_rowconfigure(0, minsize=480)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, minsize=800)



# Create a frame to hold the buttons
left_frame = tk.Frame(root)
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid(row=0, column=0)

# Create two buttons inside the frame
button1 = tk.Button(left_frame, text="Bilder Laden", command=loadImages)
button1.place(relx=0.5, rely=0.5, anchor='center')
button1.pack()

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1)

canvas = Canvas(
    right_frame,
    width=800,
    height=480
)
canvas.pack()

# add a grey background to the canvas
canvas.create_rectangle(0, 0, 800, 480, fill="grey")
# photo = ImageTk.PhotoImage(Image.open("C:/Users/Tobias/Desktop/Bilder/DSC_0001 - Copy.JPG"))  

# canvas.create_image(
#     0,
#     0, 
#     image=photo,
#     anchor='nw'
# )

# button2 = tk.Button(left_frame, text=".odt Speichern UND PDF Kombinieren", command=save_odt_and_combine_pdf)
# button2.pack(side=tk.LEFT, padx=20)

# Start the main loop
root.mainloop()
