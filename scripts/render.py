#!/usr/bin/env python3
"""
手把手教程图 · 渲染器
============================================================
把 index.html?step=N 逐张截成 2x PNG，再可选地纵向拼成长图。

用法：
  python render.py                          # 渲染 1,2,3 三步 + 长图
  python render.py --steps 1,2              # 只渲前两步
  python render.py --steps all              # 单张总览（全部标注同屏）
  python render.py --names 01-装之前.png,02-装完.png
  python render.py --size 750x1334          # 手机竖版
  python render.py --scale 3                # 更高清
  python render.py --no-stitch              # 不拼长图

默认值：html=index.html  steps=1,2,3  size=1500x720  scale=2  out=out
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]


def find_chrome(explicit: str | None) -> str:
    if explicit:
        p = Path(explicit).expanduser()
        if p.exists():
            return str(p)
        sys.exit(f"✗ 找不到 Chrome：{explicit}")
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chrome", "msedge"):
        w = shutil.which(name)
        if w:
            return w
    sys.exit("✗ 没找到 Chrome / Chromium，用 --chrome 指定可执行文件路径")


def shoot(chrome: str, url: str, dst: Path, size: tuple[int, int], scale: int,
          profile: Path, wait: int) -> None:
    cmd = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-breakpad",
        "--disable-crash-reporter",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        f"--user-data-dir={profile}",
        f"--force-device-scale-factor={scale}",
        f"--window-size={size[0]},{size[1]}",
        f"--virtual-time-budget={wait}",
        f"--screenshot={dst}",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True)
    if not dst.exists() or dst.stat().st_size < 1024:
        sys.stderr.write(r.stderr.decode("utf-8", "ignore")[-1500:] + "\n")
        sys.exit(f"✗ 截图失败：{dst.name}")


def stitch(pngs: list[Path], dst: Path, width: int | None) -> None:
    try:
        from PIL import Image
    except ImportError:
        print("  ! 没装 Pillow，跳过拼长图（pip install pillow）")
        return
    ims = []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        if width and im.width != width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        ims.append(im)
    pad, gap = 40, 40
    W = max(i.width for i in ims)
    H = pad * 2 + sum(i.height for i in ims) + gap * (len(ims) - 1)
    canvas = Image.new("RGB", (W, H), "#ffffff")
    y = pad
    for im in ims:
        canvas.paste(im, (0, y))
        y += im.height + gap
    canvas.save(dst, optimize=True)
    print(f"  ✓ {dst.name}  {canvas.width}×{canvas.height}")


def main() -> None:
    ap = argparse.ArgumentParser(description="把手把手教程图的 HTML 渲成 PNG")
    ap.add_argument("--html", default="index.html")
    ap.add_argument("--steps", default="1,2,3")
    ap.add_argument("--names", default="", help="逗号分隔的输出文件名，与 steps 一一对应")
    ap.add_argument("--out", default="out")
    ap.add_argument("--size", default="1500x720")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--stitch", dest="do_stitch", action="store_true", default=True)
    ap.add_argument("--no-stitch", dest="do_stitch", action="store_false")
    ap.add_argument("--stitch-name", default="安装步骤-长图.png")
    ap.add_argument("--stitch-width", type=int, default=0, help="长图宽度，0=原样")
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--wait", type=int, default=1500, help="渲染等待毫秒")
    a = ap.parse_args()

    html = Path(a.html).resolve()
    if not html.exists():
        sys.exit(f"✗ 找不到 {html}")
    w, h = (int(x) for x in a.size.lower().split("x"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    profile = out / ".chrome-profile"
    chrome = find_chrome(a.chrome)

    steps = [s.strip() for s in a.steps.split(",") if s.strip()]
    names = [n.strip() for n in a.names.split(",") if n.strip()]
    if names and len(names) != len(steps):
        sys.exit("✗ --names 数量必须和 --steps 一致")

    made = []
    print(f"画布 {w}×{h} @{a.scale}x  →  {out}/")
    for i, st in enumerate(steps):
        name = names[i] if names else (
            "00-总览.png" if st == "all" else f"{int(st):02d}-步骤{st}.png"
        )
        dst = out / name
        shoot(chrome, f"{html.as_uri()}?step={st}", dst, (w, h), a.scale, profile, a.wait)
        print(f"  ✓ {name}  {dst.stat().st_size // 1024} KB")
        made.append(dst)

    if a.do_stitch and len(made) > 1:
        stitch(made, out / a.stitch_name, a.stitch_width or None)

    shutil.rmtree(profile, ignore_errors=True)
    print("done")


if __name__ == "__main__":
    main()
