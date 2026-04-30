# explorer/views.py
import time, random
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

# ── Global State ──
items_store = {1: "Item Alpha", 2: "Item Beta", 3: "Item Gamma", 4: "Item Delta"}
progress_state = {"value": 0, "running": False}
oob_counter = {"n": 0}
profile_data = {"name": "Jane Doe", "email": "jane.doe@example.com", "role": "Lead Engineer"}
search_db = ["Apple", "Apricot", "Banana", "Blueberry", "Cherry", "Cranberry", "Date", "Dragonfruit", "Elderberry", "Fig", "Grape", "Grapefruit"]
cars_db = {"Toyota": ["Camry", "Corolla", "Prius", "Tacoma"], "Ford": ["Mustang", "F-150", "Explorer", "Focus"], "Honda": ["Civic", "Accord", "CR-V", "Pilot"]}

def index(request):
    colors = ["crimson", "royalblue", "seagreen", "darkorange", "mediumpurple"]
    sortable_items = [("id_1", "Learn HTMX"), ("id_2", "Master Django"), ("id_3", "Build UI"), ("id_4", "Profit")]
    return render(request, 'explorer/index.html', {'colors': colors, 'sortable_items': sortable_items})

@csrf_exempt
@never_cache
def demo_click(request):
    if request.method == "POST": return HttpResponse(f'<div class="fade-in"><p class="font-semibold text-secondary">Hello, {request.POST.get("name", "stranger")}!</p></div>')
    return HttpResponse(f'<div class="fade-in"><p class="font-semibold text-primary">Fetched via GET at {time.strftime("%H:%M:%S")}</p></div>')

@never_cache
def trigger_hover(request): return HttpResponse('<span class="text-accent font-semibold fade-in">👀 Hovered!</span>')
@never_cache
def trigger_delay(request): return HttpResponse('<span class="text-warning font-semibold fade-in">⏱️ 1s delay!</span>')
@never_cache
def trigger_keyup(request): return HttpResponse(f'<span class="badge badge-outline font-mono fade-in">"{request.GET.get("q", "")}"</span>' if request.GET.get('q', '') else '')

@never_cache
def swap_mode(request, mode): return HttpResponse(f'<div class="fade-in font-mono text-primary font-bold">hx-swap="{mode}"</div>')

@never_cache
def slow_response(request):
    time.sleep(1.5)
    return HttpResponse('<div class="fade-in text-success font-semibold">✅ Loaded</div>')

@csrf_exempt
@never_cache
def list_items(request):
    html = "".join([f'<li class="border-b border-base-200"><div class="flex items-center py-1"><span class="flex-1 text-sm">• {item}</span><button type="button" class="btn btn-xs btn-ghost text-error" hx-delete="/demo/list/{idx}/" hx-confirm="Delete?" hx-target="closest li" hx-swap="outerHTML">✕</button></div></li>' for idx, item in items_store.items()])
    return HttpResponse(f'<ul class="w-full">{html}</ul>' if items_store else '<p class="text-error text-sm italic">Empty</p>')

@csrf_exempt
def delete_item(request, idx):
    if request.method == "DELETE" and idx in items_store: del items_store[idx]
    return HttpResponse("")

@never_cache
def page_a(request): return HttpResponse('<div class="fade-in text-primary font-bold">📄 Page A <button type="button" class="btn btn-sm btn-secondary mt-2" hx-get="/demo/page-b/" hx-target="#boost-result" hx-push-url="true">Go Page B</button></div>')
@never_cache
def page_b(request): return HttpResponse('<div class="fade-in text-secondary font-bold">📄 Page B <button type="button" class="btn btn-sm btn-primary mt-2" hx-get="/demo/page-a/" hx-target="#boost-result" hx-push-url="true">Go Page A</button></div>')

@never_cache
def vals_demo(request): return HttpResponse(f'<div class="fade-in font-mono text-xs"><div style="background:{request.GET.get("color")}" class="w-16 h-16 rounded-xl mb-2"></div>Color: {request.GET.get("color")}, Size: {request.GET.get("size")}<br>Extra: {request.GET.get("extra")}</div>')

def progress_widget(value, done=False):
    attrs = 'hx-get="/demo/progress/poll/" hx-trigger="every 300ms" hx-swap="outerHTML"' if not done else ''
    return f'<div id="progress-container" {attrs}><div class="w-full bg-base-200 h-4 rounded-full"><div class="progress-bar {"bg-success" if done else "bg-primary"} h-4 rounded-full" style="width:{value}%"></div></div><p class="text-xs text-center mt-1">{"Done!" if done else str(value)+"%"}</p></div>'

