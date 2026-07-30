# Django E-commerce Website

This is a basic Django e-commerce website with buyer and seller features. It includes user authentication, product management for sellers, cart and checkout flows, order tracking, and a contact page.

## Project Overview

- Built with Django
- Multi-app structure:
  - `home` app: products, seller profiles, cart, orders, contact form
  - `system` app: user signup, login, logout, password pages
- Templates are stored in the `template/` folder
- Static assets are stored under `static1/`
- Uses SQLite database (`db.sqlite3`)

## Key Features

- Buyer registration and login
- Seller registration and seller dashboard
- Add products with name, description, price, and image URL
- Add products to cart and manage cart items
- Checkout and create orders
- Buyers can view their orders and track order status
- Sellers can view their orders and update status
- Contact form for user messages
- Basic informational pages: Home, About, Services

## Project Structure

- `manage.py` - Django command-line utility
- `home/` - Main e-commerce app models, views, URLs
- `system/` - Authentication app and login/signup views
- `template/` - HTML templates for pages
- `static1/` - Static files directory
- `db.sqlite3` - SQLite database file

## URLs and Pages

### Authentication (`system` app)
- `/` → Login page
- `/signup/` → Signup page
- `/home/` → User home page after login
- `/logout/` → Logout
- `/forget/` → Forgot password page
- `/change/` → Change password page

### E-commerce pages (`home` app)
- `/` → Product listing / home page
- `/about` → About page
- `/services` → Services page
- `/contact` → Contact form
- `/seller/register/` → Seller registration
- `/seller/dashboard/` → Seller dashboard
- `/seller/products/add/` → Add new product
- `/cart/` → View cart
- `/cart/add/<product_id>/` → Add product to cart
- `/cart/remove/<item_id>/` → Remove item from cart
- `/checkout/` → Checkout page
- `/orders/` → Buyer orders page
- `/orders/<order_id>/` → Order tracking
- `/seller/orders/<order_id>/<status>/` → Update order status by seller

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

2. Install Django (use a compatible version, e.g. Django 5.x or Django 3.2.x):
   ```bash
   pip install django
   ```

3. Install any additional dependencies if required.

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open the app in your browser at:
   ```
   http://127.0.0.1:8000/
   ```

## Notes

- `manage.py` references `mysite.settings`, so the Django project settings module should be present and correctly configured.
- The project currently uses SQLite via `db.sqlite3`.
- If a `requirements.txt` file is not available, install Django manually and add any extra packages you need.

## Recommended Improvements

- Add password reset handling and email support
- Use Django forms for validation and cleaner form handling
- Add media support for product images instead of image URLs
- Add user roles and permission checks for sellers and buyers
- Improve UI by organizing static files and using Bootstrap or Tailwind

---

## Hindi Summary

यह Django प्रोजेक्ट एक बेसिक ई-कॉमर्स वेबसाइट है जिसमें खरीदार और विक्रेता दोनों के लिए सुविधाएँ हैं। इसमें यूजर लॉगिन, उत्पाद प्रबंधन, शॉपिंग कार्ट, चेकआउट, और ऑर्डर ट्रैकिंग शामिल है।