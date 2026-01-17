import base64
import os
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class StegoEngine:
    def __init__(self):
        self.end_marker = "-----EOF-----"  # Marks end of message

    def _generate_key(self, password: str, salt: bytes) -> bytes:
        """Derives a strong AES key from the user password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_message(self, message: str, password: str) -> str:
        """Encrypts text using AES-256."""
        salt = os.urandom(16)  # Generate random salt
        key = self._generate_key(password, salt)
        f = Fernet(key)
        encrypted_bytes = f.encrypt(message.encode())
        # We prepend salt to the message so we can recover it later
        combined = base64.urlsafe_b64encode(salt + b"::" + encrypted_bytes).decode()
        return combined + self.end_marker

    def decrypt_message(self, encrypted_string: str, password: str) -> str:
        """Decrypts text using AES-256."""
        try:
            # Remove marker
            clean_string = encrypted_string.replace(self.end_marker, "")
            decoded = base64.urlsafe_b64decode(clean_string)
            
            # Split salt and data
            salt, encrypted_data = decoded.split(b"::", 1)
            
            key = self._generate_key(password, salt)
            f = Fernet(key)
            return f.decrypt(encrypted_data).decode()
        except Exception:
            return None

    def embed_data(self, image_path, secret_message, output_path):
        """Hides encrypted string into image LSB."""
        img = Image.open(image_path).convert('RGB')
        encoded = img.copy()
        width, height = img.size
        
        # Convert message to binary
        binary_msg = ''.join(format(ord(i), '08b') for i in secret_message)
        data_len = len(binary_msg)
        
        if data_len > width * height * 3:
            raise ValueError("Message too large for this image!")

        data_index = 0
        pixels = encoded.load()

        for y in range(height):
            for x in range(width):
                if data_index < data_len:
                    r, g, b = pixels[x, y]
                    
                    # Modify Red channel LSB
                    if data_index < data_len:
                        r = (r & ~1) | int(binary_msg[data_index])
                        data_index += 1
                    
                    # Modify Green channel LSB
                    if data_index < data_len:
                        g = (g & ~1) | int(binary_msg[data_index])
                        data_index += 1
                    
                    # Modify Blue channel LSB
                    if data_index < data_len:
                        b = (b & ~1) | int(binary_msg[data_index])
                        data_index += 1
                        
                    pixels[x, y] = (r, g, b)
                else:
                    break
        
        encoded.save(output_path)
        return img, encoded # Return both for PSNR calc

    def extract_data(self, image_path):
        """Extracts binary data from image LSB."""
        img = Image.open(image_path).convert('RGB')
        binary_data = ""
        pixels = img.load()
        width, height = img.size

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

        # Convert binary to string chunks
        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        decoded_string = ""
        
        for byte in all_bytes:
            decoded_string += chr(int(byte, 2))
            if decoded_string.endswith(self.end_marker):
                return decoded_string
        
        return decoded_string # Fallback