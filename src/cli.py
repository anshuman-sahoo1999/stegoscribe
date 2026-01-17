import click
import tkinter as tk
from tkinter import filedialog
import os
import time
from pathlib import Path
from src.core import StegoEngine
from src.dct import DCTStego
from src.utils import calculate_psnr
from PIL import Image

# Initialize Engines
lsb_engine = StegoEngine()
dct_engine = DCTStego()

def get_file_path(title="Select File"):
    """Opens a native OS file dialog to select an image."""
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    root.attributes('-topmost', True) # Bring to front
    file_path = filedialog.askopenfilename(title=title)
    return file_path

def get_downloads_folder():
    """Reliably finds the user's Downloads folder on Windows, Mac, or Linux."""
    if os.name == 'nt':  # Windows
        # Standard location for Windows
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        # Standard location for Mac/Linux
        return os.path.join(os.path.expanduser("~"), "Downloads")

@click.group()
def main():
    """StegoScribe: Advanced Steganography Tool."""
    pass

@main.command()
@click.option('--method', type=click.Choice(['lsb', 'dct']), default='lsb', help='Choose "lsb" for capacity or "dct" for robustness.')
def hide(method):
    """Encrypt and Hide a message."""
    click.echo(f"MODE: {method.upper()}")
    click.echo(">>> Opening file dialog...")
    
    # 1. Select Source Image
    image_path = get_file_path("Select Source Image")
    if not image_path:
        click.echo("No file selected. Aborting.")
        return

    # 2. Input Data
    message = click.prompt("Enter secret message")
    password = click.prompt("Set password", hide_input=True)
    
    click.echo("\n[1/3] Encrypting data...")
    encrypted_msg = lsb_engine.encrypt_message(message, password)
    
    # 3. Determine Output Path (The "Download" Logic)
    downloads_folder = get_downloads_folder()
    timestamp = int(time.time())
    output_filename = f"stego_{method}_{timestamp}.png"
    output_path = os.path.join(downloads_folder, output_filename)
    
    click.echo(f"[2/3] Embedding data using {method.upper()}...")
    
    try:
        if method == 'lsb':
            original, stego = lsb_engine.embed_data(image_path, encrypted_msg, output_path)
        else:
            # DCT Mode
            original_path, stego_path = dct_engine.embed_dct(image_path, encrypted_msg, output_path)
            original = Image.open(original_path)
            stego = Image.open(stego_path)

        # Scientific Metric
        psnr = calculate_psnr(original, stego)
        
        click.echo("-" * 50)
        click.echo(f"✔ SUCCESS! Image 'downloaded' to: \n{output_path}")
        click.echo("-" * 50)
        click.echo(f"QUALITY METRIC (PSNR): {psnr} dB")
        if psnr > 40:
            click.echo("(Excellent quality. Invisible to human eye.)")
        click.echo("-" * 50)
        
    except ValueError as v:
        click.echo(f"Capacity Error: {v}")
    except Exception as e:
        click.echo(f"Error: {e}")

@main.command()
@click.option('--method', type=click.Choice(['lsb', 'dct']), default='lsb', help='Must match the method used to hide.')
def unhide(method):
    """Reveal a message."""
    click.echo(f"MODE: {method.upper()}")
    click.echo(">>> Opening file dialog to find Stego Image...")
    
    # Receiver selects image from their system
    image_path = get_file_path("Select Stego Image")
    
    if not image_path:
        click.echo("No file selected.")
        return

    password = click.prompt("Enter decryption password", hide_input=True)
    
    click.echo("\n[1/2] Extracting...")
    try:
        if method == 'lsb':
            extracted_raw = lsb_engine.extract_data(image_path)
        else:
            extracted_raw = dct_engine.extract_dct(image_path)
        
        click.echo("[2/2] Decrypting...")
        decrypted_msg = lsb_engine.decrypt_message(extracted_raw, password)
        
        if decrypted_msg:
            click.echo("\n" + "="*40)
            click.echo(f"SECRET MESSAGE: {decrypted_msg}")
            click.echo("="*40)
        else:
            click.echo("\n[ERROR] Decryption failed! Wrong password or corrupted image.")
            
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    main()