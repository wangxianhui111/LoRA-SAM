import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=730, height=730)
        self.canvas.pack()

        self.select_button = tk.Button(root, text="选择图片", command=self.load_image)
        self.select_button.pack(side=tk.LEFT)

        self.sample_button = tk.Button(root, text="生成样本点", command=self.generate_and_display_samples)
        self.sample_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(root, text="退出", command=root.quit)
        self.quit_button.pack(side=tk.RIGHT)

        self.image_path = ''
        self.image = None
        self.photo = None
        self.pointa = None

        self.canvas.bind("<Button-1>", self.mark_point)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if not self.image_path:
            return
        self.image = Image.open(self.image_path).convert("RGB")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.pointa = None

    def mark_point(self, event):
        self.pointa = (event.x, event.y)
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill='red')

    def generate_and_display_samples(self):
        if not self.image or not self.pointa:
            return
        samples = self.generate_samples(self.image, self.pointa)
        for x, y in samples:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='blue')

    def generate_samples(self, image, pointa):
        # Simplified Algorithm A

        samples = []
        optimized_samples = []
        block_size = 13
        stride = 7
        min_distance = 40  # Minimum distance between points
        width, height = image.size

        # Extract the reference block
        reference_block = np.array(image.crop((pointa[0] - 6, pointa[1] - 6, pointa[0] + 7, pointa[1] + 7)))
        print(reference_block.shape)

        for y in range(0, height - block_size + 1, stride):
            for x in range(0, width - block_size + 1, stride):
                block = np.array(image.crop((x, y, x + block_size, y + block_size)))

                # Calculate similarity (using sum of absolute differences of each element here)
                similarity = np.sum(np.abs(block - reference_block))
                if similarity < 20000:  # You need to define a suitable threshold
                    samples.append((x + block_size // 2, y + block_size // 2))

        # Optimization to ensure all points are at least min_distance apart
        for sample in samples:
            if all(np.linalg.norm(np.array(sample) - np.array(existing_sample)) >= min_distance for existing_sample in
                   optimized_samples):
                optimized_samples.append(sample)

        return optimized_samples


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()
