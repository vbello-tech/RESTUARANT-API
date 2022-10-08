from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,  include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"product", FoodViewSet, basename="tweetslist")

urlpatterns = [
    path("", include(router.urls)),
    path('', HomeView.as_view(), name="api_home"),
    path('food/<int:pk>/', getproduct, name='product'),
    path('food/add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('food/remove-from-cart/<int:pk>/', remove_from_cart, name="remove_from_cart"),
    path('food/remove-single-item-from-cart/<int:pk>/', remove_from_cart_item, name="remove_from_cart_item"),
    path('food/order_summary/', order_summaryView.as_view(), name="order_summary"),
    path('food/checkout/', CheckOutView.as_view(), name="checkout"),
]