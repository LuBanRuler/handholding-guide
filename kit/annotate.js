/* ============================================================
   手把手教程图 · 标注引擎
   ------------------------------------------------------------
   页面里定义 window.GUIDE 即可，本文件负责：
     1. 从 ?step= 读当前步骤，写到 <body data-step="…">
     2. 填 #ttl / #sub / #foot 三处文案
     3. 调 onState(step) 切换界面状态（开关、显隐…）
     4. 给每个 target 画红框 + 引线 + 编号标签

   GUIDE = {
     copy:  { '1': {ttl:'…', sub:'…', foot:'…'}, … },
     steps: { '1': [ {target:'#id', text:'…', side:'right', gap:24} ], … },
     onState: (step) => {},        // 可选
     ring: 6                       // 可选，红框外扩像素
   }

   steps[] 每项可用的键：
     target  必填，CSS 选择器（建议用 id）
     text    标签文案，越短越好
     side    right(默认) | left | below | above
     align   side=below 时用，'right' 让标签右对齐元素
     gap     标签与元素的距离，默认 24
     dy      垂直微调（负值上移）
     n       编号，缺省按数组顺序 1,2,3…
     done    true = 灰色 ✓ 标签，不画红框（表示这一步已完成）
     ring    false = 只画标签不画框
   ============================================================ */
(function () {
  const G = window.GUIDE || {};
  const RING = G.ring == null ? 6 : G.ring;

  const step = new URLSearchParams(location.search).get('step') || 'all';
  document.body.dataset.step = step;

  // ---- 1. 文案 ----
  const c = (G.copy || {})[step];
  if (c) {
    const t = document.getElementById('ttl');
    const s = document.getElementById('sub');
    const f = document.getElementById('foot');
    if (t && c.ttl != null) t.innerHTML = c.ttl;
    if (s && c.sub != null) s.innerHTML = c.sub;
    if (f && c.foot != null) f.innerHTML = c.foot;
  }

  // ---- 2. 界面状态 ----
  if (typeof G.onState === 'function') G.onState(step);

  // ---- 3. 标注 ----
  const chips = document.getElementById('chips');
  const wires = document.getElementById('wires');
  const canvas = document.getElementById('canvas');
  if (!chips || !wires || !canvas) return;

  const list = (G.steps || {})[step] || [];
  const base = canvas.getBoundingClientRect();

  list.forEach((s, i) => {
    const el = document.querySelector(s.target);
    if (!el) { console.warn('[annotate] 找不到目标:', s.target); return; }

    const r = el.getBoundingClientRect();
    const b = { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height };

    if (!s.done && s.ring !== false) {
      const ring = document.createElement('div');
      ring.className = 'ring' + (s.dash ? ' dash' : '');
      ring.style.cssText =
        `left:${b.x - RING}px;top:${b.y - RING}px;` +
        `width:${b.w + RING * 2}px;height:${b.h + RING * 2}px`;
      chips.appendChild(ring);
    }

    const chip = document.createElement('div');
    chip.className = 'chip' + (s.done ? ' done' : '');
    chip.innerHTML = `<i>${s.done ? '✓' : (s.n || i + 1)}</i>${s.text || ''}`;
    chips.appendChild(chip);

    const cw = chip.offsetWidth, ch = chip.offsetHeight;
    const gap = s.gap == null ? 24 : s.gap;
    const side = s.side || 'right';
    let cx, cy;

    if (side === 'below') {
      cx = (s.align === 'right') ? b.x + b.w + RING - cw : b.x + b.w / 2 - cw / 2;
      cy = b.y + b.h + RING + gap;
      if (!s.done) {
        const ax = b.x + b.w - 26, top = b.y + b.h + RING + 3;
        wire(`left:${ax - 1}px;top:${top + 9}px;width:2px;height:${cy - top - 9}px`);
        head(ax, top, 'up');
      }
    } else if (side === 'above') {
      cx = b.x + b.w / 2 - cw / 2;
      cy = b.y - RING - gap - ch;
      if (!s.done) {
        const ax = b.x + b.w / 2, bot = b.y - RING - 3;
        wire(`left:${ax - 1}px;top:${cy + ch + 9}px;width:2px;height:${bot - cy - ch - 9}px`);
        head(ax, bot, 'down');
      }
    } else if (side === 'left') {
      cx = b.x - RING - gap - cw;
      cy = b.y + b.h / 2 - ch / 2 + (s.dy || 0);
      if (!s.done) {
        const ay = b.y + b.h / 2 + (s.dy || 0), tip = b.x - RING - 3;
        wire(`left:${cx + cw + 9}px;top:${ay - 1}px;height:2px;width:${tip - cx - cw - 9}px`);
        head(tip, ay, 'right');
      }
    } else {
      cx = b.x + b.w + RING + gap;
      cy = b.y + b.h / 2 - ch / 2 + (s.dy || 0);
      if (!s.done) {
        const ay = b.y + b.h / 2 + (s.dy || 0), tip = b.x + b.w + RING + 3;
        wire(`left:${tip + 9}px;top:${ay - 1}px;height:2px;width:${cx - tip - 9}px`);
        head(tip, ay, 'left');
      }
    }
    chip.style.left = `${cx}px`;
    chip.style.top = `${cy}px`;
  });

  function wire(css) {
    const w = document.createElement('div');
    w.className = 'wire'; w.style.cssText = css; wires.appendChild(w);
  }
  function head(x, y, dir) {
    const h = document.createElement('div');
    h.className = 'head';
    const R = 'var(--red)';
    if (dir === 'up') h.style.cssText = `left:${x - 7}px;top:${y}px;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:9px solid ${R}`;
    else if (dir === 'down') h.style.cssText = `left:${x - 7}px;top:${y - 9}px;border-left:7px solid transparent;border-right:7px solid transparent;border-top:9px solid ${R}`;
    else if (dir === 'right') h.style.cssText = `left:${x}px;top:${y - 7}px;border-top:7px solid transparent;border-bottom:7px solid transparent;border-left:9px solid ${R}`;
    else h.style.cssText = `left:${x}px;top:${y - 7}px;border-top:7px solid transparent;border-bottom:7px solid transparent;border-right:9px solid ${R}`;
    wires.appendChild(h);
  }
})();
