## Step 1 — Enable Django's auth URLs

Django ships with built-in login and logout views. Wire them up in `zoo_site/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # ← add this
    path('', include('animals.urls', namespace='animals')),
]
```

`django.contrib.auth.urls` registers these routes automatically:

| URL | View | Name |
|-----|------|------|
| `/accounts/login/` | LoginView | `login` |
| `/accounts/logout/` | LogoutView | `logout` |
| `/accounts/password_change/` | PasswordChangeView | `password_change` |
| `/accounts/password_change/done/` | PasswordChangeDoneView | `password_change_done` |
| `/accounts/password_reset/` | PasswordResetView | `password_reset` |

---

## Step 2 — Configure settings

Add these three lines to `zoo_site/settings.py`:

```python
# Where to redirect after a successful login
LOGIN_REDIRECT_URL = 'animals:home'

# Where to send users who hit a @login_required page without being logged in
LOGIN_URL = 'login'

# Where to redirect after logout
LOGOUT_REDIRECT_URL = 'login'
```

---

## Step 3 — Add a signup view

Django has no built-in signup view, so add one to `animals/views.py`:

```python
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

class SignUpView(CreateView):
    """
    Uses Django's built-in UserCreationForm (username + password × 2).
    On successful registration the user is logged in immediately and
    redirected to the home page — no separate login step required.

    Extra context added:
      - page_title: for the heading
    """
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('animals:home')

    def form_valid(self, form):
        # Save the new user, then log them in straight away
        response = super().form_valid(form)
        login(self.request, self.obj)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Account'
        return context
```

Add the signup URL to `animals/urls.py`:

```python
from .views import SignUpView   # add to existing imports

urlpatterns = [
    ...
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]
```

---

## Step 4 — Protect all animal views with LoginRequiredMixin

Open `animals/views.py` and add `LoginRequiredMixin` to **every** animal view. It must be the **first** class in the inheritance list — Django's MRO requires this:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

# Apply to every view that should require authentication, for example:

class AnimalListView(LoginRequiredMixin, ListView):
    ...

class AnimalDetailView(LoginRequiredMixin, DetailView):
    ...

class AnimalCreateView(LoginRequiredMixin, CreateView):
    ...

class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    ...

class AnimalDeleteView(LoginRequiredMixin, DeleteView):
    ...

class AnimalSearchView(LoginRequiredMixin, FormView):
    ...

class AnimalArchiveIndexView(LoginRequiredMixin, ArchiveIndexView):
    ...

# ... and all remaining archive views
```

`HomeView` and `ZooRedirectView` can stay public — they show no sensitive data.

`LoginRequiredMixin` checks `request.user.is_authenticated` before the view runs. If the user is not logged in it redirects them to `LOGIN_URL` (set in Step 2) with `?next=/the/url/they/wanted/` appended, so after login they land on the right page.

---

## Step 5 — Create the templates

Django's auth views look for templates under `registration/`. Create the directory:

```bash
mkdir -p animals/templates/registration
```

### `animals/templates/registration/login.html`

```html
{% extends 'animals/base.html' %}

{% block title %}Login{% endblock %}
{% block heading %}Login{% endblock %}

{% block content %}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Log In</button>
</form>

<p>Don't have an account? <a href="{% url 'animals:signup' %}">Sign up</a></p>
{% endblock %}
```

### `animals/templates/registration/signup.html`

```html
{% extends 'animals/base.html' %}

{% block title %}{{ page_title }}{% endblock %}
{% block heading %}{{ page_title }}{% endblock %}

{% block content %}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Account</button>
</form>

<p>Already have an account? <a href="{% url 'login' %}">Log in</a></p>
{% endblock %}
```

### `animals/templates/registration/password_change_form.html`

```html
{% extends 'animals/base.html' %}

{% block title %}Change Password{% endblock %}
{% block heading %}Change Password{% endblock %}

{% block content %}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Change Password</button>
</form>
{% endblock %}
```

### `animals/templates/registration/password_change_done.html`

```html
{% extends 'animals/base.html' %}

{% block title %}Password Changed{% endblock %}
{% block heading %}Password Changed{% endblock %}

{% block content %}
<p>Your password was changed successfully.</p>
<p><a href="{% url 'animals:home' %}">Back to home</a></p>
{% endblock %}
```

---

## Step 6 — Update the navbar in `base.html`

Replace the `<nav>` block so it shows the logged-in username and a logout button, or a login link for guests:

```html
<nav>
    <strong>Zoo Management</strong> |
    <a href="{% url 'animals:home' %}">Home</a> |

    {% if user.is_authenticated %}
        <a href="{% url 'animals:animal-list' %}">All Animals</a> |
        <a href="{% url 'animals:animal-create' %}">Add Animal</a> |
        <a href="{% url 'animals:animal-search' %}">Search</a> |
        <a href="{% url 'animals:animal-archive-index' %}">Archive</a> |
        <a href="{% url 'animals:animal-today-archive' %}">Added Today</a> |
        <a href="{% url 'password_change' %}">Change Password</a> |
        Logged in as <strong>{{ user.username }}</strong> |
        <form method="post" action="{% url 'logout' %}" style="display:inline">
            {% csrf_token %}
            <button type="submit">Logout</button>
        </form>
    {% else %}
        <a href="{% url 'login' %}">Login</a> |
        <a href="{% url 'animals:signup' %}">Sign Up</a>
    {% endif %}
</nav>
```

> **Why a form for logout?** Since Django 5.0, `LogoutView` only accepts POST requests for security reasons (to prevent logout via a crafted link). Wrapping it in a `<form method="post">` with a CSRF token is the correct approach.

---

## Summary of all changes

| What | Where | Why |
|------|-------|-----|
| `include('django.contrib.auth.urls')` | `zoo_site/urls.py` | Registers login, logout, password views |
| `LOGIN_REDIRECT_URL`, `LOGIN_URL`, `LOGOUT_REDIRECT_URL` | `settings.py` | Controls redirect behaviour |
| `SignUpView` | `animals/views.py` | Django has no built-in signup |
| `LoginRequiredMixin` on all animal views | `animals/views.py` | Blocks unauthenticated access |
| `login.html`, `signup.html`, `password_change_form.html`, `password_change_done.html` | `animals/templates/registration/` | Templates for the auth views |
| Updated `<nav>` in `base.html` | `animals/templates/animals/base.html` | Shows user state on every page |

No new database migrations are needed — `django.contrib.auth` (which provides the `User` model) is already in `INSTALLED_APPS` and its tables were created when you first ran `migrate`.