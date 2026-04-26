const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Team Chirutha";
pres.title = "Végam – TVASTR '26";

// ── BRAND PALETTE ──────────────────────
const C = {
  floralWhite: "FFFCF2",
  dustGrey: "CCC5B9",
  charcoal: "403D39",
  carbonBlack: "252422",
  paprika: "EB5E28",
  green: "2D6A4F",
  blue: "1C7293",
  purple: "7B5EA7",
  white: "FFFFFF",
};

const FH = "Georgia";
const FB = "Calibri";
const FM = "Courier New";

const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

// ─── helpers ──────────────────────────────────────────────────────────────────

function card(slide, x, y, w, h, accent, title, body, bodySize = 10) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 },
    shadow: makeShadow()
  });
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.06, fill: { color: accent } });
  if (title) slide.addText(title, { x: x + 0.14, y: y + 0.12, w: w - 0.28, h: 0.32, fontSize: 11, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
  if (body) slide.addText(body, { x: x + 0.14, y: y + 0.48, w: w - 0.28, h: h - 0.58, fontSize: bodySize, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });
}

function darkCard(slide, x, y, w, h, accent, title, subtitle, body, bodySize = 10) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.carbonBlack } });
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h, fill: { color: accent } });
  if (title) slide.addText(title, { x: x + 0.2, y: y + 0.1, w: w - 0.3, h: 0.3, fontSize: 11, bold: true, color: C.white, fontFace: FB, margin: 0 });
  if (subtitle) slide.addText(subtitle, { x: x + 0.2, y: y + 0.38, w: w - 0.3, h: 0.2, fontSize: 8, italic: true, color: accent, fontFace: FB, margin: 0 });
  if (body) slide.addText(body, { x: x + 0.2, y: subtitle ? y + 0.6 : y + 0.45, w: w - 0.3, h: subtitle ? h - 0.7 : h - 0.55, fontSize: bodySize, color: C.dustGrey, fontFace: FB, valign: "top", margin: 0 });
}

function sectionTag(slide, x, y, label, color) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.05, h: 0.28, fill: { color } });
  slide.addText(label, { x: x + 0.1, y: y, w: 4, h: 0.28, fontSize: 8, bold: true, color, fontFace: FB, charSpacing: 2, margin: 0 });
}

// ====================================================================
// SLIDE 1 — COVER
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Left accent strip
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.paprika } });

  // Top-right tag
  s.addShape(pres.shapes.RECTANGLE, { x: 7.2, y: 0.28, w: 2.6, h: 0.55, fill: { color: C.paprika } });
  s.addText("TVASTR '26  //  HACKATHON", { x: 7.2, y: 0.28, w: 2.6, h: 0.55, fontSize: 9, bold: true, color: C.white, fontFace: FB, align: "center", valign: "middle", charSpacing: 2, margin: 0 });

  // Hero name
  s.addText("Végam", { x: 0.4, y: 1.2, w: 6.5, h: 1.8, fontSize: 108, bold: true, color: C.carbonBlack, fontFace: FH, align: "left", margin: 0 });

  // Tagline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.1, w: 5.8, h: 0.04, fill: { color: C.paprika } });
  s.addText("LOGISTICS INTELLIGENCE & FORENSIC DEEP DIVE", {
    x: 0.4, y: 3.24, w: 6, h: 0.38,
    fontSize: 13, bold: true, color: C.paprika, fontFace: FB, charSpacing: 3, margin: 0
  });

  // Sub-tagline
  s.addText("Predict  ·  Prioritize  ·  Optimize", {
    x: 0.4, y: 3.7, w: 6, h: 0.35,
    fontSize: 12, color: C.charcoal, fontFace: FH, italic: true, margin: 0
  });

  // Team block
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 4.35, w: 3.2, h: 0.9, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 }, shadow: makeShadow() });
  s.addText("TEAM CHIRUTHA", { x: 0.55, y: 4.45, w: 3, h: 0.3, fontSize: 11, bold: true, color: C.paprika, fontFace: FB, charSpacing: 2, margin: 0 });
  s.addText("Bindu Darshitha  ·  Abhinav Mucharla  ·  Pranav Raj Galipalli", {
    x: 0.55, y: 4.78, w: 3, h: 0.3, fontSize: 7.5, color: C.charcoal, fontFace: FB, margin: 0
  });

  // Right decorative grid of dots
  for (let r = 0; r < 6; r++) {
    for (let c = 0; c < 6; c++) {
      s.addShape(pres.shapes.OVAL, {
        x: 7.5 + c * 0.38, y: 1.5 + r * 0.65,
        w: 0.06, h: 0.06,
        fill: { color: r === 2 && c === 2 ? C.paprika : C.dustGrey }
      });
    }
  }
}

// ====================================================================
// SLIDE 2 — PROBLEM STATEMENT
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Problem Statement", {
    x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0
  });
  s.addText("Why current logistics systems are failing operations teams", {
    x: 0.5, y: 0.72, w: 9, h: 0.3, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0
  });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.71, w: 2.7, h: 0.04, fill: { color: C.paprika } });

  // ── 4 pain-point rows (icon-circle + bold title + description) ──────────
  const pains = [
    { color: C.paprika, num: "01", title: "Reactive, Not Proactive", desc: "Delays are discovered after they happen — leaving no time to course-correct or reschedule." },
    { color: C.blue, num: "02", title: "Cascading Project Delays", desc: "One late delivery halts an entire project site, multiplying costs and missing SLAs." },
    { color: C.charcoal, num: "03", title: "Opaque Decision-Making", desc: "Managers lack visibility into why delays occur — so the same problems repeat every cycle." },
    { color: C.green, num: "04", title: "No Prioritization Framework", desc: "Limited delivery capacity is allocated subjectively, not by risk or business impact." },
  ];

  pains.forEach((p, i) => {
    const y = 1.2 + i * 0.97;
    // Number pill
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 0.55, h: 0.75, fill: { color: p.color } });
    s.addText(p.num, { x: 0.5, y, w: 0.55, h: 0.75, fontSize: 18, bold: true, color: C.white, fontFace: FM, align: "center", valign: "middle", margin: 0 });
    // Content block
    s.addShape(pres.shapes.RECTANGLE, {
      x: 1.15, y, w: 8.35, h: 0.75,
      fill: { color: C.white }, line: { color: C.dustGrey, width: 0.6 },
      shadow: makeShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, { x: 1.15, y, w: 0.05, h: 0.75, fill: { color: p.color } });
    s.addText(p.title, { x: 1.3, y: y + 0.1, w: 3.8, h: 0.28, fontSize: 12, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
    s.addText(p.desc, { x: 1.3, y: y + 0.38, w: 8.0, h: 0.28, fontSize: 10, color: C.charcoal, fontFace: FB, margin: 0 });
  });
}

