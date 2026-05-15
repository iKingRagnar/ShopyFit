#!/usr/bin/env python3
"""
Generate product motion clips via fal.ai (Kling 2.0 image-to-video).

Setup (when TQ has a key):
  1. Sign up free at fal.ai → get API key
  2. export FAL_KEY="your-key"
  3. pip install fal-client requests
  4. python3 scripts/gen_product_videos.py

Takes the product hero images (Pollinations or real photos) and animates
them: subtle model movement, camera dolly, gym lighting. ~$0.30/clip on
Kling. Full catalog (8 SKUs) ≈ $2.40 USD.

Output: assets/videos/{sku}.mp4
"""
import os, sys, json, time, urllib.request
from pathlib import Path

FAL_KEY = os.environ.get("FAL_KEY")
if not FAL_KEY:
    sys.exit("FAL_KEY env var required. Get one free at https://fal.ai")

OUT = Path(__file__).resolve().parent.parent / "assets" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

# Each SKU: source image URL + motion prompt
CATALOG = {
    "TQ-TEE-GBLK": {
        "img": "https://image.pollinations.ai/prompt/oversize%20black%20tee%20red%20curved%20panels%20gymrat%20studio?width=720&height=1280&seed=71&nologo=true&model=flux",
        "prompt": "Athletic model wearing oversize black tee with red accent lines, "
                  "slow turn toward camera, subtle dolly-in, dark gym lighting, "
                  "cinematic, premium streetwear film, 5 seconds",
    },
    "TQ-JOG-PHN": {
        "img": "https://image.pollinations.ai/prompt/tapered%20black%20jogger%20red%20seam%20lines%20gymrat?width=720&height=1280&seed=72&nologo=true&model=flux",
        "prompt": "Athletic model in black tapered joggers with red side lines, "
                  "walking toward camera, gym backdrop, moody rim light, "
                  "premium athletic film, 5 seconds",
    },
    "TQ-HOOD-VOID": {
        "img": "https://image.pollinations.ai/prompt/oversize%20black%20hoodie%20red%20panels%20embroidered%20bull?width=720&height=1280&seed=73&nologo=true&model=flux",
        "prompt": "Athletic model in oversize black hoodie with red curved panels, "
                  "pulls hood up, slow camera orbit, dramatic studio lighting, "
                  "cinematic gymrat aesthetic, 5 seconds",
    },
}

FAL_ENDPOINT = "https://fal.run/fal-ai/kling-video/v2/standard/image-to-video"


def gen(sku, spec):
    out = OUT / f"{sku}.mp4"
    if out.exists() and out.stat().st_size > 10000:
        print(f"  ✓ {out.name} exists, skip"); return False
    body = json.dumps({
        "image_url": spec["img"],
        "prompt": spec["prompt"],
        "duration": "5",
        "aspect_ratio": "9:16",
    }).encode()
    req = urllib.request.Request(
        FAL_ENDPOINT, data=body,
        headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"},
        method="POST")
    print(f"  → {sku} submitting…", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"  ERR {sku}: {e}"); return False
    video_url = (data.get("video") or {}).get("url")
    if not video_url:
        print(f"  no video for {sku}: {json.dumps(data)[:200]}"); return False
    urllib.request.urlretrieve(video_url, out)
    print(f"  ✓ saved {out.name} ({out.stat().st_size:,} bytes)")
    return True


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for sku, spec in CATALOG.items():
        if only and only != sku:
            continue
        print(f"[{sku}]")
        if gen(sku, spec):
            n += 1
        time.sleep(1)
    print(f"\n=== {n} clips generated. Wire them as <video> in index.html. ===")


if __name__ == "__main__":
    main()
