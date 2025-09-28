import base64
import json
import os
from dataclasses import dataclass

from morse import to_morse, from_morse
from transposition import rail_fence_encrypt, rail_fence_decrypt
from keystream import (
    derive_key_material,
    rails_from_key,
    keystream,
    xor_bytes,
    PBKDF2_ITERS,
    SALT_LEN,
)

VERSION = 3  # custom (no standard cipher) build


@dataclass
class Envelope:
    """Metadata + encrypted data (JSON envelope)."""
    version: int
    kdf: str
    iters: int
    salt_hex: str
    rails: int
    data_b64: str

    def to_json(self) -> str:
        """Convert envelope to a JSON string."""
        return json.dumps(
            {
                "version": self.version,
                "kdf": self.kdf,
                "iters": self.iters,
                "salt": self.salt_hex,
                "rails": self.rails,
                "data": self.data_b64,
            },
            indent=2,
        )

    @staticmethod
    def from_json(s: str) -> "Envelope":
        """Parse JSON back into an Envelope object."""
        obj = json.loads(s)
        for k in ("version", "kdf", "iters", "salt", "rails", "data"):
            if k not in obj:
                raise ValueError(f"Missing field: {k}")
        return Envelope(
            version=int(obj["version"]),
            kdf=str(obj["kdf"]),
            iters=int(obj["iters"]),
            salt_hex=str(obj["salt"]),
            rails=int(obj["rails"]),
            data_b64=str(obj["data"]),
        )


def encrypt_text(plaintext: str, password: str) -> str:
    """Encrypt text using: Morse substitution → rail-fence → XOR keystream."""
    salt = os.urandom(SALT_LEN)
    key_material = derive_key_material(password, salt, PBKDF2_ITERS)
    rails = rails_from_key(key_material)

    morse = to_morse(plaintext)
    transposed = rail_fence_encrypt(morse, rails)
    ct = xor_bytes(transposed.encode("utf-8"), keystream(password, salt))

    env = Envelope(
        version=VERSION,
        kdf="PBKDF2-HMAC-SHA256+SHA256-CTR-XOR",
        iters=PBKDF2_ITERS,
        salt_hex=salt.hex(),
        rails=rails,
        data_b64=base64.b64encode(ct).decode("ascii"),
    )
    return env.to_json()


def decrypt_text(envelope_json: str, password: str) -> str:
    """Decrypt text previously encrypted by encrypt_text()."""
    env = Envelope.from_json(envelope_json)
    if env.version != VERSION:
        raise ValueError(f"Unsupported version: {env.version}")

    salt = bytes.fromhex(env.salt_hex)
    ct = base64.b64decode(env.data_b64)
    transposed_bytes = xor_bytes(ct, keystream(password, salt))
    transposed = transposed_bytes.decode("utf-8")

    morse = rail_fence_decrypt(transposed, env.rails)
    return from_morse(morse)


# ---------- TXT-only File helpers ----------

def _ensure_txt(path: str, role: str) -> None:
    """Ensure a file path ends with .txt; raise otherwise."""
    if not path.lower().endswith(".txt"):
        raise ValueError(f"{role} must be a .txt file: {path}")


def encrypt_file(in_path: str, out_path: str, password: str) -> None:
    """Read plaintext TXT, encrypt, and save encrypted JSON envelope to TXT."""
    _ensure_txt(in_path, "Input")
    _ensure_txt(out_path, "Output")
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")

    with open(in_path, "r", encoding="utf-8") as f:
        plaintext = f.read()
    env_json = encrypt_text(plaintext, password)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(env_json)


def decrypt_file(in_path: str, out_path: str, password: str) -> None:
    """Read encrypted TXT (JSON envelope), decrypt, and save plaintext to TXT."""
    _ensure_txt(in_path, "Input")
    _ensure_txt(out_path, "Output")
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")

    with open(in_path, "r", encoding="utf-8") as f:
        env_json = f.read()
    plaintext = decrypt_text(env_json, password)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(plaintext)


# ---------- Simple TXT-only CLI ----------

def _menu() -> None:
    """Display the text-based menu for encryption/decryption."""
    print("\nMorse Secure Cipher — Custom (No Standard Cipher) [TXT I/O]")
    print("-----------------------------------------------------------")
    print("1) Encrypt a TXT file")
    print("2) Decrypt a TXT file")
    print("3) Quit")


if __name__ == "__main__":
    import getpass

    while True:
        try:
            _menu()
            choice = input("Choose an option (1-3): ").strip()
            if choice == "1":
                inp = input("Input plaintext file path (.txt): ").strip()
                outp = input("Output ENCRYPTED file path (.txt): ").strip()
                pwd = getpass.getpass("Password: ")
                if not pwd:
                    print("[Error] Empty password not allowed.")
                    continue
                try:
                    encrypt_file(inp, outp, pwd)
                    print(f"[OK] Encrypted -> {outp}")
                except Exception as e:
                    print(f"[Error] {e}")
            elif choice == "2":
                inp = input("Input ENCRYPTED file path (.txt): ").strip()
                outp = input("Output DECRYPTED file path (.txt): ").strip()
                pwd = getpass.getpass("Password: ")
                if not pwd:
                    print("[Error] Empty password not allowed.")
                    continue
                try:
                    decrypt_file(inp, outp, pwd)
                    print(f"[OK] Decrypted -> {outp}")
                except Exception as e:
                    print(f"[Error] {e}")
            elif choice == "3":
                print("Bye.")
                break
            else:
                print("Please choose 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nInterrupted. Bye.")
            break
        except Exception as e:
            print(f"[Unexpected Error] {e}")