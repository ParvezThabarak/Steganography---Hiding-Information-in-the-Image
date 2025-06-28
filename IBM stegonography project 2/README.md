# Steganography Web App

A secure web application for hiding (encrypting) and extracting secret messages inside images using AES encryption and LSB steganography.

## Features
- AES-CBC encryption with PBKDF2 + salt
- LSB steganography for hiding encrypted data in images
- Flask web interface for upload, encryption, decryption, and download
- Capacity check to ensure message fits in image
- Clean, modern UI (Bulma CSS)

## Folder Structure
```
.
├── app.py                  # Flask web app
├── stegano_utils.py        # Core encryption & steganography logic
├── requirements.txt        # Python dependencies
├── static/
│   ├── uploads/            # Uploaded images
│   └── encrypted/          # Encrypted images
└── templates/
    ├── index.html          # Main UI
    ├── result.html         # Shows encrypted image
    └── decrypted.html      # Shows decrypted message
```

## Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python app.py
   ```

3. **Open in browser**
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage
- **Encrypt:** Upload an image, enter your secret message and key, and download the encrypted image.
- **Decrypt:** Upload an encrypted image and enter the key to reveal the hidden message.

## Security Notes
- Uses AES-CBC with PBKDF2 key derivation and random salt/IV.
- Checks image capacity before embedding.
- Only PNG/JPG/JPEG images are allowed.

---

**Enjoy secure steganography!** 