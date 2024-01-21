import cv2
import numpy as np

def compare_images(img1_path, img2_path, mse_threshold=60):
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("Error loading images.")
        return False

    # Convert images to grayscale
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Convert images to NumPy arrays
    np_img1 = np.array(gray_img1)
    np_img2 = np.array(gray_img2)

    # Calculate Mean Squared Error (MSE)
    mse = np.sum((np_img1 - np_img2) ** 2) / float(np_img1.shape[0] * np_img1.shape[1])

    print(f"Mean Squared Error (MSE): {mse}")

    # Compare images based on MSE
    if mse < mse_threshold:
        print("Images are similar.")
        return True
    else:
        print("Images are not similar.")
        return False

if __name__ == "__main__":
    img1_path = "C:/Users/HP/Desktop/captured_frames/frame_2.png"
    img2_path = "C:/Users/HP/Desktop/captured_frames/frame_1.png"

    result = compare_images(img1_path, img2_path)

    if result:
        print("Images match.")
    else:
        print("Images do not match.")
