from store.models import Product, Profile
import json

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.request = request

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # stored as string for JSON
            }
        self.cart[product_id]['quantity'] = int(quantity)

        # Mark session dirty so Django saves it
        self.session.modified = True

        # Persist to DB if logged in
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                profile.old_cart = json.dumps(self.cart)
                profile.save()
            except Profile.DoesNotExist:
                pass

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

            # Update DB too (keep it consistent)
            if self.request.user.is_authenticated:
                try:
                    profile = Profile.objects.get(user=self.request.user)
                    profile.old_cart = json.dumps(self.cart)
                    profile.save()
                except Profile.DoesNotExist:
                    pass

    def get_prods(self):
        # If user has an old_cart saved in DB, load it into session
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                if profile.old_cart:
                    self.cart = json.loads(profile.old_cart)
                    self.session['cart'] = self.cart  # sync session
            except Profile.DoesNotExist:
                pass

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart_items = []
        for product in products:
            cart_items.append({
                "product": product,
                "quantity": self.cart[str(product.id)]["quantity"],
            })
        return cart_items

    def __len__(self):
        """Return number of items in cart (sum of quantities)."""
        self.get_prods()
        return len(self.cart)

    def get_totals(self):
        total_price = 0
        for item in self.get_prods():
            product = item["product"]
            quantity = int(item["quantity"])
            price = product.sale_price if product.sale_price else product.price
            total_price += price * quantity
        return total_price
    
    def clear_cart(self):
        # Clear from session
        self.session['cart'] = {}
        self.cart = {}
        self.session.modified = True

        # Clear from DB if logged in
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user__id=self.request.user.id)
                profile.old_cart = json.dumps({})
                profile.save()
            except Profile.DoesNotExist:
                pass