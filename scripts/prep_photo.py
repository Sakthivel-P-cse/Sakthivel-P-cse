#!/usr/bin/env python3
import argparse
import os

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def prepare(source, output):
    image = Image.open(source).convert("RGB")
    width, height = image.size
    crop = image.crop((
        int(width * 0.02),
        int(height * 0.14),
        int(width * 0.79),
        int(height * 0.91),
    ))
    array = np.asarray(crop).astype(np.float32)
    luminance = (
        array[:, :, 0] * 0.299
        + array[:, :, 1] * 0.587
        + array[:, :, 2] * 0.114
    )
    saturation = array.max(axis=2) - array.min(axis=2)
    background = (luminance > 162) & (saturation < 34)
    gray = ImageOps.grayscale(crop)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.24)
    gray = ImageEnhance.Brightness(gray).enhance(1.05)
    gray = gray.filter(ImageFilter.GaussianBlur(radius=0.2))
    processed = np.asarray(gray).copy()
    processed[background] = 255
    Image.fromarray(processed.astype(np.uint8), mode="L").save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output", nargs="?", default="source-prepped.png")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    prepare(args.source, args.output)
    print(f"wrote {args.output}")
