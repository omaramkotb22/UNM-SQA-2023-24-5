import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def on_configure(event):
    # Update the scroll region to cover the entire content
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def on_image_enter(event):
    # Change the cursor to a pointing hand when hovering over an image
    content_frame.config(cursor="hand2")

def on_image_leave(event):
    # Restore the default cursor when the mouse leaves the image
    content_frame.config(cursor="")

def button_action(title):
    # Define the action to perform when the image is clicked
    print(f"Image Clicked: {title}")

root = tk.Tk()
root.title("Video Player")
root.geometry("1920x1050")  # Adjust the size for better visibility

# Set the window attributes to allow resizing
root.state('zoomed')

# Create a Frame for the left side (1/4 of the window)
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, sticky="nsew")

# Create a Label widget for the title (centered in the left frame)
title_label = ttk.Label(left_frame, text="Video Collection", font=("Arial", 16))
title_label.pack()

# Add a separator line
separator = ttk.Separator(left_frame, orient="horizontal")
separator.pack(fill="x")

# Create a Canvas for the scrollable content on the left side
canvas = tk.Canvas(left_frame)
scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Bind the canvas to update the scroll region when resized
canvas.bind("<Configure>", on_configure)

# Create a Frame for the content on the left side
content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

root.bind("<MouseWheel>", on_mousewheel)

# List of image paths to use as placeholders
image_data = [
    {
        "image_path": "Interface/army.gif",
        "title": "Image 1 Title",
    },
    {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 2 Title",
    },
    {
        "image_path": "Interface/army.gif",
        "title": "Image 3 Title",
    },
    {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 4 Title",
    },
    {
        "image_path": "Interface/army.gif",
        "title": "Image 5 Title",
    },
    {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 6 Title",
    },
    {
        "image_path": "Interface/army.gif",
        "title": "Image 7 Title",
    },
        {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 8 Title",
    },
    {
        "image_path": "Interface/army.gif",
        "title": "Image 9 Title",
    },
    {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 10 Title",
    },
    {
        "image_path": "Interface/army.gif",
        "title": "Image 11 Title",
    },
        {
        "image_path": "Interface/mordo.jpg",
        "title": "Image 12 Title",
    }, 
]

style = ttk.Style()
style.configure("ImageTitle.TLabel", font=("Times New Roman", 16), foreground="black")



# Load and add images with titles from the list to the content frame
for i, data in enumerate(image_data):
    image = Image.open(data["image_path"])
    image = image.resize((300, 200))
    photo = ImageTk.PhotoImage(image)
    button_label = ttk.Label(content_frame, image=photo)
    button_label.image = photo
    button_label.grid(row=i, column=0, padx=20, pady=20)  # Place image in the first column

    title_label = ttk.Label(content_frame, text=data["title"], style="ImageTitle.TLabel")
    title_label.grid(row=i, column=1, sticky="w")  # Place title in the second column to the right

    # Bind events for cursor change and action
    button_label.bind("<Enter>", on_image_enter)
    button_label.bind("<Leave>", on_image_leave)
    button_label.bind("<Button-1>", lambda event, title=data["title"]: button_action(title))

# Create a Frame for the right side (3/4 of the window)
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")

# Add content to the right side
right_label = ttk.Label(right_frame, text="Currently Playing:",  font=("Arial", 16))
right_label.pack()

# Configure grid weights to allow resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=4)

root.mainloop()
