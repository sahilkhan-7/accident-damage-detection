# This code generates a secret key for the Flask application.

import os
import binascii

def generate_secret_key():
    return binascii.hexlify(os.urandom(16)).decode()

SECRET_KEY = generate_secret_key()
print(SECRET_KEY)