#!/usr/bin/env python3
"""
MIUI Secret Album .lsa → .jpg decryptor
Works on files from Xiaomi / Redmi / POCO phones (MIUI 12, 13, 14, HyperOS)

Requires: pip install pycryptodome filetype

Usage:
    python lsa_to_jpg.py photo.lsa
    python lsa_to_jpg.py /path/to/folder/
    python lsa_to_jpg.py *.lsa
"""

import os
import sys
import glob

try:
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
except ImportError:
    print("[ERROR] Missing library. Run:  pip install pycryptodome")
    sys.exit(1)

try:
    import filetype
except ImportError:
    print("[ERROR] Missing library. Run:  pip install filetype")
    sys.exit(1)


# ── AES-CTR key & IV hardcoded in MIUI Gallery APK certificate ──────────────
# IV as integer (bytes: 17,19,33,35,49,51,65,67,81,83,97,102,103,104,113,114)
AES_IV  = 22696201676385068962342234041843478898
# First 16 bytes of MIUI Gallery APK certificate (same on all Xiaomi devices)
AES_KEY = b'0\x82\x04l0\x82\x03T\xa0\x03\x02\x01\x02\x02\t\x00'
# ----------------------------------------------------------------------------


def decrypt_lsa(filepath: str) -> bytes:
    """Decrypt a full .lsa file (photo) — entire file is AES-CTR encrypted."""
    with open(filepath, 'rb') as f:
        data = f.read()
    counter = Counter.new(128, initial_value=AES_IV)
    aes = AES.new(AES_KEY, mode=AES.MODE_CTR, counter=counter)
    return aes.decrypt(data)


def decrypt_lsav_header(filepath: str) -> bytes:
    """Decrypt only the header of a .lsav file (video) — rest is plain MP4."""
    size = os.path.getsize(filepath)
    header_size = max(min(1024, size), 16)
    with open(filepath, 'rb') as f:
        encrypted_header = f.read(header_size)
        rest = f.read()
    counter = Counter.new(128, initial_value=AES_IV)
    aes = AES.new(AES_KEY, mode=AES.MODE_CTR, counter=counter)
    return aes.decrypt(encrypted_header) + rest


def convert(input_path: str) -> str:
    """Decrypt one .lsa or .lsav file and save with the correct extension."""
    ext = input_path.rsplit('.', 1)[-1].lower()

    if ext == 'lsa':
        data = decrypt_lsa(input_path)
    elif ext == 'lsav':
        data = decrypt_lsav_header(input_path)
    else:
        raise ValueError(f"Unsupported extension: .{ext}")

    # Auto-detect the real format (jpg, mp4, png, ...)
    kind = filetype.guess(data[:1024])
    out_ext = kind.extension if kind else 'unknown'

    base = input_path.rsplit('.', 1)[0]
    out_path = f"{base}.{out_ext}"

    # Avoid overwriting
    counter = 1
    while os.path.exists(out_path):
        out_path = f"{base}_{counter}.{out_ext}"
        counter += 1

    with open(out_path, 'wb') as f:
        f.write(data)

    return out_path


def resolve_inputs(args):
    files = []
    for arg in args:
        if os.path.isdir(arg):
            for ext in ('*.lsa', '*.lsav'):
                files.extend(glob.glob(os.path.join(arg, '**', ext), recursive=True))
        elif '*' in arg or '?' in arg:
            files.extend(glob.glob(arg))
        elif os.path.isfile(arg):
            files.append(arg)
        else:
            print(f"[WARN] Not found: {arg}")
    return files


def main():
    if len(sys.argv) < 2:
        print("Usage: python lsa_to_jpg.py <file.lsa | folder | glob>")
        print("Examples:")
        print("  python lsa_to_jpg.py photo.lsa")
        print("  python lsa_to_jpg.py *.lsa")
        print("  python lsa_to_jpg.py /sdcard/MIUI/gallery/cloud/secretAlbum/")
        sys.exit(1)

    lsa_files = resolve_inputs(sys.argv[1:])

    if not lsa_files:
        print("No .lsa / .lsav files found.")
        sys.exit(1)

    success, failed = 0, 0
    for path in lsa_files:
        try:
            out = convert(path)
            print(f"[OK]   {path}  →  {out}")
            success += 1
        except Exception as e:
            print(f"[FAIL] {path}: {e}")
            failed += 1

    print(f"\nDone: {success} converted, {failed} failed.")


if __name__ == '__main__':
    main()