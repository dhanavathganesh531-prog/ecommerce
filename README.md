# NovaStore - Modern Django eCommerce Platform

A full-featured, responsive, production-ready Django eCommerce web application.

---

## 📁 Project Structure

```
ecommerce-store/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── ecommerce/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── seed_data.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── login.html
│   ├── register.html
│   └── order_success.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

---

## 🚀 Quick Start Guide

### 1. Open Terminal in the Project Directory
```powershell
cd c:\Users\ganesh\OneDrive\Desktop\ecommerce-store
```

### 2. Activate the Virtual Environment
On Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
*(Or Command Prompt: `.\venv\Scripts\activate.bat`)*

### 3. Run the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Credentials

- **Admin Portal URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛍️ Features Included

1. **Catalog & Filtering**:
   - Categorized browsing with live category badges and counts.
   - Search across product titles and detailed descriptions.
   - Dynamic sorting: Price (Low to High, High to Low), Newest, and Alphabetical.
2. **Product Details**:
   - Image gallery display, pricing, discount percentages, stock indicators, and related product recommendations.
3. **Cart Management**:
   - Real-time cart badge counter available in navbar on every page.
   - Increment, decrement, and item removal controls.
   - Free shipping calculation threshold ($50).
   - Session-persistent guest cart automatically synced into user account upon login.
4. **Checkout & Order Tracking**:
   - Clean 2-column checkout with form validation and order summary review.
   - Instant order confirmation and receipt page with generated Order ID.
5. **Authentication**:
   - User registration and login forms with custom validation.
6. **Django Admin**:
   - Inlined Order Items and Cart Items management.
   - Editable prices, stock, and featured status right from the list view.
7. **Database Seeder**:
   - Pre-populated with 4 categories and 8 curated products with demo images via `python manage.py seed_data`.
8. **Automated Test Suite**:
   - Run tests anytime with `python manage.py test store`.
