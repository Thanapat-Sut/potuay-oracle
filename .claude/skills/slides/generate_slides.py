#!/usr/bin/env python3
"""
generate_slides.py — Self-contained HTML presentation generator.

Usage:
    python generate_slides.py input.json --output presentation.html --style dark
    echo '{"title":"Test","slides":[...]}' | python generate_slides.py --output out.html
"""

import argparse
import json
import sys
import html
from datetime import date

THEMES = {
    "dark": {
        "--bg": "#1a1a2e",
        "--bg-slide": "#16213e",
        "--text": "#e0e0e0",
        "--text-muted": "#8a8a9a",
        "--heading": "#ffffff",
        "--accent": "#0f9ef7",
        "--accent2": "#6c63ff",
        "--bullet": "#0f9ef7",
        "--quote-bg": "#1e2a4a",
        "--quote-border": "#0f9ef7",
        "--notes-bg": "#0d1525",
        "--notes-text": "#9ab0d0",
        "--progress": "#0f9ef7",
        "--overview-bg": "rgba(0,0,0,0.92)",
        "--slide-shadow": "0 8px 32px rgba(0,0,0,0.4)",
        "--gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
    },
    "light": {
        "--bg": "#f5f5f0",
        "--bg-slide": "#ffffff",
        "--text": "#333333",
        "--text-muted": "#777777",
        "--heading": "#1a1a1a",
        "--accent": "#2d8f4e",
        "--accent2": "#1a6b35",
        "--bullet": "#2d8f4e",
        "--quote-bg": "#f0f7f2",
        "--quote-border": "#2d8f4e",
        "--notes-bg": "#e8ede9",
        "--notes-text": "#445544",
        "--progress": "#2d8f4e",
        "--overview-bg": "rgba(245,245,240,0.95)",
        "--slide-shadow": "0 4px 20px rgba(0,0,0,0.1)",
        "--gradient": "linear-gradient(135deg, #f5f5f0 0%, #ffffff 100%)",
    },
    "neon": {
        "--bg": "#0a0a0a",
        "--bg-slide": "#111111",
        "--text": "#e0e0e0",
        "--text-muted": "#888888",
        "--heading": "#ffffff",
        "--accent": "#ff006e",
        "--accent2": "#00f5d4",
        "--bullet": "#00f5d4",
        "--quote-bg": "#1a1a1a",
        "--quote-border": "#ff006e",
        "--notes-bg": "#0a0a0a",
        "--notes-text": "#00f5d4",
        "--progress": "linear-gradient(90deg, #ff006e, #8338ec, #00f5d4)",
        "--overview-bg": "rgba(0,0,0,0.95)",
        "--slide-shadow": "0 0 30px rgba(255,0,110,0.2), 0 0 60px rgba(0,245,212,0.1)",
        "--gradient": "linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 50%, #0a1a1a 100%)",
    },
    "nature": {
        "--bg": "#f4efe4",
        "--bg-slide": "#faf7f0",
        "--text": "#3d3229",
        "--text-muted": "#8a7b6b",
        "--heading": "#2c1e0f",
        "--accent": "#b85c38",
        "--accent2": "#5c8a4e",
        "--bullet": "#b85c38",
        "--quote-bg": "#ede7d9",
        "--quote-border": "#b85c38",
        "--notes-bg": "#e6dfd1",
        "--notes-text": "#5c4a3a",
        "--progress": "linear-gradient(90deg, #b85c38, #5c8a4e)",
        "--overview-bg": "rgba(244,239,228,0.95)",
        "--slide-shadow": "0 4px 20px rgba(60,40,20,0.12)",
        "--gradient": "linear-gradient(135deg, #f4efe4 0%, #faf7f0 100%)",
    },
    "bw": {
        "--bg": "#ffffff",
        "--bg-slide": "#ffffff",
        "--text": "#1a1a1a",
        "--text-muted": "#666666",
        "--heading": "#000000",
        "--accent": "#000000",
        "--accent2": "#333333",
        "--bullet": "#000000",
        "--quote-bg": "#f5f5f5",
        "--quote-border": "#000000",
        "--notes-bg": "#f0f0f0",
        "--notes-text": "#333333",
        "--progress": "#000000",
        "--overview-bg": "rgba(255,255,255,0.96)",
        "--slide-shadow": "0 2px 16px rgba(0,0,0,0.12)",
        "--gradient": "linear-gradient(135deg, #ffffff 0%, #fafafa 100%)",
    },
}


def e(text):
    """HTML-escape text."""
    return html.escape(str(text)) if text else ""


