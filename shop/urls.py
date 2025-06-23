from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about_us_view, name='about_us'),
    path('contact/', views.contact_us_view, name='contact_us'),
    path('vendor-info/', views.vendor_info, name='vendor_info'),
    path('buyer_info/', views.buyer_info, name='buyer_info'),
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('buyer/', views.buyer, name='buyer'),
    path('vendor/', views.vendor, name='vendor'),
    path('vendor/products/', views.vendor_products, name='vendor_products'),
    path('logout/', views.logout_view, name='logout_view'),
    path('add_product/', views.add_product, name='add_product'),
    path('search/', views.search, name='search'),
    path('products/', views.products, name='products'),
    path('single_product/<int:pk>', views.single_product, name='single_product'),
    path('seller-landing/', views.seller_landing_page, name='seller_landing_page'),
    path('admin_view_single_product/<int:pk>', views.admin_view_single_product, name='admin_view_single_product'),
    
    path('vendor_view_single_product/<int:pk>', views.vendor_view_single_product, name='vendor_view_single_product'),

    path('admin_view_products/', views.admin_view_products, name='admin_view_products'),

    path('admin_count/', views.admin_count, name='admin_count'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'), 
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_failed/', views.payment_failed, name='payment_failed'), # Add this line
    path('buyer_view_orders/', views.buyer_view_orders, name='buyer_view_orders'),
    path('profile/', views.profile, name='profile'),
    path('vendor_view_orders/', views.vendor_view_orders, name='vendor_view_orders'),
    path('view_order_details/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('admin_view_orders/', views.admin_view_orders, name='admin_view_orders'),
    path('admin_order_details/<int:order_id>/', views.admin_order_details, name='admin_order_details'),






   #  path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
   # path('checkout_process/', views.checkout_process, name='checkout_process'),
]






    
