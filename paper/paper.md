---
title: 'StegoScribe: A Dual-Domain Python Framework for Secure and Robust Image Steganography via Discrete Cosine Transform (DCT) and Least Significant Bit (LSB) Modulation with Integrated AES-256 Encryption'
tags:
  - Python
  - steganography
  - cryptography
  - image processing
  - security
  - DCT
  - LSB
  - research
authors:
  - name: Anshuman Sahoo
    orcid: 0000-0003-3719-6177
    affiliation: 1
    email: anshuman.sahoo@driems.ac.in
  - name: Raghunath Rout
    affiliation: 1
  - name: Ankita Parida
    affiliation: 1
  - name: Subhasish Mohapatra
    affiliation: 1
affiliations:
 - name: Department of Computer Science and Engineering, DRIEMS University, India
   index: 1
date: 17 January 2026
bibliography: paper.bib
---

# Summary

In the contemporary digital landscape, the security of data transmission is paramount. While cryptography protects the content of a message, it often raises suspicion by its very nature—an encrypted file is obviously a secret. Steganography, the art of hiding information within innocuous cover media, offers a complementary layer of security by concealing the *existence* of the communication itself. `StegoScribe` is a comprehensive, open-source Python research framework designed to bridge the gap between theoretical steganographic algorithms and practical, secure implementation.

`StegoScribe` uniquely integrates military-grade cryptography with a dual-domain embedding engine. Unlike traditional tools that rely solely on fragile spatial domain techniques, `StegoScribe` offers researchers the ability to switch between **Least Significant Bit (LSB)** modulation for high-capacity payloads and **Discrete Cosine Transform (DCT)** embedding for high robustness against compression. By enforcing an "Encrypt-then-Hide" paradigm using AES-256, the framework ensures that the semantic security of the payload remains intact even if the steganographic carrier is compromised. This software serves as both a secure communication tool and a workbench for researchers analyzing the trade-offs between embedding capacity, perceptual quality (PSNR), and statistical detectability.

# Statement of Need

The field of digital forensics and steganalysis requires robust tools to generate diverse datasets for training detection algorithms. However, a significant gap exists in the current open-source ecosystem. Many existing Python steganography libraries operate as "toy" implementations, offering basic LSB functionality without cryptographic pre-processing or quality validation [@moerland2003steganography]. Conversely, advanced research tools are often proprietary or implemented in complex C/C++ environments that are difficult to modify for rapid experimentation. `StegoScribe` addresses this need by providing a modular, pure-Python framework that is accessible to students and researchers while maintaining the mathematical rigor required for academic work [@fridrich2009steganography].

Furthermore, there is a critical need for tools that allow for the comparative analysis of spatial versus frequency domain embedding within a unified interface. Research in steganography often treats these domains in isolation [@subhedar2014current]. `StegoScribe` enables users to seamlessly toggle between high-capacity LSB embedding and robust DCT embedding. This capability is vital for researchers studying "channel robustness"—specifically, how different embedding algorithms survive image compression, resizing, and noise addition. By integrating an automated Peak Signal-to-Noise Ratio (PSNR) calculator, the tool provides immediate quantitative feedback on the imperceptibility of the hidden data, a standard metric in image processing literature [@wang2004image].

In addition to research utility, there is a practical need for "usable security" tools. Command-line interfaces (CLIs) are powerful for automation but often alienate non-technical users. `StegoScribe` bridges this usability gap by implementing a context-aware hybrid interface. It combines the scriptability of a CLI with native OS file-picker dialogs and automatic routing of output files to the user's local `Downloads` directory. This design lowers the barrier to entry for privacy advocates and educators who wish to demonstrate secure communication concepts without navigating complex file system paths.

Finally, the integration of cryptography is often overlooked in standard steganography tools, which frequently embed plaintext [@provos2003hide]. This practice leaves the hidden message vulnerable to trivial extraction if the embedding method is discovered. `StegoScribe` mandates the use of AES-256 encryption with PBKDF2HMAC key derivation [@kaliski2000pkcs], ensuring that the tool adheres to Kerckhoffs's principle: the security of the system relies on the secrecy of the key, not the obscurity of the algorithm [@shannon1949communication].

