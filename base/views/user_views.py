from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from base.models import Product, Review


from base.serializer import ProductSerializer, UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
import math


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

"""
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getDistance(request):
    user = request.user
    serializer = UserSerializer(user, many=False)

    x=user.locationX
    y=user.locationY

    products = Product.objects.all()

    for product in products:
        userID=product.user_id
        user = get_user_model().objects.get(id=userID)
        xs=(x-user.locationX)
        ys=(y-user.locationY)
        sqrt=(xs*xs)+(ys*ys)
        distance=math.sqrt(sqrt)
        product.distance = distance
        product.save()
        print(distance)
    
    

    
    return Response(distance)
"""

@api_view(["POST"])
def registerUser(request):
    data = request.data
    try:
        user = get_user_model().objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.isFarmer = data['isFarmer']
    user.locationX = data['locationX']
    user.locationY = data['locationY']
    user.farmName = data['farmName']
    user.address = data['address']
    user.description = data['description']
    user.farmerPoint = data['farmerPoint']
    user.numReviews = data['numReviews']
    

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = get_user_model().objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = get_user_model().objects.get(id=pk)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    user.isFarmer = data['isFarmer']
    user.locationX = data['locationX']
    user.locationY = data['locationY']
    user.farmName = data['farmName']
    user.address = data['address']
    user.description = data['description']
    user.farmerPoint = data['farmerPoint']
    user.numReviews = data['numReviews']

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def uploadUserImage(request):
    
    user = request.user
    
    user.farmerPicture = request.FILES.get('image')
    
    user.save()

    return Response('Image was uploaded')

@api_view(['POST'])
def uploadFarmImage(request):
    
    user = request.user
    
    user.farmPicture = request.FILES.get('image')
    
    user.save()

    return Response('Image was uploaded')

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = get_user_model().objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')