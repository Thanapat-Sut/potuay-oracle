# /slides — Create Presentations via Gemini Canvas

## Trigger
- `/slides` command
- Keywords: "slides", "presentation", "สไลด์", "พรีเซน", "canvas"

## Usage
```
/slides <topic> [--slides N] [--lang th|en] [--no-gemini] [--style dark|light|neon|nature|bw]
```

**Defaults**: `--slides 8`, `--lang en`

## Workflow

### Step 1: Parse Arguments

Extract from user input:
- `TOPIC`: the presentation subject
- `SLIDE_COUNT`: number of slides (default 8)
- `LANG`: language for content (default "en", use "th" for Thai)
- `USE_GEMINI`: default true. `--no-gemini` falls back to local HTML generation

### Step 2: Check Gemini Proxy

```bash
python3 D:/Claude/.claude/skills/slides/gemini_chat.py --check
```

**Output**: JSON `{"online": true/false, "tabId": N}`

- If `online: true` → proceed to Step 3 (Gemini Canvas)
- If `online: false` or `--no-gemini` → fallback to Step 4 (Local HTML)

### Step 3: Send Canvas Prompt to Gemini (Primary Path)

Send a single prompt to Gemini that instructs it to create a Canvas presentation.
Gemini will automatically open Canvas mode when asked to create structured content.

```bash
python3 D:/Claude/.claude/skills/slides/gemini_chat.py --timeout 90 "PROMPT_TEXT"
```

**Build the PROMPT_TEXT** as follows (adapt language if `--lang th`):

```
Create a presentation in Canvas about "[TOPIC]" with exactly [N] slides.

Please use Canvas to create this as a beautiful, well-structured presentation document.

Requirements:
- Slide 1: Title slide with main title and subtitle
- Mix slide types for variety: bullet points, comparisons, key quotes, section headers
- Each content slide: 3-5 concise bullet points
- Include a section break every 3-4 slides to separate major topics
- End with a summary or key takeaways slide
- Make it professional, engaging, and visually well-organized
- Use clear headings and hierarchy
[If --lang th: "Write all content in Thai (ภาษาไทย)"]

Create this in Canvas now.
```

**IMPORTANT**: The prompt must explicitly ask Gemini to use **Canvas**. This triggers Gemini's built-in Canvas editor which creates an interactive, editable document directly in the browser.

After sending, Claude does NOT need to parse the response. Gemini handles everything — the Canvas will open automatically in the Gemini tab.

If the command fails (exit code != 0) → fall back to Step 4.

### Step 4: Local HTML Fallback (when Gemini is unavailable)

Only used when Gemini is offline or `--no-gemini` is specified.

Generate slide content as Claude and build HTML locally:

1. Create the slide JSON following this schema:

```json
{
  "title": "Presentation Title",
  "author": "",
  "date": "YYYY-MM-DD",
  "theme": "STYLE",
  "slides": [
    {"layout": "title", "title": "Main Title", "subtitle": "Subtitle"},
    {"layout": "content", "title": "Slide Title", "bullets": ["Point 1", "Point 2", "Point 3"], "notes": "Speaker notes"},
    {"layout": "two-col", "title": "Comparison", "left": {"heading": "Left", "bullets": ["Item 1"]}, "right": {"heading": "Right", "bullets": ["Item 1"]}},
    {"layout": "quote", "quote": "Quote text...", "author": "Attribution"},
    {"layout": "section", "title": "Section Break", "subtitle": "Next topic"}
  ]
}
```

Available layouts: `title`, `content`, `two-col`, `quote`, `section`

2. Write JSON and generate HTML:
```bash
cat > /tmp/slides_data.json << 'SLIDES_EOF'
{ ... the JSON ... }
SLIDES_EOF

python3 D:/Claude/.claude/skills/slides/generate_slides.py /tmp/slides_data.json --output /tmp/presentation.html --style STYLE
cp /tmp/presentation.html "D:/Claude/presentation.html"
start "D:/Claude/presentation.html"
```

### Step 5: Report to User

**If Gemini Canvas (Step 3)**:
- Tell user: "Presentation created in Gemini Canvas"
- The Canvas is open and editable in the Gemini browser tab
- User can edit, export, or share directly from Gemini

**If Local HTML (Step 4)**:
- File created at `D:/Claude/presentation.html`
- Number of slides, theme used
- Keyboard shortcuts: Arrow keys, `N` notes, `O` overview, `F` fullscreen

## Gemini Chat Helper Reference

```bash
# Check if Gemini proxy is online
python3 D:/Claude/.claude/skills/slides/gemini_chat.py --check

# Send prompt to Gemini (stdout = response, stderr = status)
python3 D:/Claude/.claude/skills/slides/gemini_chat.py --timeout 90 "Your prompt"

# Use specific tab
python3 D:/Claude/.claude/skills/slides/gemini_chat.py --tab-id 12345 "Your prompt"
```

**Exit codes**: 0=success, 1=offline, 2=timeout, 3=error

## MQTT Architecture

```
Claude (/slides skill)
  ↓ builds Canvas prompt
gemini_chat.py
  ↓ mosquitto_pub/sub (subscribe-before-publish)
Mosquitto Broker (localhost:1883)
  ↓ MQTT WebSocket (:9001)
Chrome Extension (claude-browser-proxy v2.8.8+)
  ↓ chrome.scripting.executeScript
Gemini Tab → Opens Canvas → Creates Presentation
```

## Examples

```
/slides "AI in Healthcare" --slides 12
  → Sends prompt to Gemini → Canvas presentation with 12 slides

/slides "การตลาดดิจิทัล" --slides 8 --lang th
  → Thai Canvas presentation via Gemini

/slides "Quick Update" --slides 5 --no-gemini --style light
  → Skips Gemini, generates local HTML with light theme
```
