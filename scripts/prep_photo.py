#!/usr/bin/env python3
"""Prepare Ren's red and black portrait for ASCII conversion."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def prepare(source: Path, output: Path) -> None:
    image = Image.open(source).convert("RGB")
    size = min(image.size)
    left = (image.width - size) // 2
    top = (image.height - size) // 2
    image = image.crop((left, top, left + size, top + size)).resize((900, 900), Image.Resampling.LANCZOS)

    pixels = image.load()
    cleaned = Image.new("L", image.size, 255)
    target = cleaned.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = pixels[x, y]
            is_red_field = red > 88 and red > green * 1.38 and red > blue * 1.28
            if is_red_field:
                target[x, y] = 255
            else:
                target[x, y] = int(0.22 * red + 0.68 * green + 0.10 * blue)

    cleaned = ImageOps.autocontrast(cleaned, cutoff=1)
    cleaned = ImageEnhance.Contrast(cleaned).enhance(1.35)
    cleaned = cleaned.filter(ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=3))
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.save(output)
    print(f"prepared {source.name} -> {output} ({cleaned.width}x{cleaned.height})")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("source-prepped.png"))
    args = parser.parse_args()
    prepare(args.source, args.output)


if __name__ == "__main__":
    main()