// ====================================================================
// SLIDE 3 — SOLUTION OVERVIEW
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Solution Overview", { x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Five-stage intelligence pipeline from raw data to prescriptive action", {
    x: 0.5, y: 0.72, w: 9, h: 0.3, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0
  });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.71, w: 2.6, h: 0.04, fill: { color: C.paprika } });

  // Pipeline flow
  const steps = [
    { t: "Data\nIngestion", c: C.charcoal },
    { t: "XGBoost\nPrediction", c: C.charcoal },
    { t: "SHAP\nForensics", c: C.charcoal },
    { t: "Reward\nOptimization", c: C.charcoal },
    { t: "War Room\nDashboard", c: C.paprika },
  ];
  const fw = 1.65, fh = 0.85, fy = 1.15, gap = 0.18;
  steps.forEach((st, i) => {
    const x = 0.45 + i * (fw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: fy, w: fw, h: fh, fill: { color: st.c } });
    s.addText(st.t, { x, y: fy, w: fw, h: fh, fontSize: 10, bold: true, color: C.white, fontFace: FB, align: "center", valign: "middle", margin: 0 });
    if (i < steps.length - 1) {
      s.addShape(pres.shapes.RIGHT_ARROW, { x: x + fw + 0.02, y: fy + fh / 2 - 0.1, w: gap - 0.04, h: 0.2, fill: { color: C.paprika }, line: { color: C.paprika } });
    }
  });

  // 2×2 feature cards
  const cards = [
    { t: "Predictive Forensics", d: "XGBoost regression predicts delay hours across 14 feature dimensions — weather, traffic, routing complexity, factory variability.", acc: C.paprika },
    { t: "Glass-Box Explainability", d: "TreeSHAP decomposes every prediction into ranked root-causes. Full transparency for every dispatch decision.", acc: C.blue },
    { t: "Digital Twin Optimizer", d: "Simulates thousands of corrective permutations — temporal rescheduling & factory swaps — to maximize on-time reward.", acc: C.green },
    { t: "War Room Dashboard", d: "4-page Streamlit command center: Operations Overview, Daily Optimizer, Deep Dive Forensics, and Executive LLM Reports.", acc: C.purple },
  ];
  const cw = 4.4, ch = 1.45, sx = 0.45, sy = 2.22, cgap = 0.3;
  cards.forEach((c, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const cx = sx + col * (cw + cgap), cy = sy + row * (ch + 0.2);
    darkCard(s, cx, cy, cw, ch, c.acc, c.t, null, c.d, 10);
  });
}

