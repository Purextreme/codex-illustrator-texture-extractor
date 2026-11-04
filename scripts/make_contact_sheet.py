from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def checkerboard(width: int, height: int, square: int = 24) -> Image.Image:
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    for y in range(0, height, square):
        for x in range(0, width, square):
            if (x // square + y // square) % 2:
                draw.rectangle(
                    (x, y, x + square - 1, y + square - 1),
                    fill=(224, 224, 224),
                )
    return image


def load_font() -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=18)
    except TypeError:
        return ImageFont.load_default()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a checkerboard contact sheet for transparent PNG review."
    )
    parser.add_argument("png", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--cell-width", type=int, default=720)
    parser.add_argument("--cell-height", type=int, default=520)
    args = parser.parse_args()

    if args.columns < 1:
        parser.error("--columns must be at least 1")
    if args.cell_width < 100 or args.cell_height < 100:
        parser.error("cell dimensions must be at least 100 pixels")

    header_height = 52
    rows = math.ceil(len(args.png) / args.columns)
    sheet = Image.new(
        "RGB",
        (args.cell_width * args.columns, args.cell_height * rows),
        "white",
    )
    font = load_font()
    draw = ImageDraw.Draw(sheet)

    for index, path in enumerate(args.png):
        with Image.open(path) as opened:
            original = opened.convert("RGBA")
        row, column = divmod(index, args.columns)
        x0 = column * args.cell_width
        y0 = row * args.cell_height
        body_height = args.cell_height - header_height
        background = checkerboard(args.cell_width, body_height)

        preview = original.copy()
        preview.thumbnail((args.cell_width - 48, body_height - 36))
        px = (background.width - preview.width) // 2
        py = (background.height - preview.height) // 2
        background.paste(preview, (px, py), preview)
        sheet.paste(background, (x0, y0 + header_height))

        label = f"{path.name}  {original.width}x{original.height}"
        draw.text((x0 + 12, y0 + 12), label, fill="black", font=font)
        draw.rectangle(
            (x0, y0, x0 + args.cell_width - 1, y0 + args.cell_height - 1),
            outline=(90, 90, 90),
            width=2,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
