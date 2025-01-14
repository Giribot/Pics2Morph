import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, simpledialog, messagebox, Button, Toplevel
from tqdm import tqdm
import sys

def morph_images(img1, img2, num_transitions):
    transitions = []
    for i in range(num_transitions + 1):  # Include the second image in the last step
        alpha = i / num_transitions
        morphed_img = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        transitions.append(morphed_img)
    return transitions

def create_video_from_images(image_folder, output_path, fps, quality):
    images = sorted(
        [img for img in os.listdir(image_folder) if img.lower().endswith(('png', 'jpg', 'jpeg'))]
    )
    if not images:
        messagebox.showerror("Error", "No images found in the folder for video creation!")
        return

    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image in tqdm(images, desc="Creating Video"):
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()

def show_success_window(output_path):
    success_window = Toplevel()
    success_window.title("Success")

    message_label = Button(success_window, text=f"Morphing complete! Files saved at\n{output_path}", wraplength=400, state='disabled')
    message_label.pack(pady=10)

    quit_button = Button(success_window, text="Quit", command=lambda: (success_window.destroy(), sys.exit()))
    quit_button.pack(pady=10)

    success_window.mainloop()

def main():
    Tk().withdraw()

    folder_path = filedialog.askdirectory(title="Select a folder with images")
    if not folder_path:
        messagebox.showerror("Error", "No folder selected!")
        return

    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff'))]
    )
    if len(image_files) < 2:
        messagebox.showerror("Error", "The folder must contain at least two images!")
        return

    num_transitions = simpledialog.askinteger("Input", "Enter the number of transition images between each pair:", initialvalue=15)
    if not num_transitions or num_transitions <= 0:
        messagebox.showerror("Error", "Invalid number of transitions!")
        return

    fps = simpledialog.askinteger("Input", "Enter the desired frames per second for the video:", initialvalue=15)
    if not fps or fps <= 0:
        messagebox.showerror("Error", "Invalid FPS value!")
        return

    quality = simpledialog.askinteger("Input", "Enter the quality of the video (1-100, higher is better):", initialvalue=90)
    if not quality or quality < 1 or quality > 100:
        messagebox.showerror("Error", "Invalid quality value!")
        return

    output_dir = os.path.join(folder_path, f"Picsmorph_{image_files[0]}")
    os.makedirs(output_dir, exist_ok=True)

    final_sequence = []
    for i in tqdm(range(len(image_files) - 1), desc="Processing Images"):
        img1_path = os.path.join(folder_path, image_files[i])
        img2_path = os.path.join(folder_path, image_files[i + 1])

        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1.shape != img2.shape:
            messagebox.showerror("Error", f"Images {image_files[i]} and {image_files[i+1]} have different dimensions!")
            return

        transitions = morph_images(img1, img2, num_transitions)

        final_sequence.append(img1)
        final_sequence.extend(transitions)

    final_sequence.append(cv2.imread(os.path.join(folder_path, image_files[-1])))

    for idx, img in enumerate(tqdm(final_sequence, desc="Saving Images")):
        cv2.imwrite(os.path.join(output_dir, f"{idx:04d}.jpg"), img)

    video_path = os.path.join(output_dir, "morphing_video.mp4")
    create_video_from_images(output_dir, video_path, fps, quality)

    show_success_window(output_dir)

if __name__ == "__main__":
    main()