// ====================================================================
// SLIDE 4 — DATA PIPELINE (Stages 1–2) — Exact Image Match
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Data Pipeline & Feature Engineering", { x: 0.4, y: 0.2, w: 9.2, h: 0.5, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.65, w: 4.8, h: 0.04, fill: { color: C.paprika } });

  sectionTag(s, 0.38, 0.82, "STAGE 1: RAW INPUT DATASETS", C.paprika);

  const datasets = [
    { label: "DELIVERIES", sub: "Main Table", fields: "delivery_id, factory_id,\nproject_id\ndistance_km, expected_time_hours\nactual_time_hours, delay_flag,\ndate", accent: C.paprika },
    { label: "FACTORIES", sub: "Supply Side", fields: "factory_id, latitude, longitude\nbase_production_per_week\nproduction_variability,\nmax_storage", accent: C.blue },
    { label: "PROJECTS", sub: "Demand Side", fields: "project_id, latitude, longitude\ndemand, priority_level", accent: C.green },
    { label: "EXT. FACTORS", sub: "Daily Environment", fields: "date\nweather_index\ntraffic_index", accent: C.purple },
  ];

  const cW = 2.2, cH = 1.3, cY = 1.1, cGap = 0.12, cStartX = 0.38;
  datasets.forEach((ds, i) => {
    const x = cStartX + i * (cW + cGap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cY, w: cW, h: cH, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.5 }, shadow: makeShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cY, w: cW, h: 0.06, fill: { color: ds.accent } });
    s.addText(ds.label, { x: x + 0.1, y: cY + 0.1, w: cW - 0.2, h: 0.25, fontSize: 10, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
    s.addText(ds.sub, { x: x + 0.1, y: cY + 0.33, w: cW - 0.2, h: 0.18, fontSize: 8, italic: true, color: ds.accent, fontFace: FB, margin: 0 });
    s.addShape(pres.shapes.LINE, { x: x + 0.1, y: cY + 0.52, w: cW - 0.2, h: 0, line: { color: C.dustGrey, width: 0.5 } });
    s.addText(ds.fields, { x: x + 0.1, y: cY + 0.56, w: cW - 0.2, h: 0.65, fontSize: 7, color: C.charcoal, fontFace: FM, valign: "top", margin: 0 });
  });

  // ── Dashed funnel convergence ────────────────────────────────────
  const centers = datasets.map((_, i) => cStartX + i * (cW + cGap) + cW / 2);
  const slideCenter = (centers[0] + centers[3]) / 2;
  const arrowTopY = cY + cH + 0.06;
  const mergeLineY = arrowTopY + 0.25;
  const arrowBotY = mergeLineY + 0.22;

  centers.forEach((cx) => {
    s.addShape(pres.shapes.LINE, { x: cx, y: arrowTopY, w: 0, h: mergeLineY - arrowTopY, line: { color: C.dustGrey, width: 0.8, dashType: "dash" } });
  });
  s.addShape(pres.shapes.LINE, { x: centers[0], y: mergeLineY, w: centers[3] - centers[0], h: 0, line: { color: C.dustGrey, width: 0.8, dashType: "dash" } });
  s.addShape(pres.shapes.LINE, { x: slideCenter, y: mergeLineY, w: 0, h: arrowBotY - mergeLineY, line: { color: C.charcoal, width: 1.2 } });
  s.addShape(pres.shapes.RECTANGLE, { x: slideCenter - 0.05, y: arrowBotY - 0.05, w: 0.1, h: 0.1, fill: { color: C.paprika }, rotate: 45 });

  // Merge pill
  const pY = arrowBotY + 0.05, pW = 4.2, pH = 0.32;
  s.addShape(pres.shapes.RECTANGLE, { x: slideCenter - pW / 2, y: pY, w: pW, h: pH, fill: { color: C.carbonBlack } });
  s.addText("STAGE 2: FORENSIC AUDIT & MERGED DATASET", { x: slideCenter - pW / 2, y: pY, w: pW, h: pH, fontSize: 8, bold: true, color: C.white, fontFace: FB, align: "center", valign: "middle", charSpacing: 1.5, margin: 0 });

  // ── Dotted flow from pill to features ────────────────────────────
  const chipSectionTop = pY + pH + 0.15;
  // Feature chips header
  sectionTag(s, 0.38, chipSectionTop, "14 FINAL MODEL FEATURES", C.paprika);

  const flowMid = chipSectionTop + 0.35; // Horizontal line level
  const chY = flowMid + 0.3; // Start of the feature chips group headers

  // Center vertical from pill down to flowMid
  s.addShape(pres.shapes.LINE, { x: slideCenter, y: pY + pH, w: 0, h: flowMid - (pY + pH), line: { color: C.dustGrey, width: 0.8, dashType: "dash" } });

  const groupDefs = [
    { label: "MAIN TABLE", features: [{ n: "01", f: "distance_km" }, { n: "06", f: "haversine_km" }, { n: "07", f: "routing_complexity" }], accent: C.paprika, w: 1.85 },
    { label: "SUPPLY SIDE", features: [{ n: "04", f: "base_prod_per_week" }, { n: "05", f: "prod_variability" }, { n: "08", f: "supply_risk" }], accent: C.blue, w: 1.85 },
    { label: "DEMAND SIDE", features: [{ n: "14", f: "priority_encoded" }], accent: C.green, w: 1.85 },
    {
      label: "DAILY ENV.", features: [
        { n: "02", f: "weather_index" }, { n: "03", f: "traffic_index" }, { n: "09", f: "ext_severity" }, { n: "10", f: "ext_compound" },
        { n: "11", f: "day_of_week" }, { n: "12", f: "is_weekend" }, { n: "13", f: "week_of_month" }
      ], accent: C.purple, w: 3.75
    },
  ];

  let gx = 0.38;
  const featureCenters = [];
  groupDefs.forEach(grp => {
    featureCenters.push(gx + grp.w / 2);
    gx += grp.w + 0.14;
  });

  // Horizontal line connecting column centers
  s.addShape(pres.shapes.LINE, { x: featureCenters[0], y: flowMid, w: featureCenters[3] - featureCenters[0], h: 0, line: { color: C.dustGrey, width: 0.8, dashType: "dash" } });

  // Vertical lines from flowMid down to group headers
  featureCenters.forEach(cx => {
    s.addShape(pres.shapes.LINE, { x: cx, y: flowMid, w: 0, h: (chY - 0.2) - flowMid, line: { color: C.dustGrey, width: 0.8, dashType: "dash" } });
  });

  const chH = 0.22, chG = 0.04;
  gx = 0.38; // Reset x position to draw groups

  groupDefs.forEach((grp) => {
    const gw = grp.w;
    s.addText(grp.label, { x: gx, y: chY - 0.18, w: gw, h: 0.16, fontSize: 6.5, bold: true, color: grp.accent, fontFace: FB, charSpacing: 1.5, margin: 0 });
    s.addShape(pres.shapes.LINE, { x: gx, y: chY - 0.04, w: gw, h: 0, line: { color: grp.accent, width: 1.2 } });

    const maxPerCol = 4;
    const useSub = grp.features.length > maxPerCol;
    const subW = useSub ? (gw - 0.08) / 2 : gw;

    grp.features.forEach((feat, fi) => {
      const col = useSub ? Math.floor(fi / maxPerCol) : 0;
      const row = useSub ? fi % maxPerCol : fi;
      const fx = gx + col * (subW + 0.08);
      const fy = chY + row * (chH + chG);

      s.addShape(pres.shapes.RECTANGLE, { x: fx, y: fy, w: subW, h: chH, fill: { color: C.white }, line: { color: grp.accent, width: 0.7 } });
      s.addShape(pres.shapes.RECTANGLE, { x: fx, y: fy, w: 0.04, h: chH, fill: { color: grp.accent } });
      s.addText(feat.n, { x: fx + 0.07, y: fy, w: 0.22, h: chH, fontSize: 6, bold: true, color: grp.accent, fontFace: FM, valign: "middle", margin: 0 });
      s.addText(feat.f, { x: fx + 0.28, y: fy, w: subW - 0.32, h: chH, fontSize: 6, color: C.carbonBlack, fontFace: FM, valign: "middle", margin: 0 });
    });
    gx += gw + 0.14;
  });

  // Footer note
  s.addText("“Redundancies removed for streamlined analysis.”", {
    x: 0, y: 5.25, w: 10, h: 0.3,
    fontSize: 9, italic: true, color: C.charcoal, fontFace: FB, align: "center", margin: 0
  });
}

