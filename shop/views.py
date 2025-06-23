from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, VendorInfoForm, BuyerInfoForm, ProductForm
from django.contrib.auth.decorators import login_required
from .models import User, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from shop.models import User
from .models import VendorInfo, BuyerInfo, User, Order, OrderItem, Cart
from django.shortcuts import render, redirect
from shop.models import Product



def admin_count(request):
    buyers_count = BuyerInfo.objects.count()
    sellers_count = VendorInfo.objects.count()
    all_products = Product.objects.all()

    context = {
        'user': request.user,
        'buyers_count': buyers_count,
        'sellers_count': sellers_count,
        'all_products': all_products,
    }

    return render(request, 'admin_view_buyers.html', context)


def home(request):
    # Add any logic here if needed
    return render(request, 'home.html')  # Replace 'your_app/home.html' with your actual template path


def about_us_view(request):
    return render(request, 'about_us.html')

def contact_us_view(request):
    # Your view logic goes here
    return render(request, 'contact_us.html')


@login_required
def vendor_products(request):
    # Check if the user is a vendor
    if request.user.is_vendor:
        # Filter products based on the logged-in vendor's ID
        vendor_products = Product.objects.filter(vendor=request.user.vendorinfo)
        return render(request, 'vendor_products.html', {'vendor_products': vendor_products})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})



def products(request):
    all_products = Product.objects.all()
    available_brands = Product.objects.values_list('brand', flat=True).distinct()
    available_categories = Product.objects.values_list('category', flat=True).distinct()

    if 'brand' in request.GET:
        selected_brand = request.GET['brand']
        if selected_brand != 'all':
            products = all_products.filter(brand=selected_brand)
        else:
            products = all_products
    elif 'category' in request.GET:
        selected_category = request.GET['category']
        if selected_category != 'all':
            products = all_products.filter(category=selected_category)
        else:
            products = all_products
    else:
        products = all_products

    context = {
        'products': products,
        'available_brands': available_brands,
        'available_categories': available_categories,
    }
    return render(request, 'products.html', context)
def admin_view_products(request):
    products = Product.objects.all()
    return render(request, 'admin_view_products.html', {'products': products})

def single_product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'single_product.html', {'product':product})

def admin_view_single_product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'admin_view_single_product.html', {'product':product})

