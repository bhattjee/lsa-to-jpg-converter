# LSA to JPG Converter - MIUI Secret Album Decryptor

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![MIUI](https://img.shields.io/badge/MIUI-12%2C%2013%2C%2014%2C%20HyperOS-orange)

> Decrypt and recover your hidden photos and videos from Xiaomi, Redmi, and POCO phones' Secret Album

A powerful Python tool to decrypt `.lsa` and `.lsav` files from MIUI Secret Album, converting them back to viewable formats like JPG, PNG, and MP4. Works seamlessly across MIUI 12, MIUI 13, MIUI 14, and HyperOS versions.

## Features

- **Decrypt Secret Album Files**: Convert encrypted `.lsa` (photos) and `.lsav` (videos) files to their original formats
- **Batch Processing**: Process single files, entire folders, or use glob patterns for bulk conversion
- **Auto Format Detection**: Automatically identifies the correct output format (JPG, PNG, MP4, etc.)
- **Smart File Handling**: Prevents overwriting by automatically renaming duplicate files
- **Wide Compatibility**: Supports Xiaomi, Redmi, and POCO devices running MIUI 12, 13, 14, and HyperOS
- **Simple CLI**: Easy-to-use command-line interface with clear progress feedback

## Requirements

- Python 3.6 or higher
- Required packages:
  ```bash
  pip install pycryptodome filetype
  ```

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install pycryptodome filetype
   ```
   
## Usage

-  Convert a single file
-  Convert multiple files using glob pattern
-  Convert all files in a folder (recursive)
-  Convert from MIUI Secret Album path

## How It Works

This tool uses the AES-CTR encryption key and IV hardcoded in the MIUI Gallery APK certificate to decrypt Secret Album files:

- **`.lsa` files**: Entire file is AES-CTR encrypted (typically photos)
- **`.lsav` files**: Only the header is encrypted, rest is plain MP4 (typically videos)

The decryption process:
1. Reads the encrypted file
2. Applies AES-CTR decryption using MIUI's known keys
3. Auto-detects the original file format
4. Saves the decrypted file with the correct extension

## Supported Devices

- Xiaomi phones
- Redmi phones
- POCO phones

## Supported MIUI Versions

- MIUI 12
- MIUI 13
- MIUI 14
- HyperOS

## Example Output

```
[OK]   photo.lsa  →  photo.jpg
[OK]   video.lsav  →  video.mp4
[OK]   screenshot.lsa  →  screenshot.png

Done: 3 converted, 0 failed.
```

## Important Notes

- This tool is intended for recovering your own photos from your own devices
- The encryption keys are extracted from the MIUI Gallery APK certificate
- Always backup your original `.lsa` files before conversion
- Use responsibly and in compliance with applicable laws

## Contributing

Contributions are welcome! Feel free to submit issues, fork the repository, and create pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Related Resources

- [MIUI Secret Album](https://www.miui.com/)
- [Xiaomi Community](https://community.miui.com/)

## Acknowledgments

This tool was developed to help users recover their personal photos from MIUI's Secret Album feature. The encryption parameters were reverse-engineered from the MIUI Gallery APK.

---

**Note**: This tool is for educational and personal use only. Always respect privacy and use responsibly.
