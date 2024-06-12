import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import splash_screen

def sketch(image_path, save_path, effect, params, result_label, progress_bar):
    try:
        image = cv2.imread(image_path)
        if image is None:
            messagebox.showerror("Error", "Unable to load the image.")
            return

        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if effect == "Pencil Sketch":
            blurred_img = cv2.GaussianBlur(gray_img, (params['blur_radius'], params['blur_radius']), 0)
            sketch_img = cv2.divide(gray_img, blurred_img, scale=256)
        elif effect == "Hand Drawn":
            sketch_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY, params['block_size'], params['C'])
        elif effect == "Brush Strokes":
            blurred_img = cv2.medianBlur(gray_img, params['median_blur'])
            edges = cv2.Canny(blurred_img, params['threshold1'], params['threshold2'])
            sketch_img = cv2.bitwise_not(edges)
        else:
            blurred_img = cv2.GaussianBlur(gray_img, (params['blur_radius'], params['blur_radius']), 0)
            sketch_img = cv2.divide(gray_img, blurred_img, scale=256)

        cv2.imwrite(save_path, sketch_img)
        messagebox.showinfo("Success", "Conversion completed successfully!")
        show_result_image(save_path, result_label)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        progress_bar.stop()
        progress_bar["value"] = 0

def select_image(image_label):
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg; *.jpeg; *.png")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, image_path)
    show_original_image(image_path, image_label)

def show_original_image(image_path, image_label):
    img = Image.open(image_path)
    img.thumbnail((150, 150))
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

def show_result_image(image_path, result_label):
    img = Image.open(image_path)
    img.thumbnail((500, 500))
    photo = ImageTk.PhotoImage(img)
    result_label.config(image=photo)
    result_label.image = photo

def select_save_location():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    entry_save.delete(0, tk.END)
    entry_save.insert(0, save_path)

def convert_to_scribble(result_label, progress_bar):
    image_path = entry_image.get()
    save_path = entry_save.get()
    effect = effect_var.get()

    params = {
        'blur_radius': blur_radius_var.get(),
        'block_size': block_size_var.get(),
        'C': C_var.get(),
        'median_blur': median_blur_var.get(),
        'threshold1': threshold1_var.get(),
        'threshold2': threshold2_var.get()
    }

    if not image_path:
        messagebox.showerror("Error", "Please select an image.")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a save location.")
        return

    progress_bar.start()
    sketch(image_path, save_path, effect, params, result_label, progress_bar)

def about():
    messagebox.showinfo("About", 
    "Photo to Scribble\nVersion 1.0 beta\nDeveloped by Dimonapatrick243\nThis application converts a photo into a scribble drawing with various effects.")

def update_parameters(*args):
    effect = effect_var.get()
    if effect == "Pencil Sketch":
        frame_pencil.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky=tk.W)
        frame_hand_drawn.grid_remove()
        frame_brush_strokes.grid_remove()
    elif effect == "Hand Drawn":
        frame_pencil.grid_remove()
        frame_hand_drawn.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky=tk.W)
        frame_brush_strokes.grid_remove()
    elif effect == "Brush Strokes":
        frame_pencil.grid_remove()
        frame_hand_drawn.grid_remove()
        frame_brush_strokes.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky=tk.W)

root = tk.Tk()
root.title("Photo to Scribble v10 Beta")
root.iconbitmap('assets/logo.ico')
root.geometry("1024x720")
root.resizable(False, False)
root.configure(background='gray10')

# Display splash screen
splash_screen.show_splash(root)

# Left side images
frame_images = tk.Frame(root, background='gray30')
frame_images.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

image_label = tk.Label(frame_images, text="Original Image", background='gray30')
image_label.pack(side=tk.BOTTOM, expand=True, padx=5, pady=10)

result_label = tk.Label(frame_images, text="Result Image")
result_label.pack(side=tk.TOP, expand=True, padx=5, pady=10)

# Right side controls
frame_controls = tk.Frame(root, background='gray30')
frame_controls.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

label_image = tk.Label(frame_controls, background='gray30', fg='white', text="Image:")
entry_image = tk.Entry(frame_controls, width=40)
button_browse_image = tk.Button(frame_controls, text="Browse", command=lambda: select_image(image_label))