def render_slide(slide, index, total):
    """Render a single slide to HTML."""
    layout = slide.get("layout", "content")
    notes = slide.get("notes", "")

    if layout == "title":
        inner = f"""
            <div class="slide-center">
                <h1 class="title-main">{e(slide.get('title', ''))}</h1>
                <p class="title-subtitle">{e(slide.get('subtitle', ''))}</p>
            </div>"""
    elif layout == "section":
        inner = f"""
            <div class="slide-center">
                <div class="section-marker">&#9670;</div>
                <h1 class="section-title">{e(slide.get('title', ''))}</h1>
                <p class="section-subtitle">{e(slide.get('subtitle', ''))}</p>
            </div>"""
    elif layout == "quote":
        inner = f"""
            <div class="slide-center">
                <blockquote class="slide-quote">
                    <p>&ldquo;{e(slide.get('quote', ''))}&rdquo;</p>
                    <cite>&mdash; {e(slide.get('author', ''))}</cite>
                </blockquote>
            </div>"""
    elif layout == "two-col":
        left = slide.get("left", {})
        right = slide.get("right", {})
        left_bullets = "".join(f"<li>{e(b)}</li>" for b in left.get("bullets", []))
        right_bullets = "".join(f"<li>{e(b)}</li>" for b in right.get("bullets", []))
        inner = f"""
            <h2 class="slide-heading">{e(slide.get('title', ''))}</h2>
            <div class="two-col">
                <div class="col">
                    <h3 class="col-heading">{e(left.get('heading', ''))}</h3>
                    <ul>{left_bullets}</ul>
                </div>
                <div class="col">
                    <h3 class="col-heading">{e(right.get('heading', ''))}</h3>
                    <ul>{right_bullets}</ul>
                </div>
            </div>"""
    else:  # content (default)
        bullets = "".join(f"<li>{e(b)}</li>" for b in slide.get("bullets", []))
        inner = f"""
            <h2 class="slide-heading">{e(slide.get('title', ''))}</h2>
            <ul class="slide-bullets">{bullets}</ul>"""

    notes_html = f'<div class="speaker-notes">{e(notes)}</div>' if notes else ""

    return f"""
    <section class="slide" data-index="{index}" id="slide-{index}">
        <div class="slide-content">{inner}</div>
        {notes_html}
        <div class="slide-number">{index + 1} / {total}</div>
    </section>"""


def build_theme_css(theme_name):
    """Build CSS custom properties from theme dict."""
    t = THEMES.get(theme_name, THEMES["dark"])
    props = "\n        ".join(f"{k}: {v};" for k, v in t.items())
    return f":root {{\n        {props}\n    }}"


