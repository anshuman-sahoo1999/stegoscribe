from setuptools import setup, find_packages

setup(
    name="stegoscribe",
    version="0.1.0",
    description="A robust image steganography framework with AES-256 encryption.",
    author="Anshuman Sahoo",
    author_email="anshuman.sahoo@driems.ac.in",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "cryptography",
        "click",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'stegoscribe=src.cli:main',  # This creates the command 'stegoscribe'
        ],
    },
)