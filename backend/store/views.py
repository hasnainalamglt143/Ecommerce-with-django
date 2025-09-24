from django.shortcuts import render,redirect
from .models import Product,Category,Order,Customer,Profile
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import CustomUserCreationForm,CustomUserChangeForm,CustomPasswordChangeForm,UserInfoForm
from payment.models import ShippingAddress
from payment.forms import ShippingInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def home(request):
    products=Product.objects.all()
    return render(request, 'home.html',context={"products":products})








def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            login(request, user)
            messages.info(request, "You have successfully logged in.")

            # check if 'next' is in the URL query params
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')  # fallback if no 'next'
        else:
            return render(request, 'login.html', context={"error": "Invalid username or password"})

    return render(request, 'login.html')



def user_logout(request):
    cart=request.session.get('cart', {})  # save cart before logout
    logout(request)
    # request.session['cart'] = cart  # restore cart in new session

    messages.info(request, "You have successfully logged out.")
    return redirect('home')




def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # don't save yet
            user.email = email              # assign email (if form doesn’t handle it)
            user.save()                     # password already hashed by form
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        else:
            return render(request, "register.html", {"form": form})

    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})







@login_required(login_url='login')

def update_user(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("update-user")  # change to your profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "update-user.html", {"form": form})


@login_required(login_url='login')
def update_user_info(request):
    # Get profile safely
    current_user = Profile.objects.filter(user=request.user).first()
    if not current_user:
        messages.error(request, "No such user exists.")
        return redirect("home")  # change to your homepage or dashboard

    # Get or create shipping address
    shipping_user, created = ShippingAddress.objects.get_or_create(customer=request.user)

    # Bind forms
    form = UserInfoForm(request.POST or None, instance=current_user)
    shipping_form = ShippingInfoForm(request.POST or None, instance=shipping_user)

    if request.method == "POST":
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('update-user-info')
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('update-user-info')


    return render(
        request,
        'user-info.html',
        context={"form": form, "shipping_form": shipping_form}
    )   
		



@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change-password")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("change-password")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, "change-password.html", {"form": form})


def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('home')    
    return render(request, 'ProductPage.html', context={"product": product})


def category_products(request, category):
    try:
        category = Category.objects.get(name=category)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('home') 
    products = Product.objects.filter(category=category)
    if len(products )> 0:
        return render(request, 'category_products.html', context={"category": category, "products": products})
    else:
        messages.info(request, "No products found in this category.")
        return redirect('home')
    

def search_products(request):
    searched=""
    if request.method == "POST":
        searched = request.POST.get("searched")
        products = Product.objects.filter(name__icontains=searched) | Product.objects.filter(description__icontains=searched)
        if products.exists():
            return render(request, 'searchProducts.html', context={"products": products, "searched": searched})
        else:
            messages.info(request, "No products matched your search.")
            return redirect('search-products')
    else:
        return render(request, 'searchProducts.html', context={"products": [],"searched":searched})