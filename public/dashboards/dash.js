/* Small SVG chart kit for the sample dashboards. No dependencies.
   Every chart redraws on resize and theme change, has a hover tooltip and a
   "Show data" table, and reads its colors from CSS variables in dash.css. */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const charts = new Map();

  // ---------- formatting
  const compact = (v, dp) => {
    const a = Math.abs(v);
    if (a >= 1e6) return (v / 1e6).toFixed(dp ?? (a >= 1e7 ? 1 : 2)).replace(/\.?0+$/, "") + "M";
    if (a >= 1e3) return (v / 1e3).toFixed(dp ?? (a >= 1e5 ? 0 : 1)).replace(/\.0$/, "") + "K";
    return String(Math.round(v));
  };
  const fmt = {
    sar: (v) => (v < 0 ? "−" : "") + "SAR " + compact(Math.abs(v)),
    sarFull: (v) => (v < 0 ? "−" : "") + "SAR " + Math.round(Math.abs(v)).toLocaleString("en-US"),
    num: (v) => Math.round(v).toLocaleString("en-US"),
    compact: (v) => compact(v),
    pct: (v, dp = 1) => (v == null ? "–" : v.toFixed(dp) + "%"),
    signedPct: (v, dp = 1) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(dp) + "%",
    x: (v) => v.toFixed(1) + "×",
  };

  const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const color = (c) => (c && c.startsWith("--") ? cssVar(c) : c);
  const slot = (i) => `--s${(i % 5) + 1}`;

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) if (attrs[k] != null) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  const text = (parent, x, y, str, attrs = {}) => {
    const t = el("text", { x, y, ...attrs }, parent);
    t.textContent = str;
    return t;
  };
  const textWidth = (str, size = 11) => String(str).length * size * 0.58;

  // Nice axis ticks
  const ticks = (min, max, count = 4) => {
    if (max === min) max = min + 1;
    const raw = (max - min) / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw);
    const lo = Math.floor(min / step) * step;
    const hi = Math.ceil(max / step) * step;
    const out = [];
    for (let v = lo; v <= hi + step / 2; v += step) out.push(+v.toFixed(10));
    return out;
  };

  // Bar with rounded data-end and square base
  const barPath = (x, y, w, h, r, dir = "up") => {
    r = Math.max(0, Math.min(r, w / 2, Math.abs(h)));
    if (h <= 0 || w <= 0) return "";
    if (dir === "up")
      return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
    if (dir === "right")
      return `M${x},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h - r}Q${x + w},${y + h} ${x + w - r},${y + h}H${x}Z`;
    // left
    return `M${x + w},${y}H${x + r}Q${x},${y} ${x},${y + r}V${y + h - r}Q${x},${y + h} ${x + r},${y + h}H${x + w}Z`;
  };

  // ---------- tooltip
  const tip = document.createElement("div");
  tip.className = "tooltip";
  tip.setAttribute("role", "status");
  document.addEventListener("DOMContentLoaded", () => document.body.appendChild(tip));
  const showTip = (html, evt) => {
    if (!tip.isConnected) document.body.appendChild(tip);
    tip.innerHTML = html;
    tip.classList.add("on");
    const pad = 14;
    const { innerWidth: W, innerHeight: H } = window;
    const r = tip.getBoundingClientRect();
    let x = evt.clientX + pad;
    let y = evt.clientY + pad;
    if (x + r.width > W - 8) x = evt.clientX - r.width - pad;
    if (y + r.height > H - 8) y = evt.clientY - r.height - pad;
    tip.style.left = Math.max(8, x) + "px";
    tip.style.top = Math.max(8, y) + "px";
  };
  const hideTip = () => tip.classList.remove("on");
  const tipRows = (title, rows) =>
    `<div class="t-title">${title}</div>` +
    rows
      .map(
        (r) =>
          `<div class="t-row"><span>${r.color ? `<i style="background:${color(r.color)}"></i>` : ""}${r.name}</span><b>${r.value}</b></div>`,
      )
      .join("");

  // ---------- mount / redraw
  const mount = (node, type, opts, draw) => {
    if (typeof node === "string") node = document.querySelector(node);
    let entry = charts.get(node);
    if (!entry) {
      node.classList.add("chart");
      entry = { node };
      entry.ro = new ResizeObserver(() => {
        const w = Math.round(node.clientWidth);
        if (w && w !== entry.w) {
          entry.w = w;
          entry.draw();
        }
      });
      entry.ro.observe(node);
      charts.set(node, entry);
    }
    entry.opts = opts;
    entry.draw = () => {
      const width = node.clientWidth || 600;
      const holder = node.querySelector(":scope > .plot") || node.appendChild(Object.assign(document.createElement("div"), { className: "plot" }));
      holder.innerHTML = "";
      draw(holder, width, opts);
    };
    entry.draw();
    if (opts.table !== false) dataTable(node, opts.tableData ? opts.tableData() : null, opts);
    return node;
  };
  const redrawAll = () => charts.forEach((e) => e.draw());
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", redrawAll);

  // Collapsible table view under each chart (accessibility + exact values)
  const dataTable = (node, data, opts) => {
    let det = node.querySelector(":scope > details.data");
    if (!data) {
      if (det) det.remove();
      return;
    }
    if (!det) {
      det = document.createElement("details");
      det.className = "data";
      det.innerHTML = "<summary>Show data</summary><div class='tbl-wrap'></div>";
      node.appendChild(det);
    }
    const [head, rows] = data;
    det.querySelector(".tbl-wrap").innerHTML =
      `<table class="tbl"><thead><tr>${head.map((h, i) => `<th class="${i ? "r" : ""}">${h}</th>`).join("")}</tr></thead><tbody>` +
      rows.map((r) => `<tr>${r.map((c, i) => `<td class="${i ? "r" : ""}">${c}</td>`).join("")}</tr>`).join("") +
      "</tbody></table>";
  };

  const legend = (node, items) => {
    if (typeof node === "string") node = document.querySelector(node);
    node.classList.add("legend");
    node.innerHTML = items
      .map((it) => `<span><i class="${it.type || ""}" style="background:${color(it.color)};border-color:${color(it.color)}"></i>${it.name}</span>`)
      .join("");
  };

  // ---------- vertical columns (grouped or stacked), optional overlay ticks
  const columns = (node, opts) =>
    mount(node, "columns", opts, (holder, W, o) => {
      const H = o.height || 240;
      const f = o.format || fmt.compact;
      const n = o.categories.length;
      const totals = o.categories.map((_, i) =>
        o.stacked ? o.series.reduce((s, se) => s + (se.values[i] || 0), 0) : Math.max(...o.series.map((se) => se.values[i] || 0)),
      );
      const overlayMax = o.overlay ? Math.max(...o.overlay.values.filter((v) => v != null)) : 0;
      const yt = ticks(0, Math.max(...totals, overlayMax) * 1.05, 4);
      const ymax = yt[yt.length - 1];
      const left = Math.max(...yt.map((t) => textWidth(f(t)))) + 10;
      const m = { t: 12, r: 8, b: 26, l: left };
      const pw = W - m.l - m.r;
      const ph = H - m.t - m.b;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": o.label || "" }, holder);
      const y = (v) => m.t + ph - (v / ymax) * ph;
      yt.forEach((t) => {
        el("line", { x1: m.l, x2: W - m.r, y1: y(t), y2: y(t), class: t === 0 ? "base-line" : "grid-line" }, svg);
        text(svg, m.l - 8, y(t) + 4, f(t), { "text-anchor": "end" });
      });
      const band = pw / n;
      const groups = o.stacked ? 1 : o.series.length;
      const bw = Math.min(24, (band * 0.72 - (groups - 1) * 2) / groups);
      const every = Math.ceil(n / Math.max(1, Math.floor(pw / Math.max(36, textWidth(o.categories[0]) + 10))));
      const bands = [];
      o.categories.forEach((cat, i) => {
        const cx = m.l + band * i + band / 2;
        const hb = el("rect", { x: m.l + band * i, y: m.t, width: band, height: ph, class: "hover-band" }, svg);
        bands.push(hb);
        if (i % every === 0) text(svg, cx, H - 8, cat, { "text-anchor": "middle" });
        if (o.stacked) {
          let acc = 0;
          const last = o.series.map((s) => s.values[i] || 0).reduce((li, v, k) => (v > 0 ? k : li), -1);
          o.series.forEach((s, k) => {
            const v = s.values[i] || 0;
            if (v <= 0) return;
            const y0 = y(acc), y1 = y(acc + v);
            const gap = acc > 0 ? 2 : 0;
            el("path", { d: k === last ? barPath(cx - bw / 2, y1, bw, y0 - y1 - gap, 4) : `M${cx - bw / 2},${y1}h${bw}v${Math.max(0, y0 - y1 - gap)}h${-bw}Z`, fill: color(s.color || slot(k)) }, svg);
            acc += v;
          });
        } else {
          const total = groups * bw + (groups - 1) * 2;
          o.series.forEach((s, k) => {
            const v = s.values[i];
            if (v == null || v <= 0) return;
            const x = cx - total / 2 + k * (bw + 2);
            const c = typeof s.color === "function" ? s.color(i) : s.color || slot(k);
            el("path", { d: barPath(x, y(v), bw, y(0) - y(v), 4), fill: color(c) }, svg);
          });
        }
        if (o.overlay && o.overlay.values[i] != null) {
          const ov = o.overlay.values[i];
          el("line", { x1: cx - bw / 2 - 5, x2: cx + bw / 2 + 5, y1: y(ov), y2: y(ov), stroke: color(o.overlay.color || "--ink"), "stroke-width": 2, "stroke-linecap": "round" }, svg);
        }
      });
      if (o.labelLast) {
        const i = n - 1;
        text(svg, m.l + band * i + band / 2, y(totals[i]) - 6, f(totals[i]), { "text-anchor": "middle", class: "val" });
      }
      // hover
      const hit = el("rect", { x: m.l, y: m.t, width: pw, height: ph, fill: "transparent" }, svg);
      let on = -1;
      hit.addEventListener("pointermove", (e) => {
        const r = svg.getBoundingClientRect();
        const i = Math.max(0, Math.min(n - 1, Math.floor(((e.clientX - r.left) * (W / r.width) - m.l) / band)));
        if (on !== i) { bands[on]?.classList.remove("on"); bands[i].classList.add("on"); on = i; }
        const rows = o.series.map((s, k) => ({ name: s.name, value: s.values[i] == null ? "–" : (o.tipFormat || f)(s.values[i]), color: typeof s.color === "function" ? s.color(i) : s.color || slot(k) }));
        if (o.stacked && o.series.length > 1) rows.push({ name: "Total", value: (o.tipFormat || f)(totals[i]) });
        if (o.overlay && o.overlay.values[i] != null) rows.push({ name: o.overlay.name, value: (o.tipFormat || f)(o.overlay.values[i]), color: o.overlay.color || "--ink" });
        if (o.tipExtra) rows.push(...o.tipExtra(i));
        showTip(tipRows(o.tipTitle ? o.tipTitle(i) : o.categories[i], rows), e);
      });
      hit.addEventListener("pointerleave", () => { bands[on]?.classList.remove("on"); on = -1; hideTip(); });
    });
  const columnsTable = (o) => [
    ["", ...o.series.map((s) => s.name), ...(o.overlay ? [o.overlay.name] : [])],
    o.categories.map((c, i) => [c, ...o.series.map((s) => (s.values[i] == null ? "–" : (o.tipFormat || o.format || fmt.compact)(s.values[i]))), ...(o.overlay ? [o.overlay.values[i] == null ? "–" : (o.tipFormat || o.format || fmt.compact)(o.overlay.values[i])] : [])]),
  ];

  // ---------- lines with crosshair, optional threshold, area wash and end labels
  const line = (node, opts) =>
    mount(node, "line", opts, (holder, W, o) => {
      const H = o.height || 240;
      const f = o.format || fmt.compact;
      const n = o.categories.length;
      const all = o.series.flatMap((s) => s.values.filter((v) => v != null));
      if (o.threshold) all.push(o.threshold.value);
      const lo = o.zero === false ? Math.min(...all) : Math.min(0, ...all);
      const hi = Math.max(...all);
      const pad = (hi - lo) * 0.08;
      const yt = ticks(o.zero === false ? lo - pad : lo, hi + pad, 4);
      const ymin = yt[0], ymax = yt[yt.length - 1];
      const endW = o.endLabels ? Math.max(...o.series.map((s) => textWidth(f(s.values[s.values.length - 1] ?? 0), 11.5))) + 12 : 0;
      const m = { t: 14, r: 10 + endW, b: 26, l: Math.max(...yt.map((t) => textWidth(f(t)))) + 10 };
      const pw = W - m.l - m.r, ph = H - m.t - m.b;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": o.label || "" }, holder);
      const x = (i) => m.l + (n === 1 ? pw / 2 : (i / (n - 1)) * pw);
      const y = (v) => m.t + ph - ((v - ymin) / (ymax - ymin)) * ph;
      yt.forEach((t) => {
        el("line", { x1: m.l, x2: m.l + pw, y1: y(t), y2: y(t), class: t === 0 || t === ymin ? "base-line" : "grid-line" }, svg);
        text(svg, m.l - 8, y(t) + 4, f(t), { "text-anchor": "end" });
      });
      const every = Math.ceil(n / Math.max(1, Math.floor(pw / (textWidth(o.categories[0]) + 18))));
      o.categories.forEach((c, i) => { if (i % every === 0) text(svg, x(i), H - 8, c, { "text-anchor": i === 0 ? "start" : "middle" }); });
      if (o.threshold) {
        const ty = y(o.threshold.value);
        if (o.threshold.below) el("rect", { x: m.l, y: ty, width: pw, height: y(ymin) - ty, fill: color("--bad"), opacity: 0.06 }, svg);
        el("line", { x1: m.l, x2: m.l + pw, y1: ty, y2: ty, stroke: color("--bad"), "stroke-width": 1.5 }, svg);
        text(svg, m.l + 4, ty - 6, o.threshold.label, { class: "lbl", style: "font-size:11px" });
      }
      o.series.forEach((s, k) => {
        const c = color(s.color || slot(k));
        const pts = s.values.map((v, i) => (v == null ? null : [x(i), y(v)]));
        const segs = [];
        let cur = [];
        pts.forEach((p) => { if (p) cur.push(p); else if (cur.length) { segs.push(cur); cur = []; } });
        if (cur.length) segs.push(cur);
        segs.forEach((seg) => {
          const d = seg.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + "," + p[1].toFixed(1)).join("");
          if (o.area && k === 0) el("path", { d: `${d}L${seg[seg.length - 1][0]},${y(Math.max(ymin, 0))}L${seg[0][0]},${y(Math.max(ymin, 0))}Z`, fill: c, opacity: 0.1 }, svg);
          el("path", { d, fill: "none", stroke: c, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round", "stroke-dasharray": s.dashed ? "5 4" : null }, svg);
        });
        const li = s.values.map((v, i) => (v == null ? -1 : i)).filter((i) => i >= 0).pop();
        if (li != null && (o.endLabels || o.endDots)) {
          el("circle", { cx: x(li), cy: y(s.values[li]), r: 4, fill: c, stroke: color("--surface"), "stroke-width": 2 }, svg);
          if (o.endLabels) text(svg, x(li) + 8, y(s.values[li]) + 4, f(s.values[li]), { class: "val" });
        }
      });
      (o.markers || []).forEach((mk) => {
        el("circle", { cx: x(mk.index), cy: y(mk.value), r: 5, fill: color("--bad"), stroke: color("--surface"), "stroke-width": 2 }, svg);
        text(svg, x(mk.index), y(mk.value) + 20, mk.label, { "text-anchor": "middle", class: "lbl", style: "font-size:11px;font-weight:600" });
      });
      // crosshair
      const g = el("g", { style: "display:none" }, svg);
      const cross = el("line", { y1: m.t, y2: m.t + ph, class: "cross" }, g);
      const dots = o.series.map((s, k) => el("circle", { r: 4, fill: color(s.color || slot(k)), stroke: color("--surface"), "stroke-width": 2 }, g));
      const hit = el("rect", { x: m.l - 6, y: m.t, width: pw + 12, height: ph, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", (e) => {
        const r = svg.getBoundingClientRect();
        const px = (e.clientX - r.left) * (W / r.width);
        const i = Math.max(0, Math.min(n - 1, Math.round(((px - m.l) / pw) * (n - 1))));
        g.style.display = "";
        cross.setAttribute("x1", x(i)); cross.setAttribute("x2", x(i));
        o.series.forEach((s, k) => {
          const v = s.values[i];
          dots[k].style.display = v == null ? "none" : "";
          if (v != null) { dots[k].setAttribute("cx", x(i)); dots[k].setAttribute("cy", y(v)); }
        });
        const rows = o.series.filter((s) => s.values[i] != null).map((s) => ({ name: s.name, value: (o.tipFormat || f)(s.values[i]), color: s.color || slot(o.series.indexOf(s)) }));
        if (o.tipExtra) rows.push(...o.tipExtra(i));
        showTip(tipRows(o.tipTitle ? o.tipTitle(i) : o.categories[i], rows), e);
      });
      hit.addEventListener("pointerleave", () => { g.style.display = "none"; hideTip(); });
    });
  const lineTable = (o) => [["", ...o.series.map((s) => s.name)], o.categories.map((c, i) => [c, ...o.series.map((s) => (s.values[i] == null ? "–" : (o.tipFormat || o.format || fmt.compact)(s.values[i])))])];

  // ---------- horizontal bars (stacked or diverging), optional target line
  const hbars = (node, opts) =>
    mount(node, "hbars", opts, (holder, W, o) => {
      const f = o.format || fmt.compact;
      const series = o.series || [{ name: o.valueName || "Value" }];
      const items = o.items;
      const rowH = o.rowHeight || 30;
      const bh = Math.min(16, rowH - 12);
      const labelW = Math.min(W * 0.42, Math.max(...items.map((it) => textWidth(it.label, 12))) + 12);
      const totals = items.map((it) => it.values.reduce((a, b) => a + b, 0));
      const lo = Math.min(0, ...totals);
      const hi = Math.max(0, ...totals, o.target ? o.target.value : 0);
      const valW = items.every((it) => it.valueLabel === "") ? 8 : Math.max(...items.map((it, i) => textWidth(it.valueLabel ?? f(totals[i]), 11.5))) + 10;
      const m = { t: o.target ? 18 : 4, r: valW, b: 4, l: labelW + (lo < 0 ? valW : 0) };
      const pw = Math.max(40, W - m.l - m.r);
      const H = m.t + items.length * rowH + m.b;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": o.label || "" }, holder);
      const x = (v) => m.l + ((v - lo) / (hi - lo || 1)) * pw;
      items.forEach((it, i) => {
        const cy = m.t + i * rowH + rowH / 2;
        const band = el("rect", { x: 0, y: m.t + i * rowH, width: W, height: rowH, class: "hover-band" }, svg);
        text(svg, 0, cy + 4, it.label, { class: "lbl" });
        let acc = 0;
        const nz = it.values.map((v, k) => (v ? k : -1)).filter((k) => k >= 0);
        it.values.forEach((v, k) => {
          if (!v) return;
          const c = color(it.color || (series[k] && series[k].color) || slot(k));
          if (v < 0) {
            el("path", { d: barPath(x(v), cy - bh / 2, x(0) - x(v), bh, 4, "left"), fill: c }, svg);
            return;
          }
          const x0 = x(acc) + (acc > 0 ? 2 : 0), x1 = x(acc + v);
          const isLast = k === nz[nz.length - 1];
          el("path", { d: isLast ? barPath(x0, cy - bh / 2, x1 - x0, bh, 4, "right") : `M${x0},${cy - bh / 2}H${x1}V${cy + bh / 2}H${x0}Z`, fill: c }, svg);
          acc += v;
        });
        const t = totals[i];
        if (it.valueLabel !== "") text(svg, t < 0 ? x(t) - 6 : x(t) + 6, cy + 4, it.valueLabel ?? f(t), { class: "val", "text-anchor": t < 0 ? "end" : "start" });
        const hit = el("rect", { x: 0, y: m.t + i * rowH, width: W, height: rowH, fill: "transparent" }, svg);
        hit.addEventListener("pointermove", (e) => {
          band.classList.add("on");
          const rows = series.length > 1
            ? series.map((s, k) => ({ name: s.name, value: (o.tipFormat || f)(it.values[k] || 0), color: s.color || slot(k) }))
            : [{ name: series[0].name, value: (o.tipFormat || f)(t), color: it.color || series[0].color || slot(0) }];
          if (series.length > 1) rows.push({ name: "Total", value: (o.tipFormat || f)(t) });
          if (it.extra) rows.push(...it.extra);
          showTip(tipRows(it.label, rows), e);
        });
        hit.addEventListener("pointerleave", () => { band.classList.remove("on"); hideTip(); });
      });
      if (lo < 0) el("line", { x1: x(0), x2: x(0), y1: m.t - 2, y2: H - m.b, class: "base-line" }, svg);
      if (o.target) {
        const tx = x(o.target.value);
        el("line", { x1: tx, x2: tx, y1: m.t - 4, y2: H - m.b, stroke: color("--ink"), "stroke-width": 1.5, opacity: 0.6 }, svg);
        text(svg, tx, 11, o.target.label, { "text-anchor": "middle", class: "lbl", style: "font-size:11px" });
      }
    });
  const hbarsTable = (o) => {
    const series = o.series || [{ name: o.valueName || "Value" }];
    const f = o.tipFormat || o.format || fmt.compact;
    return [["", ...series.map((s) => s.name)], o.items.map((it) => [it.label, ...series.map((_, k) => f(it.values[k] || 0))])];
  };

  // ---------- heatmap (sequential teal ramp)
  const heatmap = (node, opts) =>
    mount(node, "heatmap", opts, (holder, W, o) => {
      const f = o.format || fmt.compact;
      const labelW = Math.max(...o.rows.map((r) => textWidth(r, 11))) + 10;
      const cols = o.cols.length;
      const cw = (W - labelW) / cols;
      const ch = o.cellHeight || 26;
      const H = o.rows.length * ch + 22;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": o.label || "" }, holder);
      const flat = o.values.flat().filter((v) => v != null);
      const lo = o.min ?? Math.min(...flat), hi = o.max ?? Math.max(...flat);
      const ramp = ["--q0", "--q1", "--q2", "--q3", "--q4", "--q5", "--q6", "--q7"].map(cssVar);
      const dv = o.diverging;
      // Diverging: teal above the midpoint, orange below, neutral at it
      const pick = (v) => {
        if (!dv) return { fill: ramp[Math.max(0, Math.min(7, Math.floor(((v - lo) / (hi - lo || 1)) * 7.999)))], op: 1 };
        const t = Math.max(-1, Math.min(1, (v - dv.mid) / dv.span));
        return Math.abs(t) < 0.08 ? { fill: cssVar("--surface-2"), op: 1, neutral: true } : { fill: cssVar(t > 0 ? "--s1" : "--s2"), op: 0.18 + 0.82 * Math.abs(t) };
      };
      const every = Math.ceil(cols / Math.max(1, Math.floor((W - labelW) / 30)));
      o.cols.forEach((c, j) => { if (j % every === 0) text(svg, labelW + cw * j + cw / 2, H - 6, c, { "text-anchor": "middle", class: o.showValues ? "lbl" : null, style: o.showValues ? "font-size:11px" : null }); });
      o.rows.forEach((r, i) => {
        text(svg, 0, i * ch + ch / 2 + 4, r, { class: "lbl", style: "font-size:11.5px" });
        o.values[i].forEach((v, j) => {
          if (v == null) return;
          const pc = pick(v);
          const cell = el("rect", { x: labelW + cw * j + 1, y: i * ch + 1, width: Math.max(1, cw - 2), height: ch - 2, rx: 3, fill: pc.fill, "fill-opacity": pc.op }, svg);
          if (o.showValues && cw > 34) text(svg, labelW + cw * j + cw / 2, i * ch + ch / 2 + 4, f(v), { "text-anchor": "middle", style: `fill:${pc.op > 0.62 && !pc.neutral ? "#fff" : cssVar("--ink")};font-size:11.5px;font-weight:600;pointer-events:none` });
          cell.addEventListener("pointermove", (e) => showTip(tipRows(`${r} · ${o.cols[j]}`, [{ name: o.valueName || "Value", value: f(v) }]), e));
          cell.addEventListener("pointerleave", hideTip);
        });
      });
    });
  const heatTable = (o) => [["", ...o.cols], o.rows.map((r, i) => [r, ...o.values[i].map((v) => (v == null ? "–" : (o.format || fmt.compact)(v)))])];
  const heatLegend = (node, lowLabel, highLabel) => {
    if (typeof node === "string") node = document.querySelector(node);
    node.classList.add("legend");
    node.innerHTML = `<span>${lowLabel}</span>` + ["--q0", "--q1", "--q2", "--q3", "--q4", "--q5", "--q6", "--q7"].map((q) => `<i style="background:var(${q});margin-right:-4px"></i>`).join("") + `<span style="margin-left:6px">${highLabel}</span>`;
  };

  // ---------- waterfall (totals from zero, steps float; up = teal, down = orange)
  const waterfall = (node, opts) =>
    mount(node, "waterfall", opts, (holder, W, o) => {
      const H = o.height || 260;
      const f = o.format || fmt.compact;
      let run = 0;
      const bars = o.steps.map((s) => {
        if (s.total) { run = s.value; return { ...s, y0: 0, y1: s.value }; }
        const b = { ...s, y0: run, y1: run + s.value };
        run += s.value;
        return b;
      });
      const hi = Math.max(...bars.map((b) => Math.max(b.y0, b.y1)));
      const yt = ticks(0, hi * 1.08, 4);
      const ymax = yt[yt.length - 1];
      const m = { t: 18, r: 6, b: 34, l: Math.max(...yt.map((t) => textWidth(f(t)))) + 10 };
      const pw = W - m.l - m.r, ph = H - m.t - m.b;
      const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, height: H, role: "img", "aria-label": o.label || "" }, holder);
      const y = (v) => m.t + ph - (v / ymax) * ph;
      yt.forEach((t) => {
        el("line", { x1: m.l, x2: W - m.r, y1: y(t), y2: y(t), class: t === 0 ? "base-line" : "grid-line" }, svg);
        text(svg, m.l - 8, y(t) + 4, f(t), { "text-anchor": "end" });
      });
      const band = pw / bars.length;
      const bw = Math.min(40, band * 0.62);
      bars.forEach((b, i) => {
        const cx = m.l + band * i + band / 2;
        const top = Math.min(y(b.y0), y(b.y1)), h = Math.max(1.5, Math.abs(y(b.y0) - y(b.y1)));
        const c = b.total ? "--s3" : b.value >= 0 ? "--s1" : "--s2";
        el("path", { d: b.total || b.value >= 0 ? barPath(cx - bw / 2, top, bw, h, 3) : `M${cx - bw / 2},${top}h${bw}v${h}h${-bw}Z`, fill: color(c) }, svg);
        if (i < bars.length - 1) el("line", { x1: cx + bw / 2, x2: cx + band - bw / 2, y1: y(b.y1), y2: y(b.y1), stroke: color("--axis"), "stroke-width": 1 }, svg);
        const lf = o.labelFormat || f;
        const lbl = b.total ? f(b.value) : (b.value >= 0 ? "+" : "−") + f(Math.abs(b.value));
        text(svg, cx, top - 6, b.total ? lf(b.value) : (b.value >= 0 ? "+" : "−") + lf(Math.abs(b.value)), { "text-anchor": "middle", class: "val", style: "font-size:11px" });
        const words = b.label.split(" ");
        const lines = textWidth(b.label) > band - 4 && words.length > 1 ? [words.slice(0, Math.ceil(words.length / 2)).join(" "), words.slice(Math.ceil(words.length / 2)).join(" ")] : [b.label];
        lines.forEach((ln, k) => text(svg, cx, H - 20 + k * 12, ln, { "text-anchor": "middle", class: "lbl", style: "font-size:11px" }));
        const hit = el("rect", { x: cx - band / 2, y: m.t, width: band, height: ph, fill: "transparent" }, svg);
        hit.addEventListener("pointermove", (e) => showTip(tipRows(b.label, [{ name: b.total ? "Total" : "Change", value: lbl, color: c }, ...(b.extra || [])]), e));
        hit.addEventListener("pointerleave", hideTip);
      });
    });
  const waterfallTable = (o) => [["Step", "Value"], o.steps.map((s) => [s.label, (s.total ? "" : s.value >= 0 ? "+" : "−") + (o.format || fmt.compact)(Math.abs(s.value))])];

  // ---------- sortable table
  const table = (node, opts) => {
    if (typeof node === "string") node = document.querySelector(node);
    const state = node._tbl || (node._tbl = { sort: opts.sort || null, dir: opts.dir || -1, limit: opts.limit || Infinity });
    if (opts.resetLimit) state.limit = opts.limit || Infinity;
    const rows = [...opts.rows];
    if (state.sort) {
      const col = opts.columns.find((c) => c.key === state.sort);
      const val = col && (col.value || ((r) => r[col.key]));
      if (val) rows.sort((a, b) => { const x = val(a), y = val(b); return (x > y ? 1 : x < y ? -1 : 0) * state.dir; });
    }
    const shown = rows.slice(0, state.limit);
    node.innerHTML =
      `<div class="tbl-wrap"><table class="tbl"><thead><tr>` +
      opts.columns.map((c) => `<th class="${c.align === "right" ? "r " : ""}${c.sortable !== false ? "sortable" : ""}" data-k="${c.key}">${c.label}${state.sort === c.key ? ` <span class="arr">${state.dir > 0 ? "▲" : "▼"}</span>` : ""}</th>`).join("") +
      `</tr></thead><tbody>` +
      shown.map((r) => `<tr class="${r._class || ""}">` + opts.columns.map((c) => `<td class="${c.align === "right" ? "r" : ""} ${c.cls || ""}">${c.render ? c.render(r) : r[c.key]}</td>`).join("") + "</tr>").join("") +
      (shown.length ? "" : `<tr><td colspan="${opts.columns.length}" class="dim">No rows match the filters.</td></tr>`) +
      `</tbody></table></div>` +
      (rows.length > shown.length ? `<div class="more"><button class="btn ghost" type="button">Show all ${rows.length} rows</button></div>` : "");
    node.querySelectorAll("th.sortable").forEach((th) =>
      th.addEventListener("click", () => {
        const k = th.dataset.k;
        if (state.sort === k) state.dir *= -1; else { state.sort = k; state.dir = -1; }
        table(node, { ...opts, resetLimit: false });
      }),
    );
    const more = node.querySelector(".more button");
    if (more) more.addEventListener("click", () => { state.limit = Infinity; table(node, { ...opts, resetLimit: false }); });
  };

  // ---------- KPI tiles
  const kpis = (node, items) => {
    if (typeof node === "string") node = document.querySelector(node);
    node.innerHTML = items
      .map(
        (k) => `<div class="kpi"><div class="k-label">${k.label}</div><div class="k-value">${k.value}</div><div class="k-sub">${
          k.delta ? `<span class="delta ${k.delta.tone}">${k.delta.tone === "good" ? "▲" : k.delta.tone === "bad" ? "▼" : ""} ${k.delta.text}</span>` : ""
        }${k.sub ? `<span>${k.sub}</span>` : ""}</div></div>`,
      )
      .join("");
  };

  // ---------- segmented control + select
  const segmented = (node, options, value, onChange) => {
    if (typeof node === "string") node = document.querySelector(node);
    node.classList.add("seg");
    node.setAttribute("role", "group");
    node.innerHTML = options.map((o) => `<button type="button" data-v="${o.value}" aria-pressed="${o.value === value}">${o.label}</button>`).join("");
    node.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      node.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b));
      onChange(b.dataset.v);
    });
  };
  const select = (node, options, value, onChange) => {
    if (typeof node === "string") node = document.querySelector(node);
    node.innerHTML = options.map((o) => `<option value="${o.value}"${o.value === value ? " selected" : ""}>${o.label}</option>`).join("");
    node.addEventListener("change", () => onChange(node.value));
  };

  // Tabs: <div class="tabs" role="tablist"><button data-tab="panel-id">…</button></div>
  const tabs = (node) => {
    if (typeof node === "string") node = document.querySelector(node);
    const btns = [...node.querySelectorAll("button[data-tab]")];
    const show = (b) => {
      btns.forEach((x) => {
        const on = x === b;
        x.setAttribute("aria-selected", on);
        x.tabIndex = on ? 0 : -1;
        document.getElementById(x.dataset.tab).hidden = !on;
      });
      try { history.replaceState(null, "", "#" + b.dataset.tab); } catch (e) {}
    };
    node.setAttribute("role", "tablist");
    btns.forEach((b, i) => {
      b.setAttribute("role", "tab");
      b.setAttribute("aria-controls", b.dataset.tab);
      document.getElementById(b.dataset.tab).setAttribute("role", "tabpanel");
      b.addEventListener("click", () => show(b));
      b.addEventListener("keydown", (e) => {
        const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (d) { const n = btns[(i + d + btns.length) % btns.length]; n.focus(); show(n); }
      });
    });
    show(btns.find((b) => "#" + b.dataset.tab === location.hash) || btns[0]);
  };

  const sum = (arr, f = (x) => x) => arr.reduce((s, x, i) => s + f(x, i), 0);
  const delta = (cur, prev, upIsGood = true, suffix = "vs prior period") => {
    if (!prev) return null;
    const ch = ((cur - prev) / Math.abs(prev)) * 100;
    const tone = Math.abs(ch) < 0.5 ? "neutral" : (ch > 0) === upIsGood ? "good" : "bad";
    return { text: `${fmt.signedPct(ch)} ${suffix}`, tone };
  };

  window.Dash = {
    fmt, color, slot, legend, kpis, table, segmented, select, sum, delta, heatLegend, tabs,
    columns: (n, o) => columns(n, { ...o, tableData: () => columnsTable(o) }),
    line: (n, o) => line(n, { ...o, tableData: () => lineTable(o) }),
    hbars: (n, o) => hbars(n, { ...o, tableData: () => hbarsTable(o) }),
    heatmap: (n, o) => heatmap(n, { ...o, tableData: () => heatTable(o) }),
    waterfall: (n, o) => waterfall(n, { ...o, tableData: () => waterfallTable(o) }),
  };
})();
