# --- START OF FILE main.py ---
import os
import sys
import time
import random
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

# ── Django Micro-framework Configuration ──────────────────────────────────────
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='htmx-django-secret-key',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        MIDDLEWARE=['django.middleware.common.CommonMiddleware'],
    )

# ── State ─────────────────────────────────────────────────────────────────────
items_store = {1: "Item Alpha", 2: "Item Beta", 3: "Item Gamma", 4: "Item Delta"}
progress_state = {"value": 0, "running": False}
oob_counter = {"n": 0}

profile_data = {"name": "Jane Doe", "email": "jane.doe@example.com", "role": "Lead Engineer"}
sortable_items = [("id_1", "Learn HTMX"), ("id_2", "Master Django"), ("id_3", "Build UI"), ("id_4", "Profit")]
search_db = ["Apple", "Apricot", "Banana", "Blueberry", "Cherry", "Cranberry", "Date", "Dragonfruit", "Elderberry", "Fig", "Grape", "Grapefruit"]
cars_db = {
    "Toyota": ["Camry", "Corolla", "Prius", "Tacoma"],
    "Ford": ["Mustang", "F-150", "Explorer", "Focus"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"]
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def section_header(emoji, title, subtitle, color="primary"):
    return f"""
    <div class="mb-5">
        <span class="text-3xl">{emoji}</span>
        <h2 class="text-2xl font-bold text-{color} font-mono mt-1">{title}</h2>
        <p class="text-base-content/60 text-sm mt-1">{subtitle}</p>
    </div>
    """

def attr_badge(attr, desc):
    return f"""
    <div class="flex items-center gap-1 mb-1">
        <span class="font-mono text-xs badge badge-htmx">{attr}</span>
        <span class="text-xs text-base-content/70 ml-2">{desc}</span>
    </div>
    """

def result_box(placeholder, box_id):
    return f"""
    <div id="{box_id}" class="mt-3 min-h-10 p-2 rounded-lg bg-base-200 flex items-center">
        <p class="text-base-content/40 italic text-sm w-full">{placeholder}</p>
    </div>
    """

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES & VIEWS (1-22: Previous Features)
# ═══════════════════════════════════════════════════════════════════════════════

@csrf_exempt
@never_cache
def demo_click(request):
    if request.method == "POST": return HttpResponse(f'<div class="fade-in"><p class="font-semibold text-secondary">Hello, {request.POST.get("name", "stranger")}! Submitted via hx-post 📬</p><p class="text-xs text-base-content/50 font-mono mt-1">Received at: {time.strftime("%H:%M:%S")}</p></div>')
    msgs = ["HTMX fetched this via GET — no page reload! 🎉", "Still no reload. HTMX is smooth 😎", "Pure hypermedia in action! 🚀", "You really like clicking. Respect. 🖱️"]
    return HttpResponse(f'<div class="fade-in"><p class="font-semibold text-primary">{random.choice(msgs)}</p><p class="text-xs text-base-content/50 font-mono mt-1">Server time: {time.strftime("%H:%M:%S")}</p></div>')

@never_cache
def trigger_hover(request): return HttpResponse('<span class="text-accent font-semibold fade-in">👀 mouseover triggered this!</span>')
@never_cache
def trigger_delay(request): return HttpResponse('<span class="text-warning font-semibold fade-in">⏱️ Fired after 1s delay!</span>')
@never_cache
def trigger_keyup(request):
    q = request.GET.get('q', '')
    if not q: return HttpResponse('<span class="text-base-content/40 italic text-sm">Start typing…</span>')
    return HttpResponse(f'<div class="fade-in flex items-center gap-2"><span class="badge badge-outline font-mono">"{q}"</span><span class="text-xs text-base-content/50 ml-1">{len(q)} chars</span></div>')

@never_cache
def swap_mode(request, mode):
    labels = {"innerHTML": ("🔄", "text-primary", "Inner content replaced."), "outerHTML": ("💥", "text-secondary", "Entire element replaced."), "prepend": ("↑", "text-warning", "Added to TOP of target."), "append": ("↓", "text-success", "Added to BOTTOM of target."), "beforebegin": ("⬆️", "text-accent", "Inserted BEFORE target."), "afterend": ("⬇️", "text-info", "Inserted AFTER target.")}
    icon, color, desc = labels.get(mode, ("?", "", "Unknown mode"))
    return HttpResponse(f'<div class="fade-in"><span class="font-mono font-bold {color}">{icon} hx-swap="{mode}"</span><p class="text-xs text-base-content/60 mt-1">{desc}</p></div>')

@never_cache
def slow_response(request):
    time.sleep(1.5)
    return HttpResponse('<div class="fade-in"><p class="text-success font-semibold">✅ Response arrived after 1.5 s</p><p class="text-xs opacity-60 mt-1">The spinner showed while waiting.</p></div>')

@csrf_exempt
@never_cache
def list_items(request):
    if not items_store: return HttpResponse('<p class="text-error text-sm italic fade-in">All items deleted!</p>')
    items_html = "".join([f"""<li class="border-b border-base-200"><div class="flex items-center gap-2 py-1"><span class="flex-1 text-sm">• {item}</span><button type="button" class="btn btn-xs btn-ghost text-error" hx-delete="/demo/list/{idx}/" hx-confirm="Delete '{item}'?" hx-target="closest li" hx-swap="outerHTML">✕</button></div></li>""" for idx, item in items_store.items()])
    return HttpResponse(f'<ul class="w-full">{items_html}</ul>')

@csrf_exempt
def delete_item(request, idx):
    if request.method == "DELETE" and idx in items_store: del items_store[idx]
    return HttpResponse("")

@never_cache
def page_a(request): return HttpResponse('<div class="fade-in"><p class="font-semibold text-primary">📄 Page A</p><p class="text-sm opacity-70 mt-1">URL updated via hx-push-url.</p><button type="button" class="btn btn-sm btn-secondary mt-3" hx-get="/demo/page-b/" hx-target="#boost-result" hx-swap="innerHTML" hx-push-url="/demo/page-b/">→ Load Page B</button></div>')
@never_cache
def page_b(request): return HttpResponse('<div class="fade-in"><p class="font-semibold text-secondary">📄 Page B</p><p class="text-sm opacity-70 mt-1">URL updated via hx-push-url.</p><button type="button" class="btn btn-sm btn-primary mt-3" hx-get="/demo/page-a/" hx-target="#boost-result" hx-swap="innerHTML" hx-push-url="/demo/page-a/">← Back to Page A</button></div>')

@never_cache
def vals_demo(request):
    color, size, extra = request.GET.get("color", "none"), request.GET.get("size", "none"), request.GET.get("extra", "")
    return HttpResponse(f'<div class="fade-in flex flex-col items-center"><div style="background:{color};border:2px solid #6366f1" class="w-16 h-16 rounded-xl mb-2"></div><p class="font-mono text-xs text-primary">color={color}  size={size}</p>{f"<p class=font-mono text-xs text-secondary mt-1>extra = {extra}</p>" if extra else ""}</div>')

def progress_widget(value, done=False):
    bar_color, label = ("bg-success", "✅ Complete!") if done else ("bg-primary", f"{value}%")
    poll_attrs = 'hx-get="/demo/progress/poll/" hx-trigger="every 300ms" hx-swap="outerHTML"' if not done else ""
    return f'<div id="progress-container" {poll_attrs}><div class="w-full bg-base-200 rounded-full h-4"><div class="progress-bar {bar_color} h-4 rounded-full" style="width:{value}%"></div></div><p class="text-xs text-center mt-1 font-mono {"text-success" if done else ""}">{label}</p></div>'

@csrf_exempt
@never_cache
def progress_start(request):
    if request.method == "POST":
        progress_state.update({"value": 0, "running": True})
        return HttpResponse(progress_widget(0))
    return HttpResponse(status=405)

@never_cache
def progress_poll(request):
    if progress_state["running"]:
        progress_state["value"] = min(progress_state["value"] + random.randint(8, 22), 100)
        done = progress_state["value"] >= 100
        if done: progress_state["running"] = False
        return HttpResponse(progress_widget(progress_state["value"], done))
    return HttpResponse('<div id="progress-container"><p class="text-xs text-base-content/40 text-center">Press Start to begin</p></div>')

@csrf_exempt
def oob_swap(request):
    if request.method == "POST":
        oob_counter["n"] += 1
        return HttpResponse(f"""<div class="fade-in"><p class="text-primary font-semibold">Main content updated — click #{oob_counter["n"]}</p></div><div id="oob-counter-display" class="ml-auto" hx-swap-oob="true"><span class="badge badge-secondary font-mono">OOB Counter: {oob_counter["n"]}</span></div>""")
    return HttpResponse(status=405)

@csrf_exempt
@never_cache
def inline_edit(request):
    if request.method == "POST": profile_data.update({"name": request.POST.get("name", ""), "email": request.POST.get("email", ""), "role": request.POST.get("role", "")})
    return HttpResponse(f"""<div class="fade-in p-4 border border-base-200 rounded-lg bg-base-100 flex justify-between items-center shadow-sm" id="inline-profile"><div><h3 class="font-bold text-lg text-primary">{profile_data['name']}</h3><p class="text-sm opacity-70">{profile_data['role']} • {profile_data['email']}</p></div><button type="button" class="btn btn-outline btn-sm" hx-get="/demo/inline/form/" hx-target="#inline-profile" hx-swap="outerHTML">Edit Profile</button></div>""")

@never_cache
def inline_edit_form(request):
    return HttpResponse(f"""<form class="fade-in p-4 border border-primary rounded-lg bg-base-200 shadow-md" id="inline-profile" hx-post="/demo/inline/" hx-target="this" hx-swap="outerHTML"><div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3"><input name="name" class="input input-sm input-bordered" value="{profile_data['name']}" placeholder="Name"><input name="role" class="input input-sm input-bordered" value="{profile_data['role']}" placeholder="Role"><input name="email" class="input input-sm input-bordered md:col-span-2" value="{profile_data['email']}" placeholder="Email"></div><div class="flex gap-2"><button type="submit" class="btn btn-primary btn-sm flex-1">Save Changes</button><button type="button" class="btn btn-ghost btn-sm flex-1" hx-get="/demo/inline/" hx-target="#inline-profile" hx-swap="outerHTML">Cancel</button></div></form>""")

@never_cache
def infinite_scroll(request):
    page = int(request.GET.get('page', 1))
    time.sleep(0.4)
    html = ""
    for i in range(1, 11):
        item_num = ((page - 1) * 10) + i
        if i == 10 and page < 5: html += f"""<tr hx-get="/demo/infinite/?page={page+1}" hx-trigger="revealed" hx-swap="afterend"><td class="font-mono">Item #{item_num}</td><td class="opacity-50 text-xs text-right">Page {page} <span class="loading loading-dots loading-xs ml-2"></span></td></tr>"""
        else: html += f"<tr><td class='font-mono'>Item #{item_num}</td><td class='opacity-50 text-xs text-right'>Page {page}</td></tr>"
    return HttpResponse(html)

@never_cache
def cascading_models(request):
    make = request.GET.get('make', '')
    models = cars_db.get(make, [])
    options = "<option disabled selected>Select Model...</option>" + "".join([f"<option value='{m}'>{m}</option>" for m in models])
    return HttpResponse(options)

@csrf_exempt
@never_cache
def validate_email(request):
    email = request.POST.get('email', '')
    if not email: return HttpResponse(f'<div class="form-control w-full" id="email-group"><input type="email" name="email" placeholder="Enter email..." class="input input-bordered input-sm w-full" hx-post="/demo/validate/" hx-trigger="blur changed delay:300ms" hx-target="#email-group" hx-swap="outerHTML"></div>')
    is_taken = email in ["test@test.com", "admin@domain.com"]
    cls, msg, icon = ("input-error text-error", "Email taken!", "❌") if is_taken else ("input-success text-success", "Available!", "✅")
    return HttpResponse(f"""<div class="form-control w-full fade-in" id="email-group"><input type="email" name="email" value="{email}" class="input input-bordered {cls} input-sm w-full" hx-post="/demo/validate/" hx-trigger="blur changed delay:300ms" hx-target="#email-group" hx-swap="outerHTML"><label class="label pb-0"><span class="label-text-alt {cls} font-bold">{icon} {msg}</span></label></div>""")

@csrf_exempt
@never_cache
def active_search(request):
    q = request.POST.get('search', '').lower()
    results = [item for item in search_db if q in item.lower()] if q else []
    if not results and q: return HttpResponse('<tr><td class="text-error text-center text-sm py-4 italic">No fruits found...</td></tr>')
    if not q: return HttpResponse('<tr><td class="text-base-content/40 text-center text-sm py-4 italic">Start typing...</td></tr>')
    return HttpResponse("".join([f'<tr class="hover:bg-base-200"><td class="py-2 px-4 text-sm font-medium">{item}</td></tr>' for item in results]))

@never_cache
def select_demo(request):
    return HttpResponse("""
        <html><body>
            <div id="ignore-me" class="text-error font-bold">🚨 You should NOT see this!</div>
            <div id="target-content" class="fade-in flex items-center gap-3 p-3 bg-success/20 border border-success rounded-lg mt-2">
                <span class="text-2xl">✂️</span><div><p class="font-bold text-success">Extracted Cleanly!</p></div>
            </div>
        </body></html>
    """)
    
@never_cache
def preserve_demo(request):
    bg = random.choice(["bg-primary/20", "bg-secondary/20", "bg-accent/20", "bg-warning/20"])
    return HttpResponse(f"""<div class="fade-in p-4 rounded-lg {bg} flex flex-col gap-3 transition-colors duration-500" id="preserve-container"><p class="text-sm font-bold flex justify-between">Container swapped! <span class="badge badge-sm badge-ghost">{time.strftime('%H:%M:%S')}</span></p><input type="text" id="preserved-input" hx-preserve class="input input-sm input-bordered bg-base-100" placeholder="I won't reset on swap!"></div>""")

@csrf_exempt
@never_cache
def sortable_reorder(request):
    new_order = request.POST.getlist('item')
    return HttpResponse(f'<div class="fade-in alert alert-success mt-3 py-2"><span class="text-sm font-mono font-bold">Order: {" → ".join([x.replace("id_","") for x in new_order])}</span></div>')

@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        file = request.FILES.get('document')
        if file: return HttpResponse(f'<div class="fade-in alert alert-success mt-3 py-2"><span class="text-sm">✅ Uploaded <strong>{file.name}</strong></span></div>')
    return HttpResponse('')

@csrf_exempt
@never_cache
def prompt_demo(request):
    user_input = request.headers.get("HX-Prompt")
    if user_input: return HttpResponse(f'<p class="fade-in text-success font-semibold text-center w-full">Hello, {user_input}! 👋</p>')
    return HttpResponse('<p class="fade-in text-error font-semibold text-center w-full">You cancelled the prompt.</p>')

@csrf_exempt
@never_cache
def headers_demo(request):
    secret = request.headers.get("X-Secret-Token")
    if secret: return HttpResponse(f'<div class="fade-in text-primary font-mono text-sm break-all w-full text-center">Header Received:<br><strong class="text-secondary">{secret}</strong></div>')
    return HttpResponse('')

@csrf_exempt
@never_cache
def sync_demo(request):
    time.sleep(2)
    return HttpResponse(f'<p class="fade-in text-accent font-semibold text-center w-full">Request completed! ({time.strftime("%H:%M:%S")})</p>')

@never_cache
def replace_url_demo(request):
    tab = request.GET.get('tab', '1')
    return HttpResponse(f'<p class="fade-in font-bold text-info text-center w-full">Currently viewing Content for Tab #{tab}</p>')

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES & VIEWS (23-26: The Final HTMX Core Features)
# ═══════════════════════════════════════════════════════════════════════════════

@csrf_exempt
@never_cache
def params_demo(request):
    # Notice we only receive "firstName" and "lastName" because of hx-params.
    # The "ssn" field is securely left behind in the browser!
    first = request.POST.get('firstName', 'Unknown')
    last = request.POST.get('lastName', 'Unknown')
    ssn = request.POST.get('ssn', 'NOT RECEIVED')
    
    return HttpResponse(f"""
        <div class="fade-in w-full text-sm">
            <p><span class="opacity-60">First Name:</span> <strong class="text-success">{first}</strong></p>
            <p><span class="opacity-60">Last Name:</span> <strong class="text-success">{last}</strong></p>
            <p><span class="opacity-60">SSN:</span> <strong class="text-error">{ssn}</strong></p>
            <p class="mt-2 text-xs opacity-70">Notice how the SSN was filtered out by HTMX before transit.</p>
        </div>
    """)

@never_cache
def disable_demo(request):
    # This toggles a block of HTML between having hx-disable and not having it.
    is_disabled = request.GET.get('state') == 'true'
    
    if is_disabled:
        return HttpResponse(f"""
            <div id="disable-container" hx-disable class="fade-in p-4 border border-error rounded-lg bg-error/10 w-full text-center">
                <p class="text-error font-bold mb-3">HTMX is Disabled Here! 🛑</p>
                <button type="button" class="btn btn-sm btn-primary mb-2" hx-get="/demo/click/" hx-target="#disable-result">I do nothing now</button>
                <button type="button" class="btn btn-outline btn-error btn-sm w-full" hx-get="/demo/disable/?state=false" hx-target="#disable-container" hx-swap="outerHTML">Re-enable HTMX</button>
            </div>
        """)
    else:
        return HttpResponse(f"""
            <div id="disable-container" class="fade-in p-4 border border-success rounded-lg bg-success/10 w-full text-center">
                <p class="text-success font-bold mb-3">HTMX is Active! ✅</p>
                <button type="button" class="btn btn-sm btn-primary mb-2" hx-get="/demo/click/" hx-target="#disable-result">I work perfectly</button>
                <button type="button" class="btn btn-outline btn-success btn-sm w-full" hx-get="/demo/disable/?state=true" hx-target="#disable-container" hx-swap="outerHTML">Disable HTMX</button>
            </div>
        """)

@never_cache
def response_targets_demo(request):
    # Simulates a random backend error (50% chance of 200 OK, 50% chance of 404 Not Found)
    if random.choice([True, False]):
        return HttpResponse('<div class="fade-in text-success font-bold text-center w-full">✅ 200 OK! Data Loaded.</div>')
    else:
        # Django requires `status=404` to trigger the extension's error routing
        return HttpResponse('<div class="fade-in text-error font-bold text-center w-full">❌ 404 Error! Not Found.</div>', status=404)

@csrf_exempt
@never_cache
def rest_verbs_demo(request):
    # Django doesn't have request.PUT natively, but we can check the request.method
    method = request.method
    if method == "PUT":
        return HttpResponse(f'<div class="fade-in font-mono text-info w-full text-center font-bold">Processed HTTP PUT 🟢</div>')
    elif method == "PATCH":
        return HttpResponse(f'<div class="fade-in font-mono text-accent w-full text-center font-bold">Processed HTTP PATCH 🟣</div>')
    return HttpResponse("Method not allowed", status=405)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE (HTML Template inside view)
# ═══════════════════════════════════════════════════════════════════════════════
def index(request):
    html = f"""<!DOCTYPE html>
    <html lang="en" data-theme="night">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTMX Django Explorer</title>
        <link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.1/dist/full.min.css" rel="stylesheet" type="text/css" />
        <script src="https://cdn.tailwindcss.com"></script>
        
        <!-- Core HTMX -->
        <script src="https://unpkg.com/htmx.org@1.9.12"></script>
        <!-- HTMX Response Targets Extension -->
        <script src="https://unpkg.com/htmx.org@1.9.12/dist/ext/response-targets.js"></script>
        
        <script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {{ --font-mono: 'Space Mono', monospace; --font-sans: 'DM Sans', sans-serif; }}
            body  {{ font-family: var(--font-sans); }}
            .htmx-indicator               {{ opacity: 0; transition: opacity 200ms ease; }}
            .htmx-request .htmx-indicator {{ opacity: 1; }}
            .htmx-request.htmx-indicator  {{ opacity: 1; }}
            .feature-card {{ transition: transform 0.2s ease, box-shadow 0.2s ease; }}
            .feature-card:hover {{ transform: translateY(-2px); }}
            .badge-htmx {{ background: linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; }}
            @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
            .fade-in {{ animation: fadeIn 0.35s ease forwards; }}
            .progress-bar {{ transition: width 0.3s ease; }}
        </style>
    </head>
    <body hx-ext="response-targets"> <!-- Enable extension globally -->
        <!-- Navbar -->
        <div class="navbar bg-base-100 border-b border-base-200 sticky top-0 z-40 px-4 flex justify-between">
            <a href="/" class="btn btn-ghost px-2 text-xl"><span>⚡</span><span class="font-mono font-bold text-lg ml-1">HTMX Explorer</span></a>
            <div class="hidden md:flex gap-2">
                <span class="badge badge-outline badge-sm">Django</span>
                <span class="badge badge-outline badge-sm">DaisyUI</span>
                <span class="badge badge-outline badge-sm">Tailwind</span>
            </div>
        </div>

        <div class="py-14 px-6 max-w-3xl mx-auto">
            <h1 class="text-3xl md:text-5xl font-bold font-mono mb-3">HTMX Feature Explorer</h1>
            <p class="text-base-content/60 text-lg max-w-xl">26 exhaustive HTMX attributes & patterns, live and interactive — built with a single-file Django app.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-6xl mx-auto px-4 pb-16 items-start">
            
            <!-- 1. hx-get & hx-post -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🔁", "hx-get & hx-post", "Issue GET or POST requests from any element")}
                <div class="flex flex-col md:flex-row gap-4">
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">GET</p>
                        <button type="button" class="btn btn-primary btn-sm w-full" hx-get="/demo/click/" hx-target="#get-result" hx-swap="innerHTML">Fetch from server</button>
                        {result_box("Click the button →", "get-result")}
                    </div>
                    <div class="divider divider-horizontal hidden md:flex"></div>
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">POST</p>
                        <div class="flex gap-2">
                            <input name="name" id="post-name" placeholder="Name" class="input input-bordered input-sm flex-1 w-full max-w-[100px]">
                            <button type="button" class="btn btn-secondary btn-sm" hx-post="/demo/click/" hx-include="#post-name" hx-target="#post-result" hx-swap="innerHTML">Submit</button>
                        </div>
                        {result_box("Submit the form →", "post-result")}
                    </div>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-get", "URL to issue a GET request")}
                    {attr_badge("hx-post", "URL to issue a POST request")}
                </div>
            </div>

            <!-- 2. hx-trigger -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("⚡", "hx-trigger", "Control when requests fire — events, delays, filters", "accent")}
                <div class="flex flex-col md:flex-row gap-4">
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">mouseover</p>
                        <div class="p-2 rounded-xl bg-accent/10 border border-accent/20 text-center cursor-pointer text-sm font-mono h-8 flex items-center justify-center"
                             hx-get="/demo/trigger/hover/" hx-trigger="mouseover" hx-target="#hover-result" hx-swap="innerHTML">Hover me</div>
                        <div id="hover-result" class="mt-2 min-h-6 text-sm"></div>
                    </div>
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">keyup delay</p>
                        <input name="q" placeholder="Type..." class="input input-bordered input-sm w-full"
                               hx-get="/demo/trigger/keyup/" hx-trigger="keyup delay:500ms changed" hx-target="#keyup-result" hx-swap="innerHTML">
                        <div id="keyup-result" class="mt-2 min-h-6"></div>
                    </div>
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">click delay</p>
                        <button type="button" class="btn btn-warning btn-sm w-full" hx-get="/demo/trigger/delay/" hx-trigger="click delay:1s" hx-target="#delay-result" hx-swap="innerHTML">Click</button>
                        <div id="delay-result" class="mt-2 min-h-6 text-sm"></div>
                    </div>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger", "DOM event that fires the request")}
                    {attr_badge("delay:Xs", "Debounce — wait X s before firing")}
                </div>
            </div>

            <!-- 3. hx-swap -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🔀", "hx-swap & hx-target", "Choose exactly where and how content lands", "info")}
                <div class="flex flex-wrap gap-2 mb-3">
                    {''.join([f'<button type="button" class="btn btn-outline btn-xs font-mono" hx-get="/demo/swap/{m}/" hx-target="#swap-demo-area" hx-swap="innerHTML">{m}</button>' for m in ["innerHTML","outerHTML","prepend","append","beforebegin","afterend"]])}
                </div>
                {result_box("← Pick a swap mode above", "swap-demo-area")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-target", "CSS selector of the element to update")}
                    {attr_badge("hx-swap", "innerHTML | outerHTML | prepend | append | ...")}
                </div>
            </div>

            <!-- 4. hx-indicator -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("⏳", "hx-indicator", "Show a spinner during slow requests", "warning")}
                <p class="text-sm text-base-content/60 mb-4">The button is disabled and a spinner appears while the 1.5 s request is in flight.</p>
                <button type="button" id="slow-btn" class="btn btn-warning gap-2" hx-get="/demo/slow/" hx-target="#slow-result" hx-swap="innerHTML" hx-indicator="#slow-btn" hx-disabled-elt="this">
                    <span>Load slow response (1.5 s)</span><span class="loading loading-spinner loading-sm htmx-indicator ml-2"></span>
                </button>
                {result_box("← Trigger the slow request", "slow-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-indicator", "Element that receives .htmx-request class")}
                    {attr_badge("hx-disabled-elt", "Disable this element while in flight")}
                </div>
            </div>

            <!-- 5. hx-confirm & hx-delete -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🗑️", "hx-confirm & hx-delete", "Confirm dialogs and HTTP DELETE method", "error")}
                <p class="text-sm text-base-content/60 mb-3">Click ✕ to delete. A confirm() dialog appears first.</p>
                <div hx-get="/demo/list/" hx-trigger="load" hx-swap="innerHTML" id="delete-list"></div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-confirm", "Show confirm() dialog before request")}
                    {attr_badge("hx-delete", "Issue an HTTP DELETE request")}
                    {attr_badge("closest li", "Walk up the DOM to the nearest <li>")}
                </div>
            </div>

            <!-- 6. hx-vals & hx-include -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("📦", "hx-vals & hx-include", "Send extra data alongside a request", "secondary")}
                <div class="flex flex-col md:flex-row gap-6 mb-4">
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">hx-vals</p>
                        <div class="flex flex-wrap gap-2">
                            <button type="button" class="btn btn-sm" style="background:crimson;color:#fff" hx-get="/demo/vals/" hx-target="#vals-result" hx-vals='{{"color":"crimson"}}'>Crimson</button>
                            <button type="button" class="btn btn-sm" style="background:royalblue;color:#fff" hx-get="/demo/vals/" hx-target="#vals-result" hx-vals='{{"color":"royalblue"}}'>Blue</button>
                        </div>
                    </div>
                    <div class="flex-1">
                        <p class="font-bold text-xs mb-2 font-mono opacity-60 uppercase tracking-wider">hx-include</p>
                        <div class="flex gap-2">
                            <input id="extra-input" name="extra" placeholder="Type..." class="input input-bordered input-sm flex-1 w-full">
                            <button type="button" class="btn btn-secondary btn-sm" hx-get="/demo/vals/" hx-target="#vals-result" hx-swap="innerHTML" hx-include="#extra-input" hx-vals='{{"color":"blueviolet","size":"large"}}'>Send</button>
                        </div>
                    </div>
                </div>
                {result_box("← Pick a colour or type something and hit Send", "vals-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-vals", "JSON object of extra params to send")}
                    {attr_badge("hx-include", "CSS selector — include those inputs' values")}
                </div>
            </div>

            <!-- 7. hx-push-url -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🚀", "hx-push-url", "AJAX navigation that keeps the URL in sync", "primary")}
                <p class="text-sm text-base-content/60 mb-3">hx-push-url updates the address bar without a full reload. Back/forward history is preserved.</p>
                <div class="flex gap-2 mb-3">
                    <button type="button" class="btn btn-primary btn-sm flex-1" hx-get="/demo/page-a/" hx-target="#boost-result" hx-swap="innerHTML" hx-push-url="/demo/page-a/">Load Page A</button>
                    <button type="button" class="btn btn-secondary btn-sm flex-1" hx-get="/demo/page-b/" hx-target="#boost-result" hx-swap="innerHTML" hx-push-url="/demo/page-b/">Load Page B</button>
                </div>
                {result_box("← Click a button above", "boost-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-push-url", "Push a URL onto the browser history stack")}
                </div>
            </div>

            <!-- 8. Polling -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("📊", "Polling & Progress", "Server-driven real-time updates via polling", "success")}
                <p class="text-sm text-base-content/60 mb-3">The progress element polls every 300 ms and replaces itself (outerHTML) until done.</p>
                <button type="button" class="btn btn-success btn-sm mb-4" hx-post="/demo/progress/start/" hx-target="#progress-container" hx-swap="outerHTML">▶ Start Job</button>
                <div id="progress-container"><p class="text-xs text-base-content/40 text-center">Press Start to begin</p></div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger", "every 300ms — safely triggers polling locally")}
                    {attr_badge("hx-swap", "outerHTML — the element replaces itself each poll")}
                </div>
            </div>

            <!-- 9. OOB Swaps -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🎯", "Out-of-Band Swaps", "One response updates multiple elements", "accent")}
                <p class="text-sm text-base-content/60 mb-3">One POST response carries two payloads: the primary target and an OOB element found by id.</p>
                <div class="flex items-center gap-3 mb-3">
                    <button type="button" class="btn btn-accent btn-sm" hx-post="/demo/oob/" hx-target="#oob-main" hx-swap="innerHTML">Trigger OOB Update</button>
                    <div id="oob-counter-display" class="ml-auto"><span class="badge badge-secondary font-mono">OOB Counter: 0</span></div>
                </div>
                {result_box("← Main target (hx-target)", "oob-main")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-swap-oob", "true — htmx finds element by id and swaps it")}
                </div>
            </div>

            <!-- 10. Inline Editing -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("📝", "Inline Edit", "Click-to-edit UI pattern", "secondary")}
                <p class="text-sm text-base-content/60 mb-3">Click 'Edit Profile' to swap the display view for a form. Cancel swaps it back.</p>
                <div hx-get="/demo/inline/" hx-trigger="load"></div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-swap='outerHTML'", "Bidirectional swapping of display and form elements")}
                </div>
            </div>

            <!-- 11. Infinite Scroll -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("📜", "Infinite Scroll", "Load more on reveal", "info")}
                <p class="text-sm text-base-content/60 mb-3">Scroll to the bottom of the table to trigger the next page load automatically.</p>
                <div class="h-40 overflow-y-auto border border-base-300 rounded-lg bg-base-200/50 shadow-inner">
                    <table class="table table-sm table-pin-rows">
                        <thead class="bg-base-200"><tr><th>Item</th><th class="text-right">Page</th></tr></thead>
                        <tbody id="infinite-table" hx-get="/demo/infinite/?page=1" hx-trigger="load"></tbody>
                    </table>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger='revealed'", "Fires when the element scrolls into the viewport")}
                </div>
            </div>

            <!-- 12. Cascading Dropdowns -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🔗", "Cascading Selects", "Populate child on parent change", "warning")}
                <p class="text-sm text-base-content/60 mb-3">Selecting a Make sends a request to populate the associated Models.</p>
                <div class="flex flex-col md:flex-row gap-4">
                    <div class="flex-1 form-control">
                        <label class="label pb-1"><span class="label-text font-bold text-xs uppercase opacity-60">Parent</span></label>
                        <select class="select select-bordered select-sm w-full" name="make" hx-get="/demo/models/" hx-target="#models-dropdown">
                            <option disabled selected>Select Make...</option>
                            <option value="Toyota">Toyota</option>
                            <option value="Ford">Ford</option>
                            <option value="Honda">Honda</option>
                        </select>
                    </div>
                    <div class="flex-1 form-control">
                        <label class="label pb-1"><span class="label-text font-bold text-xs uppercase opacity-60">Child</span></label>
                        <select class="select select-bordered select-sm w-full" id="models-dropdown">
                            <option disabled selected>Select Model...</option>
                        </select>
                    </div>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-get (on select)", "Defaults to firing on the 'change' event")}
                </div>
            </div>

            <!-- 13. Inline Validation -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("✔️", "Inline Validation", "Validate on blur", "success")}
                <p class="text-sm text-base-content/60 mb-3">Click away from the input to validate. <span class="font-mono bg-base-200 px-1 rounded">test@test.com</span> is taken.</p>
                <div class="form-control w-full" id="email-group">
                    <input type="email" name="email" placeholder="Enter email address..." class="input input-bordered input-sm w-full" 
                           hx-post="/demo/validate/" hx-trigger="blur changed delay:300ms" hx-target="#email-group" hx-swap="outerHTML">
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger='blur'", "Fires when the input element loses focus")}
                </div>
            </div>

            <!-- 14. Active Search -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🔍", "Active Search", "Typeahead filtering", "primary")}
                <p class="text-sm text-base-content/60 mb-3">Table updates as you type. Try "Apple" or "Grape".</p>
                <label class="input input-bordered input-sm flex items-center gap-2 mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z" clip-rule="evenodd" /></svg>
                    <input type="search" name="search" class="grow" placeholder="Search fruits..."
                           hx-post="/demo/search/" hx-trigger="input changed delay:250ms, search" hx-target="#search-results">
                </label>
                <div class="h-32 overflow-y-auto border border-base-300 bg-base-200/50 shadow-inner rounded-lg">
                    <table class="table table-sm w-full"><tbody id="search-results">
                        <tr><td class="text-base-content/40 text-center text-sm py-4 italic">Start typing to search</td></tr>
                    </tbody></table>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger='input'", "Fires on keystrokes with a 250ms debounce")}
                </div>
            </div>

            <!-- 15. hx-select -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("✂️", "hx-select", "Extract fragment from response", "accent")}
                <p class="text-sm text-base-content/60 mb-3">Server returns a full HTML page with '🚨 Error' divs, but HTMX extracts only the target.</p>
                <button type="button" class="btn btn-accent btn-sm w-full" hx-get="/demo/select/" hx-select="#target-content" hx-target="#r15">Fetch Extracted Element</button>
                {result_box("Only the extracted div will appear here...", "r15")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-select", "Parses server response, extracts matching CSS")}
                </div>
            </div>

            <!-- 16. hx-preserve -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🛡️", "hx-preserve", "Keep elements intact during swaps", "info")}
                <p class="text-sm text-base-content/60 mb-3">Type something below, then swap the container. The input value will not be erased.</p>
                <div id="preserve-demo" hx-get="/demo/preserve/" hx-trigger="load"></div>
                <button type="button" class="btn btn-info btn-outline btn-sm w-full mt-3" hx-get="/demo/preserve/" hx-target="#preserve-demo">Swap Container</button>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-preserve", "Element inside container is immune to overwrite")}
                </div>
            </div>

            <!-- 17. Sortable Drag/Drop -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🖐️", "Sortable", "Drag & Drop integration", "secondary")}
                <p class="text-sm text-base-content/60 mb-3">Drag items to reorder. HTMX auto-submits the new order to the backend.</p>
                <form id="sortable-form" class="list-none p-0 m-0" hx-post="/demo/sortable/" hx-trigger="end" hx-target="#sort-result">
                    {''.join([f'<li class="p-2 mb-2 bg-base-200 rounded border border-base-300 cursor-move flex justify-between items-center shadow-sm"><input type="hidden" name="item" value="{k}"><span class="font-medium text-sm">{v}</span><span class="opacity-50 text-xl">≡</span></li>' for k,v in sortable_items])}
                </form>
                <div id="sort-result"></div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-trigger='end'", "Fires when SortableJS finishes the drag event")}
                </div>
            </div>

            <!-- 18. File Uploads -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("📁", "File Upload", "AJAX Multipart forms", "error")}
                <p class="text-sm text-base-content/60 mb-3">Select a file to test the HTMX progress hook.</p>
                <form id="upload-form" class="bg-base-200 p-4 rounded-lg border border-base-300" hx-encoding="multipart/form-data" hx-post="/demo/upload/" hx-target="#upload-result">
                    <div class="flex gap-2 mb-3">
                        <input type="file" name="document" class="file-input file-input-bordered file-input-error file-input-sm w-full" />
                        <button type="submit" class="btn btn-error btn-sm">Upload</button>
                    </div>
                    <progress id="upload-progress" class="progress progress-error w-full" value="0" max="100"></progress>
                </form>
                <div id="upload-result"></div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-encoding", "multipart/form-data for file transmission")}
                    {attr_badge("htmx:xhr:progress", "JS hook listening for upload completion")}
                </div>
            </div>

            <!-- 19. hx-prompt -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("💬", "hx-prompt", "Native browser input prompt", "primary")}
                <p class="text-sm text-base-content/60 mb-3">Ask the user for input before the request fires, attaching their answer to the headers.</p>
                <button type="button" class="btn btn-primary btn-sm w-full" hx-post="/demo/prompt/" hx-prompt="What is your name?" hx-target="#prompt-result">Trigger Prompt</button>
                {result_box("Prompt answer will appear here...", "prompt-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-prompt", "Shows window.prompt() before request")}
                    {attr_badge("HX-Prompt", "Django reads it from request.headers")}
                </div>
            </div>

            <!-- 20. hx-headers -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🪪", "hx-headers", "Inject custom HTTP headers", "secondary")}
                <p class="text-sm text-base-content/60 mb-3">Useful for sending CSRF tokens, Auth Bearer tokens, or custom flags via JSON.</p>
                <button type="button" class="btn btn-secondary btn-sm w-full" hx-post="/demo/headers/" hx-headers='{{"X-Secret-Token": "django-htmx-rocks-123"}}' hx-target="#headers-result">Send Custom Header</button>
                {result_box("Header output will appear here...", "headers-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-headers", "JSON object of headers to merge into request")}
                </div>
            </div>

            <!-- 21. hx-sync -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🚦", "hx-sync", "Coordinate requests & prevent spam", "accent")}
                <p class="text-sm text-base-content/60 mb-3">Spam click this button! <code>hx-sync="this:drop"</code> will ignore subsequent clicks until the 2s request completes.</p>
                <button type="button" id="sync-btn" class="btn btn-accent btn-sm w-full gap-2" hx-post="/demo/sync/" hx-sync="this:drop" hx-target="#sync-result" hx-indicator="#sync-btn" hx-disabled-elt="this">
                    Initiate 2s Request <span class="loading loading-spinner loading-xs htmx-indicator ml-2"></span>
                </button>
                {result_box("Sync status...", "sync-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-sync='this:drop'", "Drop new requests if one is in flight")}
                </div>
            </div>

            <!-- 22. hx-replace-url -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🔄", "hx-replace-url", "Update URL without history push", "warning")}
                <p class="text-sm text-base-content/60 mb-3">Watch your address bar. The URL changes, but the browser 'Back' button history isn't cluttered.</p>
                <div class="flex gap-2">
                    <button type="button" class="btn btn-outline btn-warning btn-sm flex-1" hx-get="/demo/replace_url/?tab=1" hx-replace-url="true" hx-target="#replace-result">Tab 1</button>
                    <button type="button" class="btn btn-outline btn-warning btn-sm flex-1" hx-get="/demo/replace_url/?tab=2" hx-replace-url="true" hx-target="#replace-result">Tab 2</button>
                    <button type="button" class="btn btn-outline btn-warning btn-sm flex-1" hx-get="/demo/replace_url/?tab=3" hx-replace-url="true" hx-target="#replace-result">Tab 3</button>
                </div>
                {result_box("Click a tab...", "replace-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-replace-url='true'", "Calls history.replaceState() instead of pushState()")}
                </div>
            </div>

            <!-- 23. hx-params -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🎛️", "hx-params", "Filter Request Parameters", "primary")}
                <p class="text-sm text-base-content/60 mb-3">Filter out sensitive or unnecessary fields before sending the POST request.</p>
                <form class="flex flex-col gap-2" hx-post="/demo/params/" hx-params="firstName, lastName" hx-target="#params-result">
                    <div class="flex gap-2">
                        <input name="firstName" value="John" class="input input-sm input-bordered flex-1" readonly>
                        <input name="lastName" value="Doe" class="input input-sm input-bordered flex-1" readonly>
                    </div>
                    <input name="ssn" value="SUPER_SECRET_SSN" class="input input-sm input-bordered input-error w-full font-mono text-xs" readonly>
                    <button type="submit" class="btn btn-primary btn-sm">Submit with hx-params</button>
                </form>
                {result_box("Backend will output received params here...", "params-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-params='firstName, lastName'", "Only sends these specific keys")}
                </div>
            </div>

            <!-- 24. hx-disable -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🛑", "hx-disable", "Disable HTMX Dynamically", "error")}
                <p class="text-sm text-base-content/60 mb-3">Apply this attribute to kill all HTMX processing on an element and its children.</p>
                <div id="disable-container" hx-get="/demo/disable/?state=false" hx-trigger="load"></div>
                {result_box("Result from active buttons...", "disable-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-disable", "Stops HTMX event listeners entirely")}
                </div>
            </div>

            <!-- 25. HTMX Extensions (Response Targets) -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🧩", "hx-ext", "Response Targets Extension", "accent")}
                <p class="text-sm text-base-content/60 mb-3">Handle HTTP Errors (404, 500) gracefully by targeting different DIVs depending on the status code.</p>
                <button type="button" class="btn btn-accent btn-sm w-full" hx-get="/demo/error/" hx-target="#ok-result" hx-target-404="#err-result">
                    Trigger Random Backend Response
                </button>
                <div class="flex gap-2 mt-3">
                    <div id="ok-result" class="flex-1 min-h-10 p-2 rounded-lg bg-base-200 flex items-center border border-success/30">
                        <p class="text-success text-xs opacity-60">200 OK box...</p>
                    </div>
                    <div id="err-result" class="flex-1 min-h-10 p-2 rounded-lg bg-base-200 flex items-center border border-error/30">
                        <p class="text-error text-xs opacity-60">404 Error box...</p>
                    </div>
                </div>
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-ext='response-targets'", "Loaded globally on body tag")}
                    {attr_badge("hx-target-404", "If HTTP 404, render here instead")}
                </div>
            </div>

            <!-- 26. RESTful Verbs -->
            <div class="card bg-base-100 shadow-md p-6 feature-card">
                {section_header("🌐", "hx-put & hx-patch", "Full RESTful Verbs", "info")}
                <p class="text-sm text-base-content/60 mb-3">HTMX naturally supports all HTTP verbs for building pure REST APIs.</p>
                <div class="flex gap-2">
                    <button type="button" class="btn btn-outline btn-info btn-sm flex-1" hx-put="/demo/rest/" hx-target="#rest-result">Send PUT</button>
                    <button type="button" class="btn btn-outline btn-accent btn-sm flex-1" hx-patch="/demo/rest/" hx-target="#rest-result">Send PATCH</button>
                </div>
                {result_box("Awaiting REST call...", "rest-result")}
                <div class="mt-4 pt-4 border-t border-base-200">
                    {attr_badge("hx-put / hx-patch", "Sends respective HTTP methods")}
                </div>
            </div>

        </div>
        
        <!-- Footer -->
        <footer class="footer footer-center py-8 border-t border-base-200">
            <div class="flex items-center gap-1 justify-center">
                <span class="opacity-50 text-sm">Built with </span>
                <a href="https://djangoproject.com" class="link link-primary text-sm font-mono">Django</a>
                <span class="opacity-50 text-sm"> + </span>
                <a href="https://htmx.org" class="link link-secondary text-sm font-mono">HTMX</a>
                <span class="opacity-50 text-sm"> + </span>
                <a href="https://daisyui.com" class="link link-accent text-sm font-mono">DaisyUI</a>
            </div>
        </footer>

        <!-- JS Hooks -->
        <script>
            document.addEventListener('DOMContentLoaded', function () {{
                var sortableList = document.getElementById('sortable-form');
                if (sortableList) {{
                    new Sortable(sortableList, {{
                        animation: 150,
                        ghostClass: 'bg-base-300'
                    }});
                }}
            }});
            
            htmx.on('#upload-form', 'htmx:xhr:progress', function(evt) {{
                var progress = evt.detail.loaded / evt.detail.total * 100;
                htmx.find('#upload-progress').setAttribute('value', progress);
            }});
            
            htmx.on('#upload-form', 'htmx:afterRequest', function(evt) {{
                setTimeout(function() {{ htmx.find('#upload-progress').setAttribute('value', 0); }}, 1500);
            }});
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

# ── URLs ──────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('', index),
    path('demo/click/', demo_click),
    path('demo/trigger/hover/', trigger_hover),
    path('demo/trigger/delay/', trigger_delay),
    path('demo/trigger/keyup/', trigger_keyup),
    path('demo/swap/<str:mode>/', swap_mode),
    path('demo/slow/', slow_response),
    path('demo/list/', list_items),
    path('demo/list/<int:idx>/', delete_item),
    path('demo/page-a/', page_a),
    path('demo/page-b/', page_b),
    path('demo/vals/', vals_demo),
    path('demo/progress/start/', progress_start),
    path('demo/progress/poll/', progress_poll),
    path('demo/oob/', oob_swap),
    
    path('demo/inline/', inline_edit),
    path('demo/inline/form/', inline_edit_form),
    path('demo/infinite/', infinite_scroll),
    path('demo/models/', cascading_models),
    path('demo/validate/', validate_email),
    path('demo/search/', active_search),
    path('demo/select/', select_demo),
    path('demo/preserve/', preserve_demo),
    path('demo/sortable/', sortable_reorder),
    path('demo/upload/', file_upload),
    
    path('demo/prompt/', prompt_demo),
    path('demo/headers/', headers_demo),
    path('demo/sync/', sync_demo),
    path('demo/replace_url/', replace_url_demo),
    
    # 23-26 New URLs
    path('demo/params/', params_demo),
    path('demo/disable/', disable_demo),
    path('demo/error/', response_targets_demo),
    path('demo/rest/', rest_verbs_demo),
]

# ── Execute CLI ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
# --- END OF FILE main.py ---
