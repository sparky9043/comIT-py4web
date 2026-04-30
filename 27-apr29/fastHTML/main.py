from fasthtml.common import *
import random, time

# ── CDN headers ───────────────────────────────────────────────────────────────
daisyui_css  = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.10.1/dist/full.min.css")
tailwind_js  = Script(src="https://cdn.tailwindcss.com")
google_fonts = Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap")

custom_css = Style("""
    :root { --font-mono: 'Space Mono', monospace; --font-sans: 'DM Sans', sans-serif; }
    body  { font-family: var(--font-sans); }
    .htmx-indicator               { opacity: 0; transition: opacity 200ms ease; }
    .htmx-request .htmx-indicator { opacity: 1; }
    .htmx-request.htmx-indicator  { opacity: 1; }
    .feature-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .feature-card:hover { transform: translateY(-2px); }
    .badge-htmx { background: linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; }
    @keyframes fadeIn {
        from { opacity:0; transform:translateY(8px); }
        to   { opacity:1; transform:translateY(0); }
    }
    .fade-in { animation: fadeIn 0.35s ease forwards; }
    .progress-bar { transition: width 0.3s ease; }
""")

hdrs = (daisyui_css, tailwind_js, google_fonts, custom_css)
app, rt = fast_app(hdrs=hdrs, live=False)

# ── Helpers ───────────────────────────────────────────────────────────────────

def section_header(emoji, title, subtitle, color="primary"):
    return Div(
        Span(emoji, cls="text-3xl"),
        H2(title, cls=f"text-2xl font-bold text-{color} font-mono mt-1"),
        P(subtitle, cls="text-base-content/60 text-sm mt-1"),
        cls="mb-5"
    )

def attr_badge(attr, desc):
    return Div(
        Span(attr, cls="font-mono text-xs badge badge-htmx"),
        Span(desc, cls="text-xs text-base-content/70 ml-2"),
        cls="flex items-center gap-1 mb-1"
    )

def result_box(placeholder, box_id):
    return Div(
        P(placeholder, cls="text-base-content/40 italic text-sm"),
        id=box_id,
        cls="mt-3 min-h-10 p-2 rounded-lg bg-base-200"
    )

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES — every handler must have a UNIQUE function name.
# FastHTML determines the HTTP method from the function name (get/post/put/delete).
# When two functions share a name Python silently overwrites the first one.
# ═══════════════════════════════════════════════════════════════════════════════

# ── 1. hx-get ─────────────────────────────────────────────────────────────────
@rt("/demo/click")
def get():
    msgs = [
        "HTMX fetched this via GET — no page reload! 🎉",
        "Still no reload. HTMX is smooth 😎",
        "Pure hypermedia in action! 🚀",
        "You really like clicking. Respect. 🖱️",
    ]
    return Div(
        P(random.choice(msgs), cls="font-semibold text-primary"),
        P(f"Server time: {time.strftime('%H:%M:%S')}", cls="text-xs text-base-content/50 font-mono mt-1"),
        cls="fade-in"
    )

# ── 1b. hx-post ───────────────────────────────────────────────────────────────
@rt("/demo/click")
def post(name: str = "stranger"):
    return Div(
        P(f"Hello, {name}! Submitted via hx-post 📬", cls="font-semibold text-secondary"),
        P(f"Received at: {time.strftime('%H:%M:%S')}", cls="text-xs text-base-content/50 font-mono mt-1"),
        cls="fade-in"
    )

# ── 2a. hx-trigger: mouseover ─────────────────────────────────────────────────
@rt("/demo/trigger/hover")
def trigger_hover():
    return Span("👀 mouseover triggered this request!", cls="text-accent font-semibold fade-in")

# ── 2b. hx-trigger: click delay ───────────────────────────────────────────────
@rt("/demo/trigger/delay")
def trigger_delay():
    return Span("⏱️ Fired after 1 second delay!", cls="text-warning font-semibold fade-in")

