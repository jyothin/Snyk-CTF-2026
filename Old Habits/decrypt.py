#!/usr/bin/env python3
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

def xor_decrypt(data, key):
    """XOR decryption with repeating key"""
    key_bytes = key.encode() if isinstance(key, str) else key
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

def aes_decrypt(data, key):
    """Try AES decryption in different modes"""
    try:
        # Derive a proper 16/24/32 byte key from the password
        key_hash = hashlib.md5(key.encode()).digest()  # 16 bytes for AES-128
        
        # Try ECB mode
        try:
            cipher = AES.new(key_hash, AES.MODE_ECB)
            decrypted = cipher.decrypt(data)
            return unpad(decrypted, AES.block_size)
        except:
            pass
            
        # Try without unpad
        try:
            cipher = AES.new(key_hash, AES.MODE_ECB)
            return cipher.decrypt(data)
        except:
            pass
    except:
        pass
    return None

def is_printable(data):
    """Check if data contains printable text"""
    try:
        text = data.decode('ascii')
        return all(c.isprintable() or c in '\n\r\t' for c in text)
    except:
        return False

def main():
    # Read encrypted file
    with open('cipher.bin', 'rb') as f:
        ciphertext = f.read()
    
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Ciphertext (hex): {ciphertext.hex()}\n")
    
    # Read wordlist
    with open('wordlist.txt', 'r') as f:
        wordlist = [line.strip() for line in f if line.strip()]
    
    print(f"Trying {len(wordlist)} keys from wordlist...\n")
    
    for i, key in enumerate(wordlist):
        # Try XOR decryption
        try:
            decrypted = xor_decrypt(ciphertext, key)
            if is_printable(decrypted):
                print(f"[SUCCESS] XOR Decryption with key: {key}")
                print(f"Decrypted text: {decrypted.decode('ascii')}")
                with open('decrypted.txt', 'w') as f:
                    f.write(decrypted.decode('ascii'))
                return
        except:
            pass
        
        # Try AES decryption
        try:
            decrypted = aes_decrypt(ciphertext, key)
            if decrypted and is_printable(decrypted):
                print(f"[SUCCESS] AES Decryption with key: {key}")
                print(f"Decrypted text: {decrypted.decode('ascii')}")
                with open('decrypted.txt', 'w') as f:
                    f.write(decrypted.decode('ascii'))
                return
        except:
            pass
        
        if (i + 1) % 100 == 0:
            print(f"Tried {i + 1} keys...")
    
    print("\n[FAILED] No valid decryption found with any key from wordlist")

if __name__ == '__main__':
    main()