# Overview of the Workflow

The architecture of `StegoScribe` is built upon two primary distinct pipelines: the **Injection Pipeline (Sender)** and the **Extraction Pipeline (Receiver)**. Both pipelines are governed by a central controller that manages cryptographic key derivation and algorithm selection. The workflow begins with the cryptographic layer, where the user's plaintext payload is salted and hashed using SHA-256 to generate a 32-byte key. The payload is then encrypted using the Advanced Encryption Standard (AES) in Cipher Block Chaining (CBC) mode, ensuring that the data to be embedded appears as high-entropy random noise, which is statistically harder to distinguish from natural image noise than structured ASCII text [@daemen2002design].

For the embedding phase, the framework offers two distinct paths. In the **LSB Mode**, the system operates in the spatial domain. It decomposes the encrypted binary stream and distributes it across the least significant bits of the image's Red, Green, and Blue channels. This mode maximizes capacity, allowing for the concealment of large files or lengthy documents. The algorithm ensures that the modification to any single pixel is minimal ($\pm 1$ value), preserving the visual integrity of the cover image. Following embedding, the system calculates the Mean Squared Error (MSE) and PSNR to quantify the degradation, reporting these metrics to the user for quality assurance [@hu2015high].

![Figure 1: High-Level Architecture of the StegoScribe Workflow.](figure1.png)

In the **DCT Mode**, the system shifts to the frequency domain to achieve robustness. The workflow involves dividing the image's blue channel into $8 \times 8$ non-overlapping blocks. Each block undergoes a Discrete Cosine Transform, converting spatial pixel data into frequency coefficients. The payload bits are embedded into the mid-frequency coefficients using a Quantization Index Modulation (QIM) strategy with a tunable "persistence" factor. This persistence factor forces the coefficients deeply into "even" or "odd" quantization bins, ensuring that the hidden data survives floating-point rounding errors and mild lossy compression [@cox2002watermarking]. This complex mathematical transformation is handled transparently by the `StegoScribe` engine, abstracting the difficulty of frequency-domain manipulation from the user.

Finally, the Extraction Pipeline reverses these operations. A critical feature of `StegoScribe` is its failure-safe design. If the receiver attempts to extract data using the wrong password or the wrong algorithm (e.g., attempting LSB extraction on a DCT-encoded image), the cryptographic authentication layer will fail to validate the padding or signature. This prevents the system from outputting corrupted or "garbage" data, ensuring data integrity. The workflow concludes with the decrypted message being displayed to the user or saved to a secure location.

# Code Availability

The source code for `StegoScribe` is available on GitHub (https://github.com/anshuman-sahoo1999/stegoscribe.git). It is distributed under the MIT License to encourage academic collaboration and modification. The package is structured to be installed via `pip`, with dependencies limited to standard scientific libraries (`numpy`, `opencv-python`, `pillow`, `cryptography`, `click`) to ensure broad compatibility across Windows, macOS, and Linux environments.

# Planned Enhancements

Future development of `StegoScribe` will focus on:
1.  **AI-Driven Steganography:** Integrating Generative Adversarial Networks (GANs) to synthesize cover images from scratch, eliminating the need for existing cover media and defeating current cover-source mismatch detection algorithms [@goodfellow2014generative].
2.  **Audio Steganography:** Extending the module to support `.wav` and `.mp3` files using Parity Coding and Phase Coding techniques.
3.  **Steganalysis Suite:** Adding a "defense" module that allows users to scan images for suspicious statistical anomalies using Chi-Square attacks and RS analysis [@westfeld1999attacks].

# Author Contributions

* **Anshuman Sahoo:** Conceptualization, Lead Software Architecture, Implementation of DCT/LSB algorithms, Cryptography integration.
* **Raghunath Rout:** Supervision, Methodology validation, Theoretical framework guidance.
* **Ankita Parida:** Testing, Validation of robustness metrics, Documentation.
* **Subhasish Mohapatra:** Code review, Cross-platform compatibility testing, User Interface design.

# Acknowledgements

We acknowledge the support of the Department of Computer Science and Engineering at DRIEMS University for providing the computational resources necessary for the development and testing of this software.

# References

(References are compiled from the attached `paper.bib` file).
