import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

RESOLUTIONS = {
    '720p HDTV': (1280, 720),
    '1080p Full HD': (1920, 1080),
    '1440p Quad HD': (2560, 1440),
    '4K UHD': (3840, 2160),
    # Add more resolutions here if needed
}

file_path = None
save_location = None

def downsample_image(image_path, save_path, target_resolution):
    # Load the image
    image = cv2.imread(image_path)

    # Get the original image dimensions
    original_height, original_width = image.shape[:2]

    # Get the selected target resolution
    target_width, target_height = RESOLUTIONS[target_resolution]

    # Check if the target resolution is larger than the original image resolution
    if target_width > original_width or target_height > original_height:
        messagebox.showerror("Invalid Resolution", "Output resolution cannot be larger than input resolution. Use an AI upscaler for that.")
        exit()

    # Resize the image using the target resolution
    resized_image = cv2.resize(image, (target_width, target_height))

    # Save the resized image to the specified location
    cv2.imwrite(save_path, resized_image)
    messagebox.showinfo("Image Saved", f"Image saved successfully to:\n{save_path}")
    exit()

def enable_resolution_picker(resolution_button, resolution_var):
    resolution_button.configure(state='normal')

def select_image():
    global file_path, save_location
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(title='Select Image File',
                                           filetypes=(('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*')))
    if file_path:
        save_location = filedialog.asksaveasfilename(defaultextension='.jpg',
                                                     filetypes=(('JPEG', '*.jpg'), ('PNG', '*.png')))
        if save_location:
            # Enable the resolution picker button
            enable_resolution_picker(resolution_button, resolution_var)

def downsample_and_save():
    global file_path, save_location
    target_resolution = resolution_var.get()
    downsample_image(file_path, save_location, target_resolution)

# Create the tkinter GUI
root = tk.Tk()
root.title('Image Downsampler')

# Create a button to select the image
select_button = tk.Button(root, text='Select Image', command=select_image)
select_button.pack(pady=10)

# Create the resolution selection frame
resolution_frame = tk.Frame(root)
resolution_frame.pack(pady=10)

# Create the dropdown menu for resolution selection
resolution_var = tk.StringVar(resolution_frame)
resolution_var.set(list(RESOLUTIONS.keys())[0])
resolution_dropdown = tk.OptionMenu(resolution_frame, resolution_var, *RESOLUTIONS.keys())
resolution_dropdown.pack(side='left', padx=10)

# Create the resolution picker button
resolution_button = tk.Button(resolution_frame, text='Select Resolution', state='disabled', command=downsample_and_save)
resolution_button.pack(side='left')

# Run the GUI main loop
root.mainloop()
