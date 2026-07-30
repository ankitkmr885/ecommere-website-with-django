from django.test import TestCase
from django.contrib.auth.models import User
from home.models import CartItem, SellerProfile, Product


class EcommerceFlowTests(TestCase):
    def test_seller_registration_creates_profile(self):
        response = self.client.post(
            "/seller/register/",
            {
                "username": "seller1",
                "email": "seller1@example.com",
                "password": "password123",
                "shop_name": "Fresh Market",
                "phone": "9876543210",
                "address": "Delhi",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="seller1").exists())
        self.assertTrue(SellerProfile.objects.filter(user__username="seller1").exists())

    def test_home_page_shows_active_products(self):
        seller_user = User.objects.create_user(username="seller2", password="password123")
        seller_profile = SellerProfile.objects.create(user=seller_user, shop_name="Shop 2")
        Product.objects.create(seller=seller_profile, name="Apples", price="100.00", active=True)
        Product.objects.create(seller=seller_profile, name="Hidden", price="50.00", active=False)

        response = self.client.get("/")

        self.assertContains(response, "Apples")
        self.assertNotContains(response, "Hidden")

    def test_login_redirects_to_home_and_merges_guest_cart(self):
        user = User.objects.create_user(username="customer", password="password123")
        seller_user = User.objects.create_user(username="seller3", password="password123")
        seller_profile = SellerProfile.objects.create(user=seller_user, shop_name="Shop 3")
        product = Product.objects.create(seller=seller_profile, name="Bananas", price="80.00", active=True)

        session = self.client.session
        session["cart"] = {str(product.id): 2}
        session.save()

        response = self.client.post("/login/", {"loginusername": "customer", "loginpassword": "password123"})

        self.assertRedirects(response, "/")
        self.assertEqual(CartItem.objects.filter(user=user).count(), 1)
        self.assertEqual(CartItem.objects.get(user=user, product=product).quantity, 2)

    def test_home_page_renders_product_image_when_url_is_provided(self):
        seller_user = User.objects.create_user(username="seller4", password="password123")
        seller_profile = SellerProfile.objects.create(user=seller_user, shop_name="Shop 4")
        Product.objects.create(
            seller=seller_profile,
            name="Mangoes",
            price="120.00",
            active=True,
            image="https://example.com/mango.jpg",
        )

        response = self.client.get("/")

        self.assertContains(response, 'src="https://example.com/mango.jpg"')