// ====================================================================
// SLIDE 5 — DATA MERGING & FEATURE ENGINEERING (Two-Column)
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Header
  s.addText("Data Merging and Feature Engineering", { x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Rigorous data preparation ensuring model integrity and temporal validity", {
    x: 0.5, y: 0.72, w: 9, h: 0.3, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0
  });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.71, w: 4.8, h: 0.04, fill: { color: C.paprika } });

  // Team Chirutha tag
  s.addText('TEAM CHIRUTHA', { x: 7.5, y: 0.2, w: 2.1, h: 0.26, fontSize: 8, bold: true, color: C.dustGrey, fontFace: FB, charSpacing: 2, align: 'right', margin: 0 });

  // Columns setup
  const colY = 1.3;
  const colW = 4.2;

  // Left Column
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: colY, w: colW, h: 0.4, fill: { color: C.paprika } });
  s.addText("STAGE 1 — DATA MERGING & FEATURE SYNTHESIS", { x: 0.5, y: colY, w: colW, h: 0.4, fontSize: 10, bold: true, color: C.white, fontFace: FH, align: "center", valign: "middle", charSpacing: 1, margin: 0 });

  const stage1 = [
    { t: "Problem Reframing", d: "Transitioned to a continuous target variable (delay_hours) to capture severity over binary occurrence." },
    { t: "Leakage Elimination", d: "Dropped post-delivery columns and zero-variance features to ensure model integrity." },
    { t: "Dataset Fusion", d: "Merged External Factors, Factory Data, and Projects into a single enriched record per delivery." },
    { t: "Feature Synthesis", d: "Derived 14 model-ready features (e.g., external_severity, compound_weather_risk, and supply_risk)." },
    { t: "Metadata Retention", d: "Preserved factory_id and project_id specifically for the Stage 5 Optimization Layer." }
  ];

  stage1.forEach((item, i) => {
    const y = colY + 0.55 + i * 0.75;
    // Number badge
    s.addShape(pres.shapes.OVAL, { x: 0.5, y: y + 0.05, w: 0.3, h: 0.3, fill: { color: C.paprika } });
    s.addText(String(i + 1), { x: 0.5, y: y + 0.05, w: 0.3, h: 0.3, fontSize: 10, bold: true, color: C.white, fontFace: FB, align: "center", valign: "middle", margin: 0 });

    // Content
    s.addText(item.t, { x: 0.95, y: y, w: colW - 0.45, h: 0.2, fontSize: 11, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
    s.addText(item.d, { x: 0.95, y: y + 0.22, w: colW - 0.45, h: 0.4, fontSize: 9.5, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });
  });

  // Right Column
  const rightX = 5.3;
  s.addShape(pres.shapes.RECTANGLE, { x: rightX, y: colY, w: colW, h: 0.4, fill: { color: C.blue } });
  s.addText("STAGE 2 — FEATURE AUDIT & TEMPORAL PREP", { x: rightX, y: colY, w: colW, h: 0.4, fontSize: 10, bold: true, color: C.white, fontFace: FH, align: "center", valign: "middle", charSpacing: 1, margin: 0 });

  const stage2 = [
    { t: "Chronological Integrity", d: "Sorted data by date to prevent future-data leakage—critical for time-dependent delivery patterns." },
    { t: "Correlation Audit", d: "Validated engineered features (external_compound) against the target to ensure predictive value." },
    { t: "Temporal Split", d: "Implemented an 80/20 Time-Based Split (Training on past, Testing on future) to mirror real deployment." },
    { t: "Cross-Validation", d: "Applied TimeSeriesSplit to ensure each fold validates only on subsequent data points." },
    { t: "Standardization", d: "Utilized StandardScaler (fitted only on training data) to provide a clean baseline for linear comparisons." }
  ];

  stage2.forEach((item, i) => {
    const y = colY + 0.55 + i * 0.75;
    // Number badge
    s.addShape(pres.shapes.OVAL, { x: rightX, y: y + 0.05, w: 0.3, h: 0.3, fill: { color: C.blue } });
    s.addText(String(i + 1), { x: rightX, y: y + 0.05, w: 0.3, h: 0.3, fontSize: 10, bold: true, color: C.white, fontFace: FB, align: "center", valign: "middle", margin: 0 });

    // Content
    s.addText(item.t, { x: rightX + 0.45, y: y, w: colW - 0.45, h: 0.2, fontSize: 11, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
    s.addText(item.d, { x: rightX + 0.45, y: y + 0.22, w: colW - 0.45, h: 0.4, fontSize: 9.5, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });
  });
}

// ====================================================================
// SLIDE 6 — MODELING & EXPLAINABILITY (Stages 3–4)  [GLASS-BOX VISUAL]
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Modeling & Glass-Box Explainability", { x: 0.4, y: 0.18, w: 9.2, h: 0.5, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.63, w: 4.8, h: 0.04, fill: { color: C.paprika } });

  // LEFT: Stage 3 – XGBoost Pipeline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.85, w: 4.5, h: 4.4, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.85, w: 4.5, h: 0.36, fill: { color: C.blue } });
  s.addText("STAGE 3: TUNED XGBOOST PIPELINE", { x: 0.52, y: 0.85, w: 4.26, h: 0.36, fontSize: 10, bold: true, color: C.white, fontFace: FH, valign: "middle", charSpacing: 1.5, margin: 0 });

  const s3steps = [
    { t: "1. BASELINE BENCHMARKING", d: "Null Model → Ridge Regression → XGBoost benchmark to quantify uplift." },
    { t: "2. BAYESIAN OPTIMIZATION", d: "50+ Optuna trials over tree depth, learning rate, subsample, λ & α." },
    { t: "3. MEDIAN-ROBUST LOSS (MAE)", d: "Optimizing MAE over RMSE resists heavy-tail outlier contamination." },
    { t: "4. TEMPORAL VALIDATION", d: "Strict time-based splits. TimeSeriesSplit CV. Zero data leakage." },
  ];
  s3steps.forEach((st, i) => {
    const sy = 1.37 + i * 0.82;

    // Card background inside the white container
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: sy, w: 4.2, h: 0.67, fill: { color: C.floralWhite }, line: { color: C.dustGrey, width: 0.5 } });
    // Left blue accent
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: sy, w: 0.08, h: 0.67, fill: { color: C.blue } });

    // Title (Calibri bold, spaced)
    s.addText(st.t, { x: 0.72, y: sy + 0.08, w: 3.95, h: 0.22, fontSize: 9.5, bold: true, color: C.carbonBlack, fontFace: FB, charSpacing: 1, margin: 0 });
    // Body
    s.addText(st.d, { x: 0.72, y: sy + 0.31, w: 3.95, h: 0.28, fontSize: 9, color: C.charcoal, fontFace: FB, margin: 0 });

    // Dashed connection line aligned under the blue accent
    if (i < 3) s.addShape(pres.shapes.LINE, { x: 0.59, y: sy + 0.67, w: 0, h: 0.15, line: { color: C.blue, dashType: "dash", width: 1.5 } });
  });

  // RIGHT: Stage 4 – Glass-Box visual
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 0.85, w: 4.5, h: 4.4, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 0.85, w: 4.5, h: 0.36, fill: { color: C.paprika } });
  s.addText("STAGE 4: GLASS-BOX FORENSIC AUDIT", { x: 5.22, y: 0.85, w: 4.26, h: 0.36, fontSize: 10, bold: true, color: C.white, fontFace: FH, valign: "middle", charSpacing: 1.5, margin: 0 });

  // Glass-box illustration: feature bars flowing into prediction
  s.addText("How the Model Reaches a Decision", { x: 5.2, y: 1.3, w: 4.3, h: 0.28, fontSize: 9, italic: true, color: C.charcoal, fontFace: FB, align: "center", margin: 0 });

  const features = [
    { name: "weather_index", val: +2.1, color: C.paprika },
    { name: "distance_km", val: +1.6, color: C.paprika },
    { name: "traffic_index", val: +1.2, color: C.paprika },
    { name: "supply_risk", val: +0.7, color: C.paprika },
    { name: "base_prod_per_week", val: -0.9, color: C.green },
    { name: "routing_complexity", val: -0.5, color: C.green },
    { name: "priority_encoded", val: -0.3, color: C.green },
  ];

  const barAreaX = 5.18, barBaseX = 7.7, maxBar = 1.2, rowH = 0.42;
  const baseY = 1.68;

  // Center line
  s.addShape(pres.shapes.LINE, { x: barBaseX, y: baseY - 0.05, w: 0, h: features.length * rowH + 0.1, line: { color: C.charcoal, width: 0.8 } });

  features.forEach((f, i) => {
    const ry = baseY + i * rowH;
    const barW = Math.abs(f.val) / 2.5 * maxBar;
    const isPos = f.val > 0;

    // Feature label
    s.addText(f.name, { x: barAreaX, y: ry + 0.1, w: 2.45, h: 0.22, fontSize: 7.5, color: C.charcoal, fontFace: FM, align: "right", valign: "middle", margin: 0 });
    // Bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: isPos ? barBaseX : barBaseX - barW,
      y: ry + 0.1,
      w: barW, h: 0.22,
      fill: { color: f.color }
    });
    // Value label always placed right of center line
    s.addText((f.val > 0 ? "+" : "") + f.val.toFixed(1) + "h", {
      x: barBaseX + 0.04,
      y: ry + 0.1, w: 0.65, h: 0.22,
      fontSize: 7, bold: true, color: f.color, fontFace: FM, valign: "middle", align: "left", margin: 0
    });
  });

  // Legend
  s.addShape(pres.shapes.RECTANGLE, { x: 5.18, y: 4.65, w: 0.2, h: 0.1, fill: { color: C.paprika } });
  s.addText("Delay-increasing", { x: 5.42, y: 4.62, w: 1.5, h: 0.16, fontSize: 7, color: C.charcoal, fontFace: FB, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.0, y: 4.65, w: 0.2, h: 0.1, fill: { color: C.green } });
  s.addText("Delay-reducing", { x: 7.24, y: 4.62, w: 1.5, h: 0.16, fontSize: 7, color: C.charcoal, fontFace: FB, margin: 0 });
}

