import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import platform
from PIL import Image, ImageTk

from animal_detection.utils.constants import CARNIVORES

from animal_detection.inference.detect_images import detect_image
from animal_detection.inference.detect_video import detect_video
from animal_detection.inference.detect_webcam import detect_webcam

# ==========================
# Paths & Colors
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

BANNER_PATH = BASE_DIR / "assets" / "banner.webp"

PRIMARY = "#2E7D32"
DARK = "#1B5E20"
LIGHT = "#E8F5E9"
RED = "#C62828"
WHITE = "#FFFFFF"

# ==========================
# Functions
# ==========================


def exit_application():
    try:
        import cv2

        cv2.destroyAllWindows()
    except:
        pass
    root.after(100, root.destroy)


def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")],
    )

    if not file_path:
        return

    try:
        output_path, carnivore_count, animals = detect_image(file_path)
        img = Image.open(output_path)
        img.thumbnail((950, 600))
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo, text="")
        image_label.image = photo

        unique_animals = sorted(set(animals))
        total_animals = len(unique_animals)
        carnivore_species = len([a for a in unique_animals if a.lower() in CARNIVORES])
        herbivores = total_animals - carnivore_species

        total_animals_label.config(text=f"Total Animals Detected: {total_animals}")
        carnivore_stats_label.config(text=f"Carnivores Detected: {carnivore_species}")
        herbivore_stats_label.config(text=f"Herbivores Detected: {herbivores}")
        summary_label.config(
            text="Detected Animals: "
            + (", ".join(unique_animals) if unique_animals else "None")
        )
        carnivore_label.config(text=f"Carnivores Detected: {carnivore_species}")
        status_label.config(text="✅ Image Detection Completed Successfully")

        if carnivore_count > 0:
            messagebox.showwarning(
                "Carnivore Alert", f"{carnivore_count} Carnivore(s) Detected!"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def upload_video():
    file_path = filedialog.askopenfilename(
        title="Select Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
    )

    if not file_path:
        return

    try:
        output_path, carnivore_count, animals = detect_video(file_path)

        # Update stats
        unique_animals = sorted(set(animals))
        total_animals = len(unique_animals)
        carnivore_species = len([a for a in unique_animals if a.lower() in CARNIVORES])
        herbivores = total_animals - carnivore_species

        total_animals_label.config(text=f"Total Animals Detected: {total_animals}")
        carnivore_stats_label.config(text=f"Carnivores Detected: {carnivore_species}")
        herbivore_stats_label.config(text=f"Herbivores Detected: {herbivores}")
        summary_label.config(
            text="Detected Animals: "
            + (", ".join(unique_animals) if unique_animals else "None")
        )
        carnivore_label.config(text=f"Carnivores Detected: {carnivore_species}")

        # Video placeholder preview
        image_label.config(
            image="", text="🎥 Video Detection Completed\nCheck Saved Output Video"
        )
        image_label.image = None

        status_label.config(text="✅ Video Detection Completed Successfully")

        if carnivore_count > 0:
            messagebox.showwarning(
                "Carnivore Alert", f"{carnivore_count} Carnivore(s) Detected!"
            )

        messagebox.showinfo(
            "Success",
            f"Video Detection Completed.\nSaved Output: {output_path}\nPress Q to stop the video window.",
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def start_webcam():
    try:
        status_label.config(text="📷 Webcam Detection Running...")
        output_path, carnivore_count, animals = detect_webcam()

        unique_animals = sorted(set(animals))
        total_animals = len(unique_animals)
        carnivore_species = len([a for a in unique_animals if a.lower() in CARNIVORES])
        herbivores = total_animals - carnivore_species

        total_animals_label.config(text=f"Total Animals Detected: {total_animals}")
        carnivore_stats_label.config(text=f"Carnivores Detected: {carnivore_species}")
        herbivore_stats_label.config(text=f"Herbivores Detected: {herbivores}")
        summary_label.config(
            text="Detected Animals: "
            + (", ".join(unique_animals) if unique_animals else "None")
        )
        carnivore_label.config(text=f"Carnivores Detected: {carnivore_species}")

        image_label.config(image="", text="📷 Webcam Detection Completed")
        image_label.image = None

        status_label.config(text="✅ Webcam Detection Completed Successfully")

        if carnivore_count > 0:
            messagebox.showwarning(
                "Carnivore Alert", f"{carnivore_count} Carnivore(s) Detected!"
            )

        if output_path:
            status_label.config(
                text=f"✅ Webcam Detection Completed. Output: {output_path}"
            )
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ==========================
# Main Window
# ==========================

root = tk.Tk()
root.title("Smart Wildlife Detection using YOLOv8")
root.state("zoomed")
root.resizable(True, True)

# ==========================
# Scrollable Base Setup
# ==========================

container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg=LIGHT)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=LIGHT)

# create window and keep id so we can resize the inner frame with the canvas
window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def _on_scrollable_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def _on_canvas_configure(event):
    # ensure inner frame width follows canvas width
    canvas.itemconfig(window_id, width=event.width)


scrollable_frame.bind("<Configure>", _on_scrollable_configure)
canvas.bind("<Configure>", _on_canvas_configure)