label_save = tk.Label(frame_controls, background='gray30', fg='white', text="Save as:")
entry_save = tk.Entry(frame_controls, width=40)
button_browse_save = tk.Button(frame_controls, text="Browse", command=select_save_location)

label_effect = tk.Label(frame_controls, background='gray30', fg='white', text="Effect:")
effect_var = tk.StringVar(value="Pencil Sketch")
effect_menu = tk.OptionMenu(frame_controls, effect_var, "Pencil Sketch", "Hand Drawn", "Brush Strokes", command=update_parameters)

# Parameters frames
frame_pencil = tk.Frame(frame_controls)
label_blur_radius = tk.Label(frame_pencil, text="Blur Radius:")
blur_radius_var = tk.IntVar(value=21)
slider_blur_radius = tk.Scale(frame_pencil, from_=1, to=99, orient=tk.HORIZONTAL, variable=blur_radius_var)
label_blur_radius.grid(row=0, column=0, sticky=tk.W)
slider_blur_radius.grid(row=0, column=1)

frame_hand_drawn = tk.Frame(frame_controls)
label_block_size = tk.Label(frame_hand_drawn, text="Block Size:")
block_size_var = tk.IntVar(value=11)
slider_block_size = tk.Scale(frame_hand_drawn, from_=1, to=99, orient=tk.HORIZONTAL, variable=block_size_var)
label_C = tk.Label(frame_hand_drawn, text="C:")
C_var = tk.IntVar(value=2)
slider_C = tk.Scale(frame_hand_drawn, from_=-10, to=10, orient=tk.HORIZONTAL, variable=C_var)
label_block_size.grid(row=0, column=0)
slider_block_size.grid(row=0, column=1)
label_C.grid(row=1, column=0)
slider_C.grid(row=1, column=1)

frame_brush_strokes = tk.Frame(frame_controls)
label_median_blur = tk.Label(frame_brush_strokes, text="Median Blur:")
median_blur_var = tk.IntVar(value=5)
slider_median_blur = tk.Scale(frame_brush_strokes, from_=1, to=99, orient=tk.HORIZONTAL, variable=median_blur_var)
label_threshold1 = tk.Label(frame_brush_strokes, text="Threshold1:")
threshold1_var = tk.IntVar(value=50)
slider_threshold1 = tk.Scale(frame_brush_strokes, from_=1, to=255, orient=tk.HORIZONTAL, variable=threshold1_var)
label_threshold2 = tk.Label(frame_brush_strokes, text="Threshold2:")
threshold2_var = tk.IntVar(value=150)
slider_threshold2 = tk.Scale(frame_brush_strokes, from_=1, to=255, orient=tk.HORIZONTAL, variable=threshold2_var)
label_median_blur.grid(row=0, column=0)
slider_median_blur.grid(row=0, column=1)
label_threshold1.grid(row=1, column=0)
slider_threshold1.grid(row=1, column=1)
label_threshold2.grid(row=2, column=0)
slider_threshold2.grid(row=2, column=1)

button_convert = tk.Button(frame_controls, bg='light green', text="Convert to Scribble", width=60, height=3, command=lambda: convert_to_scribble(result_label, progress_bar))

progress_bar = ttk.Progressbar(frame_controls, orient="horizontal", length=400, mode="indeterminate")

# Arrange the widgets in the controls frame
label_image.grid(row=0, column=0, sticky=tk.W, pady=5)
entry_image.grid(row=0, column=1)
button_browse_image.grid(row=0, column=2, padx=5)

label_save.grid(row=1, column=0, sticky=tk.W, pady=10)
entry_save.grid(row=1, column=1)
button_browse_save.grid(row=1, column=2, padx=10)

label_effect.grid(row=2, column=0, sticky=tk.W, pady=10)
effect_menu.grid(row=2, column=1, columnspan=2, padx=10, sticky=tk.W)
frame_pencil.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky=tk.W)
button_convert.grid(row=5, column=0, columnspan=4, pady=20, sticky=tk.W)
progress_bar.grid(row=6, column=0, columnspan=3, pady=360)

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create the About menu
about_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=about)

# Update the parameter frames based on the selected effect
update_parameters()

# Run the application
root.mainloop()
