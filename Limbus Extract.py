import random
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

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


results_frame = tk.Frame(root, bg="black")
results_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

def extract(count):
    
    for widget in results_frame.winfo_children():
        widget.destroy()

    
    columns = 1 if count == 1 else 5
    for column in range(columns):
        results_frame.columnconfigure(column, weight=1)

    result_label.config(text="Extracting...")

    def reveal_pull(index):
        
        if index >= count:
            result_label.config(text=f"Showing {count} pull(s)")
            return

        rarity = random.choices(
            ["0", "00", "000"],
            weights=[70, 20, 10],
            k=1,
        )[0]
        available_images = images_by_rarity[rarity]

        row = index // 5 if count == 10 else 0
        column = index % 5 if count == 10 else 0

        card = tk.Frame(results_frame, bg="#080700")
        card.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

        tk.Label(
            card,
            text=f"Pull {index + 1} - rarity {rarity}",
            bg="gold",
            fg="black",
        ).pack(pady=3)

        if not available_images:
            tk.Label(
                card,
                text="No images found",
                bg="#080700",
                fg="white",
            ).pack()
        else:
            image_path = random.choice(available_images)

            if count == 1:
                max_width = root.winfo_screenwidth() - 60
                max_height = root.winfo_screenheight() - 220
            else:
                max_width = root.winfo_screenwidth() // 5 - 30
                max_height = root.winfo_screenheight() // 2 - 100

            with Image.open(image_path) as source_image:
                source_image.thumbnail(
                    (max_width, max_height),
                    Image.Resampling.LANCZOS,
                )
                photo = ImageTk.PhotoImage(source_image.copy())

            picture = tk.Label(card, image=photo, bg="#080700")
            picture.image = photo  
            picture.pack(expand=True)

        
        root.after(350, reveal_pull, index + 1)

    reveal_pull(0)


tk.Button(root, text="Extract 1",bg="black", fg="gold", command=lambda: extract(1)).grid(
    row=0, column=1, sticky="ew", padx=10, pady=10
)

tk.Button(root, text="Extract 10",bg="black", fg="gold", command=lambda: extract(10)).grid(
    row=0, column=2, sticky="ew", padx=10, pady=10
)
result_label = tk.Label(root,bg="gold", fg="black", text="Click Extract to get a sinner")
result_label.grid(row=1, column=0, pady=5)
results_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
tk.Button(root, text="Close", command=root.destroy).grid(
    row=3, column=0, sticky="ew", padx=20, pady=10
)

root.config(bg="#080700") 

root.mainloop()


