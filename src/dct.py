import cv2
import numpy as np
import math

class DCTStego:
    def __init__(self):
        self.block_size = 8
        self.end_marker = "-----EOF-----"
        # Persistence: How strongly we modify the image. 
        # Higher = More robust against errors, but slightly more visible changes.
        self.persistence = 50 

    def to_bits(self, message):
        """Converts string to a list of bits."""
        bits = []
        for char in message:
            bin_val = bin(ord(char))[2:].zfill(8)
            bits.extend([int(b) for b in bin_val])
        return bits

    def from_bits(self, bits):
        """Converts list of bits back to string."""
        chars = []
        for b in range(len(bits) // 8):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return "".join(chars)

    def embed_dct(self, image_path, message, output_path):
        """
        Embeds message into the Blue channel using DCT with Persistence.
        """
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Image not found.")
            
        height, width, channels = img.shape
        
        # Use Blue channel
        b_channel = img[:, :, 0].astype(np.float32)
        
        msg_bits = self.to_bits(message + self.end_marker)
        total_bits = len(msg_bits)
        
        bit_idx = 0
        
        # Iterate 8x8 blocks
        for row in range(0, height, self.block_size):
            for col in range(0, width, self.block_size):
                if bit_idx < total_bits:
                    block = b_channel[row:row+self.block_size, col:col+self.block_size]
                    dct_block = cv2.dct(block)
                    
                    # Target the DC coefficient (0,0) or Low Freq (1,1) for max robustness
                    # We use (4,4) for balance between robustness and invisibility
                    val = dct_block[4, 4]
                    
                    bit = msg_bits[bit_idx]
                    
                    # ROBUST LOGIC:
                    # We map '0' to positive multiples of persistence
                    # We map '1' to negative multiples (or shifted values)
                    # Simple QIM (Quantization Index Modulation):
                    # Quantize to nearest multiple of persistence
                    
                    step = self.persistence
                    
                    if bit == 0:
                        # Force to nearest EVEN multiple of step (e.g., 0, 100, 200)
                        val = round(val / step) * step
                        if (val / step) % 2 != 0:
                            val += step # Make it even
                    else:
                        # Force to nearest ODD multiple of step (e.g., 50, 150)
                        val = round(val / step) * step
                        if (val / step) % 2 == 0:
                            val += step # Make it odd

                    dct_block[4, 4] = val
                    
                    # Inverse DCT
                    idct_block = cv2.idct(dct_block)
                    b_channel[row:row+self.block_size, col:col+self.block_size] = idct_block
                    
                    bit_idx += 1
        
        # Merge and Save
        img[:, :, 0] = np.clip(b_channel, 0, 255).astype(np.uint8)
        
        # IMPORTANT: We must save as PNG first to avoid double-compression loss immediately
        # If the user wants JPG output, we should warn them, but for code stability we use PNG extensions
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            output_path = output_path.rsplit('.', 1)[0] + ".png"
            
        cv2.imwrite(output_path, img)
        return image_path, output_path

    def extract_dct(self, image_path):
        """Extracts message using the same Persistence logic."""
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Image not found.")
            
        height, width, _ = img.shape
        b_channel = img[:, :, 0].astype(np.float32)
        
        extracted_bits = []
        step = self.persistence
        
        for row in range(0, height, self.block_size):
            for col in range(0, width, self.block_size):
                block = b_channel[row:row+self.block_size, col:col+self.block_size]
                dct_block = cv2.dct(block)
                
                val = dct_block[4, 4]
                
                # Robust extraction: Round to nearest step
                nearest_multiple = round(val / step)
                
                if nearest_multiple % 2 == 0:
                    extracted_bits.append(0)
                else:
                    extracted_bits.append(1)

        # Reassemble
        full_msg = self.from_bits(extracted_bits)
        
        if self.end_marker in full_msg:
            return full_msg.split(self.end_marker)[0]
        else:
            # Return raw garbage for debugging if marker not found
            return full_msg[:50] + "..."