import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import cv2
import os
import struct

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=32, count=100_000)

# ========================= ENCRYPTION =========================
def encrypt_message(message: str, password: str) -> bytes:
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return salt + iv + ciphertext  # total: 16 + 16 + len(cipher)


def decrypt_message(data: bytes, password: str) -> str:
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()

# ========================= STEGANOGRAPHY =========================
def embed_data_into_image(image: np.ndarray, data: bytes) -> np.ndarray:
    flat_image = image.flatten()
    if len(data) * 8 > len(flat_image):
        raise ValueError("Image not large enough to hold the data")

    for i in range(len(data) * 8):
        byte_idx = i // 8
        bit_idx = 7 - (i % 8)
        bit = (data[byte_idx] >> bit_idx) & 1
        flat_image[i] = (flat_image[i] & 0xFE) | bit

    return flat_image.reshape(image.shape)


def extract_data_from_image(image: np.ndarray, data_len: int) -> bytes:
    flat_image = image.flatten()
    bits = []
    for i in range(data_len * 8):
        bits.append(flat_image[i] & 1)

    byte_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        byte_list.append(byte)
    return bytes(byte_list)

# ========================= UTILS =========================
def max_data_capacity(image: np.ndarray) -> int:
    return image.size // 8

def load_image(path: str) -> np.ndarray:
    return cv2.imread(path)

def save_image(path: str, image: np.ndarray):
    cv2.imwrite(path, image)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def prepend_length(data: bytes) -> bytes:
    """Prepends a 4-byte big-endian length to the data."""
    return struct.pack('>I', len(data)) + data

def extract_length(data: bytes) -> (int, bytes):
    """Extracts the 4-byte big-endian length and returns (length, rest_of_data)."""
    length = struct.unpack('>I', data[:4])[0]
    return length, data[4:] 