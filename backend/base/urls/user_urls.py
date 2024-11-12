from base.views import user_views as views
from django.urls import path


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.getUsers, name='users'),
    path('delete/<str:pk>/', views.deleteUser, name='userDelete'),
    path('profile/', views.getUserProfile, name='getUserProfile'),
    path('profile/update/', views.updateUserProfile, name='updateUserProfile'),    
    path('register/', views.registerUser, name='registerUser'),
    path('getUserByAdmin/<str:pk>/', views.getUserByAdmin, name='getUserByAdmin'),
    path('updateUserByAdmin/<str:pk>/', views.updateUserByAdmin, name='updateUserByAdmin'),
]