@csrf_exempt
def progress_start(request):
    progress_state.update({"value": 0, "running": True})
    return HttpResponse(progress_widget(0))

def progress_poll(request):
    if progress_state["running"]:
        progress_state["value"] = min(progress_state["value"] + random.randint(10, 20), 100)
        done = progress_state["value"] >= 100
        if done: progress_state["running"] = False
        return HttpResponse(progress_widget(progress_state["value"], done))
    return HttpResponse('<div id="progress-container">Press Start</div>')

@csrf_exempt
def oob_swap(request):
    oob_counter["n"] += 1
    return HttpResponse(f'<div class="fade-in text-primary font-bold">Main content #{oob_counter["n"]}</div><div id="oob-counter-display" class="ml-auto" hx-swap-oob="true"><span class="badge badge-secondary font-mono">OOB: {oob_counter["n"]}</span></div>')

@csrf_exempt
@never_cache
def inline_edit(request):
    if request.method == "POST": profile_data.update({"name": request.POST.get("name", ""), "email": request.POST.get("email", "")})
    return HttpResponse(f'<div class="fade-in p-4 border border-base-200 rounded-lg flex justify-between items-center shadow-sm" id="inline-profile"><div><h3 class="font-bold text-primary">{profile_data["name"]}</h3><p class="text-sm opacity-70">{profile_data["email"]}</p></div><button type="button" class="btn btn-outline btn-sm" hx-get="/demo/inline/form/" hx-target="#inline-profile" hx-swap="outerHTML">Edit</button></div>')

@never_cache
def inline_edit_form(request):
    return HttpResponse(f'<form class="fade-in p-4 border border-primary rounded-lg shadow-md" id="inline-profile" hx-post="/demo/inline/" hx-target="this" hx-swap="outerHTML"><div class="flex flex-col gap-2 mb-2"><input name="name" class="input input-sm input-bordered" value="{profile_data["name"]}"><input name="email" class="input input-sm input-bordered" value="{profile_data["email"]}"></div><div class="flex gap-2"><button type="submit" class="btn btn-primary btn-sm flex-1">Save</button><button type="button" class="btn btn-ghost btn-sm flex-1" hx-get="/demo/inline/" hx-target="#inline-profile" hx-swap="outerHTML">Cancel</button></div></form>')

@never_cache
def infinite_scroll(request):
    page = int(request.GET.get('page', 1))
    time.sleep(0.3)
    html = ""
    for i in range(1, 11):
        if i == 10 and page < 5: html += f'<tr hx-get="/demo/infinite/?page={page+1}" hx-trigger="revealed" hx-swap="afterend"><td>Item #{(page-1)*10+i}</td><td class="text-right opacity-50">Page {page} <span class="loading loading-dots loading-xs"></span></td></tr>'
        else: html += f'<tr><td>Item #{(page-1)*10+i}</td><td class="text-right opacity-50">Page {page}</td></tr>'
    return HttpResponse(html)

@never_cache
def cascading_models(request):
    make = request.GET.get('make', '')
    return HttpResponse("<option disabled selected>Select Model...</option>" + "".join([f"<option value='{m}'>{m}</option>" for m in cars_db.get(make, [])]))

@csrf_exempt
@never_cache
def validate_email(request):
    email = request.POST.get('email', '')
    if not email: return HttpResponse(f'<div class="form-control" id="email-group"><input type="email" name="email" class="input input-bordered input-sm" hx-post="/demo/validate/" hx-trigger="blur changed delay:300ms" hx-target="#email-group" hx-swap="outerHTML"></div>')
    cls, msg = ("input-error text-error", "Taken!") if email in ["test@test.com", "admin@domain.com"] else ("input-success text-success", "Available!")
    return HttpResponse(f'<div class="form-control fade-in" id="email-group"><input type="email" name="email" value="{email}" class="input input-bordered {cls} input-sm" hx-post="/demo/validate/" hx-trigger="blur changed delay:300ms" hx-target="#email-group" hx-swap="outerHTML"><label class="label pb-0"><span class="label-text-alt {cls} font-bold">{msg}</span></label></div>')

@csrf_exempt
@never_cache
def active_search(request):
    q = request.POST.get('search', '').lower()
    results = [i for i in search_db if q in i.lower()] if q else []
    if not results and q: return HttpResponse('<tr><td class="text-error text-center py-2 text-sm italic">No fruits found</td></tr>')
    return HttpResponse("".join([f'<tr class="hover:bg-base-200"><td class="py-2 px-4 text-sm">{i}</td></tr>' for i in results]))