# ── 2c. hx-trigger: keyup ─────────────────────────────────────────────────────
@rt("/demo/trigger/keyup")
def trigger_keyup(q: str = ""):
    if not q:
        return Span("Start typing…", cls="text-base-content/40 italic text-sm")
    return Div(
        Span(f'"{q}"', cls="badge badge-outline font-mono"),
        Span(f"{len(q)} chars", cls="text-xs text-base-content/50 ml-1"),
        cls="fade-in flex items-center gap-2"
    )

# ── 3. hx-swap modes ──────────────────────────────────────────────────────────
@rt("/demo/swap/{mode}")
def swap_mode(mode: str):
    labels = {
        "innerHTML":   ("🔄", "text-primary",  "Inner content replaced, outer div stays."),
        "outerHTML":   ("💥", "text-secondary", "The entire element was replaced."),
        "prepend":     ("↑",  "text-warning",   "Added to the TOP of the target."),
        "append":      ("↓",  "text-success",   "Added to the BOTTOM of the target."),
        "beforebegin": ("⬆️", "text-accent",    "Inserted BEFORE the target element."),
        "afterend":    ("⬇️", "text-info",      "Inserted AFTER the target element."),
    }
    icon, color, desc = labels.get(mode, ("?", "", "Unknown mode"))
    return Div(
        Span(f'{icon} hx-swap="{mode}"', cls=f"font-mono font-bold {color}"),
        P(desc, cls="text-xs text-base-content/60 mt-1"),
        cls="fade-in"
    )

# ── 4. hx-indicator: slow GET ─────────────────────────────────────────────────
@rt("/demo/slow")
def slow_response():
    time.sleep(1.5)
    return Div(
        P("✅ Response arrived after 1.5 s", cls="text-success font-semibold"),
        P("The spinner showed while waiting.", cls="text-xs opacity-60 mt-1"),
        cls="fade-in"
    )

# ── 5a. hx-confirm + hx-delete: list ─────────────────────────────────────────
items_store = ["Item Alpha", "Item Beta", "Item Gamma", "Item Delta"]

@rt("/demo/list")
def list_items():
    if not items_store:
        return P("All items deleted! Restart the server to reset.", cls="text-error text-sm italic fade-in")
    return Ul(
        *[Li(
            Div(
                Span(f"• {item}", cls="flex-1 text-sm"),
                Button("✕",
                    cls="btn btn-xs btn-ghost text-error",
                    hx_delete=f"/demo/list/{i}",
                    hx_confirm=f"Delete '{item}'?",
                    hx_target="closest li",
                    hx_swap="outerHTML"),
                cls="flex items-center gap-2 py-1"
            ),
            cls="border-b border-base-200"
        ) for i, item in enumerate(items_store)],
        cls="w-full"
    )

# ── 5b. hx-delete handler ─────────────────────────────────────────────────────
@rt("/demo/list/{idx}")
def delete(idx: int):
    if 0 <= idx < len(items_store):
        items_store.pop(idx)
    return ""   # empty → element removed from DOM

# ── 6a. hx-push-url demo: page A ─────────────────────────────────────────────
@rt("/demo/page-a")
def page_a():
    return Div(
        P("📄 Page A loaded as a fragment", cls="font-semibold text-primary"),
        P("URL updated via hx-push-url — no full reload.", cls="text-sm opacity-70 mt-1"),
        Button("→ Load Page B",
            cls="btn btn-sm btn-secondary mt-3",
            hx_get="/demo/page-b",
            hx_target="#boost-result",
            hx_swap="innerHTML",
            hx_push_url="/demo/page-b"),
        cls="fade-in"
    )

# ── 6b. hx-push-url demo: page B ─────────────────────────────────────────────
@rt("/demo/page-b")
def page_b():
    return Div(
        P("📄 Page B — navigated from Page A", cls="font-semibold text-secondary"),
        P("Each click swaps only the result box — zero full reloads.", cls="text-sm opacity-70 mt-1"),
        Button("← Back to Page A",
            cls="btn btn-sm btn-primary mt-3",
            hx_get="/demo/page-a",
            hx_target="#boost-result",
            hx_swap="innerHTML",
            hx_push_url="/demo/page-a"),
        cls="fade-in"
    )

