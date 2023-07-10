import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from rembg import remove

# Logo Position Holders
logo_position = None
drag_data = {"x": 0, "y": 0}

# Open GUI
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = Image.open(file_path)
        image_cropped = crop_image(image, 400, 400)  # Crop image to 400x400 size
        photo = ImageTk.PhotoImage(image_cropped)
        image_label.configure(image=photo)
        image_label.image = image_cropped
        image_label.photo = photo  # Store reference to the PhotoImage

# Crop & Keep Aspect Ratio
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

# Select Logo
def open_logo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        logo_path.set(file_path)
        preview_logo()
        
def remove_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        logo_path.set(file_path)
    input = Image.open(file_path)
    output = remove(input)
    output.save("C:/Users/Mercedes and Singh/Desktop/Tests/output.png")

# Preview Logo
def preview_logo():
    logo_path_value = logo_path.get()
    if logo_path_value:
        logo = Image.open(logo_path_value)
        logo = logo.resize((int(logo.width / 3), int(logo.height / 3)))  # Scale down the logo to 1/3 of its size
        logo_preview = ImageTk.PhotoImage(logo)
        logo_label.configure(image=logo_preview)
        logo_label.image = logo_preview
        logo_label.logo = logo  # Reference for display

        # Drag to place
        logo_label.bind("<ButtonPress-1>", start_drag)
        logo_label.bind("<B1-Motion>", drag)
        logo_label.bind("<ButtonRelease-1>", end_drag)

# Drag Start function
def start_drag(event):
    global logo_position, drag_data
    logo_position = (event.x, event.y)
    drag_data["x"] = event.x
    drag_data["y"] = event.y

# Drag event
def drag(event):
    global logo_position, drag_data
    if logo_position:
        delta_x = event.x - drag_data["x"]
        delta_y = event.y - drag_data["y"]
        logo_label.place(x=logo_label.winfo_x() + delta_x, y=logo_label.winfo_y() + delta_y)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# End drag
def end_drag(event):
    global logo_position
    logo_position = None

# Generation of Post
def generate_post():
    # Get the selected image
    selected_image = image_label.image

    # logo Filepath
    logo_path_value = logo_path.get()

    if logo_path_value:
        # Open the logo image
        logo = Image.open(logo_path_value)
        logo = logo.resize((int(logo.width / 3), int(logo.height / 3)))  # Scale down the logo to 1/6 of its size

        # Overlay position
        overlay_position = (logo_label.winfo_x(), logo_label.winfo_y())

        # Copy the image
        post_image = selected_image.copy()

        # overlay the logo using a mask
        post_image.paste(logo, overlay_position, mask=logo)

        # Save and maintain quality
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            post_image.save(save_path, quality=95)  # quality scaling up
            print("Post image saved successfully.")
    else:
        print("Please select a logo.")

# Main Window
window = tk.Tk()
window.title("Instagram Post Generator")

# Create the image label to display the selected image
image_label = tk.Label(window)
image_label.pack()

# Buttons
select_button = tk.Button(window, text="Select Image", command=open_image)
select_button.pack(pady=10)

logo_path = tk.StringVar()  # Logo path storage

remove_background_button = tk.Button(window, text="BG Remover", command=remove_background)
remove_background_button.pack(pady=10)

logo_select_button = tk.Button(window, text="Select Logo", command=open_logo)
logo_select_button.pack(pady=10)

logo_label = tk.Label(window)
logo_label.pack()

generate_button = tk.Button(window, text="Generate Post", command=generate_post)
generate_button.pack(pady=10)

# Start main event loop
window.mainloop()
