#!/usr/bin/env python3
"""
手把手教程图 · 脚手架
============================================================
把一个模板 + kit 复制到目标目录，产出可直接改、直接渲染的 index.html。

用法：
  python new.py ~/Desktop/xx教程                     # 默认 chrome-extension 模板
  python new.py ~/Desktop/xx教程 --template blank    # 空骨架，自己搭界面
  python new.py ~/Desktop/xx教程 --force             # 目录已有内容也覆盖 index.html
"""
import argparse
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
KIT = SKILL / "kit"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dest", help="目标目录")
    ap.add_argument("--template", default="chrome-extension",
                    help="chrome-extension（默认）| blank")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    tpl = TEMPLATES / f"{a.template}.html"
    if not tpl.exists():
        avail = "、".join(p.stem for p in TEMPLATES.glob("*.html"))
        sys.exit(f"✗ 没有模板 {a.template}，现有：{avail}")

    dest = Path(a.dest).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    idx = dest / "index.html"
    if idx.exists() and not a.force:
        sys.exit(f"✗ {idx} 已存在，加 --force 覆盖")

    if (dest / "kit").exists():
        shutil.rmtree(dest / "kit")
    shutil.copytree(KIT, dest / "kit")
    shutil.copy2(tpl, idx)
    (dest / "assets").mkdir(exist_ok=True)

    print(f"✓ {dest}")
    print(f"  index.html   ← 改这里（文案 / 步骤 / 界面）")
    print(f"  kit/         ← 别动，公共样式与标注引擎")
    print(f"  assets/      ← 放图标 / 截图（模板默认读 assets/icon128.png）")
    print(f"  下一步：cd {dest} && python {SKILL / 'scripts/render.py'}")


if __name__ == "__main__":
    main()
