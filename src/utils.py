import math
import numpy as np

def calculate_psnr(original_img, stego_img):
    """
    Calculates Peak Signal-to-Noise Ratio (PSNR).
    Higher PSNR (>30dB) indicates better quality (harder to detect).
    """
    # Convert images to numpy arrays
    img1 = np.array(original_img)
    img2 = np.array(stego_img)

    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100.0  # Images are identical
    
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return round(psnr, 2)