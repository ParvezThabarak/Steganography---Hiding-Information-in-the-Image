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

# Homepage Interface
"Main interface of the Steganography Web App — where users can choose to either hide or reveal messages inside images."
![Screenshot 2025-06-26 195254](https://github.com/user-attachments/assets/0674e1bc-9e94-4180-b014-d53dd8b6ab7c)

# Encrypt & Embed Form
"User uploads an image, enters a secret message and encryption key to securely embed the message using steganography."
![Screenshot 2025-06-26 194315](https://github.com/user-attachments/assets/49749c2f-f8d8-4a4d-a6b2-59becc1201de)

# Successful Embedding
"Confirmation screen after successfully embedding the secret message — the user can download the encrypted image."
![Screenshot 2025-06-26 194355](https://github.com/user-attachments/assets/e9cea61d-3f7e-4c9c-a85e-7d1001aa84b7)

# Extract & Decrypt Form
"To retrieve the hidden message, the user uploads the encrypted image and provides the correct decryption key."
![Screenshot 2025-06-26 194620](https://github.com/user-attachments/assets/364f44eb-73c5-4454-9cdf-59667a835291)

# Message Decrypted
"The original secret message is successfully revealed after decryption — confirming secure and accurate message extraction."
![Screenshot 2025-06-26 194457](https://github.com/user-attachments/assets/bcf8400d-1d67-42a5-a9d8-ce7b6163e5e0)





