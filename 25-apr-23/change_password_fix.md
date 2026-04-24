This is a template discovery order problem. Django finds the admin's `registration/` templates before your app's templates because `django.contrib.admin` is listed in `INSTALLED_APPS` before `'animals'`, and both provide templates under `registration/`.

The fix is to create the templates at the **project level** instead of inside the `animals` app, and tell Django to look there first.

---

## Step 1 — Create a project-level templates directory

```bash
mkdir -p zoo_site/templates/registration
```

---

## Step 2 — Tell Django to look there first

In `zoo_site/settings.py`, update the `DIRS` key inside `TEMPLATES`:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'zoo_site' / 'templates'],  # ← add this
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
```

Django searches `DIRS` entries **before** any app's `templates/` folder, so your templates will now always win over the admin's.

---

## Step 3 — Move the auth templates to the project-level directory

```bash
mv animals/templates/registration/password_change_form.html zoo_site/templates/registration/
mv animals/templates/registration/password_change_done.html zoo_site/templates/registration/
mv animals/templates/registration/login.html               zoo_site/templates/registration/
mv animals/templates/registration/signup.html              zoo_site/templates/registration/
```

Move all four so they are consistently resolved from the same place. Your final structure looks like this:

```
zoo_project/
├── zoo_site/
│   ├── settings.py
│   ├── urls.py
│   └── templates/                        ← project-level templates (checked first)
│       └── registration/
│           ├── login.html
│           ├── signup.html
│           ├── password_change_form.html
│           └── password_change_done.html
└── animals/
    └── templates/
        └── animals/                      ← app templates (checked second)
            ├── base.html
            ├── home.html
            └── ...
```

---

## Why this happens

Django's template loader checks locations in this order when `APP_DIRS: True`:

1. Every path listed in `DIRS` (project-level — checked first)
2. Each app's `templates/` folder in `INSTALLED_APPS` order

Since `django.contrib.admin` appears in `INSTALLED_APPS` before `'animals'`, Django finds `admin`'s copy of `registration/password_change_form.html` first and stops looking. Moving your templates to a `DIRS` path puts them ahead of all apps in the search order, so Django picks yours every time regardless of app ordering.
