from django.shortcuts import render,get_object_or_404,redirect
from cart.cart import Cart
# Create your views here.
from .forms import ShippingInfoForm,PaymentForm
from .models import ShippingAddress,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.http.response import JsonResponse,HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    totals = cart.get_totals()

    shipping_user = None
    shipping_form = None

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(customer__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            # Create a blank shipping record if not found
            shipping_user = ShippingAddress(customer=request.user)
            shipping_user.save()
            messages.info(request, "Please complete your shipping details.")

        shipping_form = ShippingInfoForm(request.POST or None, instance=shipping_user)
    else:
        # Guest checkout
        shipping_form = ShippingInfoForm(request.POST or None)

    return render(
        request,
        "payment/checkout.html",
        {
            "cart_products": cart_products,
            "total_amount": totals,
            "shipping_form": shipping_form,
        },
    )



@login_required
def billing_info(request):
    cart=Cart(request)
    if request.method=="POST":
         shipping_user = ShippingAddress.objects.get(customer__id=request.user.id)
		# Shipping Form
         shipping_user = ShippingAddress.objects.get(customer__id=request.user.id)
         shipping_form = ShippingInfoForm(request.POST or None, instance=shipping_user)
         payment_form=PaymentForm()
         if not shipping_form.is_valid():
             messages.error(request,"correct errors below")
             return render(request,"payment/checkout.html",context={"shipping_form":shipping_form,"cart_products":cart.get_prods()} )
         request.session['shipping_info']=json.dumps(request.POST)
         return render(request,"payment/billing_info.html",context={"shipping_info":request.POST," shipping_form ": shipping_form ,"total_amount":cart.get_totals(),"cart_products":cart.get_prods(),"payment_form":payment_form})  
    else:
        messages.error(request,"access denied")
        return redirect("home")




def shipped_orders(request):
     if request.user.is_authenticated and request.user.is_superuser:
           orders=Order.objects.filter(shipped=True).all()
           return render(request,"payment/shipped_orders.html",context={"shipped_orders":orders})
     else:
        messages.error(request, "Access denied")
        return redirect("home")
     


def unshipped_orders(request):
     if request.user.is_authenticated and request.user.is_superuser:
           orders=Order.objects.filter(shipped=False).all()
           return render(request,"payment/unshipped_orders.html",context={"unshipped_orders":orders})
     else:
        messages.error(request, "Access denied")
        return redirect("home")




# views.py


def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('orderitem_set__product'),
        pk=pk
    )
    items = order.orderitem_set.all()
   
    subtotal = sum(item.quantity * item.price for item in items)
    context = {
        "order": order,
        "items": items,
        "subtotal": subtotal,
    }
    return render(request, "payment/order_card.html", context)


import datetime

def mark_shipping_status(request,order_id):
     if request.method=="POST" and request.user.is_superuser:
          status=request.POST.get("status")
          print(status)
          order=Order.objects.get(id=order_id)
          if status=="False":
               order.shipped=True
               order.date_ordered=datetime.datetime.now()
               order.save()
               messages.success(request,"shipping status changed to 'shipped' successfully")
               return redirect("unshipped-orders")
          
          elif status=="True":
               order.shipped=False
               order.date_ordered=datetime.datetime.now()
               order.save()
               messages.success(request,"shipped status changed to 'unshipped' successfully")
               return redirect("shipped-orders")
          else:
               pass
               
     messages.error(request,"Access denied")
     return redirect("home")





stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        # cart data
        cart = Cart(request)
        cart_items = cart.get_prods()
        if not cart_items:
            # print("empty cart")
            return render(request,"cart/cart_summary.html",context={"cart_products":cart_items})

        # shipping info from session
        my_shipping = json.loads(request.session.get("shipping_info", "{}"))
        address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping.get('shipping_address2','')}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_postal_code']}\n"
            f"{my_shipping['shipping_country']}"
        )
        email = my_shipping["shipping_email"]
        user = request.user
        amount_paid = cart.get_totals()
        order = Order.objects.create(
            user=user,
            email=email,
            amount_paid=amount_paid,
            shipping_address=address,
            paid=False,
        )
        for item in cart_items:
            product = item["product"]
            quantity = item["quantity"]
            price = product.sale_price if getattr(product, "sale_price", None) else product.price
            OrderItem.objects.create(
                order=order,
                user=user,
                product=product,
                quantity=quantity,
                price=price,
            )

        # prepare Stripe line items
        line_items = []
        for item in cart_items:
            product = item["product"]
            quantity = item["quantity"]
            price = product.sale_price if getattr(product, "sale_price", None) else product.price
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price) * 100,  # cents
                    "product_data": {"name": str(product.name)},
                },
                "quantity": quantity,
            })

        # ✅ Create Stripe Checkout Session
        try:
            session = stripe.checkout.Session.create(
                ui_mode="embedded",
                line_items=line_items,
                mode="payment",
                return_url=f"http://{request.get_host()}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
            )
            request.session["order_id"]=order.id
        except stripe.error.CardError as e:
            # Card declined, expired, etc.
            return render(request, "payment/error.html", {
                "error_message": f"Card error: {e.user_message}"
            })

        except stripe.error.RateLimitError:
            return render(request, "payment/error.html", {
                "error_message": "Too many requests made to Stripe. Please try again."
            })

        except stripe.error.InvalidRequestError as e:
            return render(request, "payment/error.html", {
                "error_message": f"Invalid request: {e.user_message}"
            })

        except stripe.error.AuthenticationError:
            return render(request, "payment/error.html", {
                "error_message": "Authentication with Stripe failed. Please contact support."
            })

        except stripe.error.APIConnectionError:
            return render(request, "payment/error.html", {
                "error_message": "Network communication with Stripe failed."
            })

        except stripe.error.StripeError:
            return render(request, "payment/error.html", {
                "error_message": "Something went wrong with payment processing. Please try again later."
            })

        except Exception as e:
            return render(request, "payments/error.html", {
                "error_message": f"Unexpected error: {str(e)}"
            })

        order.stripe_session_id = session["id"]
        order.save()
        return JsonResponse({"clientSecret": session.client_secret})

    return redirect("home")




# 🔹 Stripe webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        session = data
        try:
            order = Order.objects.get(stripe_session_id=session["id"])
            order.paid = True
            order.amount_paid = session.get("amount_total", 0) / 100  # cents → dollars
            order.save()
        except Order.DoesNotExist:
             print("⚠️ No matching order found for session:", session["id"])
             return render(request, "payment/error.html", {
            "error_message": "We couldn’t find your order. Please contact support."})

    return HttpResponse(status=200)



def checkout_success(request):
    """Render success page with loader"""
    order_id=request.session["order_id"]
    try:
        order = get_object_or_404(
        Order.objects.prefetch_related('orderitem_set__product'),
        pk=int(order_id)
    )
        items = order.orderitem_set.all()
   
        subtotal = sum(item.quantity * item.price for item in items)
        context = {
        "order": order,
        "items": items,
        "subtotal": subtotal,
    }
        return render(request, "payment/payment_success.html", context)

    except:
        messages.error(request,"could not process payment.contact to support service")
        return redirect("home")


@csrf_exempt
def check_order_status(request, order_id):
    """AJAX endpoint for polling"""
    if request.method=="POST":
        order = get_object_or_404(Order, id=order_id)
        cart=Cart(request)
        if order.paid:
            cart.clear_cart()
        return JsonResponse({"paid": order.paid})
    messages.error(request,"request not allowed")
    return redirect("home")
