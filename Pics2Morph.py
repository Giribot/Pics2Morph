import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, simpledialog, messagebox, Button, Toplevel
from tqdm import tqdm
import sys

def calculate_optical_flow(img1, img2, num_transitions):
    # Convert images to grayscale for optical flow
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate dense optical flow using Farneback method with optimized parameters
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 5, 20, 5, 7, 1.5, 0)

    h, w = gray1.shape
    flow_x, flow_y = flow[:, :, 0], flow[:, :, 1]

    results = []
    for alpha in np.linspace(0, 1, num_transitions + 1):
        flow_interpolated_x = alpha * flow_x
        flow_interpolated_y = alpha * flow_y

        # Create mapping coordinates
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        map_x = (map_x + flow_interpolated_x).astype(np.float32)
        map_y = (map_y + flow_interpolated_y).astype(np.float32)

        # Warp images with higher quality interpolation
        warped_img = cv2.remap(img1, map_x, map_y, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        results.append(warped_img)

    return results

def blend_images_sequence(img1, img2, warped_sequence, num_transitions):
    results = []
    for alpha, warped_img in zip(np.linspace(0, 1, num_transitions + 1), warped_sequence):
        blended_img = cv2.addWeighted(warped_img, 1 - alpha, img2, alpha, 0)
        results.append(blended_img)
    return results

def create_video_from_images(image_folder, output_path, fps):
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

    # Adjust the default value for number of transitions to 30 for smoother animation
    num_transitions = simpledialog.askinteger("Input", "Enter the number of transition images between each pair:", initialvalue=30)
    if not num_transitions or num_transitions <= 0:
        messagebox.showerror("Error", "Invalid number of transitions!")
        return

    fps = simpledialog.askinteger("Input", "Enter the desired frames per second for the video:", initialvalue=30)
    if not fps or fps <= 0:
        messagebox.showerror("Error", "Invalid FPS value!")
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

        warped_sequence = calculate_optical_flow(img1, img2, num_transitions)
        transitions = blend_images_sequence(img1, img2, warped_sequence, num_transitions)

        final_sequence.append(img1)
        final_sequence.extend(transitions)

    final_sequence.append(cv2.imread(os.path.join(folder_path, image_files[-1])))

    for idx, img in enumerate(tqdm(final_sequence, desc="Saving Images")):
        cv2.imwrite(os.path.join(output_dir, f"{idx:04d}.jpg"), img)

    video_path = os.path.join(output_dir, "morphing_video.mp4")
    create_video_from_images(output_dir, video_path, fps)

    show_success_window(output_dir)

if __name__ == "__main__":
    main()
