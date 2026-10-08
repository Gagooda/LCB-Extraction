import random
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk  # type: ignore[reportMissingImports]

image_folders = {
    "0": Path("C:/Users/Roman/Pictures/common"),
    "00": Path("C:/Users/Roman/Pictures/rare"),
    "000": Path("C:/Users/Roman/Pictures/super cool"),
}
images_by_rarity = {
    rarity: [
        path
        for path in folder.iterdir()
        if path.suffix.lower() in {".png", ".webp"}
    ]
    for rarity, folder in image_folders.items()
}

root = tk.Tk()
root.title("Sinner Extractor")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)


def resize_image(event=None):
    original_image = getattr(image_label, "original_image", None)
    if original_image is None:
        return

    width = image_label.winfo_width()
    height = image_label.winfo_height()
    if width <= 1 or height <= 1:
        return

    resized_image = original_image.copy()
    resized_image.thumbnail((width, height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    image_label.config(image=photo)
    image_label.image = photo


image_label = tk.Label(root)
image_label.bind("<Configure>", resize_image)


def extract():
    rarity = random.choices(["0", "00", "000"], weights=[70, 20, 10], k=1)[0]
    available_images = images_by_rarity[rarity]

    if not available_images:
        result_label.config(text=f"No images found for rarity {rarity}")
        image_label.config(image="")
        image_label.image = None
        image_label.original_image = None
        return

    image_path = random.choice(available_images)
    with Image.open(image_path) as source_image:
        image_label.original_image = source_image.copy()
    root.after_idle(resize_image)
    result_label.config(text=f"You extracted a sinner with rarity {rarity}")


tk.Button(root, text="Extract",bg="black", fg="gold", command=extract).grid(
    row=0, column=0, sticky="ew", padx=20, pady=10
)
result_label = tk.Label(root,bg="gold", fg="black", text="Click Extract to get a sinner")
result_label.grid(row=1, column=0, pady=5)
image_label.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
tk.Button(root, text="Close", command=root.destroy).grid(
    row=3, column=0, sticky="ew", padx=20, pady=10
)

root.config(bg="#080700") 

root.mainloop()