def generate_html(data, theme_name="dark"):
    """Generate the complete HTML presentation."""
    title = e(data.get("title", "Presentation"))
    author = e(data.get("author", ""))
    slides = data.get("slides", [])
    total = len(slides)

    slides_html = "\n".join(render_slide(s, i, total) for i, s in enumerate(slides))
    theme_css = build_theme_css(theme_name)

    # Neon theme needs extra glow styles
    neon_extra = ""
    if theme_name == "neon":
        neon_extra = """
        .title-main { text-shadow: 0 0 20px rgba(255,0,110,0.5), 0 0 40px rgba(255,0,110,0.2); }
        .section-title { text-shadow: 0 0 20px rgba(0,245,212,0.5); }
        .slide-heading { text-shadow: 0 0 10px rgba(131,56,236,0.4); }
        .section-marker { color: var(--accent); text-shadow: 0 0 20px var(--accent); }
        .slide-quote { border-left-color: var(--accent); box-shadow: 0 0 20px rgba(255,0,110,0.15); }
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Sarabun:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
    {theme_css}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    html, body {{
        height: 100%;
        overflow: hidden;
        font-family: 'Inter', 'Sarabun', 'Noto Sans Thai', system-ui, sans-serif;
        background: var(--bg);
        color: var(--text);
    }}

    /* ===== PROGRESS BAR ===== */
    #progress {{
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: var(--progress);
        z-index: 1000;
        transition: width 0.3s ease;
    }}

    /* ===== SLIDES CONTAINER ===== */
    #deck {{
        width: 100vw;
        height: 100vh;
        position: relative;
    }}

    .slide {{
        position: absolute;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--gradient);
        opacity: 0;
        transform: translateX(60px);
        transition: opacity 0.4s ease, transform 0.4s ease;
        pointer-events: none;
        padding: 60px 80px;
    }}

    .slide.active {{
        opacity: 1;
        transform: translateX(0);
        pointer-events: auto;
    }}

    .slide.prev {{
        opacity: 0;
        transform: translateX(-60px);
    }}

    @media (prefers-reduced-motion: reduce) {{
        .slide {{ transition: opacity 0.15s ease; transform: none !important; }}
        .slide.prev {{ transform: none !important; }}
    }}

    /* ===== SLIDE CONTENT ===== */
    .slide-content {{
        max-width: 1100px;
        width: 100%;
    }}

    .slide-center {{
        text-align: center;
    }}

    /* Title slide */
    .title-main {{
        font-size: clamp(2.2rem, 5vw, 4rem);
        font-weight: 800;
        color: var(--heading);
        margin-bottom: 0.4em;
        line-height: 1.15;
    }}

    .title-subtitle {{
        font-size: clamp(1rem, 2.2vw, 1.6rem);
        font-weight: 300;
        color: var(--text-muted);
    }}

    /* Section break */
    .section-marker {{
        font-size: 2rem;
        color: var(--accent);
        margin-bottom: 0.5em;
    }}

    .section-title {{
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 700;
        color: var(--heading);
        margin-bottom: 0.3em;
    }}

    .section-subtitle {{
        font-size: clamp(1rem, 2vw, 1.4rem);
        color: var(--text-muted);
        font-weight: 300;
    }}

    /* Content slide */
    .slide-heading {{
        font-size: clamp(1.6rem, 3.5vw, 2.4rem);
        font-weight: 700;
        color: var(--heading);
        margin-bottom: 0.8em;
        padding-bottom: 0.3em;
        border-bottom: 2px solid var(--accent);
        display: inline-block;
    }}

    .slide-bullets {{
        list-style: none;
        padding: 0;
    }}

    .slide-bullets li {{
        font-size: clamp(1rem, 2vw, 1.35rem);
        line-height: 1.6;
        padding: 0.35em 0 0.35em 1.6em;
        position: relative;
        color: var(--text);
    }}

    .slide-bullets li::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0.75em;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--bullet);
    }}

    /* Quote */
    .slide-quote {{
        background: var(--quote-bg);
        border-left: 4px solid var(--quote-border);
        padding: 2em 2.5em;
        border-radius: 0 12px 12px 0;
        max-width: 800px;
        margin: 0 auto;
    }}

    .slide-quote p {{
        font-size: clamp(1.2rem, 2.5vw, 1.8rem);
        font-style: italic;
        line-height: 1.5;
        color: var(--text);
        margin-bottom: 0.8em;
    }}

    .slide-quote cite {{
        font-size: 1.1rem;
        color: var(--text-muted);
        font-style: normal;
        font-weight: 600;
    }}

    /* Two columns */
    .two-col {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3em;
        margin-top: 0.5em;
    }}

    .col-heading {{
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 0.6em;
    }}

    .col ul {{
        list-style: none;
        padding: 0;
    }}

    .col li {{
        font-size: clamp(0.95rem, 1.8vw, 1.2rem);
        line-height: 1.6;
        padding: 0.3em 0 0.3em 1.4em;
        position: relative;
    }}

    .col li::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0.7em;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--bullet);
    }}

    /* ===== SLIDE NUMBER ===== */
    .slide-number {{
        position: absolute;
        bottom: 24px;
        right: 32px;
        font-size: 0.85rem;
        color: var(--text-muted);
        font-variant-numeric: tabular-nums;
    }}

    /* ===== SPEAKER NOTES ===== */
    .speaker-notes {{
        display: none;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--notes-bg);
        color: var(--notes-text);
        padding: 16px 32px;
        font-size: 0.9rem;
        line-height: 1.5;
        border-top: 1px solid var(--accent);
        max-height: 25vh;
        overflow-y: auto;
    }}

    body.show-notes .speaker-notes {{
        display: block;
    }}

    /* ===== OVERVIEW MODE ===== */
    #overview {{
        display: none;
        position: fixed;
        inset: 0;
        background: var(--overview-bg);
        z-index: 900;
        padding: 40px;
        overflow-y: auto;
    }}

    #overview.active {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        align-content: start;
    }}

    .overview-thumb {{
        aspect-ratio: 16/9;
        background: var(--bg-slide);
        border-radius: 8px;
        box-shadow: var(--slide-shadow);
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 2px solid transparent;
    }}

    .overview-thumb:hover {{
        transform: scale(1.04);
        border-color: var(--accent);
    }}

    .overview-thumb.current {{
        border-color: var(--accent);
    }}

    .overview-thumb h3 {{
        font-size: 0.95rem;
        color: var(--heading);
        margin-bottom: 4px;
    }}

    .overview-thumb span {{
        font-size: 0.75rem;
        color: var(--text-muted);
    }}

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {{
        .slide {{ padding: 30px 28px; }}
        .two-col {{ grid-template-columns: 1fr; gap: 1.5em; }}
        .slide-number {{ bottom: 12px; right: 16px; }}
    }}

    /* ===== PRINT ===== */
    @media print {{
        html, body {{ overflow: visible; height: auto; }}
        #progress, .slide-number, #overview {{ display: none !important; }}
        .slide {{
            position: relative !important;
            opacity: 1 !important;
            transform: none !important;
            pointer-events: auto !important;
            page-break-after: always;
            page-break-inside: avoid;
            height: 100vh;
            break-after: page;
        }}
        .speaker-notes {{ display: block; position: relative; border-top: 1px solid #ccc; }}
    }}

    {neon_extra}
</style>
</head>
<body>

<div id="progress"></div>

<div id="deck">
{slides_html}
</div>

<div id="overview"></div>

<script>
(function() {{
    const slides = document.querySelectorAll('.slide');
    const total = slides.length;
    const progress = document.getElementById('progress');
    const overview = document.getElementById('overview');
    let current = 0;
    let overviewOpen = false;

    function updateProgress() {{
        const pct = total > 1 ? (current / (total - 1)) * 100 : 100;
        progress.style.width = pct + '%';
    }}

    function goTo(n) {{
        if (n < 0 || n >= total) return;
        slides[current].classList.remove('active');
        slides[current].classList.remove('prev');
        if (n > current) slides[current].classList.add('prev');
        current = n;
        slides[current].classList.add('active');
        slides[current].classList.remove('prev');
        updateProgress();
        updateOverviewHighlight();
        history.replaceState(null, '', '#' + (current + 1));
    }}

    function next() {{ goTo(current + 1); }}
    function prev() {{ goTo(current - 1); }}

    // Keyboard
    document.addEventListener('keydown', function(ev) {{
        if (overviewOpen && ev.key === 'Escape') {{ toggleOverview(); return; }}
        if (overviewOpen) return;

        switch(ev.key) {{
            case 'ArrowRight': case ' ': case 'Enter': ev.preventDefault(); next(); break;
            case 'ArrowLeft': case 'Backspace': ev.preventDefault(); prev(); break;
            case 'Home': ev.preventDefault(); goTo(0); break;
            case 'End': ev.preventDefault(); goTo(total - 1); break;
            case 'n': case 'N': document.body.classList.toggle('show-notes'); break;
            case 'o': case 'O': toggleOverview(); break;
            case 'f': case 'F':
                if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(()=>{{}});
                else document.exitFullscreen();
                break;
            case 'Escape':
                if (document.fullscreenElement) document.exitFullscreen();
                break;
        }}
    }});

    // Touch / swipe
    let touchX = 0;
    document.addEventListener('touchstart', function(ev) {{ touchX = ev.touches[0].clientX; }});
    document.addEventListener('touchend', function(ev) {{
        const dx = ev.changedTouches[0].clientX - touchX;
        if (Math.abs(dx) > 50) {{ dx < 0 ? next() : prev(); }}
    }});

    // Click sides
    document.addEventListener('click', function(ev) {{
        if (overviewOpen) return;
        const x = ev.clientX / window.innerWidth;
        if (x > 0.75) next();
        else if (x < 0.25) prev();
    }});

    // Overview mode
    function buildOverview() {{
        overview.innerHTML = '';
        slides.forEach(function(s, i) {{
            const thumb = document.createElement('div');
            thumb.className = 'overview-thumb' + (i === current ? ' current' : '');
            const heading = s.querySelector('h1, h2, .slide-heading, .title-main, .section-title');
            const hText = heading ? heading.textContent : 'Slide ' + (i + 1);
            thumb.innerHTML = '<h3>' + hText + '</h3><span>Slide ' + (i + 1) + ' / ' + total + '</span>';
            thumb.onclick = function(ev) {{ ev.stopPropagation(); goTo(i); toggleOverview(); }};
            overview.appendChild(thumb);
        }});
    }}

    function updateOverviewHighlight() {{
        const thumbs = overview.querySelectorAll('.overview-thumb');
        thumbs.forEach(function(t, i) {{ t.classList.toggle('current', i === current); }});
    }}

    function toggleOverview() {{
        overviewOpen = !overviewOpen;
        if (overviewOpen) buildOverview();
        overview.classList.toggle('active', overviewOpen);
    }}

    // Hash navigation
    function readHash() {{
        const h = parseInt(location.hash.replace('#', ''), 10);
        if (h >= 1 && h <= total) goTo(h - 1);
        else goTo(0);
    }}

    window.addEventListener('hashchange', readHash);
    readHash();
}})();
</script>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate HTML presentation from JSON")
    parser.add_argument("input", nargs="?", help="JSON input file (reads stdin if omitted)")
    parser.add_argument("--output", "-o", default="presentation.html", help="Output HTML file")
    parser.add_argument("--style", "-s", default=None, choices=THEMES.keys(), help="Theme")
    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    # Theme: CLI flag > JSON field > default
    theme = args.style or data.get("theme", "dark")
    if theme not in THEMES:
        theme = "dark"

    html_output = generate_html(data, theme)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Generated {len(data.get('slides', []))} slides -> {args.output} (theme: {theme})")


if __name__ == "__main__":
    main()
