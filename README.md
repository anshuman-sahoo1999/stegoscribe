# StegoScribe: Secure & Robust Image Steganography Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StegoScribe** is a research-grade Python framework designed for secure and robust image steganography. It serves as a unified platform for comparing spatial domain (LSB) and frequency domain (DCT) embedding techniques, enforced by a mandatory "Encrypt-then-Hide" security architecture.

Designed for researchers, students, and privacy advocates, StegoScribe bridges the gap between theoretical algorithms and practical, user-friendly implementation.

---

## Objectives & Statement of Need

Current open-source steganography tools often suffer from three critical limitations:
1. **Lack of Robustness:** Most tools rely on fragile LSB techniques that break under minor compression.
2. **Weak Security:** Many tools embed plaintext, making detection equivalent to extraction.
3. **No Metrics:** Few tools provide immediate feedback on image quality (PSNR) for research analysis.

**StegoScribe addresses these gaps by providing:**
* **Dual-Domain Engine:** Switch seamlessly between High-Capacity LSB and Robust DCT algorithms.
* **Integrated Cryptography:** Automates AES-256 encryption with PBKDF2HMAC key derivation.
* **Scientific Validation:** Automatically calculates Peak Signal-to-Noise Ratio (PSNR) for every operation.

---

## Key Features

### 1. Hybrid Embedding Algorithms
* **LSB Mode (Spatial):** Modifies the Least Significant Bits of RGB channels. Ideal for hiding large files or long documents in PNG images.
* **DCT Mode (Frequency):** Uses Discrete Cosine Transform and Quantization Index Modulation (QIM). Embeds data into frequency coefficients, ensuring the message survives floating-point conversions and mild compression.

### 2. Military-Grade Security
* **AES-256 Encryption:** All payloads are encrypted in CBC mode before embedding.
* **Salted Keys:** User passwords are salted and hashed using SHA-256 (100,000 iterations), preventing rainbow table attacks.

### 3. Usability & Automation
* **OS-Agnostic Downloads:** Output files are automatically saved to your system's `Downloads` folder (Windows/macOS/Linux compatible).
* **GUI/CLI Hybrid:** A command-line interface for speed, paired with native file-picker dialogs for ease of use.

---

## Installation

### Prerequisites
* Python 3.8 or higher

### Install via pip (Local Development)
```bash
git clone https://github.com/anshuman-sahoo1999/stegoscribe.git
cd stegoscribe
pip install -e .
```

---

## Usage Guide

StegoScribe operates via a simple Command Line Interface (CLI).

### 1. Hiding Data (Sender)

Run the hide command and choose your method (`lsb` or `dct`).

#### Option A: High Capacity (LSB)
```bash
stegoscribe hide --method lsb
```
* **Best for:** Large text, documents, clean PNGs.
* **Effect:** Minimum visual distortion, but fragile.

#### Option B: High Robustness (DCT)
```bash
stegoscribe hide --method dct
```
* **Best for:** Short passwords, coordinates, keys.
* **Effect:** Survives image processing/resizing better.

**The Workflow:**
1. A file dialog opens. Select your cover image.
2. Enter your secret message and a strong password.
3. The system encrypts the data, embeds it, and automatically downloads the result to your `Downloads/` folder.
4. It reports the **PSNR Score** (e.g., 52.4 dB) to verify quality.

### Unhiding Data (Receiver)

Run the unhide command. You must know which method was used.

```bash
stegoscribe unhide --method lsb
# OR
stegoscribe unhide --method dct
```

**The Workflow:**
1. A file dialog opens. Select the stego-image.
2. Enter the password.
3. If the password is correct, the secret message is revealed.

**Security Check:** If the password is wrong or the image is corrupted, the decryption fails silently.

---

## Scientific Metrics (For Researchers)

StegoScribe calculates **PSNR (Peak Signal-to-Noise Ratio)** to measure image fidelity.

$$PSNR = 10 \cdot \log_{10} \left( \frac{MAX_I^2}{MSE} \right)$$

* **> 40 dB:** Excellent quality (Invisible to human eye).
* **30-40 dB:** Good quality (Minor artifacts may be visible).
* **< 30 dB:** Poor quality (Visible distortion).

---

## Planned Enhancements

* **Steganalysis Module:** Integration of Chi-Square and RS Analysis for detection.
* **Audio Support:** Extension to `.wav` files using Parity Coding.
* **AI Integration:** GAN-based cover image generation.

---

## Authors & Affiliations

* **Anshuman Sahoo** (Corresponding Author) - [ORCID]
* **Raghunath Rout**
* **Ankita Parida**
* **Subhasish Mohapatra**

**Department of Computer Science and Engineering, DRIEMS University, India.**

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

Special thanks to the **Dept. of CSE, DRIEMS University** for computational resources.
