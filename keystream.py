import hashlib

PBKDF2_ITERS = 200_000
SALT_LEN = 16  # caller generates with os.urandom(SALT_LEN)


def derive_key_material(password: str, salt: bytes, iters: int = PBKDF2_ITERS) -> bytes:
    """Derive a 32-byte key from password+salt using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iters, dklen=32)


def rails_from_key(key_material: bytes) -> int:
    """Pick rail count (4–8) deterministically from key material."""
    return 4 + (key_material[0] % 5)


def keystream(password: str, salt: bytes):
    """Generate a pseudo-random byte stream using SHA-256 in counter mode."""
    counter = 0
    base = password.encode('utf-8') + salt
    while True:
        ctr = counter.to_bytes(8, 'big')
        block = hashlib.sha256(base + ctr).digest()
        for b in block:
            yield b
        counter += 1


def xor_bytes(data: bytes, stream) -> bytes:
    """XOR a byte string with a generated keystream."""
    return bytes(b ^ next(stream) for b in data)