// ====================================================================
// SLIDE 6 — OPTIMIZATION ENGINE (Stage 5)  [LIGHT DECISION HUB]
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Header
  s.addText('Optimization Engine', { x: 0.5, y: 0.18, w: 7, h: 0.52, fontSize: 28, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText('How Végam turns a prediction into a decision', { x: 0.5, y: 0.68, w: 7, h: 0.26, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0 });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.67, w: 3.1, h: 0.04, fill: { color: C.paprika } });
  s.addText('TEAM CHIRUTHA', { x: 7.5, y: 0.2, w: 2.1, h: 0.26, fontSize: 8, bold: true, color: C.dustGrey, fontFace: FB, charSpacing: 2, align: 'right', margin: 0 });

  // Reward pill banner (light)
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05, w: 9.0, h: 0.5, fill: { color: C.white }, line: { color: C.paprika, width: 1.0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05, w: 0.08, h: 0.5, fill: { color: C.paprika } });
  s.addText('SCORING:', { x: 0.7, y: 1.05, w: 0.9, h: 0.5, fontSize: 8, bold: true, color: C.paprika, fontFace: FB, valign: 'middle', margin: 0 });
  s.addText('+10 On-time   ·   −15 Delayed   ·   +5 High-priority   ·   −2× Excess Delay Hours', {
    x: 1.6, y: 1.05, w: 7.8, h: 0.5, fontSize: 11.5, bold: true, color: C.carbonBlack, fontFace: FM, valign: 'middle', margin: 0
  });

  // Three-step horizontal flow
  const steps = [
    { num: '1', icon: '⚑', label: 'RISK DETECTION', title: 'Flag It', body: 'XGBoost predicts delay hours. Deliveries above threshold are flagged for optimization.', accent: C.blue },
    { num: '2', icon: '⟳', label: 'SIMULATE', title: 'Simulate It', body: 'Digital Twin re-runs the delivery across thousands of date & factory permutations to find the best outcome.', accent: C.paprika },
    { num: '3', icon: '✓', label: 'DISPATCH', title: 'Act On It', body: 'A ranked dispatch queue is generated. Every action is backed by a mathematical reward gain.', accent: C.green },
  ];

  const sW = 2.75, sH = 2.8, sY = 1.75, sGap = 0.38, sStartX = 0.5;

  steps.forEach((st, i) => {
    const x = sStartX + i * (sW + sGap);

    // Card
    s.addShape(pres.shapes.RECTANGLE, { x, y: sY, w: sW, h: sH, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 }, shadow: makeShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: sY, w: sW, h: 0.06, fill: { color: st.accent } });

    // Step number circle
    s.addShape(pres.shapes.OVAL, { x: x + 0.18, y: sY + 0.16, w: 0.44, h: 0.44, fill: { color: st.accent } });
    s.addText(st.num, { x: x + 0.18, y: sY + 0.16, w: 0.44, h: 0.44, fontSize: 14, bold: true, color: C.white, fontFace: FH, align: 'center', valign: 'middle', margin: 0 });

    // Tag
    s.addText(st.label, { x: x + 0.72, y: sY + 0.2, w: sW - 0.85, h: 0.2, fontSize: 7.5, bold: true, color: st.accent, fontFace: FB, charSpacing: 1.5, valign: 'middle', margin: 0 });

    // Title
    s.addText(st.title, { x: x + 0.18, y: sY + 0.7, w: sW - 0.36, h: 0.38, fontSize: 16, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });

    // Divider
    s.addShape(pres.shapes.LINE, { x: x + 0.18, y: sY + 1.12, w: sW - 0.36, h: 0, line: { color: C.dustGrey, width: 0.6 } });

    // Body
    s.addText(st.body, { x: x + 0.18, y: sY + 1.2, w: sW - 0.36, h: sH - 1.3, fontSize: 10, color: C.charcoal, fontFace: FB, valign: 'top', margin: 0 });

    // Arrow between steps
    if (i < 2) {
      s.addShape(pres.shapes.RIGHT_ARROW, {
        x: x + sW + 0.06, y: sY + sH / 2 - 0.14,
        w: sGap - 0.12, h: 0.28,
        fill: { color: C.dustGrey }, line: { color: C.dustGrey }
      });
    }
  });

  // Bottom note
  s.addText('The Digital Twin simulates 1,000s of permutations — temporal rescheduling & spatial factory swaps — to maximise the business reward score.', {
    x: 0.5, y: 4.72, w: 9.0, h: 0.65, fontSize: 9.5, italic: true, color: C.charcoal, fontFace: FB, align: 'center', valign: 'middle', margin: 0
  });
}

