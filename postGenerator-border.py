import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Global variables to store the position of the logo
logo_position = None
drag_data = {"x": 0, "y": 0}

# Function to open a file dialog and select an image
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = Image.open(file_path)
        image_cropped = crop_image(image, 400, 400)  # Crop image to 400x400 size
        photo = ImageTk.PhotoImage(image_cropped)
        image_label.configure(image=photo)
        image_label.image = image_cropped
        image_label.photo = photo  # Store reference to the PhotoImage

# Function to crop the image to the specified size without changing the aspect ratio
def crop_image(image, width, height):
    aspect_ratio = image.width / image.height
    target_ratio = width / height

    if aspect_ratio > target_ratio:
        new_height = image.height
        new_width = int(new_height * target_ratio)
    else:
        new_width = image.width
        new_height = int(new_width / target_ratio)

    left = (image.width - new_width) // 2
    top = (image.height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    return image.crop((left, top, right, bottom)).resize((width, height), resample=Image.LANCZOS)

# Function to open a file dialog and select a logo image
def open_logo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        logo_path.set(file_path)
        preview_logo()

# Function to preview the selected logo
def preview_logo():
    logo_path_value = logo_path.get()
    if logo_path_value:
        logo = Image.open(logo_path_value)
        logo = logo.resize((int(logo.width / 3), int(logo.height / 3)))  # Scale down the logo to 1/3 of its size
        logo_preview = ImageTk.PhotoImage(logo)
        logo_label.configure(image=logo_preview)
        logo_label.image = logo_preview
        logo_label.logo = logo  # Store reference to the logo Image

        # Enable dragging for the logo preview
        logo_label.bind("<ButtonPress-1>", start_drag)
        logo_label.bind("<B1-Motion>", drag)
        logo_label.bind("<ButtonRelease-1>", end_drag)

# Function to open a file dialog and select an image for the border
def open_border():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        border_path.set(file_path)
        preview_border()

# Function to preview the selected border image
def preview_border():
    border_path_value = border_path.get()
    if border_path_value:
        border = Image.open(border_path_value)
        border_preview = ImageTk.PhotoImage(border)
        border_label.configure(image=border_preview)
        border_label.image = border_preview
        border_label.border = border  # Store reference to the border Image

# Function to generate the Instagram post
def generate_post():
    # Perform image composition using the selected template, image, and border
    # Add your code here to create the final Instagram post

    # Get the selected image
    selected_image = image_label.image

    # Get the path of the selected logo
    logo_path_value = logo_path.get()

    # Get the path of the selected border
    border_path_value = border_path.get()

    if logo_path_value and border_path_value:
        # Open the logo image
        logo = Image.open(logo_path_value)
        logo = logo.resize((int(logo.width / 6), int(logo.height / 6)))  # Scale down the logo to 1/6 of its size

        # Open the border image
        border = Image.open(border_path_value)

        # Create a copy of the selected image
        post_image = selected_image.copy()

        # Resize the post image to fit inside the border
        post_image_resized = post_image.resize(border.size)

        # Composite the border and the post image
        result = Image.alpha_composite(border.convert("RGBA"), post_image_resized.convert("RGBA"))

        # Calculate the position to overlay the logo
        overlay_position = (logo_label.winfo_x(), logo_label.winfo_y())

        # Overlay the logo onto the result image
        result.paste(logo, overlay_position, mask=logo)

        # Save the final post image with higher quality
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            result.save(save_path, quality=95)  # Adjust the quality value as needed
            print("Post image saved successfully.")
    else:
        print("Please select a logo and a border.")

# Create the main window
window = tk.Tk()
window.title("Instagram Post Generator")

# Create a scrollable frame
canvas = tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)
scrollbar = tk.Scrollbar(window, command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Create the image label to display the selected image
image_label = tk.Label(frame)
image_label.pack()

# Create the buttons
select_button = tk.Button(frame, text="Select Image", command=open_image)
select_button.pack(pady=10)

logo_path = tk.StringVar()  # Variable to store the selected logo path
border_path = tk.StringVar()  # Variable to store the selected border path

logo_select_button = tk.Button(frame, text="Select Logo", command=open_logo)
logo_select_button.pack(pady=10)

logo_label = tk.Label(frame)
logo_label.pack()

border_select_button = tk.Button(frame, text="Select Border", command=open_border)
border_select_button.pack(pady=10)

border_label = tk.Label(frame)
border_label.pack()

generate_button = tk.Button(frame, text="Generate Post", command=generate_post)
generate_button.pack(pady=10)

# Add the scrollbar to the canvas
canvas.configure(scrollregion=canvas.bbox("all"))

# Start the main event loop
window.mainloop()