def _on_mousewheel(event):
    system = platform.system()
    try:
        if system == "Windows":
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif system == "Darwin":
            canvas.yview_scroll(int(-1 * (event.delta)), "units")
        else:
            if hasattr(event, "num") and event.num in (4, 5):
                canvas.yview_scroll(-1 if event.num == 4 else 1, "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta)), "units")
    except Exception:
        pass


canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", _on_mousewheel)
canvas.bind_all("<Button-5>", _on_mousewheel)

# ==========================
# UI Layout (Parents set to scrollable_frame)
# ==========================

try:
    banner_img = Image.open(BANNER_PATH)
    banner_img = banner_img.resize((1100, 220))
    banner_photo = ImageTk.PhotoImage(banner_img)
    banner_frame = tk.Frame(scrollable_frame, bg=LIGHT)
    banner_frame.pack(fill="x")
    banner_label = tk.Label(banner_frame, image=banner_photo, bg=LIGHT, bd=0)
    banner_label.pack()
except Exception as e:
    print("Banner not loaded:", e)

title_label = tk.Label(
    scrollable_frame,
    text="🦁 Smart Wildlife Detection & Monitoring System 🐅",
    font=("Arial", 24, "bold"),
    bg=LIGHT,
    fg=DARK,
)
title_label.pack(pady=(10, 0))

subtitle_label = tk.Label(
    scrollable_frame,
    text="Real-Time Animal Detection, Species Classification & Carnivore Monitoring using YOLOv8",
    font=("Arial", 12),
    bg=LIGHT,
    fg="#444444",
)
subtitle_label.pack(pady=(0, 10))

image_frame = tk.Frame(scrollable_frame, bg=WHITE, relief="ridge", bd=3)
image_frame.pack(pady=10)

image_label = tk.Label(image_frame, bg=WHITE)
image_label.pack()
image_label.config(
    text="🦁 Detection Results Will Appear Here 🐅",
    font=("Arial", 18, "bold"),
    fg=DARK,
    bg=WHITE,
    width=70,
    height=18,
)

summary_label = tk.Label(
    scrollable_frame,
    text="Detected Animals: None",
    font=("Arial", 13, "bold"),
    bg=LIGHT,
    fg=DARK,
)
summary_label.pack(pady=5)

carnivore_label = tk.Label(
    scrollable_frame,
    text="Carnivores Detected: 0",
    font=("Arial", 14, "bold"),
    bg=LIGHT,
    fg=RED,
)
carnivore_label.pack(pady=5)

status_label = tk.Label(scrollable_frame, text="Ready", font=("Arial", 12), bg=LIGHT)
status_label.pack(pady=5)

stats_frame = tk.LabelFrame(
    scrollable_frame,
    text=" Detection Statistics ",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=DARK,
    padx=20,
    pady=10,
)
stats_frame.pack(pady=15, fill="x", padx=40)

total_animals_label = tk.Label(
    stats_frame, text="Total Animals Detected: 0", font=("Arial", 14, "bold"), bg=WHITE
)
total_animals_label.pack(anchor="w")

carnivore_stats_label = tk.Label(
    stats_frame,
    text="Carnivores Detected: 0",
    font=("Arial", 14, "bold"),
    bg=WHITE,
    fg=RED,
)
carnivore_stats_label.pack(anchor="w")

herbivore_stats_label = tk.Label(
    stats_frame,
    text="Herbivores Detected: 0",
    font=("Arial", 14, "bold"),
    bg=WHITE,
    fg=PRIMARY,
)
herbivore_stats_label.pack(anchor="w")

button_frame = tk.Frame(scrollable_frame, bg=LIGHT)
button_frame.pack(pady=20)

image_btn = tk.Button(
    button_frame,
    text="🖼 Detect Image",
    width=25,
    height=2,
    bg=PRIMARY,
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2",
    relief="flat",
    bd=0,
    command=upload_image,
)
image_btn.grid(row=0, column=0, padx=10, pady=10)

video_btn = tk.Button(
    button_frame,
    text="🎥 Detect Video",
    width=25,
    height=2,
    bg=PRIMARY,
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2",
    relief="flat",
    bd=0,
    command=upload_video,
)
video_btn.grid(row=0, column=1, padx=10, pady=10)

webcam_btn = tk.Button(
    button_frame,
    text="📷 Start Webcam",
    width=25,
    height=2,
    bg=PRIMARY,
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2",
    relief="flat",
    bd=0,
    command=start_webcam,
)
webcam_btn.grid(row=1, column=0, padx=10, pady=10)


def reset_dashboard():
    # Reset image preview
    image_label.config(image="", text="🦁 Detection Results Will Appear Here 🐅")
    image_label.image = None

    # Reset labels
    summary_label.config(text="Detected Animals: None")
    carnivore_label.config(text="Carnivores Detected: 0")
    status_label.config(text="Ready")
    total_animals_label.config(text="Total Animals Detected: 0")
    carnivore_stats_label.config(text="Carnivores Detected: 0")
    herbivore_stats_label.config(text="Herbivores Detected: 0")


reset_btn = tk.Button(
    button_frame,
    text="🔄 Reset Dashboard",
    width=25,
    height=2,
    bg=PRIMARY,
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2",
    relief="flat",
    bd=0,
    command=reset_dashboard,
)
reset_btn.grid(row=1, column=1, padx=10, pady=10)

exit_btn = tk.Button(
    button_frame,
    text="❌ Exit",
    width=52,
    height=2,
    bg=RED,
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2",
    relief="flat",
    bd=0,
    command=exit_application,
)
exit_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


def on_enter(e):
    if e.widget == exit_btn:
        e.widget.config(bg="#D32F2F")
    else:
        e.widget.config(bg="#388E3C")


def on_leave(e):
    if e.widget != exit_btn:
        e.widget.config(bg=PRIMARY)
    else:
        e.widget.config(bg=RED)


for btn in [image_btn, video_btn, webcam_btn, reset_btn, exit_btn]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

footer = tk.Label(
    scrollable_frame,
    text="Developed using Python • OpenCV • YOLOv8 • Computer Vision",
    font=("Arial", 10, "italic"),
    bg=LIGHT,
    fg=DARK,
)
footer.pack(side="bottom", pady=10)

root.protocol("WM_DELETE_WINDOW", exit_application)
root.mainloop()