// ====================================================================
// SLIDE 7 — WHY REGRESSION?
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Why Regression over Classification?", { x: 0.5, y: 0.2, w: 9, h: 0.55, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Technical justification for predicting continuous delay hours vs. binary delay flag", {
    x: 0.5, y: 0.72, w: 9, h: 0.3, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0
  });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.71, w: 4.8, h: 0.04, fill: { color: C.paprika } });

  // Left column: Classification — what we rejected
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.12, w: 4.4, h: 0.42, fill: { color: C.charcoal } });
  s.addText("CLASSIFICATION  (REJECTED)", { x: 0.5, y: 1.12, w: 4.4, h: 0.42, fontSize: 11, bold: true, color: C.dustGrey, fontFace: FH, align: "center", valign: "middle", margin: 0 });

  const classProblems = [
    { t: "Binary Output Only", d: "Predicts Delayed / On-Time. Cannot distinguish a 1-hour slip from a 24-hour catastrophe." },
    { t: "No Resource Quantification", d: "Dispatchers cannot calculate costs, re-routing budgets, or SLA penalties without exact delay magnitude." },
    { t: "Loses Temporal Granularity", d: "A 2-hour delay and a 12-hour delay both output '1'. Critical business signal is destroyed." },
  ];
  classProblems.forEach((p, i) => {
    card(s, 0.5, 1.65 + i * 1.2, 4.4, 1.05, C.charcoal, p.t, p.d, 9.5);
  });

  // Right column: Regression — what we chose
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 1.12, w: 4.4, h: 0.42, fill: { color: C.paprika } });
  s.addText("REGRESSION  (CHOSEN)", { x: 5.1, y: 1.12, w: 4.4, h: 0.42, fontSize: 11, bold: true, color: C.white, fontFace: FH, align: "center", valign: "middle", margin: 0 });

  const regBenefits = [
    { t: "Exact Delay Hours Predicted", d: "Outputs precise delay magnitude (e.g., 5.8 hrs), enabling cost-per-hour penalty calculations." },
    { t: "Superior Resource Allocation", d: "Dispatch teams can pre-allocate buffer time, reroute capacity, and prioritize by urgency magnitude." },
    { t: "Enables Reward Optimization", d: "Continuous predictions directly power the Digital Twin reward function (−2× excess delay hours)." },
  ];
  regBenefits.forEach((p, i) => {
    card(s, 5.1, 1.65 + i * 1.2, 4.4, 1.05, C.paprika, p.t, p.d, 9.5);
  });

  // Bottom verdict — soft pill style
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 5.05, w: 9.0, h: 0.38, fill: { color: C.white }, line: { color: C.paprika, width: 1.2 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 5.05, w: 0.08, h: 0.38, fill: { color: C.paprika } });
  s.addText("VERDICT", { x: 0.7, y: 5.05, w: 1.0, h: 0.38, fontSize: 8, bold: true, color: C.paprika, fontFace: FB, charSpacing: 2, valign: "middle", margin: 0 });
  s.addText("Regression transforms a binary alert into a precise, actionable, financially quantifiable intelligence signal.", {
    x: 1.65, y: 5.05, w: 7.7, h: 0.38, fontSize: 10, bold: true, italic: true, color: C.carbonBlack, fontFace: FB, valign: "middle", margin: 0
  });
}

// ====================================================================
// SLIDE 8 — USPs  (4 Key Differentiators — Clean 2×2 Grid)
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Header
  s.addText("What Makes Us Stand Out", { x: 0.5, y: 0.18, w: 7.5, h: 0.52, fontSize: 28, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Four capabilities that set Végam apart from standard logistics dashboards", { x: 0.5, y: 0.68, w: 8, h: 0.26, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0 });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.67, w: 2.4, h: 0.04, fill: { color: C.paprika } });

  const usps = [
    {
      num: "01", accent: C.paprika,
      title: "Operational Loss Optimization",
      body: "We optimize MAE over MSE — resisting heavy-tail outlier contamination. Our model speaks operational reality: 'On average, the prediction is accurate within X hours.'",
    },
    {
      num: "02", accent: C.blue,
      title: "Multi-Dimensional Risk Synthesis",
      body: "14 engineered features capture cross-domain compounding risk: weather × traffic × factory variability × routing complexity — effects that simpler models miss entirely.",
    },
    {
      num: "03", accent: C.green,
      title: "TreeSHAP Forensics",
      body: "Game-theoretic Shapley values guarantee mathematically consistent, exact additive feature attribution. The forensic parts always sum to the total prediction. Not an approximation.",
    },
    {
      num: "04", accent: C.purple,
      title: "Digital Twin Optimizer",
      body: "The model becomes a Simulator, not just an inference tool. High-risk deliveries are re-simulated across thousands of temporal and spatial permutations to find the optimal reward.",
    },
  ];

  const uW = 4.35, uH = 1.85, uGap = 0.3, uStartX = 0.5, uStartY = 1.15;

  usps.forEach((u, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = uStartX + col * (uW + uGap);
    const y = uStartY + row * (uH + uGap);

    // Card background
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: uW, h: uH, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.7 }, shadow: makeShadow() });
    // Top accent bar
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: uW, h: 0.06, fill: { color: u.accent } });
    // Left accent bar
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h: uH, fill: { color: u.accent } });

    // Number circle
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fill: { color: u.accent } });
    s.addText(u.num, { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.white, fontFace: FH, align: "center", valign: "middle", margin: 0 });

    // Title
    s.addText(u.title, { x: x + 0.82, y: y + 0.22, w: uW - 1.0, h: 0.44, fontSize: 14, bold: true, color: C.carbonBlack, fontFace: FH, valign: "middle", margin: 0 });

    // Divider
    s.addShape(pres.shapes.LINE, { x: x + 0.2, y: y + 0.78, w: uW - 0.4, h: 0, line: { color: C.dustGrey, width: 0.5 } });

    // Body
    s.addText(u.body, { x: x + 0.2, y: y + 0.88, w: uW - 0.4, h: uH - 1.0, fontSize: 10.5, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });
  });

  // Bottom tagline
  // s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 5.08, w: 9.0, h: 0.36, fill: { color: C.carbonBlack } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 5.08, w: 0.08, h: 0.36, fill: { color: C.paprika } });
  s.addText("Other teams built dashboards. We built an Intelligence Command Center.", {
    x: 0.7, y: 5.08, w: 8.7, h: 0.36, fontSize: 10, bold: true, italic: true, color: C.carbonBlack, fontFace: FB, valign: "middle", margin: 0
  });
}

