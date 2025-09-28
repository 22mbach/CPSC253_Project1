import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from crypto_core import encrypt_file, decrypt_file


def _choose_txt(title: str) -> str:
    """Open a dialog to pick an existing .txt file."""
    return filedialog.askopenfilename(title=title, filetypes=[('Text files', '*.txt')])


def _save_txt(title: str) -> str:
    """Open a dialog to choose where to save a .txt file."""
    return filedialog.asksaveasfilename(title=title, defaultextension='.txt', filetypes=[('Text files', '*.txt')])


def gui_encrypt():
    """Handle GUI workflow for encrypting a TXT file."""
    in_file = _choose_txt('Select plaintext .txt file')
    if not in_file:
        return
    out_file = _save_txt('Save ENCRYPTED .txt as')
    if not out_file:
        return
    password = simpledialog.askstring('Password', 'Enter encryption key:', show='•')
    if not password:
        return
    try:
        encrypt_file(in_file, out_file, password)
        messagebox.showinfo('Success', f'Encrypted to:\n{out_file}')
    except Exception as e:
        messagebox.showerror('Error', f'{type(e).__name__}: {e}')


def gui_decrypt():
    """Handle GUI workflow for decrypting a TXT file."""
    in_file = _choose_txt('Select ENCRYPTED .txt file')
    if not in_file:
        return
    out_file = _save_txt('Save DECRYPTED .txt as')
    if not out_file:
        return
    password = simpledialog.askstring('Password', 'Enter decryption key:', show='•')
    if not password:
        return
    try:
        decrypt_file(in_file, out_file, password)
        messagebox.showinfo('Success', f'Decrypted to:\n{out_file}')
    except Exception as e:
        messagebox.showerror('Error', f'{type(e).__name__}: {e}')


def main():
    """Launch the Tkinter GUI for encryption/decryption."""
    root = tk.Tk()
    root.title('Morse Secure Cipher — Custom (TXT I/O)')
    root.resizable(False, False)

    tk.Button(root, text='Encrypt TXT → TXT', command=gui_encrypt, width=28).pack(pady=8)
    tk.Button(root, text='Decrypt TXT → TXT', command=gui_decrypt, width=28).pack(pady=8)
    tk.Button(root, text='Quit', command=root.quit, width=28).pack(pady=8)

    hint = (
        'Encrypt: input .txt → output .txt (JSON envelope inside)\n'
        'Decrypt: input .txt (envelope) → output .txt (plaintext)\n'
        'Techniques: substitution + transposition + keystream XOR'
    )
    tk.Label(root, text=hint, fg='#444').pack(padx=10, pady=6)

    root.mainloop()


if __name__ == '__main__':
    main()