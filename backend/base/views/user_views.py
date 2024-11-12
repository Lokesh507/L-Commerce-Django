from rest_framework import status 
from django.contrib.auth.models import User 
from rest_framework. decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework.response import Response
from base.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)        
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):    
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes ([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serialize_obj = UserSerializer(user, many=False)
    return Response(serialize_obj.data)


@api_view([ 'PUT' ])
@permission_classes ([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serialize_obj = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name =data['name']
    user.username = data['email']
    user.email = data[ 'email']
    if(data['password']!= ''):
        user.password=make_password(data['password'])
    user.save()
    return Response(serialize_obj.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serialize_obj = UserSerializer(users, many=True)
    return Response (serialize_obj.data)

@api_view([ 'GET'])
@permission_classes([IsAdminUser]) 
def getUserByAdmin(request, pk):
    user = User.objects.get(id = pk)
    serialize_obj =UserSerializer(user, many=False)
    return Response(serialize_obj.data)

@api_view([ 'PUT'])
@permission_classes ([IsAuthenticated]) 
def updateUserByAdmin(request, pk):
    user = User.objects.get(id = pk)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    user.save()
    serialize_obj = UserSerializerWithToken(user, many=False)
    return Response(serialize_obj.data)

@api_view([ 'DELETE'])
@permission_classes([IsAdminUser]) 
def deleteUser(request, pk):
    usersForDeletion = User.objects.get(id = pk)
    usersForDeletion.delete()
    return Response("User was Deleted")


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
        first_name=data['name'], 
        username=data['name'], 
        email=data['email'], 
        password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        
        return Response(serializer.data)
    except:        
        message = {'detail':"User with this email aready exists!"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)