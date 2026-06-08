# ✦ LuxeCart — Django E-Commerce Website

A full-featured e-commerce platform built with Django (Python) and a luxury dark-theme UI.

---

## 🚀 Quick Setup

```bash
# 1. Enter the project folder
cd ecommerce

# 2. Run setup script (installs everything, seeds data)
bash setup.sh

# 3. Start the server
python manage.py runserver

# 4. Open browser
# http://127.0.0.1:8000
```

---

## 📋 Step-by-Step Features

### ✅ Step 1: Registration & Login

| URL | Description |
|-----|-------------|
| `/register/` | Create a new account |
| `/login/` | Sign in to existing account |
| `/logout/` | Log out |

**Flow:**
1. Go to `/register/` → fill in First Name, Last Name, Username, Email, Password
2. Password strength indicator shown in real-time
3. On success → auto-login → redirect to home
4. Go to `/login/` → enter username + password → redirects to home (or previous page)

---

### ✅ Step 2: Product Detail Page

| URL | Description |
|-----|-------------|
| `/products/` | Browse all products |
| `/products/?category=electronics` | Filter by category |
| `/products/?q=headphones` | Search products |
| `/products/?sort=price_asc` | Sort products |
| `/products/<slug>/` | Individual product page |

**Features:**
- Product image, name, category, rating, price (with discount %)
- Stock availability badge
- Quantity selector (+/-)
- "Add to Cart" button (AJAX — no page reload)
- Related products from same category
- Breadcrumb navigation

---

### ✅ Step 3: Shopping Cart

| URL | Description |
|-----|-------------|
| `/cart/` | View cart |
| `/cart/add/<id>/` | Add item (POST) |
| `/cart/update/<id>/` | Update quantity (AJAX) |
| `/cart/remove/<id>/` | Remove item (AJAX) |

**Features:**
- Live quantity update without page reload
- Subtotal per item updates dynamically
- Order summary with shipping calculation
- "Free shipping" notification when cart < ₹999
- Empty cart state with CTA

---

### ✅ Step 4: Order Processing

| URL | Description |
|-----|-------------|
| `/checkout/` | Checkout form |
| `/place-order/` | Submit order (POST) |
| `/orders/` | Order history |
| `/orders/<id>/` | Order detail |
| `/orders/<id>/confirmation/` | Success page |

**Checkout form includes:**
- Shipping: full name, phone, address, city, state, PIN
- Payment methods: Cash on Delivery, UPI, Card, Net Banking

**After placing order:**
- Cart is cleared
- Order confirmation page with order number
- Progress steps (Ordered → Processing → Shipped → Delivered)
- Full order detail with shipping info

---

## 🗄️ Database Models

```
Category      → id, name, slug, icon
Product       → id, name, slug, category, description, price, original_price,
                stock, image, rating, review_count, is_featured
Cart          → id, user (OneToOne)
CartItem      → id, cart, product, quantity
Order         → id, user, status, total_price, shipping_*, payment_method
OrderItem     → id, order, product, quantity, price
```

---

## 👤 Admin Panel

Access at: `http://127.0.0.1:8000/admin`  
Username: `admin` | Password: `admin123`

Add products, manage orders, view users.

---

## 🛠️ Manual Setup (if setup.sh fails)

```bash
pip install django pillow
python manage.py makemigrations store
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 (Python) |
| Frontend | HTML5, CSS3 (custom), Vanilla JS |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Fonts | Playfair Display + DM Sans |
| Images | Unsplash (demo) |

---

## 📁 Project Structure

```
ecommerce/
├── manage.py
├── requirements.txt
├── setup.sh
├── ecommerce/           ← Django project config
│   ├── settings.py
│   └── urls.py
└── store/               ← Main app
    ├── models.py        ← Database models
    ├── views.py         ← All views (4 steps)
    ├── urls.py          ← URL routing
    ├── context_processors.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py  ← Sample data
    ├── static/store/
    │   ├── css/main.css      ← All styles
    │   └── js/main.js        ← AJAX + interactions
    └── templates/store/
        ├── base.html
        ├── home.html
        ├── register.html     ← Step 1
        ├── login.html        ← Step 1
        ├── product_list.html ← Step 2
        ├── product_detail.html ← Step 2
        ├── cart.html         ← Step 3
        ├── checkout.html     ← Step 4
        ├── order_confirmation.html ← Step 4
        ├── order_history.html
        └── order_detail.html
```
