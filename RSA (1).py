# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 21:02:56 2022

@author: Nix
"""
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import tracemalloc

tracemalloc.start()
def double_Keygen():
    for i in range(2):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=1024
        )
        
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )
        
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

double_Keygen()
x= list(tracemalloc.get_traced_memory())
print(x[1]-x[0])
tracemalloc.stop()