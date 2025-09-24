from django.urls import path,include
from . import views

urlpatterns = [
      path('checkout/', views.checkout, name='checkout'),
      path("billing-info/",views.billing_info,name="billing-info"),
      # path("process-order/",views.process_order,name="process-order"),
      path("shipped-orders/",views.shipped_orders,name="shipped-orders"),
      path("unshipped-orders/",views.unshipped_orders,name="unshipped-orders"),
      path("orders/<int:pk>/",views.order_detail,name="orders"),
      path("mark-status/<int:order_id>/",views.mark_shipping_status,name="mark-shipping-status"),
      path("create-checkout-session/",views.create_checkout_session,name="create-checkout-session"),
      path("webhooks/stripe/", views.stripe_webhook, name="stripe-webhook"),
      path("success/",views.checkout_success,name="checkout-success"),
       path("check-status/<int:order_id>/", views.check_order_status, name="check_status"),


]