def vendor_view_single_product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'vendor_view_single_product.html', {'product':product})

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(brand__icontains=searched) | Q(description__icontains=searched)| Q(category__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist !!")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})

@login_required
def admin(request):
    # Fetch all buyers, sellers, and their products
    buyers = User.objects.filter(is_buyer=True)
    sellers = User.objects.filter(is_vendor=True)
    all_products = Product.objects.all()

    return render(request, 'admin.html', {'user': request.user, 'buyers': buyers, 'sellers': sellers, 'all_products': all_products})

def vendor(request):
    return render(request,'vendor.html')

def index(request):
    return render(request, 'base.html')

def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Get the user object without saving to DB yet
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user.save()  # Now save the user to DB
            # Assign the selected role to the user based on the form data
            role = form.cleaned_data['role']

            '''
            if role == 'admin':
                user.is_admin = True
                user.is_buyer = False
                user.is_vendor = False
                '''
            if role == 'buyer':
                user.is_buyer = True
                user.is_vendor = False
            elif role == 'vendor':
                user.is_buyer = False
                user.is_vendor = True
            user.save()  # Save the user again to update the role fields

            # Log in the user
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Redirect users based on their roles
            '''
            if user.is_admin:
                return redirect('adminpage')
                '''
            if user.is_buyer:
                return redirect('login_view')
            elif user.is_vendor:
                return redirect('vendor_info')
            else:
                return redirect('register')  # Redirect to update info page if role is not specified
            
        else:
            messages.error(request, "Whoops! There was a problem registering, please try again...")
            return redirect('register')
    
    return render(request, 'register.html', {'form': form})



def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_buyer:
                login(request, user)

                return redirect('home')
            elif user is not None and user.is_vendor:
                login(request, user)
                return redirect('vendor')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    
    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
def add_product(request):
    if request.user.is_vendor:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.vendor = request.user.vendorinfo  # Assign the vendor using the User's VendorInfo instance
                product.save()
                return redirect('vendor')  # Redirect to vendor dashboard or product list page
        else:
            form = ProductForm()
        return render(request, 'add_product.html', {'form': form})
    else:
        return redirect('login')  # Redirect non-vendors to login page

def vendor_info(request):
    if request.user.is_vendor:
        if request.method == 'POST':
            form = VendorInfoForm(request.POST)
            if form.is_valid():
                vendor_info = form.save(commit=False)
                vendor_info.user = request.user  # Assign the user to the vendor info
                vendor_info.save()
                return redirect('vendor')  # Redirect to vendor dashboard or product list page
        else:
            form = VendorInfoForm()
        return render(request, 'vendor_info.html', {'form': form})
    else:
        return redirect('login')

def buyer_info(request):
    if request.user.is_buyer:
        if request.method == 'POST':
            form = BuyerInfoForm(request.POST)
            if form.is_valid():
                buyer_info = form.save(commit=False)
                buyer_info.user = request.user  # Assign the user to the vendor info
                buyer_info.save()
                return redirect('home')  # Redirect to vendor dashboard or product list page
        else:
            form = BuyerInfoForm()
        return render(request, 'buyer_info.html', {'form': form})
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    return render(request, 'home.html')


def buyer(request):
    return render(request, 'home.html')

def seller_landing_page(request):
    return render(request, 'seller_landing_page.html')


from django.shortcuts import render
from .models import Cart

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    # Calculate cart count
    cart_count = len(cart_items)
    if request.method == 'POST':
        # Handle POST request to update quantities
        for item in cart_items:
            new_quantity = int(request.POST.get(f'quantity_{item.id}', 0))
            if new_quantity >= 0:
                item.quantity = new_quantity
                item.save()
        
        # Recalculate total price after updating quantities
        total_price = sum(item.total_price() for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully.")
    return redirect('view_cart')
 
def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def update_cart_quantity(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    new_quantity = int(request.POST.get('quantity'))
    cart_item.quantity = new_quantity
    cart_item.save()
    messages.success(request, "Cart quantity updated successfully.")
    return redirect('view_cart')


from django.shortcuts import render, redirect
from .models import Cart, Order
import uuid  # for generating unique invoice numbers

from django.contrib import messages

def cart_checkout(request):
    print(request.method)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        print(city)
        user_id = request.user.id
        unique_invoice_number = str(uuid.uuid4()).replace("-", "")[:20]

        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        print(total_price)

        order = Order.objects.create(
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            user_id=user_id,
            total_price=total_price,
            invoice_number=unique_invoice_number,
        )

        # Clear the user's cart after checkout
       # cart_items.delete()

        # Display success message
        messages.success(request, "Details captured. Proceed to make payment..")

        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart_checkout.html', {'cart_items': cart_items, 'total_price': total_price})
  # Render the shipping form template

    return render(request, 'cart_checkout.html')  # Render the shipping form template for GET requests



def address_info(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        user_id = request.user.id

        # Fetch cart items associated with the current user
        cart_items = Cart.objects.filter(user=request.user)

        # Calculate total product amount
        total_product_amount = sum(cart_item.total_price() for cart_item in cart_items)
        
        shipping_fee = 109  # Sample shipping fee
        total_payment_amount = total_product_amount + shipping_fee

        # Generate a unique invoice number for the new order
        unique_invoice_number = str(uuid.uuid4()).replace("-", "")[:20]

        
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            address=address,
            user_id=user_id,
            total_price=total_payment_amount,
            invoice_number=unique_invoice_number,
        )

        # Save order items
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.product_price
            )

    

        # Redirect to a success page or any other page after saving the order
        return redirect('checkout')

    return render(request, 'address_info.html')



import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from forex_python.converter import CurrencyRates
from django.http import  HttpResponse
from decimal import Decimal


paypalrestsdk.configure({
    "mode": "sandbox",  
    "client_id": "AeT4nG2IixImV-Zjg6ME2uXZDNL61shC6jjA1JP2Rlty7pJxeSNldvNA8C0QCC34Yr5_IJpt1g-S-OnW",
    "client_secret": "EBJ8sqhq3OCgjKpe5x5gds7k4HTnras7hBQ0GmfKgkaydl7I_eBXT3MgjnNzCydigyhcbgCcDAT_QhXK",
})

def create_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_product_amount = sum(cart_item.total_price() for cart_item in cart_items)
    
    total_product_amount_decimal = Decimal(total_product_amount)
    
    shipping_fee = 207  # Sample shipping fee
    total_payment_amount = total_product_amount_decimal + shipping_fee
    
    currency_rates = CurrencyRates()
    exchange_rate = currency_rates.get_rate('KES', 'USD')

    exchange_rate = Decimal(exchange_rate)
    print("exchange_rate:", exchange_rate)
    

    # Convert total_payment_amount to Decimal
    total_payment_amount_decimal = Decimal(total_payment_amount)
    print("total_payment_amount_decimal:", total_payment_amount_decimal)


    total_payment_amount_usd = total_payment_amount_decimal * exchange_rate
    print("total_payment_amount_usd:", total_payment_amount_usd)
    
    total_payment_amount_usd_formatted = '{:.2f}'.format(total_payment_amount_usd)
    print(total_payment_amount_usd_formatted)  # Output: 786.01

    # Using the round function
    total_payment_amount_usd_rounded = round(total_payment_amount_usd, 2)
    print(total_payment_amount_usd_rounded)



    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": str(total_payment_amount_usd_rounded),  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    
from django.db import transaction

from django.db import transaction

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
    except paypalrestsdk.exceptions.ResourceNotFound as e:
        return HttpResponse("Payment not found", status=404)

    if payment.state == 'approved':
        print("approved")
        # You may add further processing or redirect here if needed

    elif payment.execute({"payer_id": payer_id}):
        # Payment executed successfully
        transID = payment.transactions[0].related_resources[0].sale.id
        print(transID)
        cart_items = Cart.objects.filter(user=request.user)
                
        print("Cart items before processing:", cart_items)
        try:

            with transaction.atomic():
                cart_items = Cart.objects.filter(user=request.user)
                
                print("Cart items before processing:", cart_items)

                if cart_items is not None:
                    latest_order = Order.objects.filter(user=request.user, paid=False).order_by('-created_at').first()
                    print('latest order:',latest_order)
                    if latest_order is None:
                        latest_order = Order.objects.create(user=request.user, order_status='Processing', paid=False)

                    latest_order.order_status = 'Processing'
                    latest_order.paid=True
                    latest_order.save()

                    # Initialize subtotal
                    subtotal = Decimal('0')

                    for cart_item in cart_items:
                        print(f"Cart item ID: {cart_item.id}, User: {cart_item.user}, Product: {cart_item.product}, Quantity: {cart_item.quantity}")
                        print(f"Cart item quantity before processing: {cart_item.quantity}")

                        order_item, created = OrderItem.objects.get_or_create(
                            
                            order=latest_order,
                            product=cart_item.product,
                            defaults={'quantity': cart_item.quantity, 'price': cart_item.product.price}
                            
                            
                        )
                        print(f"Order item created: {order_item}, Created: {created}")

                        # Update product quantity
                        cart_item.product.product_remaining = max(cart_item.product.quantity - cart_item.quantity, 0)
                        print("updated_quantity:", cart_item.product.product_remaining)
                        cart_item.product.quantity=cart_item.product.product_remaining 
                        cart_item.product.save()

                    # Clear the cart items after creating the order items
                    cart_items.delete()

                    # Filter orders based on the current user
                    current_user = request.user
                    current_order = Order.objects.filter(user=current_user).order_by('-created_at').first()
                    print(current_order)

                    # Check if there is a current order for the user
                    if current_order:
                        # Retrieve ordered products associated with the order
                        ordered_products = OrderItem.objects.filter(order=current_order)

                        # Initialize a set to store unique product names
                        unique_product_names = set()

                        # Initialize an empty list to store product data
                        product_data = []

                        # Initialize subtotal
                        subtotal = Decimal('0')
                        product_subtotal = Decimal('0') 

                        # Calculate subtotal considering quantities and collect unique product data
                        for item in ordered_products:
                            # Check if the product name is unique
                            if item.product.brand not in unique_product_names:
                                # Add the product name to the set of unique product names
                                unique_product_names.add(item.product.brand)
                                
                                # Calculate the subtotal for the current product
                                product_subtotal = item.price * item.quantity  # Calculate subtotal for the current item
                                subtotal += product_subtotal  # Add subtotal for the current item to the overall subtotal
                                
                                
                                # Append the product data to the list
                                product_data.append({
                                    'product_name': item.product.brand,
                                    'quantity': item.quantity,
                                    'product_subtotal': product_subtotal,
                                    'subtotal': subtotal,
                                })

                        # Render the payment success template with necessary data
                        order_items = current_order.items.all()
                        return render(request, 'payment_success.html', {'order': current_order, 'product_data': product_data, 'subtotal': subtotal, 'transID': transID, 'product_subtotal': product_subtotal,})
                    else:
                        error_message = "There is no current order for this user."
                        return render(request, 'error.html', {'error_message': error_message})
                
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
    
    # Handle payment failure or non-approved state
    return render(request, 'payment_failed.html')






def payment_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)  

    total_product_amount = sum(cart_item.total_price() for cart_item in cart_items)
    
    shipping_fee = 179  # Sample shipping fee
    total_payment_amount = total_product_amount + shipping_fee
    
    context = {
        'cart_items': cart_items,
        'total_product_amount': total_product_amount,
        'shipping_fee': shipping_fee,
        'total_payment_amount': total_payment_amount,
    }
    return render(request, 'check.html', context)

def payment_failed(request):
    return render(request, 'payment_failed.html')



from .models import Order

def buyer_view_orders(request):
    # Fetch orders for the current logged-in user (buyer)
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders
    }
    return render(request, 'buyer_view_orders.html', context)

def profile(request):
    # Assuming the logged-in user's information is stored in the User model
    user_info = User.objects.get(id=request.user.id)
    context = {'user_info': user_info}
    return render(request, 'profile.html', context)

def vendor_view_orders(request):
    # Get orders related to the current logged-in vendor's products
    vendor_orders = Order.objects.filter(product__vendor__user=request.user, order_status='Processing')
    
    context = {'vendor_orders': vendor_orders}
    return render(request, 'vendor_view_orders.html', context)


def vendor_view_orders(request):
    # Get the current logged-in vendor
    vendor = VendorInfo.objects.get(user=request.user)

    # Get orders for the vendor's products
    vendor_orders = Order.objects.filter(products__vendor=vendor)

    context = {'vendor_orders': vendor_orders}
    return render(request, 'vendor_view_orders.html', context)


from .models import Order, OrderItem

def view_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_details.html', context)


def admin_view_orders(request):
    processing_orders = Order.objects.filter(order_status='Processing')
    context = {'orders': processing_orders}
    return render(request, 'admin_view_orders.html', context)

def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    context = {'order': order, 'order_items': order_items}
    return render(request, 'admin_order_details.html', context)