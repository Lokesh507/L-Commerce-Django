from base.views import order_views as views
from django.urls import path

urlpatterns = [
    path('add/', views.addOrderItems, name='orders-add'),
    path('', views.getOrders, name='orders'),
    path('myorders/', views.getMyOrders, name='myorders'),
    path('<str:pk>/', views.getOrderById, name='orderbyid'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),
    path('<str:pk>/delivered/', views.updateOrderToDelivered, name='orderDelivered'),
    path('create-razorpay-order/<int:pk>', views.razorPayOrder, name='razorpayorder')
]