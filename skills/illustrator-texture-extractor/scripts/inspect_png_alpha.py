from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def inspect(path: Path) -> dict[str, object]:
    with Image.open(path) as source:
        image = source.convert("RGBA")
        alpha = image.getchannel("A")
        histogram = alpha.histogram()
        total = image.width * image.height
        painted_bbox = alpha.getbbox()

        if painted_bbox is None:
            edge_clearance = None
            touches_edge = False
        else:
            edge_clearance = {
                "left": painted_bbox[0],
                "top": painted_bbox[1],
                "right": image.width - painted_bbox[2],
                "bottom": image.height - painted_bbox[3],
            }
            touches_edge = min(edge_clearance.values()) == 0

        return {
            "path": str(path.resolve()),
            "width": image.width,
            "height": image.height,
            "mode": "RGBA",
            "long_edge": max(image.size),
            "alpha_extrema": list(alpha.getextrema()),
            "transparent_pixels": histogram[0],
            "opaque_pixels": histogram[255],
            "partial_alpha_pixels": total - histogram[0] - histogram[255],
            "painted_bbox": list(painted_bbox) if painted_bbox else None,
            "edge_clearance": edge_clearance,
            "touches_edge": touches_edge,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect PNG dimensions, alpha coverage, and painted bounds."
    )
    parser.add_argument("png", nargs="+", type=Path)
    parser.add_argument("--target-long-edge", type=int)
    parser.add_argument("--fail-on-edge-touch", action="store_true")
    args = parser.parse_args()

    rows = [inspect(path) for path in args.png]
    ok = True
    for row in rows:
        if args.target_long_edge is not None:
            row["target_long_edge"] = args.target_long_edge
            row["target_match"] = row["long_edge"] == args.target_long_edge
            ok = ok and bool(row["target_match"])
        if args.fail_on_edge_touch:
            row["edge_clearance_match"] = not row["touches_edge"]
            ok = ok and bool(row["edge_clearance_match"])

    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
