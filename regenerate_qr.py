#!/usr/bin/env python3
"""
Regenerate the 3 marker QR codes with your real deployed domain.

Usage:
    pip install qrcode[pil]
    python3 regenerate_qr.py https://your-real-domain.vercel.app
"""
import sys
import os
from qrcode import QRCode, constants
from PIL import Image, ImageDraw

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 regenerate_qr.py https://your-domain.vercel.app")
        sys.exit(1)

    domain = sys.argv[1].rstrip("/")
    out_dir = os.path.join(os.path.dirname(__file__), "qr-codes")
    os.makedirs(out_dir, exist_ok=True)

    markers = [("r1", "1 - Balcony"), ("r2", "2 - Kitchen"), ("r3", "3 - Bedroom")]

    for key, label in markers:
        url = f"{domain}/#{key}"
        qr = QRCode(border=2, box_size=10, error_correction=constants.ERROR_CORRECT_M)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        w = img.width
        canvas = Image.new("RGB", (w, img.height + 50), "white")
        canvas.paste(img, (0, 0))
        d = ImageDraw.Draw(canvas)
        d.text((10, img.height + 12), f"{label}  ({url})", fill="black")

        path = os.path.join(out_dir, f"{key}.png")
        canvas.save(path)
        print(f"Wrote {path}  ->  {url}")

if __name__ == "__main__":
    main()
