from base.views import product_views as views
from django.urls import path

urlpatterns = [
    path('', views.getProducts, name='products'),
    path('<str:id>', views.getProduct, name='getProduct'),
    path('<str:pk>/reviews/', views.createProductReview, name='createProductReview'),
    path('delete/<str:pk>/', views.deleteProduct, name='deleteProduct'),
    path('create/', views.createProduct, name='createProduct'),
    path('update/<str:pk>/', views.updateProduct, name='updateProduct'),
    path('uploadImage/', views.uploadImage, name='imageUpload'),
    path('corousel/', views.getTopProducts, name='topProducts')
]