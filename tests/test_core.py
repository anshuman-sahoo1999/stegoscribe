import unittest
import os
from PIL import Image
from src.core import StegoEngine
from src.utils import calculate_psnr

class TestStegoScribe(unittest.TestCase):

    def setUp(self):
        """Set up a dummy image for testing."""
        self.engine = StegoEngine()
        self.test_image_path = "test_img.png"
        self.output_path = "test_stego.png"
        self.password = "strongpassword123"
        self.secret_message = "This is a JOSS test message."
        
        # Create a blank red image for testing
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.test_image_path)

    def test_encryption_decryption(self):
        """Test if encryption and decryption logic works consistently."""
        encrypted = self.engine.encrypt_message(self.secret_message, self.password)
        decrypted = self.engine.decrypt_message(encrypted, self.password)
        self.assertEqual(self.secret_message, decrypted)

    def test_wrong_password(self):
        """Test that wrong passwords fail to decrypt."""
        encrypted = self.engine.encrypt_message(self.secret_message, self.password)
        decrypted = self.engine.decrypt_message(encrypted, "wrongpassword")
        self.assertIsNone(decrypted)

    def test_embedding_extraction(self):
        """Test the full hide/unhide cycle with an image."""
        # 1. Encrypt
        encrypted_msg = self.engine.encrypt_message(self.secret_message, self.password)
        
        # 2. Embed
        self.engine.embed_data(self.test_image_path, encrypted_msg, self.output_path)
        
        # 3. Extract
        extracted_raw = self.engine.extract_data(self.output_path)
        
        # 4. Decrypt
        final_msg = self.engine.decrypt_message(extracted_raw, self.password)
        
        self.assertEqual(self.secret_message, final_msg)

    def test_psnr_quality(self):
        """Test that the image quality remains high (PSNR > 50 for small text)."""
        encrypted_msg = self.engine.encrypt_message("small", self.password)
        original, stego = self.engine.embed_data(self.test_image_path, encrypted_msg, self.output_path)
        
        psnr = calculate_psnr(original, stego)
        # PSNR should be very high (or 100) for such a small change
        self.assertGreater(psnr, 30.0)

    def tearDown(self):
        """Clean up generated files."""
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == '__main__':
    unittest.main()