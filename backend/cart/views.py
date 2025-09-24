from django.shortcuts import render
from django.http import JsonResponse
from store.models import Product
from django.shortcuts import get_object_or_404, redirect
from .cart import Cart
import json
from django.contrib import messages





def cart_summary(request):
    cart_products = Cart(request).get_prods()
    return render(request, 'cart/cart_summary.html',context={"cart_products":cart_products})

def cart_add(request):
    cart=Cart(request)
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({"message": "Product added", "product": product_id,"product_name":product.name, "quantity": quantity, "ok": True,"cart_quantity": cart.__len__()})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from store.models import Product
from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart_summary.html", {
        "cart_products": cart.get_prods(),
        "total_amount":cart.get_totals(),
    })


def cart_remove(request):
    cart = Cart(request)
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        product = get_object_or_404(Product, id=int(product_id))
        cart.delete(product)
        messages.success(request, f"Removed '{product.name}' from cart.")
        return JsonResponse({"ok": True, "cart_quantity": len(cart), "total_amount": cart.get_totals()})
    
    return JsonResponse({"ok": False}, status=400)


def cart_update(request):
    cart=Cart(request)
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({ "product": product_id,"product_name":product.name, "quantity": quantity, "ok": True,"cart_quantity": cart.__len__(),"total_amount":cart.get_totals()})


    return render(request, 'cart/cart_summary.html')
