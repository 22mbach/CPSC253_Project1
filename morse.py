from typing import Dict, List

# --- Morse code mappings (letters/digits/punctuation) ---
MORSE_MAP: Dict[str, str] = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.',  '(': '-.--.',  ')': '-.--.-', '&': '.-...',  ':': '---...',
    ';': '-.-.-.', '=': '-...-',  '+': '.-.-.',  '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
}
INV_MORSE_MAP: Dict[str, str] = {v: k for k, v in MORSE_MAP.items()}
WORD_SEP = '/'   # represents space
LINE_SEP = '|'   # represents newline


def to_morse(text: str) -> str:
    """Convert plain text into Morse code tokens (space→/, newline→|, unknown→=XX)."""
    tokens: List[str] = []
    for ch in text:
        if ch == ' ':
            tokens.append(WORD_SEP)
        elif ch == '\n':
            tokens.append(LINE_SEP)
        else:
            code = MORSE_MAP.get(ch.upper())
            tokens.append(code if code is not None else f"={ord(ch):02X}")
    return ' '.join(tokens)


def from_morse(morse: str) -> str:
    """Convert a Morse token string back to the original text."""
    out: List[str] = []
    for tok in morse.split():
        if tok == WORD_SEP:
            out.append(' ')
        elif tok == LINE_SEP:
            out.append('\n')
        elif tok.startswith('=') and len(tok) == 3:
            out.append(chr(int(tok[1:], 16)))
        else:
            ch = INV_MORSE_MAP.get(tok)
            if ch is None:
                raise ValueError(f"Unknown Morse token: {tok}")
            out.append(ch)
    return ''.join(out)