@never_cache
def select_demo(request): return HttpResponse('<html><body><div id="ignore">🚨 Ignore</div><div id="target-content" class="fade-in text-success font-bold mt-2">✨ Extracted Cleanly!</div></body></html>')

@never_cache
def preserve_demo(request):
    bg = random.choice(["bg-primary/20", "bg-secondary/20", "bg-warning/20"])
    return HttpResponse(f'<div class="fade-in p-4 rounded-lg {bg} flex flex-col gap-2" id="preserve-container"><p class="text-sm font-bold">Swapped!</p><input type="text" id="preserved-input" hx-preserve class="input input-sm input-bordered" placeholder="I won\'t reset!"></div>')

@csrf_exempt
@never_cache
def sortable_reorder(request): return HttpResponse(f'<div class="fade-in alert alert-success mt-2 py-2"><span class="text-sm font-bold">Order: {" → ".join([x.replace("id_","") for x in request.POST.getlist("item")])}</span></div>')

@csrf_exempt
def file_upload(request):
    file = request.FILES.get('document') if request.method == "POST" else None
    if file: return HttpResponse(f'<div class="fade-in alert alert-success mt-2 py-2"><span class="text-sm">✅ Uploaded <strong>{file.name}</strong></span></div>')
    return HttpResponse('')

@csrf_exempt
@never_cache
def prompt_demo(request):
    user_input = request.headers.get("HX-Prompt")
    if user_input: return HttpResponse(f'<p class="fade-in text-success font-semibold text-center w-full">Hello, {user_input}!</p>')
    return HttpResponse('<p class="fade-in text-error text-center w-full">Prompt cancelled.</p>')

@csrf_exempt
@never_cache
def headers_demo(request):
    secret = request.headers.get("X-Secret-Token")
    if secret: return HttpResponse(f'<div class="fade-in text-primary font-mono text-sm break-all text-center">Header Received: <strong class="text-secondary">{secret}</strong></div>')
    return HttpResponse('')

@csrf_exempt
@never_cache
def sync_demo(request):
    time.sleep(2)
    return HttpResponse(f'<p class="fade-in text-accent font-semibold text-center w-full">Completed!</p>')

@never_cache
def replace_url_demo(request): return HttpResponse(f'<p class="fade-in font-bold text-info text-center w-full">Viewing Tab #{request.GET.get("tab", "1")}</p>')

@csrf_exempt
@never_cache
def params_demo(request): return HttpResponse(f'<div class="fade-in text-sm"><p>First: <strong class="text-success">{request.POST.get("firstName")}</strong></p><p>SSN: <strong class="text-error">{request.POST.get("ssn", "NOT RECEIVED")}</strong></p></div>')

@never_cache
def disable_demo(request):
    is_disabled = request.GET.get('state') == 'true'
    if is_disabled: return HttpResponse('<div id="disable-container" hx-disable class="fade-in p-4 border border-error bg-error/10 text-center"><p class="text-error font-bold mb-3">HTMX Disabled 🛑</p><button type="button" class="btn btn-sm btn-primary mb-2" hx-get="/demo/click/" hx-target="#disable-result">I do nothing</button><button type="button" class="btn btn-outline btn-error btn-sm w-full" hx-get="/demo/disable/?state=false" hx-target="#disable-container" hx-swap="outerHTML">Re-enable</button></div>')
    return HttpResponse('<div id="disable-container" class="fade-in p-4 border border-success bg-success/10 text-center"><p class="text-success font-bold mb-3">HTMX Active ✅</p><button type="button" class="btn btn-sm btn-primary mb-2" hx-get="/demo/click/" hx-target="#disable-result">I work</button><button type="button" class="btn btn-outline btn-success btn-sm w-full" hx-get="/demo/disable/?state=true" hx-target="#disable-container" hx-swap="outerHTML">Disable</button></div>')

@never_cache
def response_targets_demo(request):
    if random.choice([True, False]): return HttpResponse('<div class="fade-in text-success font-bold text-center w-full">✅ 200 OK!</div>')
    return HttpResponse('<div class="fade-in text-error font-bold text-center w-full">❌ 404 Error!</div>', status=404)

@csrf_exempt
@never_cache
def rest_verbs_demo(request):
    if request.method == "PUT": return HttpResponse('<div class="fade-in font-mono text-info w-full text-center font-bold">Processed HTTP PUT 🟢</div>')
    elif request.method == "PATCH": return HttpResponse('<div class="fade-in font-mono text-accent w-full text-center font-bold">Processed HTTP PATCH 🟣</div>')
    return HttpResponse("Method not allowed", status=405)