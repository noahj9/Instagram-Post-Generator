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

# Function to start dragging the logo
def start_drag(event):
    global logo_position, drag_data
    logo_position = (event.x, event.y)
    drag_data["x"] = event.x
    drag_data["y"] = event.y

# Function to drag the logo
def drag(event):
    global logo_position, drag_data
    if logo_position:
        delta_x = event.x - drag_data["x"]
        delta_y = event.y - drag_data["y"]
        logo_label.place(x=logo_label.winfo_x() + delta_x, y=logo_label.winfo_y() + delta_y)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# Function to end dragging the logo
def end_drag(event):
    global logo_position
    logo_position = None

# Function to generate the Instagram post
def generate_post():
    # Perform image composition using the selected template and image
    # Add your code here to create the final Instagram post

    # Get the selected image
    selected_image = image_label.image

    # Get the path of the selected logo
    logo_path_value = logo_path.get()

    if logo_path_value:
        # Open the logo image
        logo = Image.open(logo_path_value)
        logo = logo.resize((int(logo.width / 3), int(logo.height / 3)))  # Scale down the logo to 1/6 of its size

        # Calculate the position to overlay the logo
        overlay_position = (logo_label.winfo_x(), logo_label.winfo_y())

        # Create a copy of the selected image
        post_image = selected_image.copy()

        # Overlay the logo onto the image
        post_image.paste(logo, overlay_position, mask=logo)

        # Save the final post image with higher quality
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            post_image.save(save_path, quality=95)  # Adjust the quality value as needed
            print("Post image saved successfully.")
    else:
        print("Please select a logo.")

# Create the main window
window = tk.Tk()
window.title("Instagram Post Generator")

# Create the image label to display the selected image
image_label = tk.Label(window)
image_label.pack()

# Create the buttons
select_button = tk.Button(window, text="Select Image", command=open_image)
select_button.pack(pady=10)

logo_path = tk.StringVar()  # Variable to store the selected logo path

logo_select_button = tk.Button(window, text="Select Logo", command=open_logo)
logo_select_button.pack(pady=10)

logo_label = tk.Label(window)
logo_label.pack()

generate_button = tk.Button(window, text="Generate Post", command=generate_post)
generate_button.pack(pady=10)

# Start the main event loop
window.mainloop()
