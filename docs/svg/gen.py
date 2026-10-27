#!/usr/bin/env python3
"""
README 用的 SVG 组件生成器
============================================================
固定画布：首屏 1200×320，章节标题 1200×138
统一语言：浅色圆角容器 + 细网格 + 右侧点阵 + 黄色短线
层级：英文眉题 → 中文大标题 → 淡色章节编号
系统字体：只用系统字体栈，避免 GitHub 拉不到外部字体

改文案 → 改下面的 HERO / SECTIONS → 重跑本脚本。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = ("-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',"
        "'Microsoft YaHei','Noto Sans SC',sans-serif")

BG = "#FBFAF7"      # 容器底
EDGE = "#E9E4D9"    # 容器描边
GRID = "#F0ECE3"    # 细网格
DOT = "#DCD5C6"     # 点阵
YEL = "#F2C230"     # 黄色短线
INK = "#1B1A17"     # 大标题
INK2 = "#6B6558"    # 副标题
MUTE = "#8C8677"    # 眉题
NUM = "#E7E0CF"     # 淡色编号

HERO = {
    "file": "hero.svg",
    "eyebrow": "HANDHOLDING GUIDE",
    "title": "手把手教程图",
    "sub": "把「教别人点哪里」做成图 · 不用截屏拼贴",
    "sub2": "HTML 复刻界面 → 无头 Chrome 2x 截图 → 标注按元素自动定位",
    "tags": ["分步图", "纵向长图", "可重渲"],
}

SECTIONS = [
    ("01", "WHY", "它解决什么"),
    ("02", "QUICK START", "快速开始"),
    ("03", "HOW IT WORKS", "怎么工作的"),
    ("04", "TWO ROUTES", "两条路线"),
    ("05", "RULES", "版式硬规则"),
    ("06", "LAYOUT", "目录结构"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(w: int, h: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f'<title>{esc(title)}</title>\n'
        f'<defs><clipPath id="c"><rect x="0" y="0" width="{w}" height="{h}" rx="22"/></clipPath></defs>\n'
        f'<g clip-path="url(#c)">\n'
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>\n'
    )


def grid(w: int, h: int, step: int = 40) -> str:
    out = []
    x = step
    while x < w:
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{GRID}" stroke-width="1"/>')
        x += step
    y = step
    while y < h:
        out.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{GRID}" stroke-width="1"/>')
        y += step
    return "".join(out)


def dots(x0: int, y0: int, cols: int, rows: int, gap: int = 15, r: float = 1.6) -> str:
    out = []
    for i in range(cols):
        for j in range(rows):
            out.append(f'<circle cx="{x0 + i * gap}" cy="{y0 + j * gap}" r="{r}" fill="{DOT}"/>')
    return "".join(out)


def frame(w: int, h: int) -> str:
    return (f'</g>\n<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" '
            f'fill="none" stroke="{EDGE}" stroke-width="1"/>\n')


def build_hero() -> str:
    w, h = 1200, 320
    s = head(w, h, HERO["title"])
    s += grid(w, h, 40)
    s += f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#fade)"/>' if False else ""
    # 右侧点阵（只负责平衡画面）
    s += dots(1012, 62, 7, 8, 15)
    # 黄色短线
    s += f'<rect x="64" y="56" width="42" height="5" rx="2.5" fill="{YEL}"/>'
    # 眉题
    s += (f'<text x="64" y="94" font-family="{FONT}" font-size="13" font-weight="600" '
          f'letter-spacing="3" fill="{MUTE}">{esc(HERO["eyebrow"])}</text>')
    # 大标题
    s += (f'<text x="62" y="164" font-family="{FONT}" font-size="50" font-weight="700" '
          f'letter-spacing="1" fill="{INK}">{esc(HERO["title"])}</text>')
    # 副标题
    s += (f'<text x="64" y="204" font-family="{FONT}" font-size="17" fill="{INK2}">'
          f'{esc(HERO["sub"])}</text>')
    s += (f'<text x="64" y="232" font-family="{FONT}" font-size="14" fill="{MUTE}">'
          f'{esc(HERO["sub2"])}</text>')
    # 标签
    x = 64
    for t in HERO["tags"]:
        tw = 14 + len(t) * 15
        s += (f'<rect x="{x}" y="256" width="{tw}" height="30" rx="15" fill="#FFFFFF" '
              f'stroke="{EDGE}" stroke-width="1"/>')
        s += (f'<text x="{x + tw / 2}" y="276" text-anchor="middle" font-family="{FONT}" '
              f'font-size="13" fill="{INK2}">{esc(t)}</text>')
        x += tw + 10
    s += frame(w, h)
    return s + "</svg>\n"


def build_section(num: str, eyebrow: str, title: str) -> str:
    w, h = 1200, 138
    s = head(w, h, title)
    s += grid(w, h, 46)
    # 右侧点阵 + 淡色编号
    s += dots(984, 42, 5, 4, 14, 1.4)
    s += (f'<text x="1156" y="104" text-anchor="end" font-family="{FONT}" font-size="64" '
          f'font-weight="700" fill="{NUM}">{num}</text>')
    # 黄色竖线
    s += f'<rect x="56" y="52" width="4" height="38" rx="2" fill="{YEL}"/>'
    # 眉题
    s += (f'<text x="80" y="66" font-family="{FONT}" font-size="11.5" font-weight="600" '
          f'letter-spacing="2.6" fill="{MUTE}">{esc(eyebrow)}</text>')
    # 标题
    s += (f'<text x="79" y="100" font-family="{FONT}" font-size="27" font-weight="700" '
          f'fill="{INK}">{esc(title)}</text>')
    s += frame(w, h)
    return s + "</svg>\n"


def main() -> None:
    (OUT / HERO["file"]).write_text(build_hero(), encoding="utf-8")
    print(f"  ✓ {HERO['file']}")
    for num, eb, title in SECTIONS:
        name = f"s{num}.svg"
        (OUT / name).write_text(build_section(num, eb, title), encoding="utf-8")
        print(f"  ✓ {name}  {title}")


if __name__ == "__main__":
    main()
