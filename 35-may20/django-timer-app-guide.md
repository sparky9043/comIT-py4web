# Django Timer App — Complete Guide

> A full-stack multi-user timer application built with Django, Tailwind CSS, DaisyUI, HTMX, and Alpine.js — managed with UV.

---

## Table of Contents

1. [Installing UV](#1-installing-uv)
2. [Project Setup with UV](#2-project-setup-with-uv)
3. [Django Configuration](#3-django-configuration)
4. [Tailwind CSS & DaisyUI Setup](#4-tailwind-css--daisyui-setup)
5. [Authentication — Login, Logout & Registration](#5-authentication--login-logout--registration)
6. [Timer App — Models](#6-timer-app--models)
7. [Timer App — Views (CRUD)](#7-timer-app--views-crud)
8. [Timer App — URLs](#8-timer-app--urls)
9. [Templates — Base Layout](#9-templates--base-layout)
10. [Templates — Timer Dashboard](#10-templates--timer-dashboard)
11. [Templates — Timer Card (HTMX + Alpine.js)](#11-templates--timer-card-htmx--alpinejs)
12. [Templates — Auth Pages](#12-templates--auth-pages)
13. [Running the App](#13-running-the-app)

---

## 1. Installing UV

UV is an extremely fast Python package and project manager written in Rust. It replaces `pip`, `pip-tools`, `pipx`, `pyenv`, `virtualenv`, and more.

### macOS

Install via the official installer script (requires curl):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or with Homebrew:

```bash
brew install uv
```

After installation, restart your terminal or run:

```bash
source ~/.zshrc   # zsh (default on macOS)
source ~/.bashrc  # bash
```

Verify installation:

```bash
uv --version
```

### Windows

Install via PowerShell (run as Administrator or in a regular terminal):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or with WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Or with Scoop:

```powershell
scoop install uv
```

After installation, restart your terminal. Verify:

```powershell
uv --version
```

> **Note:** UV automatically manages Python versions. You do not need to install Python separately — UV will download and pin the correct version for your project.

---

## 2. Project Setup with UV

### Initialize the project

```bash
# Create the project directory
mkdir django-timers && cd django-timers

# Initialize a new UV project (creates pyproject.toml, .python-version, .venv)
uv init

# Pin a specific Python version (3.12 recommended)
uv python pin 3.12
```

### Add dependencies

```bash
# Core dependencies
uv add django
uv add django-browser-reload     # Hot reload in development
uv add whitenoise                # Static file serving

# Dev dependencies
uv add --dev django-debug-toolbar
```

UV automatically creates and manages a virtual environment under `.venv`. You never need to activate it manually — prefix commands with `uv run` and it handles everything.

### Create the Django project and app

```bash
uv run django-admin startproject config .
uv run python manage.py startapp timers
uv run python manage.py startapp accounts
```

Your project structure should look like this:

```
django-timers/
├── .venv/
├── .python-version
├── pyproject.toml
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── timers/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── accounts/
    ├── views.py
    ├── urls.py
    └── templates/
```

---

## 3. Django Configuration

### `config/settings.py`

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'django_browser_reload',
    # Local
    'accounts',
    'timers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',  # Dev hot reload
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('timers.urls')),
    path('__reload__/', include('django_browser_reload.urls')),  # Dev only
]
```

---

## 4. Tailwind CSS & DaisyUI Setup

This project uses the CDN approach for Tailwind and DaisyUI to keep the setup simple. For production, you would use the Node.js CLI instead.

Create the static and template directories:

```bash
mkdir -p static/css static/js templates/timers templates/accounts
```

### CDN Setup (Development)

Add these to your base template `<head>` section (shown in full in [Section 9](#9-templates--base-layout)):

```html
<!-- Tailwind CSS v3 via CDN -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- DaisyUI via CDN -->
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css" rel="stylesheet" type="text/css" />

<!-- HTMX -->
<script src="https://unpkg.com/htmx.org@2.0.3"></script>

<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

### Optional: Production Node.js Tailwind Setup

For production, install Tailwind via Node:

```bash
npm init -y
npm install -D tailwindcss daisyui
npx tailwindcss init
```

Configure `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './timers/templates/**/*.html',
    './accounts/templates/**/*.html',
  ],
  theme: { extend: {} },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light', 'dark', 'cupcake'],
  },
}
```

Add build script to `package.json`:

```json
"scripts": {
  "build:css": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
}
```

---

## 5. Authentication — Login, Logout & Registration

### `accounts/urls.py`

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
]
```

### `accounts/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def register_view(request):
    if request.user.is_authenticated:
        return redirect('timers:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('timers:dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
```

---

## 6. Timer App — Models

### `timers/models.py`

```python
from django.db import models
from django.contrib.auth.models import User


class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timers')
    name = models.CharField(max_length=100, default='My Timer')
    elapsed_seconds = models.PositiveIntegerField(default=0)
    is_running = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.user.username})'

    def formatted_time(self):
        """Return elapsed seconds as HH:MM:SS string."""
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


class Lap(models.Model):
    timer = models.ForeignKey(Timer, on_delete=models.CASCADE, related_name='laps')
    lap_number = models.PositiveIntegerField()
    elapsed_seconds = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['lap_number']

    def __str__(self):
        return f'Lap {self.lap_number} — {self.timer.name}'

    def formatted_time(self):
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
```

### Create and apply migrations

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

---

## 7. Timer App — Views (CRUD)

### `timers/views.py`

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Timer, Lap
from django.db.models import F


# ─── Dashboard ──────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    timers = Timer.objects.filter(user=request.user).prefetch_related('laps')
    return render(request, 'timers/dashboard.html', {'timers': timers})


# ─── Create ─────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['POST'])
def create_timer(request):
    name = request.POST.get('name', 'My Timer').strip() or 'My Timer'
    timer = Timer.objects.create(user=request.user, name=name)
    # Return just the new timer card via HTMX
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})


# ─── Read (single card refresh) ──────────────────────────────────────────────

@login_required
def timer_detail(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})


# ─── Update — Rename ─────────────────────────────────────────────────────────

@login_required
@require_http_methods(['POST'])
def rename_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    new_name = request.POST.get('name', '').strip()
    if new_name:
        timer.name = new_name
        timer.save()
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})



# ─── Update — Tick (called by client every second while running) ──────────────

@login_required
@require_http_methods(['POST'])
def tick_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    if timer.is_running:
        # F() expression prevents race conditions by incrementing atomically directly in the DB
        Timer.objects.filter(pk=pk).update(elapsed_seconds=F('elapsed_seconds') + 1)
        timer.refresh_from_db()
    return render(request, 'timers/partials/timer_display.html', {'timer': timer})

# ─── Update — Start ───────────────────────────────────────────────────────────
@login_required
@require_http_methods(['POST'])
def start_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    timer.is_running = True
    timer.save(update_fields=['is_running', 'updated_at']) # Only update state
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})

# ─── Update — Stop ────────────────────────────────────────────────────────────
@login_required
@require_http_methods(['POST'])
def stop_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    timer.is_running = False
    timer.save(update_fields=['is_running', 'updated_at']) # Don't overwrite elapsed_seconds
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})

# ─── Update — Reset ───────────────────────────────────────────────────────────

@login_required
@require_http_methods(['POST'])
def reset_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    timer.is_running = False
    timer.elapsed_seconds = 0
    timer.save()
    timer.laps.all().delete()
    return render(request, 'timers/partials/timer_card.html', {'timer': timer})


# ─── Create Lap ──────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['POST'])
def add_lap(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    lap_number = timer.laps.count() + 1
    Lap.objects.create(
        timer=timer,
        lap_number=lap_number,
        elapsed_seconds=timer.elapsed_seconds,
    )
    return render(request, 'timers/partials/lap_list.html', {'timer': timer})


# ─── Delete Timer ─────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['DELETE'])
def delete_timer(request, pk):
    timer = get_object_or_404(Timer, pk=pk, user=request.user)
    timer.delete()
    # Return empty response — HTMX will remove the element
    return HttpResponse(status=200)
```

---

## 8. Timer App — URLs

### `timers/urls.py`

```python
from django.urls import path
from . import views

app_name = 'timers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # CRUD
    path('timers/create/', views.create_timer, name='create'),
    path('timers/<int:pk>/', views.timer_detail, name='detail'),
    path('timers/<int:pk>/rename/', views.rename_timer, name='rename'),
    path('timers/<int:pk>/delete/', views.delete_timer, name='delete'),

    # Timer controls
    path('timers/<int:pk>/start/', views.start_timer, name='start'),
    path('timers/<int:pk>/stop/', views.stop_timer, name='stop'),
    path('timers/<int:pk>/reset/', views.reset_timer, name='reset'),
    path('timers/<int:pk>/tick/', views.tick_timer, name='tick'),

    # Laps
    path('timers/<int:pk>/lap/', views.add_lap, name='lap'),
]
```

---

## 9. Templates — Base Layout

### `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}Timer App{% endblock %}</title>

  <!-- DaisyUI (includes Tailwind base) -->
  <link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css"
        rel="stylesheet" type="text/css" />

  <!-- Tailwind CSS CDN (required for utility classes not in DaisyUI) -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- HTMX -->
  <script src="https://unpkg.com/htmx.org@2.0.3"></script>

  <!-- Alpine.js (defer is required) -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

  {% block extra_head %}{% endblock %}
</head>
<body class="min-h-screen bg-base-200" hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>

  <!-- Navbar -->
  <nav class="navbar bg-base-100 shadow-sm px-6">
    <div class="flex-1">
      <a href="{% url 'timers:dashboard' %}" class="btn btn-ghost text-xl font-bold">
        ⏱ TimerApp
      </a>
    </div>
    <div class="flex-none gap-2">
      {% if user.is_authenticated %}
        <span class="text-sm text-base-content/60">Hello, <strong>{{ user.username }}</strong></span>
        <form method="post" action="{% url 'accounts:logout' %}">
          {% csrf_token %}
          <button type="submit" class="btn btn-ghost btn-sm">Logout</button>
        </form>
      {% else %}
        <a href="{% url 'accounts:login' %}" class="btn btn-ghost btn-sm">Login</a>
        <a href="{% url 'accounts:register' %}" class="btn btn-primary btn-sm">Register</a>
      {% endif %}
    </div>
  </nav>

  <!-- Flash messages -->
  {% if messages %}
    <div class="container mx-auto px-4 mt-4">
      {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible mb-2">
          <span>{{ message }}</span>
        </div>
      {% endfor %}
    </div>
  {% endif %}

  <!-- Page content -->
  <main class="container mx-auto px-4 py-8">
    {% block content %}{% endblock %}
  </main>

  {% block extra_scripts %}{% endblock %}
</body>
</html>
```

---

## 10. Templates — Timer Dashboard

### `templates/timers/dashboard.html`

```html
{% extends 'base.html' %}

{% block title %}My Timers{% endblock %}

{% block content %}
<div class="flex items-center justify-between mb-8">
  <h1 class="text-3xl font-bold">My Timers</h1>

  <!-- Create Timer Modal Trigger -->
  <button class="btn btn-primary"
          onclick="document.getElementById('create_modal').showModal()">
    + New Timer
  </button>
</div>

<!-- Create Timer Modal (DaisyUI dialog) -->
<dialog id="create_modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg mb-4">Create New Timer</h3>
    <form hx-post="{% url 'timers:create' %}"
          hx-target="#timer-list"
          hx-swap="afterbegin"
          hx-on::after-request="this.reset(); document.getElementById('create_modal').close()">
      {% csrf_token %}
      <div class="form-control mb-4">
        <label class="label"><span class="label-text">Timer Name</span></label>
        <input type="text"
               name="name"
               placeholder="e.g. Morning Run"
               class="input input-bordered w-full"
               maxlength="100" />
      </div>
      <div class="modal-action">
        <button type="button"
                class="btn btn-ghost"
                onclick="document.getElementById('create_modal').close()">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary">Create</button>
      </div>
    </form>
  </div>
  <!-- Click outside to close -->
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>

<!-- Timer Grid -->
<div id="timer-list"
     class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
  {% for timer in timers %}
    {% include 'timers/partials/timer_card.html' %}
  {% empty %}
    <div class="col-span-full text-center py-20 text-base-content/40">
      <p class="text-5xl mb-4">⏱</p>
      <p class="text-xl">No timers yet. Create your first one!</p>
    </div>
  {% endfor %}
</div>
{% endblock %}
```

---

## 11. Templates — Timer Card (HTMX + Alpine.js)

The timer card is the core interactive component. Alpine.js handles the client-side countdown tick, which calls the server every second to persist the elapsed time via HTMX.

### `templates/timers/partials/timer_card.html`

```html
<div id="timer-{{ timer.pk }}"
     class="card bg-base-100 shadow-md"
     x-data="{
       running: {{ timer.is_running|yesno:'true,false' }},
       intervalId: null,
       startTicking() {
         this.intervalId = setInterval(() => {
           htmx.trigger(
             document.querySelector('#tick-{{ timer.pk }}'),
             'tick'
           );
         }, 1000);
       },
       stopTicking() {
         if (this.intervalId) {
           clearInterval(this.intervalId);
           this.intervalId = null;
         }
       },
       init() {
         if (this.running) this.startTicking();
       },
       destroy() {
         this.stopTicking();
       }
     }"
     x-init="init()">

  <div class="card-body gap-4">

    <!-- Timer Header: Name + Delete -->
    <div class="flex items-start justify-between">
      <!-- Inline rename form -->
      <div x-data="{ editing: false }" class="flex-1">
        <!-- Display name (click to edit) -->
        <h2 class="card-title cursor-pointer hover:text-primary transition-colors"
            x-show="!editing"
            @click="editing = true">
          {{ timer.name }}
        </h2>

        <!-- Rename input (shown when editing) -->
        <form x-show="editing"
              hx-post="{% url 'timers:rename' timer.pk %}"
              hx-target="#timer-{{ timer.pk }}"
              hx-swap="outerHTML"
              @submit="editing = false"
              class="flex gap-2">
          {% csrf_token %}
          <input type="text"
                 name="name"
                 value="{{ timer.name }}"
                 class="input input-bordered input-sm flex-1"
                 maxlength="100"
                 x-ref="nameInput"
                 x-init="$watch('editing', val => val && $nextTick(() => $refs.nameInput.focus()))"
                 @keydown.escape="editing = false" />
          <button type="submit" class="btn btn-primary btn-sm">Save</button>
          <button type="button" class="btn btn-ghost btn-sm" @click="editing = false">✕</button>
        </form>
      </div>

      <!-- Delete button -->
      <button class="btn btn-ghost btn-sm text-error ml-2"
              hx-delete="{% url 'timers:delete' timer.pk %}"
              hx-target="#timer-{{ timer.pk }}"
              hx-swap="outerHTML swap:0.3s"
              hx-confirm="Delete '{{ timer.name }}'?">
        🗑
      </button>
    </div>

    <!-- Clock Display -->
    <div id="display-{{ timer.pk }}"
         class="text-5xl font-mono font-bold text-center py-4 tracking-widest tabular-nums">
      {{ timer.formatted_time }}
    </div>

    <!-- Hidden HTMX tick trigger (fires via Alpine's setInterval) -->
    <span id="tick-{{ timer.pk }}"
          hx-post="{% url 'timers:tick' timer.pk %}"
          hx-target="#display-{{ timer.pk }}"
          hx-swap="innerHTML"
          hx-trigger="tick"
          hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    </span>

    <!-- Controls -->
    <div class="flex flex-wrap gap-2 justify-center">

      <!-- Start -->
      <button class="btn btn-success btn-sm gap-1"
              x-show="!running"
              hx-post="{% url 'timers:start' timer.pk %}"
              hx-target="#timer-{{ timer.pk }}"
              hx-swap="outerHTML">
        ▶ Start
      </button>

      <!-- Stop -->
      <button class="btn btn-warning btn-sm gap-1"
              x-show="running"
              hx-post="{% url 'timers:stop' timer.pk %}"
              hx-target="#timer-{{ timer.pk }}"
              hx-swap="outerHTML">
        ⏸ Stop
      </button>

      <!-- Lap (only when running) -->
      <button class="btn btn-info btn-sm gap-1"
              x-show="running"
              hx-post="{% url 'timers:lap' timer.pk %}"
              hx-target="#laps-{{ timer.pk }}"
              hx-swap="innerHTML">
        🏁 Lap
      </button>

      <!-- Reset -->
      <button class="btn btn-error btn-sm btn-outline gap-1"
              hx-post="{% url 'timers:reset' timer.pk %}"
              hx-target="#timer-{{ timer.pk }}"
              hx-swap="outerHTML"
              hx-confirm="Reset '{{ timer.name }}'? All laps will be deleted.">
        ↺ Reset
      </button>

    </div>

    <!-- Lap List -->
    <div id="laps-{{ timer.pk }}">
      {% include 'timers/partials/lap_list.html' %}
    </div>

  </div>
</div>
```

### `templates/timers/partials/timer_display.html`

This partial returns only the clock string, swapped in by the tick endpoint:

```html
{{ timer.formatted_time }}
```

### `templates/timers/partials/lap_list.html`

```html
{% if timer.laps.all %}
  <div class="divider text-xs text-base-content/40">Laps</div>
  <ul class="space-y-1 max-h-40 overflow-y-auto">
    {% for lap in timer.laps.all %}
      <li class="flex justify-between items-center text-sm bg-base-200 rounded px-3 py-1">
        <span class="text-base-content/60 font-medium">Lap {{ lap.lap_number }}</span>
        <span class="font-mono font-semibold">{{ lap.formatted_time }}</span>
      </li>
    {% endfor %}
  </ul>
{% endif %}
```

---

## 12. Templates — Auth Pages

### `templates/accounts/login.html`

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="flex justify-center items-center min-h-[60vh]">
  <div class="card bg-base-100 shadow-xl w-full max-w-sm">
    <div class="card-body">
      <h2 class="card-title text-2xl justify-center mb-2">Welcome back</h2>
      <p class="text-center text-base-content/60 mb-4">Sign in to your account</p>

      <form method="post">
        {% csrf_token %}

        <div class="form-control mb-3">
          <label class="label"><span class="label-text">Username</span></label>
          <input type="text"
                 name="username"
                 class="input input-bordered"
                 autofocus
                 required />
        </div>

        <div class="form-control mb-5">
          <label class="label"><span class="label-text">Password</span></label>
          <input type="password"
                 name="password"
                 class="input input-bordered"
                 required />
        </div>

        {% if form.errors %}
          <div class="alert alert-error mb-4 text-sm">
            Invalid username or password. Please try again.
          </div>
        {% endif %}

        <button type="submit" class="btn btn-primary w-full">Login</button>
      </form>

      <div class="divider text-xs">OR</div>

      <a href="{% url 'accounts:register' %}" class="btn btn-ghost w-full">
        Create an account
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

### `templates/accounts/register.html`

```html
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="flex justify-center items-center min-h-[60vh]">
  <div class="card bg-base-100 shadow-xl w-full max-w-sm">
    <div class="card-body">
      <h2 class="card-title text-2xl justify-center mb-2">Create account</h2>
      <p class="text-center text-base-content/60 mb-4">Join TimerApp today</p>

      <form method="post">
        {% csrf_token %}

        {% for field in form %}
          <div class="form-control mb-3">
            <label class="label">
              <span class="label-text">{{ field.label }}</span>
            </label>
            <input type="{{ field.field.widget.input_type }}"
                   name="{{ field.html_name }}"
                   id="{{ field.auto_id }}"
                   class="input input-bordered {% if field.errors %}input-error{% endif %}"
                   {% if field.field.required %}required{% endif %} />
            {% if field.errors %}
              {% for error in field.errors %}
                <label class="label">
                  <span class="label-text-alt text-error">{{ error }}</span>
                </label>
              {% endfor %}
            {% endif %}
            {% if field.help_text %}
              <label class="label">
                <span class="label-text-alt text-base-content/60">{{ field.help_text }}</span>
              </label>
            {% endif %}
          </div>
        {% endfor %}

        <button type="submit" class="btn btn-primary w-full mt-2">Register</button>
      </form>

      <div class="divider text-xs">OR</div>

      <a href="{% url 'accounts:login' %}" class="btn btn-ghost w-full">
        Sign in instead
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

---

## 13. Running the App

### Create a superuser (optional)

```bash
uv run python manage.py createsuperuser
```

### Run the development server

```bash
uv run python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Common UV commands

| Task | Command |
|---|---|
| Run a Django command | `uv run python manage.py <command>` |
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Show installed packages | `uv pip list` |
| Update all dependencies | `uv sync --upgrade` |
| Export requirements.txt | `uv pip freeze > requirements.txt` |
| Run a script | `uv run <script>.py` |

### Project dependency summary (`pyproject.toml`)

After all `uv add` commands, your `pyproject.toml` will look like this:

```toml
[project]
name = "django-timers"
version = "0.1.0"
description = "Multi-user timer app with Django, HTMX, Alpine.js & DaisyUI"
requires-python = ">=3.12"
dependencies = [
    "django>=5.0",
    "django-browser-reload>=1.12",
    "whitenoise>=6.7",
]

[dependency-groups]
dev = [
    "django-debug-toolbar>=4.3",
]
```

---

## Architecture Summary

```
User Request
    │
    ▼
Django View (CRUD, auth-gated)
    │
    ├── Full page? ──► render full template (base.html + block)
    │
    └── HTMX request? ──► render partial template only
            │
            ▼
        HTMX swaps HTML fragment into the DOM
            │
            ▼
        Alpine.js manages local state
        (timer running, editing mode, interval)
            │
            ▼
        Alpine's setInterval fires HTMX tick
        every 1 second → POST /timers/<pk>/tick/
            │
            ▼
        Server increments elapsed_seconds, returns
        updated display partial → HTMX swaps clock
```

### Key design decisions

- **Each user's timers are isolated** — every query is filtered by `user=request.user`, so users can never see or interact with each other's timers.
- **HTMX handles all state changes** — create, rename, start, stop, reset, lap, and delete all return HTML fragments, keeping the page interactive without a full SPA framework.
- **Alpine.js owns the client tick loop** — the interval runs in the browser and fires a server POST every second. This keeps the displayed time smooth without trusting only server-side state.
- **Laps are immutable records** — each lap captures the elapsed time at the moment the lap button is pressed and is persisted to the database.
- **DaisyUI provides the component system** — cards, modals, buttons, alerts, and form controls all use DaisyUI classes, keeping markup clean and consistent.
