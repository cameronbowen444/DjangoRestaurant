from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('menu', views.menu),

    path('cart', views.cart),
    path('cart/add/<int:item_id>', views.add_to_cart),
    path('cart/increase/<int:item_id>', views.increase_quantity),
    path('cart/decrease/<int:item_id>', views.decrease_quantity),
    path('cart/remove/<int:item_id>', views.remove_from_cart),

    path('checkout', views.checkout),
    path('post-checkout', views.post_checkout),

    path('login', views.login),
    path('login-post', views.post_login),
    path('register', views.register),
    path('logout', views.logout),
]