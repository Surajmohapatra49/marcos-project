import cv2
import os
import numpy as np
import hashlib
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def embed_message(img, msg, password):
    key = generate_key()
    encrypted_msg = encrypt_message(msg, key)
    hashed_password = hash_password(password)
    final_data = hashed_password.encode() + b'|' + key + b'|' + encrypted_msg

    if len(final_data) * 8 > img.size:
        raise ValueError("Message too large for the image provided.")

    binary_data = np.unpackbits(np.frombuffer(final_data, dtype=np.uint8))
    flat_img = img.flatten()

    flat_img[:len(binary_data)] = np.bitwise_and(flat_img[:len(binary_data)], 0xFE) | binary_data

    img = flat_img.reshape(img.shape)
    output_filename = f"advanced_encrypted_image_{np.random.randint(1000, 9999)}.png"
    cv2.imwrite(output_filename, img)
    print(f"Message embedded with encryption and saved as '{output_filename}'")

def extract_message(img, password):
    flat_img = img.flatten()
    binary_data = flat_img & 1
    all_bytes = np.packbits(binary_data)

    try:
        data_str = all_bytes.tobytes()
        if b'|' not in data_str:
            raise ValueError("No embedded data found.")

        hashed_password, key, encrypted_msg = data_str.split(b'|', 2)
        if hash_password(password).encode() == hashed_password:
            decrypted_msg = decrypt_message(encrypted_msg, key)
            output_file = f"decrypted_message_{np.random.randint(1000, 9999)}.txt"
            with open(output_file, "w") as file:
                file.write(decrypted_msg)
            print(f"Decrypted message saved as '{output_file}'")
        else:
            print("YOU ARE NOT AUTHORIZED")
    except Exception as e:
        print("Error in decryption:", str(e))

def main():
    print("--- Advanced Steganography Project for Marcos Commando ---")
    img_path = input("Enter the path of the image: ")
    img = cv2.imread(img_path)

    if img is None:
        print("Invalid image path.")
        return

    choice = input("Do you want to (1) Encode or (2) Decode a message? (1/2): ").strip()

    if choice == '1':
        msg = input("Enter the secret message: ")
        password = input("Enter a passcode: ")
        embed_message(img, msg, password)

    elif choice == '2':
        password = input("Enter the passcode used during embedding: ")
        extract_message(img, password)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
