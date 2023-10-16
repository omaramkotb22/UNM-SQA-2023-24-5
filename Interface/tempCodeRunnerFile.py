import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def on_configure(event):
    # Update the scroll region to cover the entire content
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    current_position = canvas.yview()
    if event.delta > 0 and current_position[0] > 0:
        # Scroll up only if not already at the top
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    elif event.delta < 0 and current_position[1] < 1:
        # Scroll down only if not already at the bottom
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

def button_action():
    # Define the action to perform when the button is clicked
    print("Button Clicked")

root = tk.Tk()
root.title("Video Player")
root.geometry("1920x1050")  # Adjust the size for better visibility

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

# Load the image with Pillow and create an ImageTk PhotoImage
image = Image.open("Interface/army.gif")  # Open the image
image = image.resize((300, 300))  # Resize the image
photo = ImageTk.PhotoImage(image)  # Create an ImageTk PhotoImage

# Create a Label to display the resized image as a button
button_label = ttk.Label(content_frame, image=photo)
button_label.image = photo  # Keep a reference to prevent it from being garbage collected
button_label.pack()

# Bind the button action to the label
button_label.bind("<Button-1>", lambda event: button_action())

# Create a Frame for the right side (3/4 of the window)
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")

# Add content to the right side
right_label = ttk.Label(right_frame, text="Non-Scrollable Right Side")
right_label.pack()

# Configure grid weights to allow resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

root.mainloop()