// ====================================================================
// SLIDE 9 — IMPACT & ROI  (replicating reference image layout)
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  s.addText("Impact & ROI", { x: 0.5, y: 0.18, w: 5, h: 0.5, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Measurable business value from Day 1", {
    x: 0.5, y: 0.66, w: 5, h: 0.28, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0
  });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.65, w: 2.1, h: 0.04, fill: { color: C.paprika } });

  // KPI metric cards (top row - 4 stats)
  const kpis = [
    { val: "+2,598", label: "REWARD GAIN", sub: "Optimized vs baseline" },
    { val: "~30%", label: "DELAY REDUCTION", sub: "Through proactive intervention" },
    { val: "< 1s", label: "DECISION LATENCY", sub: "Precomputed dashboard" },
    { val: "100%", label: "EXPLAINABILITY", sub: "SHAP for every delivery" },
  ];

  kpis.forEach((k, i) => {
    const x = 0.5 + i * 2.4;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.2, h: 1.05, fill: { color: C.carbonBlack } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 0.07, h: 1.05, fill: { color: C.paprika } });
    s.addText(k.val, { x: x + 0.15, y: 1.16, w: 2.0, h: 0.5, fontSize: 30, bold: true, color: C.floralWhite, fontFace: FH, margin: 0 });
    s.addText(k.label, { x: x + 0.15, y: 1.64, w: 2.0, h: 0.2, fontSize: 7.5, bold: true, color: C.paprika, fontFace: FB, charSpacing: 1.5, margin: 0 });
    s.addText(k.sub, { x: x + 0.15, y: 1.84, w: 2.0, h: 0.18, fontSize: 7, italic: true, color: C.dustGrey, fontFace: FB, margin: 0 });
  });

  // Left: Bar chart (before/after reward)
  s.addChart(pres.charts.BAR, [
    { name: "Reward", labels: ["Baseline", "After Végam"], values: [-456, 2598] }
  ], {
    x: 0.5, y: 2.3, w: 5.0, h: 2.6,
    barDir: "col",
    chartColors: [C.charcoal, C.paprika],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.charcoal,
    valAxisLabelColor: C.charcoal,
    valGridLine: { color: "E2E8F0", size: 0.5 },
    catGridLine: { style: "none" },
    showValue: true,
    dataLabelPosition: "outEnd",
    dataLabelColor: C.carbonBlack,
    showLegend: false,
    title: "REWARD: BEFORE vs AFTER OPTIMIZATION",
    titleFontSize: 10,
    titleColor: C.paprika,
    showTitle: true,
  });

  // Right: Business impact list
  sectionTag(s, 5.7, 2.3, "BUSINESS IMPACT", C.paprika);

  const impacts = [
    { icon: "$", color: C.green, t: "Cost Reduction", d: "Proactive rescheduling avoids penalty charges from late project delivery." },
    { icon: "⏱", color: C.blue, t: "Time Saved", d: "Automated forensic reports replace hours of manual analysis per delay incident." },
    { icon: "↗", color: C.paprika, t: "Resource Efficiency", d: "Truck slot optimization maximizes daily dispatch capacity without overstretching." },
    { icon: "✓", color: C.charcoal, t: "Risk Mitigation", d: "High-priority projects are guaranteed slots before lower-priority load." },
  ];

  impacts.forEach((im, i) => {
    const iy = 2.65 + i * 0.6;
    s.addShape(pres.shapes.OVAL, { x: 5.7, y: iy, w: 0.36, h: 0.36, fill: { color: im.color } });
    s.addText(im.icon, { x: 5.7, y: iy, w: 0.36, h: 0.36, fontSize: 13, color: C.white, fontFace: FB, align: "center", valign: "middle", margin: 0 });
    s.addText(im.t, { x: 6.14, y: iy + 0.01, w: 3.3, h: 0.2, fontSize: 10, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });
    s.addText(im.d, { x: 6.14, y: iy + 0.22, w: 3.3, h: 0.24, fontSize: 8.5, color: C.charcoal, fontFace: FB, margin: 0 });
  });
}

