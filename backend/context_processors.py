from store.models import Category
from cart.cart import Cart


def categories_processor(request):
    """
    Adds all categories to the template context globally.
    """
    return {
        "categories": Category.objects.all()
    }


def cart_processor(request):
    """
    Adds the cart instance to the template context globally.
    """
    return {
        "cart": Cart(request)
    }