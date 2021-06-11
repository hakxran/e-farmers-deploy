from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from base.models import Product, Review
from base.serializer import (
    ProductSerializer,
    UserSerializer
   
    
)

from django.db.models import Q


from rest_framework import status


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getFarmerProducts(request):
    user = request.user
    #farmerUser = UserSerializer(user, many=False)

    #products = Product.objects.filter(user_id=user.id)
    products = user.product_set.all()
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data)


@api_view(["GET"])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def createProduct(request):
    user = request.user
    farmerUser = UserSerializer(user, many=False)
    if user.isFarmer == True:
        product = Product.objects.create(
            user=user,
            name='Sample Name',
            description='Deneme',
            unit='Sample Unit',
            countInStock=0,
            category='Sample Category',
            unitPrice=0,

            isFarmProduct=True,
        )

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        return Response("You are did not complete Farmer informations yet")

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.description = data['description']
    product.unit = data['unit']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.unitPrice = data['unitPrice']
    product.isFarmProduct = data['isFarmProduct']
    product.productType = data['productType']
    product.harvestTime = data['harvestTime']
    product.productionTime = data['productionTime']

    

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateFarmersProduct(request, pk):
    user = request.user
    
    data = request.data
    product = Product.objects.get(_id=pk)
    if user == product.user:

        product.name = data['name']
        product.description = data['description']
        product.unit = data['unit']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.unitPrice = data['unitPrice']
        product.isFarmProduct = data['isFarmProduct']
        product.productType = data['productType']
        product.harvestTime = data['harvestTime']
        product.productionTime = data['productionTime']
        

        product.save()

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        return Response("That's not your product")

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()

    return Response('Product Deleted')

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteFarmersProduct(request, pk):
    user = request.user

    product = Product.objects.get(_id=pk)
    if user == product.user:
        product.delete()

        return Response('Product Deleted')
    else:
        return Response('You cant delete another one product')

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    #alreadyExists = product.review_set.filter(user=user).exists()
    alreadyExists = False
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['productPoint'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            productPoint=data['productPoint'],
            deliveryPoint=data['deliveryPoint'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.productPoint

        product.productPoint = total / len(reviews)
        

        #4- Go User find all product rating and update farmerPoint
        pUser= product.user
        serializer = UserSerializer(pUser, many=False)
        
        productUser = get_user_model().objects.get(id=pUser.id)
        
        productFarmerPoint = 0
        productFarmerPoint += productUser.farmerPoint
        allPoint = productFarmerPoint * productUser.numReviews 
        productUser.numReviews += 1
        productUser.farmerPoint = (allPoint + data['productPoint']) / productUser.numReviews

        productUser.save()
        product.save()
        

        return Response("Reviewed Succesfully")



@api_view(["GET"])
def getFilteredProductHighestPoints(request):
    queryset = Product.objects.filter(~Q(productPoint=None)).order_by("-productPoint")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductHighestPrice(request):
    queryset = Product.objects.filter(~Q(productPoint=None)).order_by("-unitPrice")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductLowestPrice(request):
    queryset = Product.objects.filter(~Q(productPoint=None)).order_by("unitPrice")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductWithPoints4_5AndHigher(request):

    queryset = Product.objects.filter(
        ~Q(productPoint=None) & Q(productPoint__gte=4.5)
    ).order_by("-numReviews")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductWithPoints4(request):
    queryset = Product.objects.filter(
        ~Q(productPoint=None) & Q(productPoint__gte=4.0)
    ).order_by("-numReviews")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductWithPoints3_5AndHigher(request):
    queryset = Product.objects.filter(
        ~Q(productPoint=None) & Q(productPoint__gte=3.5)
    ).order_by("-numReviews")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getFilteredProductWithPoints3(request):
    queryset = Product.objects.filter(
        ~Q(productPoint=None) & Q(productPoint__gte=3.0)
    ).order_by("-numReviews")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsFruits(request):
    queryset = Product.objects.filter(category="Meyve")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsVegetables(request):
    queryset = Product.objects.filter(category="Sebze")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsKuruyemis(request):
    queryset = Product.objects.filter(category="Kuruyemisler")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsDairy(request):
    queryset = Product.objects.filter(category="Sut,Sut Urunleri")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsMeat(request):
    queryset = Product.objects.filter(category="Et,Tavuk,Sarkutleri")
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_0_10(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=0.0) & Q(unitPrice__lte=10.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_10_25(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=10.0) & Q(unitPrice__lte=25.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_25_50(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=25.0) & Q(unitPrice__lte=50.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_50_100(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=50.0) & Q(unitPrice__lte=100.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_100_250(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=100.0) & Q(unitPrice__lte=250.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_250_500(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=250.0) & Q(unitPrice__lte=500.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_500_750(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=500.0) & Q(unitPrice__lte=750.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_750_1000(request):
    queryset = Product.objects.filter(
        ~Q(unitPrice=None) & Q(unitPrice__gte=750.0) & Q(unitPrice__lte=1000.0)
    )
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProductsPrice_gte_1000(request):
    queryset = Product.objects.filter(~Q(unitPrice=None) & Q(unitPrice__gte=1000.0))
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
