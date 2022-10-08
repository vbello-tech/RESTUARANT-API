from django.shortcuts import *
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import HttpResponse
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import *
# Create your views here.


# HOME PAGE VIEW
class HomeView(APIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        user = request.user
        qs = Food.objects.all()
        serializer = FoodSerializer(qs, many=True)
        return Response(serializer.data)


class FoodViewSet(viewsets.ModelViewSet):
    queryset =Food.objects.all()
    serializer_class =FoodSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



@api_view(['GET'])
def getproduct(request, pk):
    product = Food.objects.get(pk=pk)
    indserializer = FoodSerializer(product, many=False)
    return Response(indserializer.data)


# FUNCTION TO ADD ITEM TO CART
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_to_cart(request, pk):
    # ORDER ITEM TO BE ADDED TO CART
    food = get_object_or_404(Food, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        food=food,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # IF STATEMENT TO CHECK IF ORDER ITEM EXIST IN CART
    if order_qs.exists():
        order = order_qs[0]
        # IF STATEMENT TO INCREASE THE ORDER ITEM QUANTITY BY 1 IF THE USER ALREADY HAS THE food ITEM IN CART
        if order.foods.filter(food__pk=food.pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.foods.add(order_item)
            return Response({
                'cart_status': 'updated in cart'
            })
    else:
        # CREATE AN ORDER ITEM OF FOOD IF IT DOES NOT EXIST IN USER CART
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.foods.add(order_item)
    return Response ({
        'cart_status': 'added to cart'
    })



# REMOVE FROM CART FUNCTIONS
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remove_from_cart(request, pk):
    # ORDER ITEM TO REMOVE FROM CART
    food = get_object_or_404(Food, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    # CHECK IF ORDER ITEM EXIST IN CART ITEMS OF USER
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.foods.filter(food__pk=food.pk).exists():
            order_item = OrderItem.objects.filter(
                food=food,
                user=request.user,
                ordered=False
            )[0]
            # REMOVE FROM CART
            order.foods.remove(order_item)
            order_item.delete()
            return Response({
                'cart_status': 'removed from cart'
            })
        else:
            return Response({
                'cart_status': 'object does not exist in your cart'
            })
    else:
        return Response({
            'cart_status': 'object does not exist in your cart'
        })


# FUNCTION TO REMOVE SINGLE ITEM FROM CART
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remove_from_cart_item(request, pk):
    # CHECK IF ORDERED ITEM EXIST IN CART
    food = get_object_or_404(Food, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is in the order
        if order.foods.filter(food__pk=food.pk).exists():
            order_item = OrderItem.objects.filter(
                food=food,
                user=request.user,
                ordered=False
            )[0]
            # REDUCE QUANTITY OF ORDER ITEM BY 1
            if order_item.quantity <=0:
                return Response({
                    'cart_status': 'object does not exist in your cart'
                })
            else:
                order_item.quantity -= 1
                order_item.save()
                return Response({
                    'cart_status': 'object quantity was reduced in your cart'
                })
        else:
            return Response({
                'cart_status': 'object quantity was reduced in your cart'
            })
    else:
        return Response({
            'cart_status': 'object does not exist in your cart'
        })


# VIEW TO DISPLAY ALL AVAILABLE ORDER ITEM THAT THE ORDERED STATUS IS FALSE
class order_summaryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({
                'cart_status': 'YOU HAVE NO ORDER IN CART'
            })


class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.get(user=request.user, ordered=False)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        address = data.get('address')
        order = Order.objects.get(user=request.user, ordered=False)
        order.billing_address = address  # billing_address
        order.ordered = True
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=HTTP_201_CREATED)


