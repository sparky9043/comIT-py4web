---
marp: true
theme: default
paginate: true
backgroundColor: #f9f9f9
style: |
  section { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  h1 { color: #092e20; } 
  code { background: #e8e8e8; color: #d63384; }
---

# Introduction to Django
### From Python Scripts to Web Applications
**Instructor:** y44k0v
*Goal: Understand the "Batteries Included" Web Framework*

---

# The "Restaurant" Metaphor 🍽️
Building a web app is like running a professional kitchen. 

1. **The URL (The Host):** Directs the customer to the right table.
2. **The View (The Waiter):** Takes the order and talks to the kitchen.
3. **The Model (The Pantry):** Where all the ingredients (data) are kept.
4. **The Template (The Plate):** How the food is presented to the customer.

---

# The Django Architecture (MVT)
Django uses the **Model-View-Template** pattern to keep code organized.



---

# 🛠️ Pre-Class Setup
Before we start, ensure your environment is ready:

1. **Install Django:**
   `pip install django`
2. **Create the Project:**
   `django-admin startproject bistro_project .`
3. **Create the App:**
   `python manage.py startapp menu`
4. **Test the Server:**
   `python manage.py runserver`

---

# Step 1: The Pantry (The Model)
In `menu/models.py`, we define what a "Dish" looks like.

```python
from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
```
**Action:** Run `python manage.py makemigrations` and `migrate`.

---

# Step 2: The Waiter (The View)
In `menu/views.py`, we write the logic to fetch the dishes.

```python
from django.shortcuts import render
from .models import Dish

def menu_view(request):
    # Fetching all items from the "Pantry"
    all_dishes = Dish.objects.all()
    
    # Handing the data to the "Plating Station"
    return render(request, 'menu.html', {'menu_items': all_dishes})
```

---

# Step 3: The Plating (The Template)
Create `menu/templates/menu.html`. This is what the user sees.

```html
<link href="[https://cdn.jsdelivr.net/npm/daisyui@latest/dist/full.css](https://cdn.jsdelivr.net/npm/daisyui@latest/dist/full.css)" rel="stylesheet">
<script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>

<div class="p-10">
  <h1 class="text-3xl font-bold mb-5">Bistro Menu</h1>
  <ul class="menu bg-base-200 w-56 rounded-box">
    {% for item in menu_items %}
      <li><a>{{ item.name }} - ${{ item.price }}</a></li>
    {% endfor %}
  </ul>
</div>
```

---

# Step 4: Connecting the Signs (URLs)
In `bistro_project/urls.py`, tell Django where the menu is.

```python
from django.contrib import admin
from django.urls import path
from menu.views import menu_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', menu_view),
]
```

---

# The "Magic" Admin Interface 🪄
Django gives you a professional backend for free.

1. **Create an Owner:** `python manage.py createsuperuser`
2. **Register the Model:** In `menu/admin.py` add:
   `admin.site.register(Dish)`
3. **Visit:** `http://127.0.0.1:8000/admin`
4. **Result:** Add data here, and watch it appear on your `/menu/` page!

---

# Summary: Why Django?
- **ORM:** Talk to databases using Python classes.
- **Admin:** Instant UI to manage your data.
- **Security:** Built-in protection against common web attacks.
- **Scalability:** It grows with your project (from nanodjango to Instagram).

**Questions? Let's keep coding!**