// ====================================================================
// SLIDE 10 — FUTURE SCOPE  [LIGHT 2x2 GRID]
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Header
  s.addText('Future Scope', { x: 0.5, y: 0.18, w: 7.5, h: 0.52, fontSize: 32, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("Four high-value expansions on Végam's intelligence platform", { x: 0.5, y: 0.68, w: 7.5, h: 0.26, fontSize: 11, italic: true, color: C.charcoal, fontFace: FB, margin: 0 });
  s.addText('TEAM CHIRUTHA', { x: 7.5, y: 0.2, w: 2.1, h: 0.26, fontSize: 8, bold: true, color: C.dustGrey, fontFace: FB, charSpacing: 2, align: 'right', margin: 0 });
  // Accent underline
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.67, w: 2.0, h: 0.04, fill: { color: C.paprika } });

  const modules = [
    {
      num: '01', accent: C.paprika,
      tag: 'BUSINESS IMPACT',
      title: 'ROI & Financial Translation',
      body: 'Converting delay hour predictions into real dollar-value savings — translating operational metrics into board-level financial language that drives executive buy-in.',
    },
    {
      num: '02', accent: C.green,
      tag: 'SUSTAINABILITY',
      title: 'ESG & Carbon Impact Tracking',
      body: 'Every optimized route and factory swap is mapped to its CO₂ reduction. Végam aligns logistics intelligence with corporate sustainability and ESG reporting goals.',
    },
    {
      num: '03', accent: C.blue,
      tag: 'DATA LAYER',
      title: 'Cross-Modal Data Integration',
      body: 'Incorporating real-time satellite imagery as a high-fidelity weather signal, dramatically improving delay prediction precision beyond ground-level indices.',
    },
    {
      num: '04', accent: C.purple,
      tag: 'INFRASTRUCTURE',
      title: 'Edge Deployment',
      body: 'Compressing the XGBoost inference pipeline for sub-10ms latency on industrial IoT edge nodes — enabling field operations with zero cloud dependency.',
    },
  ];

  const mW = 4.35, mH = 1.98, gap = 0.3, startX = 0.5, startY = 1.1;

  modules.forEach((m, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = startX + col * (mW + gap);
    const y = startY + row * (mH + gap);

    // Card
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: mW, h: mH, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.7 }, shadow: makeShadow() });
    // Left accent bar
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h: mH, fill: { color: m.accent } });
    // Top accent bar
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: mW, h: 0.05, fill: { color: m.accent } });

    // Tag + number row
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.18, y: y + 0.12, w: 1.55, h: 0.2, fill: { color: m.accent } });
    s.addText(m.tag, { x: x + 0.18, y: y + 0.12, w: 1.55, h: 0.2, fontSize: 6.5, bold: true, color: C.white, fontFace: FB, align: 'center', valign: 'middle', charSpacing: 1.5, margin: 0 });
    s.addText(m.num, { x: x + mW - 0.62, y: y + 0.08, w: 0.5, h: 0.3, fontSize: 20, bold: true, color: m.accent, fontFace: FH, align: 'right', valign: 'top', transparency: 40, margin: 0 });

    // Title
    s.addText(m.title, { x: x + 0.18, y: y + 0.4, w: mW - 0.3, h: 0.42, fontSize: 13, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });

    // Divider
    s.addShape(pres.shapes.LINE, { x: x + 0.18, y: y + 0.86, w: mW - 0.3, h: 0, line: { color: C.dustGrey, width: 0.5 } });

    // Body
    s.addText(m.body, { x: x + 0.18, y: y + 0.94, w: mW - 0.3, h: mH - 1.04, fontSize: 9.5, color: C.charcoal, fontFace: FB, valign: 'top', margin: 0 });
  });
}
// ====================================================================
// ====================================================================
// SLIDE 12 — CONCLUSION / THANK YOU
// ====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.floralWhite };

  // Header
  s.addText("We didn't just build a model.", { x: 0.4, y: 0.4, w: 9, h: 0.5, fontSize: 36, bold: true, color: C.carbonBlack, fontFace: FH, margin: 0 });
  s.addText("We built a logistics brain.", { x: 0.4, y: 0.95, w: 9, h: 0.5, fontSize: 36, bold: true, color: C.paprika, fontFace: FH, margin: 0 });

  // Top horizontal rule
  s.addShape(pres.shapes.LINE, { x: 0.4, y: 1.55, w: 9.2, h: 0, line: { color: C.dustGrey, width: 0.5 } });

  // Left Column Text
  const p1 = "Starting from four raw CSV files, we engineered a system that thinks the way a seasoned logistics manager does — reading weather, traffic, factory reliability, and project urgency all at once — and then acts on it.";
  const p2 = "Our XGBoost pipeline doesn't just predict delays. It explains why they happen, which deliveries are at risk, and what to do — rescheduling, re-routing, or re-prioritizing — all scored against a reward framework that speaks the language of business outcomes.";
  s.addText(p1, { x: 0.4, y: 1.7, w: 4.2, h: 0.8, fontSize: 10, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });
  s.addText(p2, { x: 0.4, y: 2.65, w: 4.2, h: 1.0, fontSize: 10, color: C.charcoal, fontFace: FB, valign: "top", margin: 0 });

  // Right Column Bullets
  s.addText("Every decision was deliberate:", { x: 5.0, y: 1.7, w: 4.6, h: 0.3, fontSize: 10, bold: true, color: C.carbonBlack, fontFace: FB, margin: 0 });

  const bList = [
    { b: "Regression over Classification", i: " — to capture severity, not just occurrence" },
    { b: "Time-based splits", i: " — to prevent data leakage" },
    { b: "MAE over RMSE", i: " — to handle real-world outliers" },
    { b: "TreeSHAP", i: " — to make the black box transparent" },
    { b: "Reward engine", i: " — to make predictions actionable" }
  ];

  bList.forEach((item, i) => {
    const by = 2.05 + i * 0.35;
    s.addShape(pres.shapes.OVAL, { x: 5.0, y: by + 0.05, w: 0.08, h: 0.08, fill: { color: C.paprika } });
    s.addText([
      { text: item.b, options: { bold: true, color: C.carbonBlack } },
      { text: item.i, options: { italic: true, color: C.charcoal } }
    ], { x: 5.2, y: by, w: 4.4, h: 0.2, fontSize: 9.5, fontFace: FB, margin: 0, valign: "middle" });
  });

  // Highlight Box (Bottom Center)
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.8, w: 9.2, h: 1.0, fill: { color: C.white }, line: { color: C.dustGrey, width: 0.8 }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.8, w: 0.08, h: 1.0, fill: { color: C.paprika } });
  s.addText("The result is not a submission. It is a deployable decision system — one that turns uncertainty into strategy, and data into competitive advantage.", {
    x: 0.6, y: 3.8, w: 8.8, h: 1.0, fontSize: 13, bold: true, italic: true, color: C.carbonBlack, fontFace: FH, valign: "middle", margin: 0
  });

  // Footer Rule
  s.addShape(pres.shapes.LINE, { x: 0.4, y: 5.0, w: 9.2, h: 0, line: { color: C.dustGrey, width: 0.5 } });

  // Footer text
  s.addText("Built for Smart Procurement. Ready for the real world.", {
    x: 0.4, y: 5.05, w: 5.0, h: 0.25, fontSize: 9.5, italic: true, color: C.charcoal, fontFace: FH, margin: 0
  });

  s.addText("Bindu Darshitha", { x: 0.4, y: 5.35, w: 2.0, h: 0.2, fontSize: 9.5, italic: true, color: C.charcoal, fontFace: FH, margin: 0 });
  s.addText("Abhinav Mucharla", { x: 3.0, y: 5.35, w: 2.0, h: 0.2, fontSize: 9.5, italic: true, color: C.charcoal, fontFace: FH, margin: 0 });
  s.addText("Pranav Raj Galipalli", { x: 5.6, y: 5.35, w: 2.0, h: 0.2, fontSize: 9.5, italic: true, color: C.charcoal, fontFace: FH, margin: 0 });

  s.addText("Predict  ·  Prioritize  ·  Optimize", {
    x: 7.0, y: 5.05, w: 2.6, h: 0.2, fontSize: 9, bold: true, color: C.paprika, fontFace: FB, align: "right", charSpacing: 3, margin: 0
  });
  s.addText("Végam", {
    x: 7.0, y: 5.25, w: 2.6, h: 0.35, fontSize: 26, bold: true, color: C.carbonBlack, fontFace: FH, align: "right", margin: 0
  });
}

// ── Write file ──────────────────────────────────────────────────────
pres.writeFile({ fileName: "Vegam_Pitch_V19.pptx" })
  .then(() => console.log("✓ V19 generated"))
  .catch(e => console.error("Error:", e));
