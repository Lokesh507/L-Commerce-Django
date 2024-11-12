from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product, Order, OrderItem, ShippingAddress 
from base.serializers import ProductSerializer, OrderSerializer 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from datetime import datetime
import razorpay

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request) :
    user = request.user
    data = request.data
    
    orderItems = data['orderItems']
    if orderItems and len(orderItems)==0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        #(1) create order
        order = Order.objects.create(
            user = user,
            paymentMethod= data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice']
        )
        #(2) create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalcode'],
            country = data['shippingAddress']['country']
        )
        #(3) create order items and set order to orderItem model 
        for i in orderItems:
            product = Product.objects.get(_id = i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name, 
                qty = i['qty'],
                price = i['price'], 
                image = product.image.url
            )
            #(4) update product stock after order. i.e. countInStock in product model
            product.countInStock -= int(item.qty)
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view([ 'GET' ])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view([ 'GET'])
@permission_classes ([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id = pk)
        if user.is_staff or order.user==user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({ 'detail': 'Not Authorized to view this order'}, status-status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exists'}, status-status.HTTP_400_BAD_REQUEST)


@api_view([ 'PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id = pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response("Order was paid")



@api_view (['POST'])
def razorPayOrder(request, pk):
    data = request.data
    
    client = razorpay.Client(auth=("rzp_test_oUXbADIa65AnUy", "syUxdDv5PBOiQTP8E5ARGJJq"))
    DATA = {
    "amount": int(data['amount']),
    "currency" : "INR",
    "receipt": f"receipt#{data['order_id']}",
    }
    res = client.order.create(data=DATA)
    if(res):
        payment_status_msg ={
        'bool': True,
        'data': res
        }
    else:
        payment_status_msg = {
        'bool': False
        }
    return Response(payment_status_msg)



@api_view([ 'GET'])
@permission_classes ([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)



@permission_classes([IsAdminUser])
@api_view(['PUT'])
def updateOrderToDelivered (request, pk):
    order = Order.objects.get(_id = pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response("Order was delivered")