# ── 7. hx-vals & hx-include ──────────────────────────────────────────────────
@rt("/demo/vals")
def vals_demo(color: str = "none", size: str = "none", extra: str = ""):
    children = [
        Div(style=f"background:{color};border:2px solid #6366f1", cls="w-16 h-16 rounded-xl mb-2"),
        P(f"color={color}  size={size}", cls="font-mono text-xs text-primary"),
    ]
    if extra:
        children.append(P(f'extra (hx-include) = "{extra}"', cls="font-mono text-xs text-secondary mt-1"))
    return Div(*children, cls="fade-in flex flex-col items-center")

# ── 8a. Progress: start (POST) ────────────────────────────────────────────────
progress_state = {"value": 0, "running": False}

def progress_widget(value, done=False):
    """Returns a self-polling progress bar div."""
    bar_color = "bg-success" if done else "bg-primary"
    label     = "✅ Complete!" if done else f"{value}%"
    label_cls = "text-xs text-center mt-1 font-mono" + (" text-success" if done else "")
    # Build kwargs: only add polling attrs when not done
    kw = dict(id="progress-container")
    if not done:
        kw["hx_get"]     = "/demo/progress/poll"
        kw["hx_trigger"] = "load delay:300ms"
        kw["hx_swap"]    = "outerHTML"
        kw["hx_target"]  = "#progress-container"
    return Div(
        Div(
            Div(cls=f"progress-bar {bar_color} h-4 rounded-full", style=f"width:{value}%"),
            cls="w-full bg-base-200 rounded-full h-4"
        ),
        P(label, cls=label_cls),
        **kw
    )

@rt("/demo/progress/start")
def progress_start():
    progress_state["value"]   = 0
    progress_state["running"] = True
    return progress_widget(0)

# ── 8b. Progress: poll (GET) ──────────────────────────────────────────────────
@rt("/demo/progress/poll")
def progress_poll():
    if progress_state["running"]:
        progress_state["value"] = min(progress_state["value"] + random.randint(8, 22), 100)
        v    = progress_state["value"]
        done = v >= 100
        if done: progress_state["running"] = False
        return progress_widget(v, done=done)
    return Div(P("Press Start to begin", cls="text-xs text-base-content/40 text-center"), id="progress-container")

# ── 9. Out-of-Band swaps ──────────────────────────────────────────────────────
oob_counter = {"n": 0}

