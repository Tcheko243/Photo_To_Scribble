import tkinter as tk

def show_splash(root):
    splash = tk.Toplevel(root)
    splash.geometry("300x300+800+400")
    splash.overrideredirect(True)
    splash.configure(background='gray10')

    splash_label = tk.Label(splash, text="Photo to Scribble", bg='gray10', fg='white', font=("Helvetica", 16, "bold"))
    splash_label.pack(pady=20)

    splash_info = tk.Label(splash, text="Loading...", bg='gray10', fg='white')
    splash_info.pack(pady=40)

    splash_info2 = tk.Label(splash, text="Developed by Dimonapatrick243", bg='gray10', fg='white')
    splash_info2.pack(pady=50)

    root.withdraw()  # Hide the main window
    splash.update()
    splash.after(3000, lambda: close_splash(splash, root))

def close_splash(splash, root):
    splash.destroy()
    root.deiconify()
