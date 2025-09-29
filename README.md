# Morse Secure Cipher (Custom Encryption)

A simple but educational **file encryption & decryption tool** that uses a **custom, key-based cipher**.  
It applies **three cryptographic techniques** — **substitution**, **transposition**, and a **SHA-256 keystream XOR** — to transform text.

The program supports both **command-line** and **graphical interface (GUI)** usage and works entirely with `.txt` files.

---

## ✨ Features

- 🔑 **Key-based encryption** — You choose the password; without it, decryption is impossible.  
- 🔒 **Custom cipher** — Uses **Morse-like substitution**, **rail-fence transposition**, and a **SHA-256 counter-mode keystream** (no standard ciphers).  
- 🖥️ **Graphical user interface** (Tkinter) for easy file selection.  
- 💻 **Command-line interface** for quick terminal use.  
- ✅ **TXT-only I/O** — always works with `.txt` files.

---

## 📸 Screenshots

### GUI Main Window
![GUI Main Window](images/gui_main.png)

### Encrypting a TXT File
![Encrypt Window](images/gui_encrypt.png)

### Decrypting a TXT File
![Decrypt Window](images/gui_decrypt.png)

*(Save screenshots in an `images/` folder or adjust the paths.)*

---

## 📂 Project Structure

morse.py # Morse code conversion (substitution layer)
transposition.py # Rail-fence transposition (scramble layer)
keystream.py # Key derivation & SHA-256 keystream generator
crypto_core.py # Main encryption/decryption logic + CLI
gui_app.py # Tkinter GUI for file selection & easy use

yaml
Copy code

---

## ⚡ Installation

1. Install [Python 3.8+](https://www.python.org/downloads/).
2. (Optional) Upgrade pip:
   ```bash
   pip install --upgrade pip
No extra dependencies — uses only the Python standard library (Tkinter is included on most systems).

🚀 Usage
🖥️ Option 1 — GUI (Recommended)
Run the GUI:

bash
Copy code
python gui_app.py
Encrypt TXT → TXT
Select your plain .txt file → choose where to save the encrypted .txt → enter password.

Decrypt TXT → TXT
Select the encrypted .txt file → choose where to save the restored .txt → enter the same password.

💻 Option 2 — CLI (Terminal)
Run the CLI:

bash
Copy code
python crypto_core.py
Menu:

mathematica
Copy code
1) Encrypt a TXT file
2) Decrypt a TXT file
3) Quit
Choose an option and follow the prompts.

📂 File Behavior
Action	Input	Output
Encrypt	message.txt	message_encrypted.txt
Decrypt	message_encrypted.txt	message_restored.txt

The encrypted file is still text but contains a JSON “envelope” (with salt, rail count, etc.).

The decrypted file restores your exact original text.

🔐 Algorithm Overview
Substitution — Converts plaintext into Morse-like codes (letters, numbers, punctuation).

Transposition — Uses a rail-fence pattern derived from your password.

Keystream XOR — Mixes bytes with a SHA-256 counter-mode keystream built from the password + random salt.

⚠️ If you lose your password, the encrypted file cannot be recovered.

⚠️ Notes
This cipher is for educational purposes only.

It is not intended for real-world secure communication or protecting sensitive data.

Always back up your password; decryption is impossible without it.

📜 License
This project is released under the MIT License — free to use, modify, and learn from.