@rt("/demo/oob")
def oob_swap():
    oob_counter["n"] += 1
    n = oob_counter["n"]
    # Return a tuple: FastHTML sends both; htmx routes each by hx_swap_oob
    return (
        Div(
            P(f"Main content updated — click #{n}", cls="text-primary font-semibold"),
            P("Swapped via primary hx-target.", cls="text-xs opacity-60 mt-1"),
            cls="fade-in"
        ),
        Div(
            Span(f"OOB Counter: {n}", cls="badge badge-secondary font-mono"),
            id="oob-counter-display",
            hx_swap_oob="true"
        )
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE
# FastHTML auto-builds the full HTML document; just return body content.
# HEAD tags (Link, Script, Style) in hdrs are injected automatically via fast_app.
# ═══════════════════════════════════════════════════════════════════════════════
@rt("/")
def index():
    return (
        # ── Navbar ────────────────────────────────────────────────────────────
        Div(
            A(Span("⚡"), Span("HTMX Explorer", cls="font-mono font-bold text-lg ml-1"),
              href="/", cls="btn btn-ghost px-2 text-xl"),
            Div(
                Span("FastHTML", cls="badge badge-outline badge-sm"),
                Span("DaisyUI",  cls="badge badge-outline badge-sm"),
                Span("Tailwind", cls="badge badge-outline badge-sm"),
                cls="hidden md:flex gap-2"
            ),
            cls="navbar bg-base-100 border-b border-base-200 sticky top-0 z-40 px-4 flex justify-between"
        ),

        # ── Hero ──────────────────────────────────────────────────────────────
        Div(
            H1("HTMX Feature Explorer", cls="text-3xl md:text-5xl font-bold font-mono mb-3"),
            P("Every major HTMX attribute, live and interactive — built with FastHTML + DaisyUI",
              cls="text-base-content/60 text-lg max-w-xl"),
            Div(
                *[Span(t, cls=f"badge badge-{c} badge-sm font-mono")
                  for t, c in [("hx-get","primary"),("hx-post","secondary"),("hx-trigger","accent"),
                                ("hx-swap","warning"),("hx-target","info"),("hx-vals","success"),
                                ("hx-indicator","error"),("hx-swap-oob","ghost")]],
                cls="flex flex-wrap gap-2 mt-4"
            ),
            cls="py-14 px-6 max-w-3xl mx-auto"
        ),

        # ── Feature grid ──────────────────────────────────────────────────────
        Div(

            # 1. hx-get & hx-post
            Div(
                section_header("🔁", "hx-get & hx-post", "Issue GET or POST requests from any element"),
                Div(
                    # GET column
                    Div(
                        P("GET", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Button("Fetch from server",
                            cls="btn btn-primary btn-sm",
                            hx_get="/demo/click",
                            hx_target="#get-result",
                            hx_swap="innerHTML"),
                        result_box("Click the button →", "get-result"),
                        cls="flex-1"
                    ),
                    Div(cls="divider divider-horizontal hidden md:flex"),
                    # POST column
                    Div(
                        P("POST", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Div(
                            Input(name="name", id="post-name", placeholder="Your name",
                                  cls="input input-bordered input-sm flex-1"),
                            Button("Submit",
                                cls="btn btn-secondary btn-sm",
                                hx_post="/demo/click",
                                hx_include="#post-name",
                                hx_target="#post-result",
                                hx_swap="innerHTML"),
                            cls="flex gap-2"
                        ),
                        result_box("Submit the form →", "post-result"),
                        cls="flex-1"
                    ),
                    cls="flex flex-col md:flex-row gap-4"
                ),
                Div(
                    attr_badge("hx-get",  "URL to issue a GET request"),
                    attr_badge("hx-post", "URL to issue a POST request"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 2. hx-trigger
            Div(
                section_header("⚡", "hx-trigger", "Control when requests fire — events, delays, filters", "accent"),
                Div(
                    # mouseover
                    Div(
                        P("mouseover", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Div("Hover over me",
                            cls="p-4 rounded-xl bg-accent/10 border border-accent/20 text-center cursor-pointer text-sm font-mono",
                            hx_get="/demo/trigger/hover",
                            hx_trigger="mouseover",
                            hx_target="#hover-result",
                            hx_swap="innerHTML"),
                        Div(id="hover-result", cls="mt-2 min-h-6 text-sm"),
                        cls="flex-1"
                    ),
                    # keyup debounce
                    Div(
                        P("keyup delay:500ms changed", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Input(name="q", placeholder="Type to search…",
                              cls="input input-bordered input-sm w-full",
                              hx_get="/demo/trigger/keyup",
                              hx_trigger="keyup delay:500ms changed",
                              hx_target="#keyup-result",
                              hx_swap="innerHTML"),
                        Div(id="keyup-result", cls="mt-2 min-h-6"),
                        cls="flex-1"
                    ),
                    # click delay
                    Div(
                        P("click delay:1s", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Button("Click (fires after 1 s)",
                            cls="btn btn-warning btn-sm w-full",
                            hx_get="/demo/trigger/delay",
                            hx_trigger="click delay:1s",
                            hx_target="#delay-result",
                            hx_swap="innerHTML"),
                        Div(id="delay-result", cls="mt-2 min-h-6 text-sm"),
                        cls="flex-1"
                    ),
                    cls="flex flex-col md:flex-row gap-4"
                ),
                Div(
                    attr_badge("hx-trigger", "DOM event that fires the request"),
                    attr_badge("delay:Xs",   "Debounce — wait X s before firing"),
                    attr_badge("changed",    "Only fire if the element value changed"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 3. hx-swap
            Div(
                section_header("🔀", "hx-swap & hx-target", "Choose exactly where and how content lands", "info"),
                Div(
                    *[Button(mode,
                        cls="btn btn-outline btn-xs font-mono",
                        hx_get=f"/demo/swap/{mode}",
                        hx_target="#swap-demo-area",
                        hx_swap="innerHTML")
                      for mode in ["innerHTML","outerHTML","prepend","append","beforebegin","afterend"]],
                    cls="flex flex-wrap gap-2 mb-3"
                ),
                Div(
                    P("← Pick a swap mode above", cls="text-base-content/40 text-sm italic"),
                    id="swap-demo-area",
                    cls="min-h-14 p-3 rounded-lg bg-base-200 text-sm"
                ),
                Div(
                    attr_badge("hx-target", "CSS selector of the element to update"),
                    attr_badge("hx-swap",   "innerHTML | outerHTML | prepend | append | beforebegin | afterend"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 4. hx-indicator
            Div(
                section_header("⏳", "hx-indicator", "Show a spinner during slow requests", "warning"),
                P("The button is disabled and a spinner appears while the 1.5 s request is in flight.",
                  cls="text-sm text-base-content/60 mb-4"),
                Button(
                    Span("Load slow response (1.5 s)"),
                    Span(cls="loading loading-spinner loading-sm htmx-indicator ml-2"),
                    cls="btn btn-warning gap-2",
                    id="slow-btn",
                    hx_get="/demo/slow",
                    hx_target="#slow-result",
                    hx_swap="innerHTML",
                    hx_indicator="#slow-btn",
                    hx_disabled_elt="this",
                ),
                result_box("← Trigger the slow request", "slow-result"),
                Div(
                    attr_badge("hx-indicator",    "Element that receives .htmx-request class"),
                    attr_badge("hx-disabled-elt", "Disable this element while in flight"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 5. hx-confirm + hx-delete
            Div(
                section_header("🗑️", "hx-confirm & hx-delete", "Confirm dialogs and HTTP DELETE method", "error"),
                P("Click ✕ to delete. A confirm() dialog appears first.",
                  cls="text-sm text-base-content/60 mb-3"),
                # hx_trigger="load" fires the GET on page load to populate the list
                Div(hx_get="/demo/list", hx_trigger="load", hx_swap="innerHTML", id="delete-list"),
                Div(
                    attr_badge("hx-confirm", "Show confirm() dialog before request"),
                    attr_badge("hx-delete",  "Issue an HTTP DELETE request"),
                    attr_badge("closest li", "Walk up the DOM to the nearest <li>"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 6. hx-vals & hx-include
            Div(
                section_header("📦", "hx-vals & hx-include", "Send extra data alongside a request", "secondary"),
                Div(
                    Div(
                        P("hx-vals — embed JSON data", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Div(
                            *[Button(c.capitalize(),
                                cls="btn btn-sm",
                                style=f"background:{c};border-color:{c};color:#fff",
                                hx_get="/demo/vals",
                                hx_target="#vals-result",
                                hx_swap="innerHTML",
                                **{"hx-vals": f'{{"color":"{c}","size":"medium"}}'})
                              for c in ["crimson","royalblue","seagreen","darkorange","mediumpurple"]],
                            cls="flex flex-wrap gap-2"
                        ),
                        cls="flex-1"
                    ),
                    Div(
                        P("hx-include — pull from other elements", cls="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider"),
                        Div(
                            Input(id="extra-input", name="extra", placeholder="Type something…",
                                  cls="input input-bordered input-sm flex-1"),
                            Button("Send",
                                cls="btn btn-secondary btn-sm",
                                hx_get="/demo/vals",
                                hx_target="#vals-result",
                                hx_swap="innerHTML",
                                hx_include="#extra-input",
                                **{"hx-vals": '{"color":"blueviolet","size":"large"}'}),
                            cls="flex gap-2"
                        ),
                        cls="flex-1"
                    ),
                    cls="flex flex-col md:flex-row gap-6 mb-4"
                ),
                Div(
                    P("← Pick a colour or type something and hit Send", cls="text-base-content/40 text-sm italic"),
                    id="vals-result",
                    cls="p-3 bg-base-200 rounded-lg min-h-20 flex items-center justify-center"
                ),
                Div(
                    attr_badge("hx-vals",    "JSON object of extra params to send"),
                    attr_badge("hx-include", "CSS selector — include those inputs' values"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 7. hx-push-url
            Div(
                section_header("🚀", "hx-boost & hx-push-url", "AJAX navigation that keeps the URL in sync", "primary"),
                P("hx-push-url updates the browser address bar without a full reload. Back/forward history is preserved.",
                  cls="text-sm text-base-content/60 mb-3"),
                Div(
                    Button("Load Page A",
                        cls="btn btn-primary btn-sm",
                        hx_get="/demo/page-a",
                        hx_target="#boost-result",
                        hx_swap="innerHTML",
                        hx_push_url="/demo/page-a"),
                    Button("Load Page B",
                        cls="btn btn-secondary btn-sm",
                        hx_get="/demo/page-b",
                        hx_target="#boost-result",
                        hx_swap="innerHTML",
                        hx_push_url="/demo/page-b"),
                    cls="flex gap-2 mb-3"
                ),
                Div(
                    P("← Click a button above", cls="text-base-content/40 text-sm italic"),
                    id="boost-result",
                    cls="p-3 bg-base-200 rounded-lg min-h-12"
                ),
                Div(
                    attr_badge("hx-boost",    "true — upgrades all child <a>/<form> to AJAX"),
                    attr_badge("hx-push-url", "Push a URL onto the browser history stack"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 8. Polling / Progress
            Div(
                section_header("📊", "Polling & Progress", "Server-driven real-time updates via polling", "success"),
                P("The progress element polls every 300 ms and replaces itself (outerHTML) until the job is done.",
                  cls="text-sm text-base-content/60 mb-3"),
                Button("▶ Start Job",
                    cls="btn btn-success btn-sm mb-4",
                    hx_post="/demo/progress/start",
                    hx_target="#progress-container",
                    hx_swap="outerHTML"),
                Div(P("Press Start to begin", cls="text-xs text-base-content/40 text-center"),
                    id="progress-container"),
                Div(
                    attr_badge("hx-trigger", "load delay:300ms — re-fires on each new swap"),
                    attr_badge("hx-swap",    "outerHTML — the element replaces itself each poll"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            # 9. OOB swaps
            Div(
                section_header("🎯", "Out-of-Band Swaps", "One response updates multiple elements", "accent"),
                P("One POST response carries two payloads: the primary target and an OOB element found by id.",
                  cls="text-sm text-base-content/60 mb-3"),
                Div(
                    Button("Trigger OOB Update",
                        cls="btn btn-accent btn-sm",
                        hx_post="/demo/oob",
                        hx_target="#oob-main",
                        hx_swap="innerHTML"),
                    Div(Span("OOB Counter: 0", cls="badge badge-secondary font-mono"),
                        id="oob-counter-display", cls="ml-auto"),
                    cls="flex items-center gap-3 mb-3"
                ),
                Div(
                    P("← Main target (hx-target)", cls="text-base-content/40 text-sm italic"),
                    id="oob-main",
                    cls="p-3 bg-base-200 rounded-lg min-h-10"
                ),
                Div(
                    attr_badge("hx-swap-oob", "true — htmx finds the element by id and swaps it independently"),
                    cls="mt-4 pt-4 border-t border-base-200"
                ),
                cls="card bg-base-100 shadow-md p-6 feature-card"
            ),

            cls="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-6xl mx-auto px-4 pb-16"
        ),

        # ── Footer ────────────────────────────────────────────────────────────
        Footer(
            Div(
                Span("Built with ", cls="opacity-50 text-sm"),
                A("FastHTML", href="https://fastht.ml",  cls="link link-primary  text-sm font-mono"),
                Span(" + ", cls="opacity-50 text-sm"),
                A("HTMX",    href="https://htmx.org",    cls="link link-secondary text-sm font-mono"),
                Span(" + ", cls="opacity-50 text-sm"),
                A("DaisyUI", href="https://daisyui.com", cls="link link-accent    text-sm font-mono"),
                cls="flex items-center gap-1 justify-center"
            ),
            cls="footer footer-center py-8 border-t border-base-200"
        ),
    )

serve()
