from rest_framework. decorators import api_view 
from rest_framework.response import Response 
from base.models import Product, Review 
from base.serializers import ProductSerializer 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework import status

@api_view(['GET' ])
def getProducts(request):
    products = Product.objects.all()
    serialize_obj = ProductSerializer(products, many=True)
    return Response(serialize_obj.data)


@api_view([ 'GET'])
def getProduct(request, id):
    
    product = Product.objects.get(_id = id)
    serialize_obj1 = ProductSerializer(product, many=False)
    return Response(serialize_obj1.data)


@api_view([ 'DELETE' ])
@permission_classes ([IsAdminUser]) 
def deleteProduct(request, pk):
    productForDeletion =Product.objects.get(_id = pk)
    productForDeletion.delete()
    return Response("Product was Deleted")

@api_view(['POST' ])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(id = user, name='Sample Name', price = 0, brand='Sample Brand', countInStock = 0, category = 'Sample Category', description = '')
    serialize_obj1 = ProductSerializer(product, many=False)
    return Response(serialize_obj1.data)


@api_view(['PUT' ])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id = pk)
    product.name = data['name'] 
    product.price = data[ 'price'] 
    product.brand = data['brand']
    product.category = data['category']
    product.countInStock = data['countInStock']
    product.description  = data['description' ] 
    product.save()
    serialize_obj1 = ProductSerializer(product, many=False)
    return Response(serialize_obj1. data)

@api_view (['POST' ])
def uploadImage(request):
    data = request.data
    productId = data['productId']
    product = Product.objects.get(_id = productId)
    product.image = request.FILES.get('image') 
    product.save()
    return Response("Image Uploaded")

@api_view([ 'POST' ])
@permission_classes ([IsAuthenticated]) 
def createProductReview(request, pk):
    product = Product.objects.get(_id = pk)
    user = request.user
    data = request.data

    # Review Already exist
    already_exists = product.review_set.filter(user =user).exists()
    if(already_exists):
        content = {'detail': 'Product Already Reviewed'}
        return Response (content, status = status.HTTP_400_BAD_REQUEST)
    #No rating or 0
    elif data[ 'rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response (content, status = status.HTTP_400_BAD_REQUEST)
    #Create Review 
    else:
        review = Review.objects.create(user = user, product = product, name = user.first_name, rating = data['rating'], comment = data['comment' ])
        reviews = product.review_set.all()
        product.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()
        return Response( 'Review added')


@api_view([ 'GET' ])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte = 4).order_by('-rating')[0:5] 
    #returning top 5 products with rating greater than or equal to
    serialize_obj = ProductSerializer(products, many=True)
    return Response(serialize_obj.data)