## `django-debug-toolbar`

It's a developer-only tool that injects a collapsible sidebar panel into your Django pages showing detailed debug information for each request, including SQL queries and their execution time, cache hits and misses, template rendering times, HTTP headers and request/response details, signals fired, and static files loaded.

It's invaluable for catching N+1 query problems, slow templates, and unexpected database calls during development.

---

## Is it being used in the guide?

**No — it was added as a dev dependency but never actually configured.** It requires a few extra steps in `settings.py` and `urls.py` to activate. Here's how to wire it up properly:

### `config/settings.py`

```python
INSTALLED_APPS = [
    ...
    'debug_toolbar',  # add this
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # add as first middleware
    ...
]

# Required: debug toolbar only shows for these IPs
INTERNAL_IPS = ['127.0.0.1']
```

### `config/urls.py`

```python
from django.conf import settings

urlpatterns = [
    ...
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

Once configured, a **Django Debug Toolbar** panel will appear on the right side of every page when you run the dev server.

---

If you don't want to bother with it, you can simply skip the `uv add --dev django-debug-toolbar` line entirely — the app works fine without it.